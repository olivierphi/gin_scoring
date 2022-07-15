package queries

import (
	"context"
	"github.com/drbenton/gin-scoring/internal"
	"github.com/volatiletech/sqlboiler/v4/queries"
	"sort"
	"time"
)

type hallOfFameMonthlyRowRaw struct {
	Month      time.Time `boil:"month"`
	WinnerName string    `boil:"winner_name"`
	WinCounts  int       `boil:"win_counts"`
	GrandTotal int       `boil:"grand_total"`
}

type HallOfFameMonthlyRow struct {
	Month      time.Time `boil:"month"`
	GameCounts int       `boil:"-"`
	WinnerName string    `boil:"winner_name"`
	WinCounts  int       `boil:"win_counts"`
	GrandTotal int       `boil:"grand_total"`
	Delta      int       `boil:"-"`
}

const getHallOFameMonthlySQL = `
with first_pass as (
	select
	    date_trunc('month', created_at) as month,
		winner_name,
		count(*) as win_counts,
		sum(winner_score) as total_score
	from
		game_result
	where
		winner_score is not null
	group by 
		winner_name,
		month
	order by 
		month desc,
		win_counts desc
)
select
	month,
	winner_name,
	win_counts,
	total_score,
   (total_score + (win_counts * 25)) as grand_total
from
	first_pass
order by 
	grand_total desc
`

func CalculateHallOfFameMonthly(ctx context.Context) ([]*HallOfFameMonthlyRow, error) {
	var rawRes []*hallOfFameMonthlyRowRaw
	err := queries.Raw(getHallOFameMonthlySQL).Bind(ctx, internal.DB(), &rawRes)
	if err != nil {
		return nil, err
	}

	// Let's group our rows by month:
	resByMonth := make(map[time.Time][]*hallOfFameMonthlyRowRaw)
	for _, rawRow := range rawRes {
		monthRows, ok := resByMonth[rawRow.Month]
		if !ok {
			monthRows := []*hallOfFameMonthlyRowRaw{}
			resByMonth[rawRow.Month] = monthRows
		}
		resByMonth[rawRow.Month] = append(monthRows, &hallOfFameMonthlyRowRaw{
			Month:      rawRow.Month,
			WinnerName: rawRow.WinnerName,
			WinCounts:  rawRow.WinCounts,
			GrandTotal: rawRow.GrandTotal,
		})
	}

	res := make([]*HallOfFameMonthlyRow, 0, len(resByMonth))
	for month, rawRows := range resByMonth {
		gameCounts := 0
		for _, rawRow := range rawRows {
			gameCounts += rawRow.WinCounts
		}

		winner := rawRows[0]
		winnerGrandTotal := winner.GrandTotal
		var delta int
		if len(rawRows) > 1 {
			secondBest := rawRows[1]
			delta = winnerGrandTotal - secondBest.GrandTotal
		} else {
			delta = winnerGrandTotal
		}

		res = append(res, &HallOfFameMonthlyRow{
			Month:      month,
			GameCounts: gameCounts,
			WinnerName: winner.WinnerName,
			WinCounts:  winner.WinCounts,
			GrandTotal: winnerGrandTotal,
			Delta:      delta,
		})
	}

	sort.Slice(res, func(i, j int) bool {
		return res[i].Month.After(res[j].Month)
	})

	return res, nil
}
