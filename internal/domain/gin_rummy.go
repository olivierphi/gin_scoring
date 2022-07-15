package domain

import "fmt"

func CalculateRoundScore(outcome GameOutcome, deadwood uint) (score uint, err error) {
	switch outcome {
	case GameOutcomeDraw:
		return
	case GameOutcomeKnock:
		score = deadwood
		return
	case GameOutcomeGin:
		score = deadwood + 25
		return
	case GameOutcomeBigGin:
		score = deadwood + 31
		return
	case GameOutcomeUndercut:
		score = deadwood + 15
		return
	}
	return 0, fmt.Errorf("invalid game outcome '%#v'", outcome)
}
