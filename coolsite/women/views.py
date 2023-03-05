from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import Women, Category
from .utils import *

# def index(request):
#     posts = Women.objects.all()
#     data = {
#         'posts': posts,
#         'cat_selected': 0,
#         'title': 'Главная страница'
#     }
#     return render(request, 'women/index.html', context=data)

class WomenHome(DataMixin, ListView):  #  В ListView уже встроен Paginator и автоматически передаёт в
                # шаблон ссылку на класс Paginator и page_obj который содержит список обьектов для
                # текущей страницы
    # paginate_by = 3
    # Создаёт по умолчанию коллекцию object_list
    model = Women
    # По умолчанию ищет шаблон 'имя приложения'/'имя модели'_list.html
    template_name = 'women/index.html'
    # Переименовываем коллекцию object_list
    context_object_name = 'posts'
    # extra_context = {'title': 'Главная страница'}

    # Функция создаёт стат. и динам. контекст и передаёт в шаблон index.html
    def get_context_data(self, *, object_list=None, **kwargs):
        # Обращаемся к классу WomenHome и берем существующий контекст, **kwargs - все именованные парам.
        context = super().get_context_data(**kwargs)
        # Обращаемся к методу родительского класса DataMixin
        c_def = self.get_user_context(title='Главная страница')
        # Возвращаем dict в шаблон
        return dict(list(context.items()) + list(c_def.items()))

    # Метод возвращает список записей отфильтрованный по условию
    def get_queryset(self):
        # select_related - жадная загрузка данных первичной модели, чтобы избавиться от дублирующих sql запросов
        return Women.objects.filter(is_published=True).select_related('cat')


# В функциях для ограничения доступа используют декоратор
# @login_required
# @cache_page(60 * 15)   # Декоратор для кеширования ф. пред.
def about(request):  # Пагинация в функциях представлений
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    # Берем номер текущей страницы: обращаясь к колекции GET берем атрибут 'page'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Передаём page_obj в шаблон
    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})

# def addpage(request):
#     # Если форма с заполненными данными
#     if request.method == 'POST':
#         # При создании формы обр. к обь. request и берем колекции POST и FILES
#         form = AddPostForm(request.POST, request.FILES)
#         # Проверка коректности данных переданных на сервер
#         if form.is_valid():
#             form.save()  # Cохранение данных формы связанной с моделью
#             return redirect('home')
#
#             # print(form.cleaned.data)   # Принт очищенных данных
#             # try:    # (если форма не связанна с моделью)
#             #     # Добавление записи в модель Women
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         # Пустая форма
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})

# LoginRequiredMixin проверяет авторизован ли пользователь
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # Указывает с какой формой связан этот класс представления
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # Адрес переадресации после добавления статьи
    # Ленивая ссылка формируется только когда понадобится
    success_url = reverse_lazy('home')
    # Адрес перенаправления для незарегистрированного пользователя
    login_url = 'home'

    # Формируем контекст для шаблона
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

# def contact(request):
#     return HttpResponse("Обратная связь")

# FormView стандартный класс для форм не связанных с моделями
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    # Mетод формирует контекст для шаблона
    def get_сontext_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    # Mетод вызывается если пользователь верно заполнил все поля формы
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# Наследуем класс от стандартного класса LoginView в котором реализованна вся
# необходимая логика для авторизации пользователя
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  #AuthenticationForm  # Стандартная форма авторизации Django
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(tetle='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # По умолчанию стандартная форма авторизации перенаправляет на '...account/profile/'
    # чтобы перенаправить на главную страницу нужно проаисать метод
    def get_success_url(self):
        return reverse_lazy('home')
    # Переадресацию можно прописать и в settings.py

def logout_user(request):
    # Стандартная функция Django для выхода из авторизации
    logout(request)
    return redirect('login')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)

# DetailView класс для отображения 1 модели
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # По умолчанию DetailView использует для слага имя переменной 'slug', чтобы использовать
    # 'post_slug' нужно её переименовать
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'   по умолчанию = pk
    context_object_name = 'post'

    # Формируем котекст для шаблона
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     c = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat=c.id)
#     # Выбор постов через свойства первичной модели
#     # posts = c.women_set.all()
#     # Или в одну строчку
#     # posts = Category.objects.get(slug=cat_slug).women_set.all()
#
#     if len(posts) == 0:
#         raise Http404()
#     data = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': posts[0].cat_id,
#     }
#     return render(request, 'women/index.html', context=data)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # Если категория не содержит записей генерируем ошибку 404
    allow_empty = False

    def get_queryset(self):
        # Когда будет формироваться экз. кл. WomenCategory для конкретного запроса
        # Через cсылку self обращаемся к словарю kwargs и берем параметр cat_slug
        # 'cat__slug' обращение к полю slug связанного первичного класса
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    # Формируем контекст для щаблона
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id
        c = Category.objects.get(slug=self.kwargs['cat_slug'])  # Избавляемся от дублей
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


# Так как он работает с формой (заносит данные в бд), наследуем его от класса CreateView
class RegisterUser(DataMixin, CreateView):
    # Ссылка на стандартную форму джанго для регистрации пользовотелей
    form_class = RegisterUserForm  #UserCreationForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    # Формируем контекст для шаблона
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    # При успешной регистрации авторизуем пользователя (вызывается этот метод)
    def form_valid(self, form):
        user = form.save()  # Самостоятельно сохраняем форму (добавляем польз. в бд)
        login(self.request, user)  # Вызываем функцию login которая авторизовывает польз.
        return redirect('home')

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
