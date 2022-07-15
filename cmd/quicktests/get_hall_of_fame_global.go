package main

import (
	"context"
	"fmt"
	"github.com/drbenton/gin-scoring/internal/domain/queries"
)

func main() {
	ctx := context.Background()

	hallOfFameRows, err := queries.GetHallOfFameGlobal(ctx)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Found %d halle of fame rows\n", len(hallOfFameRows))
	for _, row := range hallOfFameRows {
		fmt.Printf("Row: %#v\n", row)
	}
}
