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
	hallOfFameRows, err := queries.CalculateHallOfFameGlobal(ctx, db)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Found %d hall of fame rows\n", len(hallOfFameRows))
	for _, row := range hallOfFameRows {
		fmt.Printf("Row: %#v\n", row)
	}
}
