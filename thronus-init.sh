#!/usr/bin/env bash
# thronus-init.sh — Inicializa um novo projeto a partir do thronus-template.
#
# Uso: ./thronus-init.sh <nome-projeto> "<nome-cliente>" [diretorio-destino]
#
# Exemplo:
#   ./thronus-init.sh edutrack "Prefeitura de Salvador" ~/projetos/edutrack
#   ./thronus-init.sh saudebahia "SMS Bahia"
#
# O que faz:
#   1. Copia o template para o diretório destino
#   2. Substitui todos os placeholders {{PROJECT_NAME}} e {{CLIENT_NAME}}
#   3. Renomeia src/app/ para src/<nome-projeto>/
#   4. Ajusta pytest.ini e settings com o novo nome
#   5. Inicializa git e instala pre-commit
#   6. Cria a primeira migration (EventoAuditoria)

set -euo pipefail

# ── Argumentos ────────────────────────────────────────────────────────────────
PROJECT_NAME="${1:-}"
CLIENT_NAME="${2:-}"
DEST_DIR="${3:-"${HOME}/projetos/${PROJECT_NAME}"}"

if [[ -z "$PROJECT_NAME" || -z "$CLIENT_NAME" ]]; then
  echo "Uso: ./thronus-init.sh <nome-projeto> \"<nome-cliente>\" [diretorio-destino]"
  echo "Exemplo: ./thronus-init.sh edutrack \"Prefeitura de Salvador\""
  exit 1
fi

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY="$(date +%Y-%m-%d)"

echo "► Criando projeto '$PROJECT_NAME' para '$CLIENT_NAME'..."
echo "  Template: $TEMPLATE_DIR"
echo "  Destino : $DEST_DIR"
echo ""

# ── 1. Copiar template ────────────────────────────────────────────────────────
if [[ -d "$DEST_DIR" ]]; then
  echo "ERRO: diretório '$DEST_DIR' já existe. Escolha outro destino."
  exit 1
fi
cp -r "$TEMPLATE_DIR" "$DEST_DIR"
cd "$DEST_DIR"
rm -f thronus-init.sh  # Remove o script de init do projeto novo

# ── 2. Substituir placeholders ────────────────────────────────────────────────
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.ini" -o -name "*.toml" \) | while read -r file; do
  sed -i \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{CLIENT_NAME}}/${CLIENT_NAME}/g" \
    -e "s/{{DATA_INICIO}}/${TODAY}/g" \
    "$file"
done

# ── 3. Renomear src/app/ para src/<projeto>/ ─────────────────────────────────
mv "src/app" "src/${PROJECT_NAME}"

# Ajustar imports que referenciam "app." para "<projeto>."
find . -type f -name "*.py" | while read -r file; do
  sed -i "s/from app\./from ${PROJECT_NAME}./g" "$file"
  sed -i "s/import app\./import ${PROJECT_NAME}./g" "$file"
done

# Ajustar pytest.ini e CI
sed -i "s|src/app/infrastructure|src/${PROJECT_NAME}/infrastructure|g" pytest.ini
sed -i "s|app\.infrastructure\.config\.settings_test|${PROJECT_NAME}.infrastructure.config.settings_test|g" pytest.ini
sed -i "s|app\.infrastructure\.config\.settings_test|${PROJECT_NAME}.infrastructure.config.settings_test|g" .github/workflows/ci.yml

# Ajustar DJANGO_SETTINGS_MODULE no settings_test.py
sed -i "s|from \.settings import|from .settings import|g" "src/${PROJECT_NAME}/infrastructure/config/settings_test.py"

# ── 4. Ajustar logger name nos settings ──────────────────────────────────────
sed -i "s|\"app\": {|\"${PROJECT_NAME}\": {|g" "src/${PROJECT_NAME}/infrastructure/config/settings.py"

# ── 5. Inicializar git ────────────────────────────────────────────────────────
git init -b main
git add .
git commit -m "chore: inicializa projeto ${PROJECT_NAME} a partir do thronus-template

Co-Authored-By: Thronus TCA <noreply@thronus.dev>"

# ── 6. Instalar pre-commit (se disponível) ───────────────────────────────────
if command -v pre-commit &>/dev/null; then
  pre-commit install
  echo "  ✓ pre-commit instalado"
else
  echo "  ⚠ pre-commit não encontrado — instale com: pip install pre-commit && pre-commit install"
fi

# ── 7. Criar __init__.py faltantes ──────────────────────────────────────────
for dir in \
  "src/${PROJECT_NAME}/infrastructure" \
  "src/${PROJECT_NAME}/infrastructure/config" \
  "src/${PROJECT_NAME}/infrastructure/persistence" \
  "src/${PROJECT_NAME}/application" \
  "src/${PROJECT_NAME}/application/validators" \
  "tests" \
  "tests/domain" \
  "tests/application" \
  "tests/application/services" \
  "tests/infrastructure"; do
  touch "${dir}/__init__.py" 2>/dev/null || true
done

# ── Resumo ───────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════"
echo "  [THRONUS-INIT] PROJETO CRIADO COM SUCESSO"
echo "  Nome     : ${PROJECT_NAME}"
echo "  Cliente  : ${CLIENT_NAME}"
echo "  Destino  : ${DEST_DIR}"
echo ""
echo "  Próximos passos:"
echo "  1. cd ${DEST_DIR}"
echo "  2. pip install -r requirements-dev.txt"
echo "  3. Preencha as variáveis em .env (copie de .env.example)"
echo "  4. Abra o CLAUDE.md e confirme os dados do projeto"
echo "  5. Invoque: /tcaOrchestratorSkill para iniciar MS-001"
echo "════════════════════════════════════════════════════════"
