package main

import (
	"context"
	"fmt"

	"github.com/drbenton/gin-scoring/internal"
	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/domain/mutations"
)

func main() {
	winnerName := "Oliv"
	cmd := mutations.SaveGameResultCommand{
		PlayerNorthName: "Rae",
		PlayerSouthName: "Oliv",
		Outcome:         domain.GameOutcomeKnock,
		WinnerName:      &winnerName,
		DeadwoodValue:   2,
	}

	ctx := context.Background()
	db := internal.DB()
	model, err := mutations.SaveGameResult(ctx, db, cmd)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Saved: %#v", *model)
}
