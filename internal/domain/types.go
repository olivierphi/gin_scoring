package domain

type GameOutcome string

const (
	GameOutcomeKnock    GameOutcome = "knock"
	GameOutcomeGin      GameOutcome = "gin"
	GameOutcomeBigGin   GameOutcome = "big_gin"
	GameOutcomeUndercut GameOutcome = "undercut"
	GameOutcomeDraw     GameOutcome = "draw"
)
