
.PHONY: db/schema/update
db/schema/update: host ?= localhost
db/schema/update: port ?= 5433
db/schema/update: user ?= ginscoringuser
db/schema/update: password ?= localdev
db/schema/update: db_name ?= ginscoring
db/schema/update: opts ?=
db/schema/update:
# @link https://github.com/k0kubun/sqldef#readme
	@psqldef --host=${host} --port=${port} --user=${user} --password=${password} ${db_name} \
		${opts} \
		< db_schema.sql

.PHONY: db/models/generate
db/models/generate:
	sqlboiler psql
