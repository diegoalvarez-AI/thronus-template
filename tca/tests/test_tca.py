#!/usr/bin/env python3
"""
Testes do pacote tca. Biblioteca padrão apenas — o pacote não pode exigir
runner de testes de nenhum stack.

Executar:  python3 tca/tests/test_tca.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_loader("tca_cli", importlib.machinery.SourceFileLoader("tca_cli", str(PKG / "bin" / "tca")))
tca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tca)

P_INDEX = "docs/ThronusSpec/03_Desenvolvimento/payload_index.json"
P_ARCHIVE = "docs/ThronusSpec/03_Desenvolvimento/payload_archive"
P_LOGS = "docs/ThronusSpec/05_Monitoramento/performance_logs.json"
P_EXEC = "docs/ThronusSpec/05_Monitoramento/tca_execution_log.jsonl"
P_CTX = "context/activeContext.md"

CTX_ATIVO = """# Active Context — TCA Session RAM

**Fase atual:** GREEN
**MS ativa:** MS-021 — Cadastro de turma
**Arquivos a criar/modificar:** src/dominio/turma.py
**Cenários BDD:** CT-01, CT-02
"""


def projeto(tmp: Path, *, extras_estado: dict | None = None) -> Path:
    """Monta um projeto TCA mínimo, com campos extras para provar preservação."""
    (tmp / "context").mkdir(parents=True)
    (tmp / P_ARCHIVE).mkdir(parents=True)
    (tmp / "docs/ThronusSpec/05_Monitoramento").mkdir(parents=True)
    estado = {
        "modulo": "demo", "perfil": "standard", "fase_atual": "GREEN",
        "ultima_micro_spec_concluida": None, "micro_spec_ativa": "MS-021",
        "proximo_gate": "GATE_X", "total_testes": 10,
    }
    estado.update(extras_estado or {})
    (tmp / P_INDEX).write_text(json.dumps({
        "projeto": "demo",
        "campo_do_projeto_que_nao_e_da_tca": {"preservar": True},
        "estado_da_trilha": estado,
        "_archive": {"path": P_ARCHIVE, "keys": []},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp / P_LOGS).write_text(json.dumps({"projeto": "demo", "registros": []}), encoding="utf-8")
    (tmp / P_CTX).write_text(CTX_ATIVO, encoding="utf-8")
    return tmp


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.raiz = projeto(self.dir)
        self._cwd = Path.cwd()
        import os
        os.chdir(self.raiz)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def indice(self) -> dict:
        return json.loads((self.raiz / P_INDEX).read_text(encoding="utf-8"))


class TestCloseMs(Base):
    def test_fecha_ciclo_completo(self):
        self.assertEqual(tca.main(["close-ms", "MS-021", "--testes", "42"]), 0)

        arq = self.raiz / P_ARCHIVE / "ms021.json"
        self.assertTrue(arq.exists(), "archive não foi criado")
        d = json.loads(arq.read_text(encoding="utf-8"))
        for k in tca.ARCHIVE_CORE:
            self.assertIn(k, d, f"núcleo do archive sem {k}")
        self.assertEqual(d["ms"], "MS-021")
        self.assertEqual(d["titulo"], "Cadastro de turma")
        self.assertIn("CT-01", d["contexto_ativo"], "contexto deve ser preservado verbatim")

        est = self.indice()["estado_da_trilha"]
        self.assertEqual(est["ultima_micro_spec_concluida"], "MS-021")
        self.assertIsNone(est["micro_spec_ativa"])
        self.assertEqual(est["total_testes"], 42)
        self.assertEqual(self.indice()["_archive"]["keys"], ["ms021"])

        logs = json.loads((self.raiz / P_LOGS).read_text(encoding="utf-8"))
        self.assertEqual(len(logs["registros"]), 1)

        ctx = (self.raiz / P_CTX).read_text(encoding="utf-8")
        self.assertIsNone(tca.ms_ativa_no_contexto(ctx), "contexto deveria estar limpo")

    def test_preserva_campos_que_nao_sao_do_contrato(self):
        tca.main(["close-ms", "MS-021", "--testes", "1"])
        idx = self.indice()
        self.assertEqual(idx["campo_do_projeto_que_nao_e_da_tca"], {"preservar": True})
        self.assertEqual(idx["estado_da_trilha"]["proximo_gate"], "GATE_X")

    def test_idempotente(self):
        tca.main(["close-ms", "MS-021", "--testes", "42"])
        antes = (self.raiz / P_ARCHIVE / "ms021.json").read_text(encoding="utf-8")
        self.assertEqual(tca.main(["close-ms", "MS-021"]), 0, "segunda execução deve ser no-op")
        depois = (self.raiz / P_ARCHIVE / "ms021.json").read_text(encoding="utf-8")
        self.assertEqual(antes, depois, "no-op não pode reescrever o archive")
        logs = json.loads((self.raiz / P_LOGS).read_text(encoding="utf-8"))
        self.assertEqual(len(logs["registros"]), 1, "no-op não pode duplicar registro")

    def test_ms_id_invalido_falha(self):
        self.assertEqual(tca.main(["close-ms", "ms21"]), 2)

    def test_sem_titulo_derivavel_falha_em_vez_de_inventar(self):
        (self.raiz / P_CTX).write_text("**MS ativa:** —\n", encoding="utf-8")
        self.assertEqual(tca.main(["close-ms", "MS-021"]), 2)
        self.assertFalse((self.raiz / P_ARCHIVE / "ms021.json").exists())

    def test_dry_run_nao_escreve(self):
        self.assertEqual(tca.main(["close-ms", "MS-021", "--dry-run"]), 0)
        self.assertFalse((self.raiz / P_ARCHIVE / "ms021.json").exists())
        self.assertEqual(self.indice()["estado_da_trilha"]["micro_spec_ativa"], "MS-021")

    def test_emite_evidencia_de_execucao(self):
        tca.main(["close-ms", "MS-021", "--testes", "3"])
        linhas = (self.raiz / P_EXEC).read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(linhas), 1)
        reg = json.loads(linhas[0])
        self.assertEqual(reg["comando"], "close-ms")
        self.assertEqual(reg["resultado"], "ok")
        self.assertIn("tca_versao", reg)


class TestDiff(Base):
    """Snapshot-diff bidirecional: o previsto e não entregue também reprova."""

    @staticmethod
    def _git(cwd, *args):
        import subprocess
        subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)

    def setUp(self):
        super().setUp()
        self._git(self.raiz, "init", "-q", "-b", "main")
        (self.raiz / "src").mkdir(exist_ok=True)
        for n in ("a.py", "b.py"):
            (self.raiz / "src" / n).write_text("original\n", encoding="utf-8")
        self._git(self.raiz, "add", "-A")
        self._git(self.raiz, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base")

    def _spec(self, linha):
        (self.raiz / P_CTX).write_text(
            f"**Fase atual:** GREEN\n**MS ativa:** MS-021 — X\n{linha}\n", encoding="utf-8")

    def _muda(self, *nomes):
        for n in nomes:
            (self.raiz / n).write_text("alterado\n", encoding="utf-8")

    def test_conforme_passa(self):
        self._spec("**Arquivos a criar/modificar:** src/a.py, src/b.py")
        self._muda("src/a.py", "src/b.py")
        self.assertEqual(tca.main(["diff"]), 0)

    def test_detecta_previsto_e_nao_entregue(self):
        """O caso que passava sem ruído: a spec previa, o commit não trouxe."""
        self._spec("**Arquivos a criar/modificar:** src/a.py, src/b.py")
        self._muda("src/a.py")
        self.assertEqual(tca.main(["diff"]), 1)

    def test_detecta_inesperado(self):
        self._spec("**Arquivos a criar/modificar:** src/a.py")
        self._muda("src/a.py", "src/b.py")
        self.assertEqual(tca.main(["diff"]), 1)

    def test_aceita_lista_em_marcadores(self):
        (self.raiz / P_CTX).write_text(
            "**MS ativa:** MS-021 — X\n"
            "**Arquivos a criar/modificar:**\n- src/a.py\n- src/b.py\n\n"
            "**Cenários BDD:** CT-01\n", encoding="utf-8")
        self._muda("src/a.py", "src/b.py")
        self.assertEqual(tca.main(["diff"]), 0)

    def test_campo_ausente_e_lacuna_nao_aprovacao(self):
        (self.raiz / P_CTX).write_text("**MS ativa:** MS-021 — X\n", encoding="utf-8")
        self._muda("src/a.py")
        self.assertEqual(tca.main(["diff"]), 2, "sem lista prevista não se aprova por omissão")

    def test_travessao_significa_nenhum_arquivo(self):
        self._spec("**Arquivos a criar/modificar:** —")
        self.assertEqual(tca.main(["diff"]), 0)
        self._muda("src/a.py")
        self.assertEqual(tca.main(["diff"]), 1, "nada previsto mas algo tocado deve reprovar")

    def test_artefatos_de_controle_nao_contam(self):
        """Todo commit de fechamento toca activeContext e índice — se contassem,
        o portão reprovaria sempre e viraria ruído."""
        self._spec("**Arquivos a criar/modificar:** src/a.py")
        self._muda("src/a.py")
        (self.raiz / P_INDEX).write_text('{"estado_da_trilha":{"fase_atual":"COMMIT"}}',
                                         encoding="utf-8")
        self.assertEqual(tca.main(["diff"]), 0)

    def test_artefato_de_controle_declarado_nao_vira_faltante(self):
        """Ele é removido dos tocados; permanecer nos previstos produziria
        FALTANTE em todo commit de fechamento."""
        self._spec("**Arquivos a criar/modificar:** src/a.py, tca.lock.json")
        self._muda("src/a.py")
        self.assertEqual(tca.main(["diff"]), 0)

    def test_compara_contra_a_spec_arquivada_apos_o_fechamento(self):
        """O close-ms limpa o contexto e o commit vem depois: sem ler o archive,
        o portão de commit compara contra spec vazia e reprova tudo."""
        self._spec("**Arquivos a criar/modificar:** src/a.py")
        self._muda("src/a.py")
        tca.main(["close-ms", "MS-021"])
        self.assertEqual(tca.main(["diff"]), 1, "contexto limpo: tudo vira inesperado")
        self.assertEqual(tca.main(["diff", "--ms", "MS-021"]), 0,
                         "contra a spec arquivada, o diff confere")

    def test_ms_sem_archive_e_erro_explicito(self):
        self.assertEqual(tca.main(["diff", "--ms", "MS-999"]), 2)

    def test_emite_evidencia(self):
        self._spec("**Arquivos a criar/modificar:** src/a.py")
        self._muda("src/a.py")
        tca.main(["diff"])
        reg = json.loads((self.raiz / P_EXEC).read_text(encoding="utf-8").strip().splitlines()[-1])
        self.assertEqual(reg["comando"], "diff")
        self.assertIn("faltantes", reg["detalhes"])


class TestSelfcheck(Base):
    """A verificação está de pé? — responde ao CI que rodava sem banco."""

    def _cfg(self, **comandos):
        (self.raiz / tca.P_PROJETO_CFG).write_text(
            json.dumps({"comandos": comandos}), encoding="utf-8")

    def _medicao(self, testes, host=None, resultado="ok"):
        amb = tca.ambiente()
        reg = {"ts": "2026-08-25T10:00:00-03:00", "ref": "abc", "tca_versao": "9.9.9",
               "ambiente": {**amb, "host": host or amb["host"]},
               "indicadores": {
                   "suite_testes": {"valor": testes, "origem": "derivado:execucao"},
                   "suite_segundos": {"valor": 10, "origem": "derivado:execucao",
                                      "resultado": resultado}},
               "nao_instrumentado": []}
        with (self.raiz / tca.P_METRICAS).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(reg) + "\n")

    def test_sem_contrato_de_execucao_reprova(self):
        self.assertEqual(tca.main(["selfcheck"]), 1,
                         "sem comandos.testes não se afirma que a suíte roda")

    def test_queda_na_contagem_reprova(self):
        self._cfg(testes="python3 -c \"pass\"", contar_testes="python3 -c \"print(500)\"")
        self._medicao(1000)
        self.assertEqual(tca.main(["selfcheck"]), 1, "queda de 1000 para 500 deve reprovar")

    def test_variacao_dentro_da_tolerancia_passa(self):
        self._cfg(testes="python3 -c \"pass\"", contar_testes="python3 -c \"print(999)\"")
        self._medicao(1000)
        self.assertEqual(tca.main(["selfcheck"]), 0)

    def test_suite_que_falhou_na_ultima_medicao_reprova(self):
        self._cfg(testes="python3 -c \"pass\"", contar_testes="python3 -c \"print(1000)\"")
        self._medicao(1000, resultado="exit 1")
        self.assertEqual(tca.main(["selfcheck"]), 1)

    def test_medicao_de_outra_maquina_nao_serve_de_base(self):
        self._cfg(testes="python3 -c \"pass\"", contar_testes="python3 -c \"print(10)\"")
        self._medicao(1000, host="outra-maquina")
        self.assertEqual(tca.main(["selfcheck"]), 0,
                         "sem base desta máquina, avisa em vez de reprovar por comparação inválida")


class TestTrace(Base):
    """Índice de rastreabilidade: requisito ↔ arquivo ↔ Micro Spec."""

    @staticmethod
    def _git(cwd, *args):
        import subprocess
        subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)

    def setUp(self):
        super().setUp()
        self._git(self.raiz, "init", "-q", "-b", "main")
        (self.raiz / "tests").mkdir(exist_ok=True)
        (self.raiz / "src").mkdir(exist_ok=True)

    def _arquivo(self, caminho, conteudo):
        alvo = self.raiz / caminho
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
        return alvo

    def _commit(self, msg):
        self._git(self.raiz, "add", "-A")
        self._git(self.raiz, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", msg)

    def _indice(self):
        return json.loads((self.raiz / tca.P_TRACE).read_text(encoding="utf-8"))

    def test_indexa_marcador_em_qualquer_linguagem(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014 UC-003\ndef test_x(): pass\n")
        self._arquivo("tests/turma.test.ts", "// @tca RF-031\nit('x', () => {})\n")
        self._arquivo("src/turma.go", "/* @tca RNF-007 */\n")
        self.assertEqual(tca.main(["trace", "--write"]), 0)
        por_id = self._indice()["por_identificador"]
        self.assertEqual(sorted(por_id), ["RF-014", "RF-031", "RNF-007", "UC-003"])
        self.assertEqual(por_id["RF-014"]["arquivos"], ["tests/test_turma.py"])

    def test_liga_identificador_a_micro_spec_pelo_commit(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014\n")
        self._commit("feat(turma): cadastro [MS-021]")
        tca.main(["trace", "--write"])
        self.assertEqual(self._indice()["por_identificador"]["RF-014"]["micro_specs"], ["MS-021"])

    def test_arquivo_sem_marcador_nao_entra(self):
        self._arquivo("tests/sem_marcador.py", "def test_x(): pass\n")
        tca.main(["trace", "--write"])
        self.assertEqual(self._indice()["por_arquivo"], {})

    def test_cobertura_e_lacuna_sem_universo_declarado(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014\n")
        tca.main(["trace", "--write"])
        self.assertIn("_lacuna", self._indice()["cobertura"],
                      "sem universo declarado a cobertura não é calculável, não é 100%")

    def test_cobertura_com_universo_declarado(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014\n")
        (self.raiz / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "listar_requisitos": "python3 -c \"print('RF-014'); print('RF-099')\"",
        }}), encoding="utf-8")
        tca.main(["trace", "--write"])
        cob = self._indice()["cobertura"]
        self.assertEqual((cob["universo"], cob["cobertos"]), (2, 1))
        self.assertEqual(cob["sem_teste"], ["RF-099"])

    def test_strict_reprova_requisito_sem_teste(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014\n")
        (self.raiz / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "listar_requisitos": "python3 -c \"print('RF-014'); print('RF-099')\"",
        }}), encoding="utf-8")
        self.assertEqual(tca.main(["trace", "--strict"]), 1)

    def test_conteudo_gerado_nao_declara_cobertura(self):
        """O AGENTS.md carrega os exemplos da metodologia; indexá-lo faria o
        índice afirmar cobertura que não existe."""
        self._arquivo("AGENTS.md", "<!-- GERADO por `tca agents --write` -->\n\n# @tca RF-999\n")
        tca.main(["trace", "--write"])
        self.assertEqual(self._indice()["por_arquivo"], {})

    def test_indice_e_conteudo_gerado(self):
        self._arquivo("tests/test_turma.py", "# @tca RF-014\n")
        tca.main(["trace", "--write"])
        self.assertIn("_gerado_por", self._indice())

    def test_impacto_sem_grafo_usa_o_marcador_do_arquivo(self):
        self._arquivo("src/turma.py", "# @tca RF-014\n")
        self._commit("feat(turma): x [MS-021]")
        self.assertEqual(tca.main(["trace", "--impacto", "src/turma.py"]), 0)


class TestSeveridadeEGate(Base):
    """Severidade é consulta, não julgamento. E a agregação é não compensatória."""

    def test_registro_e_bem_formado(self):
        self.assertEqual(tca.main(["sev", "--validar"]), 0)

    def test_toda_linha_tem_ancora(self):
        """Severidade sem origem é julgamento com aparência de regra."""
        for r in tca._ler_severidades().values():
            self.assertTrue(str(r["origem"]).strip(), f"{r['id']} sem origem")
            self.assertIn(r["severidade"], tca.NIVEIS)

    def test_consulta_por_id(self):
        self.assertEqual(tca.main(["sev", "SEV-007"]), 0)
        self.assertEqual(tca.main(["sev", "sev-007"]), 0, "consulta é insensível a caixa")

    def test_id_inexistente_falha(self):
        self.assertEqual(tca.main(["sev", "SEV-999"]), 2)

    def test_sem_achado_o_portao_esta_atendido(self):
        self.assertEqual(tca.main(["gate", "--portao", "PLAN"]), 0)

    def test_informativo_nao_afeta_o_portao(self):
        self.assertEqual(tca.main(["gate", "--achados", "SEV-025"]), 0)

    def test_bloqueante_reprova(self):
        self.assertEqual(tca.main(["gate", "--achados", "SEV-007"]), 1)

    def test_nao_compensacao_bloqueante_nao_e_neutralizado(self):
        """Desempenho em outro critério não compensa condição necessária."""
        self.assertEqual(
            tca.main(["gate", "--achados", "SEV-007,SEV-023,SEV-025",
                      "--pendencia", "SEV-023=Diego"]), 1,
            "pendência acompanhada e nota não neutralizam um bloqueante")

    def test_residual_com_responsavel_condiciona(self):
        self.assertEqual(
            tca.main(["gate", "--achados", "SEV-023", "--pendencia", "SEV-023=Diego"]), 0)

    def test_residual_sem_responsavel_bloqueia(self):
        """Pendência sem dono não é pendência acompanhada — é achado não endereçado."""
        self.assertEqual(tca.main(["gate", "--achados", "SEV-023"]), 1)

    def test_pendencia_sem_nome_e_erro(self):
        self.assertEqual(
            tca.main(["gate", "--achados", "SEV-023", "--pendencia", "SEV-023="]), 2)

    def test_achado_fora_do_registro_e_erro_nao_julgamento(self):
        self.assertEqual(tca.main(["gate", "--achados", "SEV-999"]), 2,
                         "severidade não consta: declarar a linha é decisão de método")

    def test_gate_colhe_achados_das_verificacoes(self):
        """O portão executa as verificações e traduz o que elas encontram."""
        import subprocess
        subprocess.run(["git", "-C", str(self.raiz), "init", "-q", "-b", "main"],
                       check=True, capture_output=True)
        (self.raiz / "src").mkdir(exist_ok=True)
        (self.raiz / "src/a.py").write_text("x\n", encoding="utf-8")
        (self.raiz / "src/b.py").write_text("y\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.raiz), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.raiz), "-c", "user.email=t@t",
                        "-c", "user.name=t", "commit", "-qm", "base"],
                       check=True, capture_output=True)
        (self.raiz / P_CTX).write_text(
            "**MS ativa:** MS-021 — X\n"
            "**Arquivos a criar/modificar:** src/a.py, src/b.py\n", encoding="utf-8")
        (self.raiz / "src/a.py").write_text("alterado\n", encoding="utf-8")   # b.py não entregue

        tca.ACHADOS.clear()
        self.assertEqual(tca.main(["gate", "--portao", "COMMIT", "--de", "diff"]), 1)
        self.assertIn("SEV-007", tca.ACHADOS, "faltante deve virar achado do registro")

    def test_de_usa_os_defaults_do_proprio_parser(self):
        """Montar o namespace à mão quebrava a cada flag nova numa verificação."""
        for nome in ("diff", "trace", "selfcheck", "doctor"):
            ns = tca._parser().parse_args([nome])
            self.assertTrue(callable(ns.fn), nome)

    def test_verificacao_desconhecida_em_de_e_erro(self):
        tca.ACHADOS.clear()
        self.assertEqual(tca.main(["gate", "--de", "inexistente"]), 2)

    def test_achados_manuais_e_colhidos_se_somam(self):
        """Projeto sem os arquivos do canon: o doctor acha ausência (SEV-004),
        que se soma à nota informada à mão — e o bloqueante vence."""
        tca.ACHADOS.clear()
        self.assertEqual(tca.main(["gate", "--achados", "SEV-025", "--de", "doctor"]), 1)
        self.assertIn("SEV-004", tca.ACHADOS, "achado colhido do doctor")

    # ── classe da mudança ──

    def test_classe_deriva_do_tipo_do_commit(self):
        self.assertEqual(tca.classe_do_commit("fix(auth): corrige [MS-021]"), "fix")
        self.assertEqual(tca.classe_do_commit("feat(turma): cadastro"), "feat")
        self.assertEqual(tca.classe_do_commit("refactor: extrai helper"), "tecnico")
        self.assertEqual(tca.classe_do_commit("chore(deps): bump"), "tecnico")
        self.assertIsNone(tca.classe_do_commit("mensagem solta"))

    def test_correcao_dispensa_requisito_e_exige_teste(self):
        """O requisito já existe; o que faltava era teste."""
        tca.ACHADOS.clear()
        self.assertEqual(
            tca.main(["gate", "--classe", "fix", "--achados", "SEV-014"]), 0,
            "cobertura de requisito não se aplica a correção")
        self.assertEqual(
            tca.main(["gate", "--classe", "fix", "--achados", "SEV-029"]), 1,
            "correção sem teste de regressão bloqueia")

    def test_nova_capacidade_condiciona_em_vez_de_bloquear(self):
        """Refinamento não pode parar em documentação: emenda vira pendência."""
        self.assertEqual(
            tca.main(["gate", "--classe", "feat", "--achados", "SEV-030",
                      "--pendencia", "SEV-030=Diego Alvarez"]), 0)
        self.assertEqual(tca.main(["gate", "--classe", "feat", "--achados", "SEV-030"]), 1,
                         "sem dono, a emenda não é pendência acompanhada")

    def test_mudanca_tecnica_dispensa_requisito(self):
        self.assertEqual(
            tca.main(["gate", "--classe", "tecnico", "--achados", "SEV-014,SEV-029"]), 0)

    def test_classe_invalida_e_erro(self):
        self.assertEqual(tca.main(["gate", "--classe", "melhoria"]), 2)

    # ── signatário ──

    def _autoriza(self, **portoes):
        (self.raiz / tca.P_SIGNATARIOS).write_text(
            json.dumps({"padrao": ["Diego Alvarez"], "portoes": portoes}), encoding="utf-8")

    def test_signatario_autorizado_assina(self):
        self._autoriza(COMMIT=["Diego Alvarez"])
        self.assertEqual(tca.main(["gate", "--portao", "COMMIT",
                                   "--assinar", "Diego Alvarez"]), 0)

    def test_signatario_nao_autorizado_bloqueia(self):
        """Autodesignação no momento da aprovação é o viés que o método restringe."""
        self._autoriza(COMMIT=["Diego Alvarez"])
        tca.ACHADOS.clear()
        self.assertEqual(tca.main(["gate", "--portao", "COMMIT", "--assinar", "Fulano"]), 1)
        self.assertIn("SEV-033", tca.ACHADOS)

    def test_cai_no_padrao_quando_o_portao_nao_e_declarado(self):
        self._autoriza(RELEASE=["Bernardo"])
        self.assertEqual(tca.main(["gate", "--portao", "PLAN",
                                   "--assinar", "Diego Alvarez"]), 0)

    def test_exigir_assinatura_sem_signatario_bloqueia(self):
        self._autoriza(COMMIT=["Diego Alvarez"])
        self.assertEqual(tca.main(["gate", "--portao", "COMMIT", "--exigir-assinatura"]), 1)

    def test_assinatura_vincula_se_ao_que_foi_aprovado(self):
        """Assinatura sem conteúdo não vincula nada."""
        self._autoriza(COMMIT=["Diego Alvarez"])
        tca.main(["gate", "--portao", "COMMIT", "--assinar", "Diego Alvarez"])
        reg = json.loads((self.raiz / P_EXEC).read_text(encoding="utf-8").strip().splitlines()[-1])
        self.assertEqual(reg["detalhes"]["signatario"], "Diego Alvarez")
        self.assertIn("ref_aprovada", reg["detalhes"])

    def test_gate_emite_evidencia(self):
        tca.main(["gate", "--portao", "COMMIT", "--achados", "SEV-025"])
        reg = json.loads((self.raiz / P_EXEC).read_text(encoding="utf-8").strip().splitlines()[-1])
        self.assertEqual(reg["comando"], "gate")
        self.assertEqual(reg["detalhes"]["estado"], "ATENDIDO")


class TestFase(Base):
    """Marcação de fase: o que torna o custo de especificar derivável."""

    def test_marca_transicao_e_atualiza_a_trilha(self):
        self.assertEqual(tca.main(["fase", "SPEC", "--ms", "MS-021"]), 0)
        est = self.indice()["estado_da_trilha"]
        self.assertEqual(est["fase_atual"], "SPEC")
        self.assertEqual(est["micro_spec_ativa"], "MS-021")

    def test_fase_desconhecida_e_erro_nao_inferencia(self):
        self.assertEqual(tca.main(["fase", "ESPECIFICANDO"]), 2)

    def test_caixa_e_normalizada(self):
        self.assertEqual(tca.main(["fase", "green"]), 0)
        self.assertEqual(self.indice()["estado_da_trilha"]["fase_atual"], "GREEN")

    def test_herda_a_ms_ativa_do_indice(self):
        tca.main(["fase", "SPEC", "--ms", "MS-021"])
        tca.main(["fase", "PLAN"])
        reg = json.loads((self.raiz / P_EXEC).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertEqual(reg["detalhes"]["ms"], "MS-021")
        self.assertEqual(reg["detalhes"]["de"], "SPEC")

    # ── MS-001: linha do tempo das fases ──

    def test_ct01_lista_fases_em_ordem_com_duracao(self):
        for f in ("SPEC", "PLAN", "RED"):
            tca.main(["fase", f, "--ms", "MS-021"])
        self.assertEqual(tca.main(["fase", "--listar"]), 0)

    def test_ct02_sem_marcacao_avisa(self):
        self.assertEqual(tca.main(["fase", "--listar"]), 0,
                         "sem marcação, avisa em vez de lista vazia")

    def test_ct03_lista_so_a_ms_ativa(self):
        tca.main(["fase", "SPEC", "--ms", "MS-021"])
        tca.main(["fase", "GREEN", "--ms", "MS-099"])
        linha = tca.linha_do_tempo(self.raiz, "MS-021")
        self.assertTrue(all(m["ms"] == "MS-021" for m in linha))
        self.assertEqual([m["fase"] for m in linha], ["SPEC"])

    def test_metrics_funciona_sem_git(self):
        """Custo de fase vem da trilha, não do histórico: exigir git seria
        acoplamento indevido."""
        self.assertEqual(tca.main(["metrics", "--write"]), 0)
        self.assertTrue((self.raiz / tca.P_METRICAS).exists())

    def test_custo_por_fase_exige_marcacoes(self):
        """Sem marcação, é lacuna declarada — não zero."""
        tca.main(["metrics", "--write"])
        reg = json.loads((self.raiz / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertNotIn("custo_spec_horas_mediana", reg["indicadores"])
        self.assertTrue(any("fase" in n for n in reg["nao_instrumentado"]))

    def test_separa_custo_de_especificar_de_construir(self):
        for f in ("SPEC", "PLAN", "RED", "GREEN", "COMMIT"):
            tca.main(["fase", f, "--ms", "MS-021"])
        tca.main(["metrics", "--write"])
        ind = self._indicadores()
        self.assertIn("custo_spec_horas_mediana", ind)
        self.assertEqual(ind["custo_spec_horas_mediana"]["origem"], "derivado:trilha")
        self.assertIn("construção", ind["custo_spec_horas_mediana"]["nota"])

    def _indicadores(self):
        return json.loads((self.raiz / tca.P_METRICAS).read_text(encoding="utf-8")
                          .strip().splitlines()[-1])["indicadores"]


class TestVerify(Base):
    def test_detecta_ciclo_aberto_sem_registro(self):
        idx = self.indice()
        idx["estado_da_trilha"]["micro_spec_ativa"] = None
        (self.raiz / P_INDEX).write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(tca.main(["verify"]), 1, "contexto com MS ativa e índice sem ela deve reprovar")

    def test_detecta_archive_orfao(self):
        (self.raiz / P_ARCHIVE / "ms099.json").write_text("{}", encoding="utf-8")
        self.assertEqual(tca.main(["verify"]), 1)

    def test_detecta_concluida_sem_archive(self):
        idx = self.indice()
        idx["estado_da_trilha"]["ultima_micro_spec_concluida"] = "MS-007"
        idx["estado_da_trilha"]["micro_spec_ativa"] = None
        (self.raiz / P_CTX).write_text("**MS ativa:** —\n", encoding="utf-8")
        (self.raiz / P_INDEX).write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(tca.main(["verify"]), 1)

    def test_aprova_estado_coerente_apos_fechamento(self):
        tca.main(["close-ms", "MS-021", "--testes", "42"])
        self.assertEqual(tca.main(["verify"]), 0)
        self.assertEqual(tca.main(["verify", "--strict"]), 0, "archive da própria TCA deve passar em --strict")

    def test_strict_reprova_archive_legado(self):
        (self.raiz / P_ARCHIVE / "ms001.json").write_text(
            json.dumps({"ms": "MS-001", "nome": "legado"}), encoding="utf-8")
        idx = self.indice()
        idx["_archive"]["keys"] = ["ms001"]
        idx["estado_da_trilha"]["micro_spec_ativa"] = None
        (self.raiz / P_CTX).write_text("**MS ativa:** —\n", encoding="utf-8")
        (self.raiz / P_INDEX).write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
        self.assertEqual(tca.main(["verify"]), 0, "legado é aviso por padrão")
        self.assertEqual(tca.main(["verify", "--strict"]), 1, "legado reprova em --strict")


class TestCanonDoctor(unittest.TestCase):
    """canon e doctor — detecção de inferência local."""

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        # projeto mínimo com cópia do conteúdo canônico declarado
        (self.dir / "docs/ThronusSpec/03_Desenvolvimento").mkdir(parents=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        raiz_tpl = PKG.parent
        self.copiados = []
        for nome in tca._ler_canon():
            src = raiz_tpl / nome
            dst = self.dir / nome
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            self.copiados.append(nome)
        self._cwd = Path.cwd()
        os.chdir(self.dir)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_canon_do_template_confere(self):
        self.assertEqual(tca.main(["canon"]), 0)

    def test_copia_intacta_nao_diverge(self):
        self.assertEqual(tca.main(["doctor", "--strict"]), 0)

    def test_detecta_edicao_local(self):
        alvo = self.dir / self.copiados[0]
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n<!-- local -->\n", encoding="utf-8")
        self.assertEqual(tca.main(["doctor"]), 0, "sem --strict é relatório")
        self.assertEqual(tca.main(["doctor", "--strict"]), 1, "com --strict reprova")

    def test_detecta_arquivo_ausente(self):
        (self.dir / self.copiados[0]).unlink()
        self.assertEqual(tca.main(["doctor", "--strict"]), 1)

    def test_detecta_skill_extra_nao_declarada(self):
        extra = self.dir / "docs/ThronusSpec/02_Setup/inventadoSkill.md"
        extra.write_text("# skill local\n", encoding="utf-8")
        self.assertEqual(tca.main(["doctor", "--strict"]), 1)

    def test_override_declarado_nao_reprova(self):
        alvo = self.copiados[0]
        (self.dir / alvo).write_text("alterado\n", encoding="utf-8")
        (self.dir / tca.P_OVERRIDES).write_text(json.dumps({"overrides": [
            {"arquivo": alvo, "motivo": "adaptação do domínio", "responsavel": "Diego Alvarez"}
        ]}), encoding="utf-8")
        self.assertEqual(tca.main(["doctor", "--strict"]), 0)

    def test_override_sem_responsavel_falha(self):
        (self.dir / tca.P_OVERRIDES).write_text(json.dumps({"overrides": [
            {"arquivo": "x", "motivo": "y"}
        ]}), encoding="utf-8")
        self.assertEqual(tca.main(["doctor"]), 2, "papel genérico não satisfaz")


class TestAgents(unittest.TestCase):
    """AGENTS.md é conteúdo gerado — nunca editado à mão."""

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / "docs/ThronusSpec/03_Desenvolvimento").mkdir(parents=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        (self.dir / "tca").mkdir()
        (self.dir / tca.P_METODOLOGIA).write_text("# Metodologia\n\nregra canônica.\n", encoding="utf-8")
        (self.dir / tca.P_PROJETO).write_text("# Projeto: demo\n\nconteúdo do projeto.\n", encoding="utf-8")
        self._cwd = Path.cwd()
        os.chdir(self.dir)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_gera_e_verifica(self):
        self.assertEqual(tca.main(["agents", "--write"]), 0)
        texto = (self.dir / tca.P_AGENTS).read_text(encoding="utf-8")
        self.assertIn("GERADO por", texto, "falta o marcador de geração")
        self.assertIn("regra canônica", texto)
        self.assertIn("conteúdo do projeto", texto)
        self.assertEqual(tca.main(["agents"]), 0)

    def test_edicao_manual_reprova(self):
        tca.main(["agents", "--write"])
        alvo = self.dir / tca.P_AGENTS
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\nlinha editada à mão\n", encoding="utf-8")
        self.assertEqual(tca.main(["agents"]), 1)

    def test_fonte_alterada_deixa_gerado_desatualizado(self):
        tca.main(["agents", "--write"])
        met = self.dir / tca.P_METODOLOGIA
        met.write_text(met.read_text(encoding="utf-8") + "\nregra nova.\n", encoding="utf-8")
        self.assertEqual(tca.main(["agents"]), 1, "AGENTS.md deve acusar defasagem")
        self.assertEqual(tca.main(["agents", "--write"]), 0)
        self.assertEqual(tca.main(["agents"]), 0)

    def test_ausencia_reprova(self):
        self.assertEqual(tca.main(["agents"]), 1)

    def test_fonte_ausente_e_erro_explicito(self):
        (self.dir / tca.P_PROJETO).unlink()
        self.assertEqual(tca.main(["agents", "--write"]), 2)

    def test_verify_reprova_agents_desatualizado(self):
        # verify precisa dos artefatos de estado completos
        (self.dir / "context").mkdir()
        (self.dir / P_CTX).write_text("**MS ativa:** —\n", encoding="utf-8")
        (self.dir / P_ARCHIVE).mkdir(parents=True)
        (self.dir / P_INDEX).write_text(json.dumps({
            "estado_da_trilha": {"micro_spec_ativa": None},
            "_archive": {"keys": []},
        }), encoding="utf-8")
        tca.main(["agents", "--write"])
        self.assertEqual(tca.main(["verify"]), 0)
        (self.dir / tca.P_AGENTS).write_text("editado\n", encoding="utf-8")
        self.assertEqual(tca.main(["verify"]), 1, "verify deve acusar AGENTS.md fora de dia")


class TestLock(unittest.TestCase):
    """O lock fixa o canon: sem ele, regenerar o canon esconde toda divergência."""

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / "docs/ThronusSpec/03_Desenvolvimento").mkdir(parents=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        raiz_tpl = PKG.parent
        self.copiados = []
        for nome in tca._ler_canon():
            src, dst = raiz_tpl / nome, self.dir / nome
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            self.copiados.append(nome)
        self._cwd = Path.cwd()
        os.chdir(self.dir)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_escreve_e_confere(self):
        self.assertEqual(tca.main(["lock", "--write", "--origem", "http://x", "--ref", "abc123"]), 0)
        d = json.loads((self.dir / tca.P_LOCK).read_text(encoding="utf-8"))["tca"]
        self.assertEqual(d["origem"], "http://x")
        self.assertEqual(d["ref"], "abc123")
        self.assertEqual(len(d["canon_sha256"]), 64)
        self.assertEqual(tca.main(["lock"]), 0)

    def test_lock_ausente_reprova(self):
        self.assertEqual(tca.main(["lock"]), 1)

    def test_detecta_canon_regenerado(self):
        """O caso que motivou o lock: o canon deixou de ser o que foi instalado.

        A condição observável é sha256(CANON) != lock.canon_sha256 — não importa
        se veio de `canon --write` ou de edição direta. O teste a produz sem
        tocar no repositório real.
        """
        tca.main(["lock", "--write", "--origem", "http://x", "--ref", "abc"])
        self.assertEqual(tca.main(["doctor", "--strict"]), 0, "estado limpo")

        lock_path = self.dir / tca.P_LOCK
        d = json.loads(lock_path.read_text(encoding="utf-8"))
        d["tca"]["canon_sha256"] = "0" * 64
        lock_path.write_text(json.dumps(d), encoding="utf-8")

        self.assertEqual(tca.main(["doctor", "--strict"]), 1,
                         "canon diferente do instalado é divergência não declarada")
        self.assertEqual(tca.main(["lock"]), 1, "lock deve acusar canon divergente")


class TestUpdate(unittest.TestCase):
    """update contra uma origem git local — sem rede."""

    @staticmethod
    def _git(cwd, *args):
        import subprocess
        subprocess.run(["git", "-C", str(cwd), *args], check=True,
                       capture_output=True, text=True)

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        tpl = PKG.parent
        self.origem = self.dir / "origem"
        shutil.copytree(tpl, self.origem, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self._git(self.origem, "init", "-q", "-b", "main")
        self._git(self.origem, "add", "-A")
        self._git(self.origem, "-c", "user.email=t@t", "-c", "user.name=t",
                  "commit", "-qm", "origem")
        self._git(self.origem, "tag", "v9.9.9")

        self.proj = self.dir / "proj"
        shutil.copytree(tpl, self.proj, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        lock = self.proj / tca.P_LOCK
        d = json.loads(lock.read_text(encoding="utf-8"))
        d["tca"]["origem"] = str(self.origem)
        d["tca"]["versao"] = "0.1.0"
        lock.write_text(json.dumps(d), encoding="utf-8")

        self._cwd = Path.cwd()
        os.chdir(self.proj)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def _skill(self, nome="docs/ThronusSpec/02_Setup/deploySkill.md"):
        return self.proj / nome

    def test_detecta_atraso(self):
        self.assertEqual(tca.main(["update"]), 1, "versão atrás da origem deve acusar")

    def test_recusa_apply_com_divergencia_nao_declarada(self):
        alvo = self._skill()
        alvo.write_text(alvo.read_text(encoding="utf-8") + "\n<!-- local -->\n", encoding="utf-8")
        self.assertEqual(tca.main(["update", "--apply"]), 1,
                         "não pode sobrescrever divergência não declarada")
        d = json.loads((self.proj / tca.P_LOCK).read_text(encoding="utf-8"))["tca"]
        self.assertEqual(d["versao"], "0.1.0", "lock não pode avançar numa recusa")

    def test_apply_atualiza_e_preserva_override(self):
        alvo = self._skill()
        marcado = alvo.read_text(encoding="utf-8") + "\n<!-- adaptação do projeto -->\n"
        alvo.write_text(marcado, encoding="utf-8")
        (self.proj / tca.P_OVERRIDES).write_text(json.dumps({"overrides": [{
            "arquivo": "docs/ThronusSpec/02_Setup/deploySkill.md",
            "motivo": "infra do cliente", "responsavel": "Diego Alvarez",
        }]}), encoding="utf-8")

        self.assertEqual(tca.main(["update", "--apply"]), 0)
        self.assertEqual(alvo.read_text(encoding="utf-8"), marcado,
                         "override declarado não pode ser sobrescrito")
        d = json.loads((self.proj / tca.P_LOCK).read_text(encoding="utf-8"))["tca"]
        self.assertEqual(d["versao"], "9.9.9")
        self.assertEqual(tca.main(["update"]), 0, "depois de aplicar, deve estar em dia")

    def test_sem_lock_e_erro_explicito(self):
        (self.proj / tca.P_LOCK).unlink()
        self.assertEqual(tca.main(["update"]), 2)


class TestMetrics(unittest.TestCase):
    """Linha de base derivada de git — sem instrumentar nada no processo."""

    @staticmethod
    def _git(cwd, *args, **kw):
        import subprocess
        subprocess.run(["git", "-C", str(cwd), *args], check=True,
                       capture_output=True, text=True, env=kw.get("env"))

    def _commit(self, msg, arquivo, conteudo):
        (self.dir / arquivo).parent.mkdir(parents=True, exist_ok=True)
        (self.dir / arquivo).write_text(conteudo, encoding="utf-8")
        self._git(self.dir, "add", arquivo)
        self._git(self.dir, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", msg)

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / P_ARCHIVE).mkdir(parents=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        self._git(self.dir, "init", "-q", "-b", "main")
        self._commit("chore: base", "README.md", "x\n")
        self._commit("feat(a): primeira [MS-001]", "a.py", "a\n")
        self._commit("feat(b): segunda [MS-002]", "b.py", "b\n")
        self._commit("fix(b): corrige a segunda [MS-002]", "b.py", "bb\n")
        self._commit("docs: sem ms", "c.md", "c\n")
        (self.dir / P_ARCHIVE / "ms001.json").write_text(
            json.dumps({"ms": "MS-001", "testes": 7}), encoding="utf-8")
        self._cwd = Path.cwd()
        os.chdir(self.dir)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def _registro(self):
        linha = (self.dir / tca.P_METRICAS).read_text(encoding="utf-8").strip().splitlines()[-1]
        return json.loads(linha)["indicadores"]

    def test_conta_apenas_commits_com_ms(self):
        self.assertEqual(tca.main(["metrics", "--write"]), 0)
        self.assertEqual(self._registro()["ms_entregues"]["valor"], 2)

    def test_cobertura_de_archive_dimensiona_o_gap(self):
        tca.main(["metrics", "--write"])
        d = self._registro()["ms_com_archive_pct"]
        self.assertEqual(d["valor"], 50.0, "1 de 2 MS tem archive")
        self.assertIn("1/2", d["nota"])

    def test_correcao_apos_entrega_e_contada(self):
        tca.main(["metrics", "--write"])
        self.assertEqual(self._registro()["correcoes_apos_entrega"]["valor"], 1)

    def test_todo_indicador_declara_origem(self):
        tca.main(["metrics", "--write"])
        for nome, d in self._registro().items():
            self.assertIn("origem", d, f"{nome} sem procedência")

    def test_testes_reporta_cobertura_do_campo(self):
        tca.main(["metrics", "--write"])
        self.assertEqual(self._registro()["testes_por_ms_mediana"]["cobertura"], "1/1")

    def test_modo_relatorio_nao_escreve(self):
        self.assertEqual(tca.main(["metrics"]), 0)
        self.assertFalse((self.dir / tca.P_METRICAS).exists())

    def test_mede_suite_pelo_contrato_declarado(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes": "python3 -c \"pass\"",
            "contar_testes": "python3 -c \"print(17)\"",
        }}), encoding="utf-8")
        self.assertEqual(tca.main(["metrics", "--write", "--medir-suite"]), 0)
        ind = self._registro()
        self.assertEqual(ind["suite_segundos"]["origem"], "derivado:execucao")
        self.assertEqual(ind["suite_testes"]["valor"], 17)
        self.assertNotIn("suite_segundos", " ".join(
            json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                       .strip().splitlines()[-1])["nao_instrumentado"]),
            "medido não pode constar como não instrumentado")

    def test_sem_contrato_vira_lacuna_e_nao_adivinha(self):
        self.assertEqual(tca.main(["metrics", "--write", "--medir-suite"]), 0)
        reg = json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertNotIn("suite_segundos", reg["indicadores"])
        self.assertTrue(any(tca.P_PROJETO_CFG in n for n in reg["nao_instrumentado"]),
                        "ausência de contrato deve virar lacuna declarada")

    def test_suite_que_falha_e_registrada_como_falha(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes": "python3 -c \"import sys; sys.exit(3)\"",
        }}), encoding="utf-8")
        tca.main(["metrics", "--write", "--medir-suite"])
        self.assertEqual(self._registro()["suite_segundos"]["resultado"], "exit 3")

    def test_contar_testes_fora_do_contrato_vira_lacuna(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes": "python3 -c \"pass\"",
            "contar_testes": "python3 -c \"print('dezessete')\"",
        }}), encoding="utf-8")
        tca.main(["metrics", "--write", "--medir-suite"])
        d = self._registro()["suite_testes"]
        self.assertIsNone(d["valor"])
        self.assertEqual(d["origem"], "lacuna")

    def test_conta_testes_sem_rodar_a_suite(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes": "python3 -c \"open('RODOU','w')\"",
            "contar_testes": "python3 -c \"print(2855)\"",
        }}), encoding="utf-8")
        self.assertEqual(tca.main(["metrics", "--write", "--contar-testes"]), 0)
        self.assertEqual(self._registro()["suite_testes"]["valor"], 2855)
        self.assertFalse((self.dir / "RODOU").exists(), "contar não pode executar a suíte")
        self.assertNotIn("suite_segundos", self._registro())

    def test_lacuna_distingue_falta_de_contrato_de_falta_de_ambiente(self):
        tca.main(["metrics", "--write"])
        reg = json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertTrue(any("declare comandos.testes" in n for n in reg["nao_instrumentado"]))

        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes": "python3 -c \"pass\""}}), encoding="utf-8")
        tca.main(["metrics", "--write"])
        reg = json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertTrue(any("--medir-suite" in n and "declare" not in n
                            for n in reg["nao_instrumentado"]),
                        "com contrato declarado, a lacuna é de ambiente, não de declaração")

    def test_perfil_suite_calcula_overhead(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "perfil_suite": "python3 -c \"print('{\\\"setup\\\":10.6,\\\"prepare\\\":12.0,\\\"total\\\":24.5}')\"",
        }}), encoding="utf-8")
        self.assertEqual(tca.main(["metrics", "--write", "--perfil-suite"]), 0)
        d = self._registro()["overhead_pct"]
        self.assertEqual(d["valor"], 92.2, "(10.6+12.0)/24.5")
        self.assertEqual(d["origem"], "derivado:execucao")

    def test_perfil_suite_fora_do_contrato_vira_lacuna(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "perfil_suite": "python3 -c \"print('lento')\"",
        }}), encoding="utf-8")
        tca.main(["metrics", "--write", "--perfil-suite"])
        self.assertEqual(self._registro()["overhead_pct"]["origem"], "lacuna")

    def test_loop_local_amostra_commits_reais(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "contar_testes": "python3 -c \"print(1000)\"",
            "testes_relacionados": "python3 -c \"pass\" {arquivos}",
            "contar_relacionados": "python3 -c \"print(30)\" {arquivos}",
        }}), encoding="utf-8")
        self.assertEqual(tca.main(["metrics", "--write", "--medir-loop", "--amostra", "3"]), 0)
        ind = self._registro()
        self.assertIsNotNone(ind["loop_local_segundos"]["valor"])
        self.assertIn("varridos", ind["loop_local_segundos"]["nota"],
                      "a nota deve dizer quantos commits foram varridos e quantos foram pulados")
        self.assertEqual(ind["testes_selecionados_pct"]["valor"], 3.0, "30 de 1000")

    def test_selecionados_sem_total_vira_lacuna(self):
        (self.dir / tca.P_PROJETO_CFG).write_text(json.dumps({"comandos": {
            "testes_relacionados": "python3 -c \"pass\" {arquivos}",
            "contar_relacionados": "python3 -c \"print(30)\" {arquivos}",
        }}), encoding="utf-8")
        tca.main(["metrics", "--write", "--medir-loop"])
        d = self._registro()["testes_selecionados_pct"]
        self.assertIsNone(d["valor"])
        self.assertEqual(d["origem"], "lacuna")

    def test_loop_sem_contrato_nao_adivinha(self):
        tca.main(["metrics", "--write", "--medir-loop"])
        reg = json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertNotIn("loop_local_segundos", reg["indicadores"])
        self.assertTrue(any("testes_relacionados" in n for n in reg["nao_instrumentado"]))

    def _fecha(self, ms, declarados, cenarios="CT-01, CT-02"):
        (self.dir / P_CTX).parent.mkdir(parents=True, exist_ok=True)
        (self.dir / P_CTX).write_text(
            f"**Fase atual:** GREEN\n**MS ativa:** {ms} — X\n"
            f"**Arquivos a criar/modificar:** {declarados}\n"
            f"**Cenários BDD:** {cenarios}\n", encoding="utf-8")
        tca.main(["close-ms", ms])

    def test_densidade_exige_contexto_preservado(self):
        """Archive legado não tem o contexto: densidade vira lacuna, não zero."""
        (self.dir / P_ARCHIVE / "ms001.json").write_text(
            json.dumps({"ms": "MS-001", "nome": "legado"}), encoding="utf-8")
        tca.main(["metrics", "--write"])
        reg = json.loads((self.dir / tca.P_METRICAS).read_text(encoding="utf-8")
                         .strip().splitlines()[-1])
        self.assertNotIn("linhas_por_arquivo_declarado", reg["indicadores"])
        self.assertTrue(any("contexto" in n for n in reg["nao_instrumentado"]))

    def test_densidade_calculada_de_ms_fechada_pelo_comando(self):
        self._fecha("MS-001", "a.py, b.py")
        self._commit("feat(x): entrega [MS-001]", "a.py", "conteudo\n")
        tca.main(["metrics", "--write"])
        ind = self._registro()
        self.assertIn("cenarios_por_ms_mediana", ind)
        self.assertEqual(ind["cenarios_por_ms_mediana"]["valor"], 2)
        self.assertIn("cobertura", ind["cenarios_por_ms_mediana"])

    def test_custo_fixo_declara_ser_teto_e_nao_piso(self):
        tca.main(["metrics", "--write"])
        d = self._registro().get("custo_fixo_estimado_horas", {})
        if d.get("valor") is not None:
            self.assertIn("TETO", d["nota"], "estimativa tem de declarar que é limite superior")
        else:
            self.assertEqual(d["origem"], "lacuna")

    def test_parcela_mecanica_do_custo_fixo_e_medida(self):
        tca.main(["metrics", "--write"])
        d = self._registro()["custo_fixo_mecanico_segundos"]
        self.assertEqual(d["origem"], "derivado:execucao")
        self.assertIsNotNone(d["valor"])

    def test_detectar_nao_executa(self):
        (self.dir / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        (self.dir / "marcador").write_text("intacto", encoding="utf-8")
        self.assertEqual(tca.main(["metrics", "--detectar"]), 0)
        self.assertFalse((self.dir / tca.P_METRICAS).exists(), "detectar não escreve")

    def test_valor_reportado_e_marcado_como_tal(self):
        tca.main(["metrics", "--write", "--suite-segundos", "93"])
        d = self._registro()["suite_segundos"]
        self.assertEqual((d["valor"], d["origem"]), (93, "reportado"))

    def test_sem_ms_no_historico_avisa_em_vez_de_inventar(self):
        self._git(self.dir, "checkout", "-q", "--orphan", "vazio")
        self._git(self.dir, "rm", "-rqf", ".")
        (self.dir / P_ARCHIVE).mkdir(parents=True, exist_ok=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        self._commit("chore: nada", "z.md", "z\n")
        self.assertEqual(tca.main(["metrics"]), 0)


class TestAmbienteETune(unittest.TestCase):
    """Máquinas distintas: medida sem ambiente é incomparável."""

    def setUp(self):
        import os
        self.dir = Path(tempfile.mkdtemp())
        (self.dir / "docs/ThronusSpec/05_Monitoramento").mkdir(parents=True)
        (self.dir / "docs/ThronusSpec/03_Desenvolvimento").mkdir(parents=True)
        (self.dir / P_INDEX).write_text('{"estado_da_trilha":{}}', encoding="utf-8")
        self._cwd = Path.cwd()
        os.chdir(self.dir)

    def tearDown(self):
        import os
        os.chdir(self._cwd)
        shutil.rmtree(self.dir, ignore_errors=True)

    def _grava(self, host, **indicadores):
        reg = {"ts": "2026-08-25T10:00:00-03:00", "ref": "abc", "tca_versao": "9.9.9",
               "ambiente": {"host": host, "cores": 8, "ram_gb": 32,
                            "disco_rotacional": False, "so": "Linux"},
               "indicadores": {k: {"valor": v, "origem": "derivado:execucao"}
                               for k, v in indicadores.items()},
               "nao_instrumentado": []}
        with (self.dir / tca.P_METRICAS).open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(reg) + "\n")

    def test_ambiente_tem_os_campos_que_tornam_a_medida_comparavel(self):
        amb = tca.ambiente()
        for k in ("host", "cores", "ram_gb", "disco_rotacional", "so"):
            self.assertIn(k, amb)

    def test_tune_ignora_medicao_de_outra_maquina(self):
        self._grava("outra-maquina", overhead_pct=95.0)
        self.assertEqual(tca.main(["tune", "--write"]), 0)
        host = tca.ambiente()["host"]
        d = json.loads((self.dir / tca.P_TUNING.format(host=host)).read_text(encoding="utf-8"))
        self.assertIsNone(d["baseado_em"], "medição de outra máquina não pode ser usada")
        self.assertIsNone(d["parametros"]["isolamento_por_arquivo"])

    def test_tune_usa_medicao_da_propria_maquina(self):
        self._grava(tca.ambiente()["host"], overhead_pct=92.8, loop_local_segundos=4.4)
        tca.main(["tune", "--write"])
        host = tca.ambiente()["host"]
        d = json.loads((self.dir / tca.P_TUNING.format(host=host)).read_text(encoding="utf-8"))
        self.assertIs(d["parametros"]["isolamento_por_arquivo"], False)
        self.assertIsNotNone(d["baseado_em"])

    def test_overhead_baixo_mantem_isolamento(self):
        self._grava(tca.ambiente()["host"], overhead_pct=12.0)
        tca.main(["tune", "--write"])
        host = tca.ambiente()["host"]
        d = json.loads((self.dir / tca.P_TUNING.format(host=host)).read_text(encoding="utf-8"))
        self.assertIs(d["parametros"]["isolamento_por_arquivo"], True)

    def test_toda_recomendacao_carrega_evidencia(self):
        self._grava(tca.ambiente()["host"], overhead_pct=92.8)
        tca.main(["tune", "--write"])
        host = tca.ambiente()["host"]
        d = json.loads((self.dir / tca.P_TUNING.format(host=host)).read_text(encoding="utf-8"))
        for r in d["recomendacoes"]:
            self.assertTrue(r.get("porque") and r.get("evidencia"),
                            f"{r['parametro']} sem porquê ou evidência")

    def test_arquivo_e_por_maquina(self):
        tca.main(["tune", "--write"])
        gerados = list((self.dir / ".tca").glob("tuning-*.json"))
        self.assertEqual(len(gerados), 1)
        self.assertIn(tca.ambiente()["host"], gerados[0].name)


class TestPacote(unittest.TestCase):
    def test_manifesto_integro(self):
        self.assertEqual(tca.main(["verify-self"]), 0)

    def test_manifesto_em_dia(self):
        self.assertEqual(tca.main(["manifest"]), 0,
                         "manifesto desatualizado — rode: tca manifest --write")

    def test_bytecode_nunca_entra_no_manifesto(self):
        """Bytecode existe na máquina de quem rodou os testes e não existe em
        checkout limpo. Incluí-lo faz o verify-self passar aqui e falhar no CI."""
        listados = [f.relative_to(PKG).as_posix() for f in tca._arquivos_do_pacote()]
        for nome in listados:
            self.assertNotIn("__pycache__", nome)
            self.assertFalse(nome.endswith(".pyc"), nome)
        self.assertNotIn("MANIFEST.sha256", listados, "o manifesto não se lista")

    def test_ms_ativa_reconhece_ausencia(self):
        for vazio in ("**MS ativa:** —", "**MS ativa:**", "**MS ativa:** -", "sem campo"):
            self.assertIsNone(tca.ms_ativa_no_contexto(vazio), repr(vazio))
        self.assertEqual(tca.ms_ativa_no_contexto("**MS ativa:** MS-009 — X"), "MS-009 — X")


if __name__ == "__main__":
    unittest.main(verbosity=2)
