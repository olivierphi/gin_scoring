package domain

import (
	"github.com/drbenton/gin-scoring/internal/models"
	"github.com/volatiletech/null/v8"
)

type GameOutcome string

const (
	GameOutcomeKnock    GameOutcome = "knock"
	GameOutcomeGin      GameOutcome = "gin"
	GameOutcomeBigGin   GameOutcome = "big_gin"
	GameOutcomeUndercut GameOutcome = "undercut"
	GameOutcomeDraw     GameOutcome = "draw"
)

type GameResult struct {
	*models.GameResult
}

func (r GameResult) LoserName() null.String {
	if !r.WinnerName.Valid {
		return null.String{}
	}
	if r.WinnerName.String == r.PlayerNorthName {
		return null.StringFrom(r.PlayerSouthName)
	} else {
		return null.StringFrom(r.PlayerNorthName)
	}
}