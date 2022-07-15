package queries

import (
	"context"
	"github.com/drbenton/gin-scoring/internal"
	"github.com/drbenton/gin-scoring/internal/domain"
	"github.com/drbenton/gin-scoring/internal/models"
	"github.com/volatiletech/sqlboiler/v4/queries/qm"
)

func GetLastGames(ctx context.Context) ([]*domain.GameResult, error) {
	rawRes, err := models.GameResults(qm.OrderBy("created_at desc"), qm.Limit(10)).All(ctx, internal.DB())
	if err != nil {
		return nil, err
	}
	res := make([]*domain.GameResult, len(rawRes))
	for i, rawResRow := range rawRes {
		res[i] = &domain.GameResult{GameResult: rawResRow}
	}
	return res, nil
}
