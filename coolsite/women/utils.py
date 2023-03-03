from django.db.models import Count

from women.models import Category

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        # {'title': 'Войти', 'url_name': 'login'}
        ]

class DataMixin:
    paginate_by = 20
    def get_user_context(self, **kwargs):
        # Формируем начальный словарь из именнованных параметров переданных этой функции
        context = kwargs
        # Импортируем аггр. ф. и дабавляем к категориям поле с кол-вом постов в категории
        cats = Category.objects.all().annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        # context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
