#!/usr/bin/env bash
# thronus-init.sh — Inicializa um novo projeto a partir do thronus-template.
#
# Uso: ./thronus-init.sh <nome-projeto> "<nome-cliente>" [perfil] [diretorio-destino]
#
# Perfis: nano | micro | agentes | standard | enterprise (padrão: standard)
#
# Exemplos:
#   ./thronus-init.sh edutrack "Prefeitura de Salvador"
#   ./thronus-init.sh migrador-dados "Secretaria de Fazenda" nano
#   ./thronus-init.sh saude-api "SMS Bahia" micro ~/projetos/saude-api
#   ./thronus-init.sh atendente-wpp "Clínica Vida" agentes
#
# Pré-requisitos para criação automática do repo GitHub:
#   - gh CLI autenticado (gh auth login)
#   - Variável GITHUB_ORG definida abaixo ou via env

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
  echo "  agentes    — Agentes de IA, copilotos e automações conversacionais. 3–12 MSs."
  echo "  standard   — Sistema de gestão, SaaS, plataforma. 15–50 MSs. (padrão)"
  echo "  enterprise — Sistema crítico, contrato governamental. 50+ MSs. Gates + compliance."
  echo ""
  echo "Exemplo:"
  echo "  ./thronus-init.sh edutrack \"Prefeitura de Salvador\" standard"
  exit 1
fi

# Validar perfil
PERFIS_VALIDOS="nano micro agentes standard enterprise"
if ! echo "$PERFIS_VALIDOS" | grep -qw "$PERFIL"; then
  echo "ERRO: perfil '$PERFIL' inválido. Use: nano | micro | agentes | standard | enterprise"
  exit 1
fi

# O nome do projeto aceita hífen; o pacote de código não — Python, Go e Java
# rejeitam hífen em identificador. PACKAGE_NAME é o slug usado em src/.
PACKAGE_NAME="${PROJECT_NAME//-/_}"

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY="$(date +%Y-%m-%d)"
GITHUB_ORG="${GITHUB_ORG:-diegoalvarez-AI}"
TEMPLATE_REPO="thronus-template"
TEMPLATE_VERSION="$(cd "$TEMPLATE_DIR" && git describe --tags --abbrev=0 2>/dev/null || echo "v1.0.0")"

echo "► Criando projeto '$PROJECT_NAME' para '$CLIENT_NAME'..."
echo "  Perfil  : $PERFIL"
echo "  Template: $TEMPLATE_DIR @ $TEMPLATE_VERSION"
echo "  Destino : $DEST_DIR"
echo "  GitHub  : github.com/${GITHUB_ORG}/${PROJECT_NAME}"
echo ""

# ── 1. Copiar template ────────────────────────────────────────────────────────
if [[ -d "$DEST_DIR" ]]; then
  # Idempotência: reexecutar sobre um projeto já inicializado é no-op, não erro.
  if [[ -f "${DEST_DIR}/.thronus-template-version" ]] \
     && grep -qx "project=${PROJECT_NAME}" "${DEST_DIR}/.thronus-template-version"; then
    echo "  ✓ '${PROJECT_NAME}' já inicializado em ${DEST_DIR} — nada a fazer."
    echo "    Para aplicar um starter:  cd ${DEST_DIR} && ./apply-starter.sh <stack>"
    exit 0
  fi
  echo "ERRO: diretório '$DEST_DIR' já existe e não é um projeto '${PROJECT_NAME}'."
  echo "      Escolha outro destino."
  exit 1
fi
cp -r "$TEMPLATE_DIR" "$DEST_DIR"
cd "$DEST_DIR"
rm -f thronus-init.sh  # Não propagar o script de init no projeto derivado

# ── 2. Substituir placeholders ────────────────────────────────────────────────
# Duas exclusões deliberadas:
#  - starters/ é template-dentro-de-template: seus placeholders só são resolvidos
#    por ./apply-starter.sh, depois do ADR.
#  - apply-starter.sh é ferramenta, não conteúdo: os placeholders no código dele
#    são os padrões que ele procura. Substituí-los o transformaria num no-op.
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.json" -o -name "*.yml" \
  -o -name "*.yaml" -o -name "*.ini" -o -name "*.toml" -o -name "*.sh" \) \
  -not -path "./starters/*" -not -name "apply-starter.sh" | while read -r file; do
  sed -i \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{PACKAGE_NAME}}/${PACKAGE_NAME}/g" \
    -e "s/{{CLIENT_NAME}}/${CLIENT_NAME}/g" \
    -e "s/{{DATA_INICIO}}/${TODAY}/g" \
    -e "s/{{PERFIL}}/${PERFIL}/g" \
    "$file"
done

# ── 3. Criar estrutura agnóstica de src/ ──────────────────────────────────────
# Apenas o esqueleto de pastas — a stack real é decidida em [ESTADO_ARCHITECTURE].
# Starters tecnológicos em starters/<stack>/ são opcionais e aplicados após o ADR.
mkdir -p "src/${PACKAGE_NAME}/domain"
mkdir -p "src/${PACKAGE_NAME}/application/ports"
mkdir -p "src/${PACKAGE_NAME}/application/services"
mkdir -p "src/${PACKAGE_NAME}/infrastructure"
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
  # Apenas diretórios — starters/README.md não é um starter.
  for d in starters/*/; do
    [[ -d "$d" ]] && STARTERS_DISPONIVEIS+="$(basename "$d") "
  done
fi

# ── 6. Registrar versão do template ──────────────────────────────────────────
cat > ".thronus-template-version" <<EOF
template_repo=https://github.com/${GITHUB_ORG}/${TEMPLATE_REPO}
template_version=${TEMPLATE_VERSION}
derived_at=${TODAY}
project=${PROJECT_NAME}
package=${PACKAGE_NAME}
client=${CLIENT_NAME}
perfil=${PERFIL}
starter=
EOF

# ── 7. Inicializar git ────────────────────────────────────────────────────────
[[ -d .git ]] || git init -b main
git add .
if git diff --cached --quiet; then
  echo "  ✓ nada a commitar — árvore já registrada"
else
  git commit -m "chore: inicializa projeto ${PROJECT_NAME} (perfil: ${PERFIL}) a partir do thronus-template@${TEMPLATE_VERSION}

Co-Authored-By: Thronus TCA <noreply@thronus.dev>"
fi

# ── 8. Criar repositório no GitHub e configurar remotes ──────────────────────
if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
  if git remote get-url origin &>/dev/null; then
    echo "  ✓ remote 'origin' já configurado — pulando criação do repositório"
  else
    echo "► Criando repositório no GitHub..."
    gh repo create "${GITHUB_ORG}/${PROJECT_NAME}" \
      --private \
      --description "${PROJECT_NAME} — ${CLIENT_NAME} (Thronus TCA ${TEMPLATE_VERSION})" \
      --source=. \
      --remote=origin \
      --push
  fi

  # Adiciona thronus-template como upstream para receber atualizações futuras
  git remote get-url upstream &>/dev/null \
    || git remote add upstream "https://github.com/${GITHUB_ORG}/${TEMPLATE_REPO}.git"
  echo "  ✓ Remote 'upstream' configurado → github.com/${GITHUB_ORG}/${TEMPLATE_REPO}"
  echo ""
  echo "  Para sincronizar com uma nova versão do template:"
  echo "    git fetch upstream"
  echo "    git merge upstream/main --allow-unrelated-histories"
else
  echo "  ⚠ gh CLI não encontrado ou não autenticado. Configure manualmente:"
  echo "    gh auth login"
  echo "    gh repo create ${GITHUB_ORG}/${PROJECT_NAME} --private --source=. --remote=origin --push"
  echo "    git remote add upstream https://github.com/${GITHUB_ORG}/${TEMPLATE_REPO}.git"
fi

# ── 9. Instalar pre-commit ───────────────────────────────────────────────────
# A raiz é agnóstica de stack e não traz .pre-commit-config.yaml — os hooks de
# lint chegam com o starter, e ./apply-starter.sh reinstala o pre-commit depois.
if [[ -f ".pre-commit-config.yaml" ]] && command -v pre-commit &>/dev/null; then
  pre-commit install
  echo "  ✓ pre-commit instalado"
fi

# ── Resumo ───────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════"
echo "  [THRONUS-INIT] PROJETO CRIADO COM SUCESSO"
echo "  Nome       : ${PROJECT_NAME}"
echo "  Cliente    : ${CLIENT_NAME}"
echo "  Perfil     : ${PERFIL}"
echo "  Template   : ${TEMPLATE_VERSION}"
echo "  Destino    : ${DEST_DIR}"
echo "  Repo       : github.com/${GITHUB_ORG}/${PROJECT_NAME}"
echo ""
echo "  Próximos passos:"
echo "  1. cd ${DEST_DIR}"
echo "  2. Abra o projeto no seu agente de código (leia AGENTS.md)"
echo "  3. Acione: [ESTADO_DISCOVERY] para iniciar o pipeline TCA"
echo ""
echo "  Atualizar template no futuro:"
echo "    git fetch upstream && git merge upstream/main"
echo ""
if [[ -n "$STARTERS_DISPONIVEIS" ]]; then
  echo "  Starters disponíveis (aplicar SOMENTE após [ESTADO_ARCHITECTURE]):"
  for s in $STARTERS_DISPONIVEIS; do
    echo "    ./apply-starter.sh ${s}"
  done
  echo ""
fi
echo "  A stack tecnológica será decidida em [ESTADO_ARCHITECTURE]."
echo "  Não assuma Python/Django nem nenhum framework específico até lá."
echo "════════════════════════════════════════════════════════"
