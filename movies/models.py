from django.db import models
from datetime import *
from django.urls import reverse

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=155)

class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    descripion=models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

class Actor(models.Model):
    name = models.CharField("Категория", max_length=150)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    descripion=models.TextField("Описание")
    image = models.ImageField('Изображение', upload_to='actors/')
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug":self.name})
    
    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'
    
    
class Genre(models.Model):
    name = models.CharField("Категория", max_length=100)
    descripion=models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    descripion=models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to='movies/')
    screenshots = models.ImageField("Скриншоты", upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default='2019')
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text='Указывать сумму в долларах'
    )
    fees_in_world = models.PositiveIntegerField(
        'Мировые сборы', default=0, help_text='Указывать сумму в долларах'
    )
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField('Черновик', default=False)
    
    def __str__(self):
        return self.title
    
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = 'Фильмы'

class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    descripion=models.TextField("Описание")
    movie = models.ForeignKey(Movie, verbose_name='Фильмы', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение',default=0)
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = 'Звёзды рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'

class Rating(models.Model):
    ip = models.CharField('IP адресс', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f"{self.star} - {self.movie}"
    
    class Meta:
        verbose_name = 'Рейтинги'
        verbose_name_plural = 'Рейтинги'

class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} - {self.movie}"
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзыв'