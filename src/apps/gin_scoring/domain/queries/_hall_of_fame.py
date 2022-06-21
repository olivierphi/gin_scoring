from django.db.models import Count, Sum

from ...models import GameResult


def hall_of_fame():
    # @link https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
    win_counts = Count("winner_score")
    total_score = Sum("winner_score")

    return (
        GameResult.objects.all()
        .values("winner_name")
        .distinct()
        .annotate(win_counts=win_counts, total_score=total_score)
        # Each won round is worth 25 points:
        .annotate(grand_total=(win_counts * 25) + total_score)
        .order_by("-grand_total")
    )
