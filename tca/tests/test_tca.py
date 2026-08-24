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


class TestPacote(unittest.TestCase):
    def test_manifesto_integro(self):
        self.assertEqual(tca.main(["verify-self"]), 0)

    def test_ms_ativa_reconhece_ausencia(self):
        for vazio in ("**MS ativa:** —", "**MS ativa:**", "**MS ativa:** -", "sem campo"):
            self.assertIsNone(tca.ms_ativa_no_contexto(vazio), repr(vazio))
        self.assertEqual(tca.ms_ativa_no_contexto("**MS ativa:** MS-009 — X"), "MS-009 — X")


if __name__ == "__main__":
    unittest.main(verbosity=2)
