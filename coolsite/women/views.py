from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPostForm
from .models import Women, Category

def index(request):
    posts = Women.objects.all()
    data = {
        'posts': posts,
        'cat_selected': 0,
        'title': 'Главная страница'
    }
    return render(request, 'women/index.html', context=data)

def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})

def addpage(request):
    # Если форма с заполненными данными
    if request.method == 'POST':
        # При создании формы обр. к обь. request и берем колекции POST и FILES
        form = AddPostForm(request.POST, request.FILES)
        # Проверка коректности данных переданных на сервер
        if form.is_valid():
            form.save()  # Cохранение данных формы связанной с моделью
            return redirect('home')

            # print(form.cleaned.data)   # Принт очищенных данных
            # try:    # (если форма не связанна с моделью)
            #     # Добавление записи в модель Women
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
    else:
        # Пустая форма
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Войти")

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    slovar = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    # Передаём эти параметры шаблону women/post.html
    return render(request, 'women/post.html', context=slovar)

def show_category(request, cat_slug):
    c = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(cat=c.id)

    # Выбор постов через свойства первичной модели
    # posts = c.women_set.all()

    # Или в одну строчку
    # posts = Category.objects.get(slug=cat_slug).women_set.all()


    if len(posts) == 0:
        raise Http404()

    data = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': posts[0].cat_id,
    }

    return render(request, 'women/index.html', context=data)


def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=True)  # 302 (врем)редирект, если указать перманент то 301 (пост.) редирект
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
