start-services:
  docker compose up -d database mailpit valkey

clear-migrations:
  rm -f ./sde/migrations/0*.py
