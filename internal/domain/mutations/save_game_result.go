package mutations

import (
	"context"
	"fmt"
	"strings"

	"github.com/volatiletech/null/v8"
	"github.com/volatiletech/sqlboiler/v4/boil"

	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/models"
)

type SaveGameResultCommand struct {
	PlayerNorthName string
	PlayerSouthName string
	Outcome         domain.GameOutcome
	WinnerName      *string
	DeadwoodValue   uint
}

func SaveGameResult(ctx context.Context, db boil.ContextExecutor, cmd SaveGameResultCommand) (*models.GameResult, error) {
	err := checkSaveGameResultInput(cmd)
	if err != nil {
		return nil, err
	}

	winnerScore, err := domain.CalculateRoundScore(cmd.Outcome, cmd.DeadwoodValue)
	if err != nil {
		return nil, err
	}

	playerNorthName := strings.ToLower(cmd.PlayerNorthName)
	playerSouthName := strings.ToLower(cmd.PlayerSouthName)
	var winnerNamePtr *string
	if cmd.WinnerName != nil {
		winnerName := strings.ToLower(*cmd.WinnerName)
		winnerNamePtr = &winnerName
	}

	resultModel := models.GameResult{
		PlayerNorthName: playerNorthName,
		PlayerSouthName: playerSouthName,
		Outcome:         string(cmd.Outcome),
		DeadwoodValue:   int16(cmd.DeadwoodValue),
		WinnerName:      null.StringFromPtr(winnerNamePtr),
		WinnerScore:     null.Int16From(int16(winnerScore)),
	}
	err = resultModel.Insert(ctx, db, boil.Infer())
	if err != nil {
		return nil, err
	}
	return &resultModel, nil
}

func checkSaveGameResultInput(cmd SaveGameResultCommand) error {
	//TODO: use proper validation, powered by the "validator" package :-)

	// Check the outcome
	outcomeOk := false
	for _, outcome := range domain.ValidGameOutcomes {
		if outcome == cmd.Outcome {
			outcomeOk = true
			break
		}
	}
	if !outcomeOk {
		return fmt.Errorf("invalid game outcome '%s'", cmd.Outcome)
	}

	// Winner name must be one of the 2 players's name
	winnerName := *cmd.WinnerName
	if cmd.Outcome != domain.GameOutcomeDraw && winnerName != cmd.PlayerNorthName && winnerName != cmd.PlayerSouthName {
		return fmt.Errorf("winner name '%s' is neither '%s' or '%s'", winnerName, cmd.PlayerNorthName, cmd.PlayerSouthName)
	}
	return nil
}
