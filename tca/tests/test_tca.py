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


class TestPacote(unittest.TestCase):
    def test_manifesto_integro(self):
        self.assertEqual(tca.main(["verify-self"]), 0)

    def test_ms_ativa_reconhece_ausencia(self):
        for vazio in ("**MS ativa:** —", "**MS ativa:**", "**MS ativa:** -", "sem campo"):
            self.assertIsNone(tca.ms_ativa_no_contexto(vazio), repr(vazio))
        self.assertEqual(tca.ms_ativa_no_contexto("**MS ativa:** MS-009 — X"), "MS-009 — X")


if __name__ == "__main__":
    unittest.main(verbosity=2)
