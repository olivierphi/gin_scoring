package internal

import (
	"database/sql"

	_ "github.com/lib/pq"
)

var dbConn *sql.DB

func DB() *sql.DB {
	// Naive version of a shared DB connection for the moment
	// Will likely be mocked during tests with a DB transaction for example
	if dbConn == nil {
		connStr := Config().DatabaseURL

		db, err := sql.Open("postgres", connStr)
		if err != nil {
			panic(err)
		}
		dbConn = db
	}

	return dbConn
}
