package main

import (
	"context"
	"fmt"

	"github.com/drbenton/gin-scoring/internal/domain/queries"
)

func main() {
	ctx := context.Background()

	hallOfFameRows, err := queries.CalculateHallOfFameGlobal(ctx)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Found %d hall of fame rows\n", len(hallOfFameRows))
	for _, row := range hallOfFameRows {
		fmt.Printf("Row: %#v\n", row)
	}
}
