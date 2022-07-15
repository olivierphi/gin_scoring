package mutations

import (
	"context"
	"fmt"
	"github.com/drbenton/gin-scoring/internal"
	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/models"
	"github.com/volatiletech/null/v8"
	"github.com/volatiletech/sqlboiler/v4/boil"
)

type SaveGameResultCommand struct {
	PlayerNorthName string
	PlayerSouthName string
	Outcome         domain.GameOutcome
	WinnerName      *string
	DeadwoodValue   uint
}

func SaveGameResult(ctx context.Context, cmd SaveGameResultCommand) (*models.GameResult, error) {
	err := checkSaveGameResultInput(cmd)
	if err != nil {
		return nil, err
	}

	winnerScore, err := domain.CalculateRoundScore(cmd.Outcome, cmd.DeadwoodValue)
	if err != nil {
		return nil, err
	}

	resultModel := models.GameResult{
		PlayerNorthName: cmd.PlayerNorthName,
		PlayerSouthName: cmd.PlayerSouthName,
		Outcome:         string(cmd.Outcome),
		DeadwoodValue:   int16(cmd.DeadwoodValue),
		WinnerName:      null.StringFromPtr(cmd.WinnerName),
		WinnerScore:     null.Int16From(int16(winnerScore)),
	}
	err = resultModel.Insert(ctx, internal.DB(), boil.Infer())
	if err != nil {
		return nil, err
	}
	return &resultModel, nil
}

func checkSaveGameResultInput(cmd SaveGameResultCommand) error {
	winnerName := *cmd.WinnerName
	if cmd.Outcome != domain.GameOutcomeDraw && winnerName != cmd.PlayerNorthName && winnerName != cmd.PlayerSouthName {
		return fmt.Errorf("winner name '%s' is neither '%s' or '%s'", winnerName, cmd.PlayerNorthName, cmd.PlayerSouthName)
	}
	return nil
}
