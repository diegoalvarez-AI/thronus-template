# Starter: node-express

**Stack:** Node.js 20 · Express 4 · TypeScript 5 · Prisma ORM · PostgreSQL 16 · Jest · Docker Compose

**Quando usar:** APIs REST leves, BFFs (Backend For Frontend), integrações e webhooks, serviços event-driven.

## Aplicar este starter

```bash
cp -r starters/node-express/. .
sed -i "s/{{PROJECT_NAME}}/<nome-projeto>/g" $(find . -type f -name "*.ts" -o -name "*.json" -o -name "*.yml")
npm install
```

## Estrutura gerada

```
src/
├── domain/              # Entidades e interfaces de domínio (TypeScript types puros)
├── application/
│   ├── ports/           # Interfaces TypeScript (Port/Adapter)
│   └── services/        # Casos de uso — dependem apenas de ports
└── infrastructure/
    ├── config/          # env.ts (zod validation), app.ts (Express setup)
    ├── persistence/     # Prisma schema, repositories (implementam ports)
    └── http/            # Express routers, middlewares, DTOs

tests/
├── domain/
├── application/services/  # Jest + ts-jest, stubs de ports
└── infrastructure/        # Jest + supertest
```

## Comandos

```bash
# Testes
npx jest                     # suíte completa
npx jest --testPathPattern="unit"   # testes unitários (sem banco)

# Desenvolvimento
npx ts-node-dev src/infrastructure/config/app.ts

# Prisma
npx prisma migrate dev --name ms001_descricao
npx prisma generate

# Docker
docker compose up --build
```

## Variáveis de ambiente

```
DATABASE_URL=postgresql://user:pass@localhost:5432/db
PORT=3000
NODE_ENV=development
JWT_SECRET=<gerar com: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))">
SENTRY_DSN=    # opcional
```

> Scaffold detalhado será adicionado em versão futura. Por enquanto, use este README como referência de estrutura e adapte manualmente após [ESTADO_ARCHITECTURE].
