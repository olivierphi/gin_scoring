package queries

import (
	"context"

	"github.com/volatiletech/sqlboiler/v4/boil"
	"github.com/volatiletech/sqlboiler/v4/queries"
)

type HallOfFameGlobalRow struct {
	WinnerName string `boil:"winner_name"`
	WinCounts  int    `boil:"win_counts"`
	TotalScore int    `boil:"total_score"`
	GrandTotal int    `boil:"grand_total"`
	Delta      int    `boil:"-"`
}

const getHallOFameGlobalSQL = `
with first_pass as (
	select
	    winner_name,
		count(*) as win_counts,
		sum(winner_score) as total_score
	from
		game_result
	where
		winner_score is not null
	group by 
		winner_name
)
select
    winner_name,
	win_counts,
	total_score,
   (total_score + (win_counts * 25)) as grand_total
from
	first_pass
order by 
	grand_total desc
`

func CalculateHallOfFameGlobal(ctx context.Context, db boil.ContextExecutor) ([]*HallOfFameGlobalRow, error) {
	var res []*HallOfFameGlobalRow
	err := queries.Raw(getHallOFameGlobalSQL).Bind(ctx, db, &res)
	if err != nil {
		return nil, err
	}

	// Let's compute the "deltas" - i.e. the difference between each player's score and the previous one
	prevScore := 0
	for i, row := range res {
		if i > 0 {
			row.Delta = row.GrandTotal - prevScore
		}
		prevScore = row.GrandTotal
	}

	return res, nil
}
