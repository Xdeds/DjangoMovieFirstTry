from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Movie, Category, Actor, Genre
from django.views.generic import DetailView
from .forms import ReviewForm
# Create your views here.

class GenreYear:
    #Жанры И Фильмы
    def get_genres(self):
        return Genre.objects.all()
    def get_years(self):
        return Actor.objects.filter(draft=True)

def movies(request):
    genre = Genre.objects.all()
    movie = Movie.objects.all()
    year = Movie.objects.all()
    return render(request, 'movies.html', {"movie":movie, "genre":genre, 'year':year})

def moviesingle(request, id):
    genre = Genre.objects.all()
    movie = Movie.objects.get(id = id)
    year = Movie.objects.all()
    return render(request, 'moviesingle.html', {"movie":movie, "genre":genre, 'year':year})

class AddReview(View):
    #Отзывы
    def post(sekf, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect("/")

class ActorView(DetailView):
    model = Actor
    template_name = 'actor.html'
    slug_field = "name"

def search(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        product_model = Movie.objects.filter(title__contains = product)
        return render(request, 'search.html', {'product':product_model})

# def search(request):
#     if request.method == 'POST':
#         query = request.POST.get('q')
#         results = Movie.objects.filter(title__contains=query)
#         return render(request, 'search_results.html', {'results': results})

# def search(request):
#     if request.method == 'POST':
#         movies = request.POST.get('movies')
#         movies_model = Movie.objects.filter(title__contains = movies)
#         return render(request, 'search.html', {'movies':movies_model})

class FilterMovie(GenreYear):
    def get_queryset(self):
        queryset = Movie.objects.filter(year__in=self.request.GET.getlist("year"))
        return queryset