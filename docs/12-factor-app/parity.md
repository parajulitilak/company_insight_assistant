# 10. Dev/Prod Parity

> Keep development, staging, and production as similar as possible

Docker ensures consistent environments across development and production.

## Implementation
- **Docker**: Same image used in all environments.
- **SQLite**: Used consistently (consider PostgreSQL for production).
- **.env**: Environment-specific configuration.

## Setup
> docker-compose up --build