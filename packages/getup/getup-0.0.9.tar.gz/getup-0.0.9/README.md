
# Getup

Projectless Django setup tool

See Gitlab repository for small helper apps.

## Getup config tool

Included getup.py can function as projectless Django starter. Use provided sample conf file with it or substitute own with `GETUP_CONF_PATH` env variable.

Run `python getup.py`, `./getup.py` or add the file into global $PATH to have it available everywhere there's Django app.

Following settings can be set by env vars:

  - GETUP_READ_ENV (set this to get others read)
  - DATABASE_URL
  - SECRET_KEY
  - ALLOWED_HOSTS
  - DATABASE_URL
  - SENTRY_DSN
