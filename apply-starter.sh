#!/usr/bin/env bash
# apply-starter.sh — Aplica um starter tecnológico ao projeto, APÓS [ESTADO_ARCHITECTURE].
#
# Uso: ./apply-starter.sh <starter> [--force]
#
# Exemplos:
#   ./apply-starter.sh python-django
#   ./apply-starter.sh node-express
#
# Idempotente: reaplicar o mesmo starter é no-op. Use --force para sobrescrever
# os arquivos do starter (isso descarta edições locais neles).
#
# O script copia starters/<starter>/ sobre a raiz do projeto, renomeia os
# diretórios {{PACKAGE_NAME}} e substitui os placeholders no conteúdo dos
# arquivos. Nunca execute antes do ADR aprovado — a stack não está decidida.

set -euo pipefail

STARTER=""
FORCE="false"
for arg in "$@"; do
  case "$arg" in
    --force) FORCE="true" ;;
    -*)      echo "ERRO: opção desconhecida '$arg'"; exit 1 ;;
    *)       [[ -z "$STARTER" ]] && STARTER="$arg" ;;
  esac
done

ROOT="$(cd "$(dirname "$0")" && pwd)"
META="${ROOT}/.thronus-template-version"

listar_starters() {
  echo "Starters disponíveis:"
  for d in "${ROOT}"/starters/*/; do
    [[ -d "$d" ]] || continue
    nome="$(basename "$d")"
    if [[ -d "${d}src" ]]; then
      echo "  ${nome}  — scaffold completo"
    else
      echo "  ${nome}  — somente referência (README): scaffold manual"
    fi
  done
}

if [[ -z "$STARTER" ]]; then
  echo "Uso: ./apply-starter.sh <starter> [--force]"
  echo ""
  listar_starters
  exit 1
fi

if [[ ! -d "${ROOT}/starters/${STARTER}" ]]; then
  echo "ERRO: starter '${STARTER}' não existe."
  echo ""
  listar_starters
  exit 1
fi

# ── 1. Recuperar identidade do projeto ────────────────────────────────────────
if [[ ! -f "$META" ]]; then
  echo "ERRO: .thronus-template-version não encontrado."
  echo "Este script roda no projeto derivado, não no thronus-template."
  exit 1
fi

ler_meta() { sed -n "s/^$1=//p" "$META" | head -1; }

PROJECT_NAME="$(ler_meta project)"
PACKAGE_NAME="$(ler_meta package)"
CLIENT_NAME="$(ler_meta client)"
PERFIL="$(ler_meta perfil)"
TODAY="$(date +%Y-%m-%d)"

# Projetos criados antes do campo `package` existir
[[ -n "$PACKAGE_NAME" ]] || PACKAGE_NAME="${PROJECT_NAME//-/_}"

if [[ -z "$PROJECT_NAME" ]]; then
  echo "ERRO: campo 'project' ausente em .thronus-template-version."
  exit 1
fi

# ── 2. Gate: o ADR precisa estar aprovado ─────────────────────────────────────
ADR="${ROOT}/docs/ThronusSpec/01_Planejamento/architecture_decision.md"
if [[ ! -f "$ADR" ]]; then
  echo "⚠  ADR não encontrado em docs/ThronusSpec/01_Planejamento/architecture_decision.md"
  echo "   Starters só devem ser aplicados após [ESTADO_ARCHITECTURE]."
  read -r -p "   Aplicar mesmo assim? [y/N] " resposta
  [[ "$resposta" =~ ^[Yy]$ ]] || exit 1
fi

# ── 2-A. Idempotência: starter já aplicado ────────────────────────────────────
STARTER_ATUAL="$(ler_meta starter)"
if [[ -n "$STARTER_ATUAL" && "$FORCE" != "true" ]]; then
  if [[ "$STARTER_ATUAL" == "$STARTER" ]]; then
    echo "  ✓ starter '${STARTER}' já aplicado — nada a fazer."
    echo "    Para sobrescrever os arquivos do starter: ./apply-starter.sh ${STARTER} --force"
    exit 0
  fi
  echo "ERRO: o starter '${STARTER_ATUAL}' já foi aplicado a este projeto."
  echo "      Trocar de stack depois do ADR exige um novo ADR. Se for mesmo o caso:"
  echo "      ./apply-starter.sh ${STARTER} --force"
  exit 1
fi

echo "► Aplicando starter '${STARTER}'..."
echo "  Projeto : ${PROJECT_NAME}"
echo "  Pacote  : ${PACKAGE_NAME}"
echo "  Perfil  : ${PERFIL}"
echo ""

if [[ ! -d "${ROOT}/starters/${STARTER}/src" ]]; then
  echo "⚠  O starter '${STARTER}' é somente referência — não tem scaffold."
  echo "   Consulte starters/${STARTER}/README.md e construa a estrutura manualmente."
  exit 0
fi

# ── 3. Copiar o starter sobre a raiz (complementa, não substitui) ─────────────
cp -r "${ROOT}/starters/${STARTER}/." "${ROOT}/"
rm -f "${ROOT}/README.md.starter"

# ── 4. Renomear diretórios com placeholder (o sed só toca em conteúdo) ────────
while IFS= read -r dir; do
  destino="$(dirname "$dir")/${PACKAGE_NAME}"
  if [[ -d "$destino" ]]; then
    cp -r "$dir/." "$destino/" && rm -rf "$dir"
  else
    mv "$dir" "$destino"
  fi
done < <(find "$ROOT" -depth -type d -name '{{PACKAGE_NAME}}' -not -path "*/starters/*")

# ── 5. Substituir placeholders no conteúdo ────────────────────────────────────
find "$ROOT" -type f \( -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" \
  -o -name "*.yaml" -o -name "*.ini" -o -name "*.toml" -o -name "*.ts" -o -name "*.js" \
  -o -name "*.cfg" -o -name "*.txt" -o -name "*.example" \) \
  -not -path "*/starters/*" -not -path "*/.git/*" | while read -r file; do
  sed -i \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{PACKAGE_NAME}}/${PACKAGE_NAME}/g" \
    -e "s/{{CLIENT_NAME}}/${CLIENT_NAME}/g" \
    -e "s/{{DATA_INICIO}}/${TODAY}/g" \
    -e "s/{{PERFIL}}/${PERFIL}/g" \
    "$file"
done

# ── 6. Registrar o starter aplicado ──────────────────────────────────────────
if grep -q '^starter=' "$META"; then
  sed -i "s|^starter=.*|starter=${STARTER}|" "$META"
else
  echo "starter=${STARTER}" >> "$META"
fi

# ── 7. pre-commit, se o starter trouxe configuração ──────────────────────────
if [[ -f "${ROOT}/.pre-commit-config.yaml" ]] && command -v pre-commit &>/dev/null; then
  (cd "$ROOT" && pre-commit install) && echo "  ✓ pre-commit instalado"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  [APPLY-STARTER] STARTER APLICADO"
echo "  Starter : ${STARTER}"
echo "  Pacote  : src/${PACKAGE_NAME}/"
echo ""
echo "  Próximos passos:"
echo "  1. Revise as dependências e o CI trazidos pelo starter"
echo "  2. Preencha 'arquitetura_e_padroes' em payload_index.json conforme o ADR"
echo "  3. git add -A && git commit -m \"chore: aplica starter ${STARTER} conforme ADR-001\""
echo "  4. Acione [ESTADO_SPEC] para iniciar o ciclo TDD"
echo "════════════════════════════════════════════════════════"
