# Deployment Guide

## Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3.x installed
- Docker registry access (GitHub Container Registry)

## Quick Start

### 1. Setup GitHub Secrets

Add the following secrets to your GitHub repository:

- `KUBECONFIG` - base64 encoded kubeconfig file
- `BOT_TOKEN` - Telegram bot token
- `AWS_ACCESS_KEY_ID` - AWS access key for S3
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `POSTGRES_PASSWORD` - PostgreSQL password for production

```bash
# Example: encode kubeconfig
cat ~/.kube/config | base64 | pbcopy
```

### 2. Deploy via GitHub Actions

Push to `main` branch for production or `develop` for dev environment:

```bash
git push origin main
```

### 3. Manual Deployment

#### Development
```bash
make deploy-dev
```

#### Production
```bash
make deploy-prod
```

## Helm Chart Structure

```
helm/outreach-expenses/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default values
├── values-dev.yaml         # Dev environment overrides
├── values-production.yaml  # Production overrides
└── templates/
    ├── _helpers.tpl        # Template helpers
    ├── deployment.yaml     # Bot deployment
    ├── configmap.yaml      # Configuration
    ├── secret.yaml         # Secrets
    ├── migration-job.yaml  # Database migration job
    └── postgresql.yaml     # PostgreSQL StatefulSet
```

## Configuration

### Environment Variables

- `BOT_TOKEN` - Telegram bot token (required)
- `DATABASE_URL` - PostgreSQL connection string
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `AWS_REGION` - AWS region (default: us-east-1)
- `S3_BUCKET` - S3 bucket for photos

### Custom Values

Override values using `--set` or custom values file:

```bash
helm upgrade --install outreach-expenses ./helm/outreach-expenses \
  --set image.tag=v1.2.3 \
  --set env.BOT_TOKEN=your-token
```

## Monitoring

Check deployment status:

```bash
kubectl get pods -n outreach-expenses-production
kubectl logs -f deployment/outreach-expenses -n outreach-expenses-production
```

## Troubleshooting

### Migration Job Failed

Check migration logs:
```bash
kubectl logs job/outreach-expenses-migration-1 -n outreach-expenses-production
```

### Database Connection Issues

Verify PostgreSQL is running:
```bash
kubectl get statefulset -n outreach-expenses-production
kubectl logs outreach-expenses-postgresql-0 -n outreach-expenses-production
```

## Rollback

```bash
helm rollback outreach-expenses -n outreach-expenses-production
```
