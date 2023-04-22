from django import template
from movies.models import Category, Movie

register = template.Library()

@register.simple_tag()
def get_category():
    """Вывод всех фильмов"""
    return Category.objects.all()


@register.inclusion_tag("movies/tags/last_movie.html")
def get_last_movie():
    movie = Movie.objects.order_by("id")[:5]
    return({"last_movies":movie})