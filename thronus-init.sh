#!/usr/bin/env bash
# thronus-init.sh — Inicializa um novo projeto a partir do thronus-template.
#
# Uso: ./thronus-init.sh <nome-projeto> "<nome-cliente>" [perfil] [diretorio-destino]
#
# Perfis: nano | micro | standard | enterprise (padrão: standard)
#
# Exemplos:
#   ./thronus-init.sh edutrack "Prefeitura de Salvador"
#   ./thronus-init.sh migrador-dados "Secretaria de Fazenda" nano
#   ./thronus-init.sh saude-api "SMS Bahia" micro ~/projetos/saude-api

set -euo pipefail

# ── Argumentos ────────────────────────────────────────────────────────────────
PROJECT_NAME="${1:-}"
CLIENT_NAME="${2:-}"
PERFIL="${3:-standard}"
DEST_DIR="${4:-"${HOME}/projetos/${PROJECT_NAME}"}"

if [[ -z "$PROJECT_NAME" || -z "$CLIENT_NAME" ]]; then
  echo "Uso: ./thronus-init.sh <nome-projeto> \"<nome-cliente>\" [perfil] [diretorio-destino]"
  echo ""
  echo "Perfis disponíveis:"
  echo "  nano       — Script, automação, POC. ≤5 Micro Specs. Pipeline mínimo."
  echo "  micro      — API, MVP, portal simples. 5–15 MSs. Pipeline completo sem gates formais."
  echo "  standard   — Sistema de gestão, SaaS, plataforma. 15–50 MSs. (padrão)"
  echo "  enterprise — Sistema crítico, contrato governamental. 50+ MSs. Gates + compliance."
  echo ""
  echo "Exemplo:"
  echo "  ./thronus-init.sh edutrack \"Prefeitura de Salvador\" standard"
  exit 1
fi

# Validar perfil
PERFIS_VALIDOS="nano micro standard enterprise"
if ! echo "$PERFIS_VALIDOS" | grep -qw "$PERFIL"; then
  echo "ERRO: perfil '$PERFIL' inválido. Use: nano | micro | standard | enterprise"
  exit 1
fi

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY="$(date +%Y-%m-%d)"

echo "► Criando projeto '$PROJECT_NAME' para '$CLIENT_NAME'..."
echo "  Perfil  : $PERFIL"
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
rm -f thronus-init.sh  # Não propagar o script de init no projeto novo

# ── 2. Substituir placeholders ────────────────────────────────────────────────
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" \
  -o -name "*.yaml" -o -name "*.ini" -o -name "*.toml" -o -name "*.sh" \) | while read -r file; do
  sed -i \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{CLIENT_NAME}}/${CLIENT_NAME}/g" \
    -e "s/{{DATA_INICIO}}/${TODAY}/g" \
    -e "s/{{PERFIL}}/${PERFIL}/g" \
    "$file"
done

# ── 3. Criar estrutura agnóstica de src/ ──────────────────────────────────────
# Apenas o esqueleto de pastas — a stack real é decidida em [ESTADO_ARCHITECTURE].
# Starters tecnológicos em starters/<stack>/ são opcionais e aplicados após o ADR.
mkdir -p "src/${PROJECT_NAME}/domain"
mkdir -p "src/${PROJECT_NAME}/application/ports"
mkdir -p "src/${PROJECT_NAME}/application/services"
mkdir -p "src/${PROJECT_NAME}/infrastructure"
mkdir -p "tests/domain"
mkdir -p "tests/application/services"
mkdir -p "tests/infrastructure"
mkdir -p "context"
mkdir -p "docs/ThronusSpec/01_Planejamento"

# Arquivo de contexto ativo (RAM da sessão)
cat > "context/activeContext.md" <<'EOF'
# Active Context — TCA Session RAM

> Este arquivo é a RAM da sessão TCA. É preenchido e limpo automaticamente pelo pipeline.
> Não editar manualmente durante uma sessão ativa.

**Fase atual:** DISCOVERY
**MS ativa:** —
**Arquivos a criar/modificar:** —
**Cenários BDD:** —
EOF

# ── 4. Criar .gitignore base ──────────────────────────────────────────────────
# Um .gitignore mínimo — o starter tecnológico adiciona entradas específicas da stack
if [[ ! -f ".gitignore" ]]; then
  cat > ".gitignore" <<'EOF'
# TCA session files
context/activeContext.md

# Dependências (completar após decisão de arquitetura)
node_modules/
__pycache__/
*.pyc
.venv/
target/
vendor/

# Ambiente
.env
.env.*
!.env.example

# Build
dist/
build/
*.egg-info/

# IDEs
.idea/
.vscode/
*.sw*
EOF
fi

# ── 5. Listar starters disponíveis ───────────────────────────────────────────
STARTERS_DISPONIVEIS=""
if [[ -d "starters" ]]; then
  STARTERS_DISPONIVEIS=$(ls starters/ 2>/dev/null | tr '\n' ' ')
fi

# ── 6. Inicializar git ────────────────────────────────────────────────────────
git init -b main
git add .
git commit -m "chore: inicializa projeto ${PROJECT_NAME} (perfil: ${PERFIL}) a partir do thronus-template

Co-Authored-By: Thronus TCA <noreply@thronus.dev>"

# ── 7. Instalar pre-commit (se disponível e se .pre-commit-config.yaml existir) ──
if [[ -f ".pre-commit-config.yaml" ]] && command -v pre-commit &>/dev/null; then
  pre-commit install
  echo "  ✓ pre-commit instalado"
fi

# ── Resumo ───────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════"
echo "  [THRONUS-INIT] PROJETO CRIADO COM SUCESSO"
echo "  Nome   : ${PROJECT_NAME}"
echo "  Cliente: ${CLIENT_NAME}"
echo "  Perfil : ${PERFIL}"
echo "  Destino: ${DEST_DIR}"
echo ""
echo "  Próximos passos:"
echo "  1. cd ${DEST_DIR}"
echo "  2. Abra o projeto no Claude Code"
echo "  3. Acione: [ESTADO_DISCOVERY] para iniciar o pipeline TCA"
echo ""
if [[ -n "$STARTERS_DISPONIVEIS" ]]; then
  echo "  Starters disponíveis (aplicar após [ESTADO_ARCHITECTURE]):"
  for s in $STARTERS_DISPONIVEIS; do
    echo "    → starters/${s}/"
  done
  echo ""
fi
echo "  A stack tecnológica será decidida em [ESTADO_ARCHITECTURE]."
echo "  Não assuma Python/Django nem nenhum framework específico até lá."
echo "════════════════════════════════════════════════════════"
