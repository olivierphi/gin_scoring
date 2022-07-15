package queries

import (
	"context"

	"github.com/volatiletech/sqlboiler/v4/boil"
	"github.com/volatiletech/sqlboiler/v4/queries/qm"

	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/models"
)

func GetLastGames(ctx context.Context, db boil.ContextExecutor) ([]*domain.GameResult, error) {
	rawRes, err := models.GameResults(qm.OrderBy("created_at desc"), qm.Limit(10)).All(ctx, db)
	if err != nil {
		return nil, err
	}
	res := make([]*domain.GameResult, len(rawRes))
	for i, rawResRow := range rawRes {
		res[i] = &domain.GameResult{GameResult: rawResRow}
	}
	return res, nil
}
