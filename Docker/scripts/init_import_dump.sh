#!/usr/bin/env bash
pg_restore -d openods "$POSTGRES_DUMP_LOCATION/openods_012.dump"