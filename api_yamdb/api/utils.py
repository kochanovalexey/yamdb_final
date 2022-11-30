from django.db.models import Avg
from reviews.models import Review


def get_count_rating(self, obj):
    return Review.objects.filter(title=obj).aggregate(
        Avg("score")
    )["score__avg"]
