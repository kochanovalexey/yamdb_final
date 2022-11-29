from reviews.models import Review
from django.db.models import Avg


def get_count_rating(self, obj):
    return Review.objects.filter(title=obj).aggregate(
        Avg("score")
    )["score__avg"]
