#!/usr/bin/env bash
pg_restore -U openods -d openods "$POSTGRES_DUMP_LOCATION/openods_015_a.dump"