package main

import (
	"context"
	"fmt"

	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/domain/mutations"
)

func main() {
	winnerName := "Rae"
	res := mutations.SaveGameResultCommand{
		PlayerNorthName: "Rae",
		PlayerSouthName: "Oliv",
		Outcome:         domain.GameOutcomeKnock,
		WinnerName:      &winnerName,
		DeadwoodValue:   12,
	}
	ctx := context.Background()
	model, err := mutations.SaveGameResult(ctx, res)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Saved: %#v", *model)
}
