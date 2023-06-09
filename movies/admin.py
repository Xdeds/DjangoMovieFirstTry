from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Movie, Genre, MovieShots, Actor, Reviews, RatingStar, Rating
# Register your models here.
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    descripion = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)

class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="170" height="100"')
    
    get_image.short_description = "Изображение"


class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year",)
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    readonly_fields = ("get_image",)
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    fieldsets = (
        (None, {
        "fields":(("title", "tagline",))
        }),
        (None, {
        "fields":("descripion", "poster", "get_image")
        }),
        (None, {
        "fields":(("year", "world_premiere", "country"),)
        }),
        ('Actors', {
        "classes":("collapse",),
        "fields":(("actors", "directors", "genres", "category"),)
        }),
        ('Options', {
        "fields":(("budget", "fees_in_usa", "fees_in_world"),)
        }),
        (None, {
        "fields":(("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="200" height="300"')
    
    def unpublish(self, request, queryset):
        #Снять с публикации
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")
    def publish(self, request, queryset):
        #Опубликовать
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


class ReviewAdmin(admin.ModelAdmin):
    #Отзывы
    list_display = ("name", "email", "parent", "movie", "id",)
    readonly_fields = ("name", "email",)

class GenreAdmin(admin.ModelAdmin):
    #Жанры
    list_display = ("name", "url",)

class ActorAdmin(admin.ModelAdmin):
    #Актеры
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
    
    get_image.short_description = "Изображение"

class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="90" height="60"')
    
    get_image.short_description = "Изображение"

admin.site.register(MovieShots, MovieShotsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movie"
