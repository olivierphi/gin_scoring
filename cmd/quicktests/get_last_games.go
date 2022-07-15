package main

import (
	"context"
	"fmt"

	"github.com/drbenton/gin-scoring/internal"
	"github.com/drbenton/gin-scoring/internal/domain/queries"
)

func main() {
	ctx := context.Background()
	db := internal.DB()
	lastGames, err := queries.GetLastGames(ctx, db)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Found %d last games\n", len(lastGames))
	for _, gameResult := range lastGames {
		fmt.Printf("Game: %#v\n", gameResult)
	}
}
