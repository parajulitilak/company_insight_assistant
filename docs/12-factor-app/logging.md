
##### `docs/12-factor-app/logging.md`
Logging principle.

# 11. Logs

> Treat logs as event streams

Logs are handled as event streams using `loguru`.

## Implementation
- **Loguru**: Configured in `logging_config.py` to write to `logs/info.log`.
- **Level**: Set via `LOG_LEVEL` in `.env`.
- **Rotation**: Logs rotate at 10MB.

## Setup
# Logs are written to logs/info.log
> tail -f logs/info.log