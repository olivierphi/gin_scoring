package main

import (
	"fmt"
	apphttp "github.com/drbenton/gin-scoring/internal/http"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"time"
)

func main() {
	err := apphttp.LoadTemplates()
	if err != nil {
		panic(err)
	}

	srv := &http.Server{
		Handler:      createRouter(),
		Addr:         "127.0.0.1:8000", //TODO: extract this from a Viper config
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	fmt.Printf("Server starting on '%s'\n", srv.Addr)
	log.Fatal(srv.ListenAndServe())
}

func createRouter() http.Handler {
	r := mux.NewRouter()
	r.HandleFunc("/", apphttp.HomepageHandler).Methods("GET")
	r.HandleFunc("/game/result", apphttp.PostGameResultHandler).Methods("POST")
	r.HandleFunc("/ping", apphttp.PingHandler)

	return r
}
