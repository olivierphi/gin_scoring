package internal

import (
	"database/sql"
	_ "github.com/lib/pq"
)

var dbConn *sql.DB

func DB() *sql.DB {
	if dbConn == nil {
		connStr := "postgres://ginscoringuser:localdev@localhost:5433/ginscoring?sslmode=disable"
		db, err := sql.Open("postgres", connStr)
		if err != nil {
			panic(err)
		}
		dbConn = db
	}

	return dbConn
}
