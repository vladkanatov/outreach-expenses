# Outreach Expenses Bot

Telegram bot для учёта расходов на мероприятия (ББ, Киноклуб, Аутрич, Настолки).

## Features

- 🎯 Выбор мероприятия из фиксированного списка
- 💰 Учёт расходов с категориями и суммами
- 📅 Ввод даты расхода
- 📸 Загрузка фото чеков в S3
- 📊 PostgreSQL для хранения данных
- 🔐 Логирование через loguru

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/vladkanatov/outreach-expenses.git
cd outreach-expenses
```

2. Copy `.env.example` to `.env` and fill in values:
```bash
cp .env.example .env
```

3. Run with Docker Compose:
```bash
docker compose up --build
```

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for Kubernetes/Helm deployment guide.

Quick deploy:
```bash
make deploy-prod
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot Token | ✅ |
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `AWS_ACCESS_KEY_ID` | AWS credentials for S3 | ✅ |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | ✅ |
| `AWS_REGION` | AWS region | ❌ (default: us-east-1) |
| `S3_BUCKET` | S3 bucket name | ✅ |

## Bot Commands

- `/start` - Показать справку
- `/new` - Добавить новый расход

## Architecture

```
├── bot.py              # Main bot entry point
├── config.py           # Configuration
├── handlers/           # Command handlers
│   ├── start.py
│   └── new_expense.py
├── database/           # Database layer
│   └── db.py
├── utils/              # Utilities
│   └── s3.py
└── migrations/         # Yoyo database migrations
```

## Development

### Database Migrations

Migrations are managed with [yoyo-migrations](https://ollycope.com/software/yoyo/latest/):

```bash
# Create new migration
docker compose run --rm migrator yoyo new -m "description" migrations

# Apply migrations
docker compose run --rm migrator yoyo apply -b --database $DATABASE_URL migrations
```

### Testing

```bash
# Run tests (when available)
docker compose run --rm bot pytest
```

## CI/CD

GitHub Actions automatically:
- Builds Docker image on push
- Pushes to GitHub Container Registry
- Deploys to Kubernetes (main → production, develop → dev)

## License

MIT
