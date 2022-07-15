package main

import (
	"context"
	"fmt"
	"github.com/drbenton/gin-scoring/internal/domain/queries"
)

func main() {
	ctx := context.Background()

	lastGames, err := queries.GetLastGames(ctx)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Found %d last games\n", len(lastGames))
	for _, gameResult := range lastGames {
		fmt.Printf("Game: %#v\n", gameResult)
	}
}
