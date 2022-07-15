package main

import (
	"context"
	"fmt"

	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/domain/mutations"
)

func main() {
	winnerName := "Oliv"
	res := mutations.SaveGameResultCommand{
		PlayerNorthName: "Rae",
		PlayerSouthName: "Oliv",
		Outcome:         domain.GameOutcomeKnock,
		WinnerName:      &winnerName,
		DeadwoodValue:   2,
	}
	ctx := context.Background()
	model, err := mutations.SaveGameResult(ctx, res)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Saved: %#v", *model)
}
