from django.contrib import admin
from django.utils.safestring import mark_safe

from women.models import Women, Category

class WomenAdmin(admin.ModelAdmin):
    # Поля которые будут отображаться в админ панели
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')

    # Поля на которые мы можем кликнуть и перейти
    list_display_links = ('id', 'title')

    # По каким полям можно будет производить поиск
    search_fields = ('title', 'content')

    # Список полей которые можно редактировать в админ панели
    list_editable = ('is_published',)

    # Поля по которым можно фильтровать список статей (сайт-бар)
    list_filter = ('is_published', 'time_create')

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'slug': ('title',)}

    # Порядок отображения (редактируемых) полей при редактировонии
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    # Поля только для чтения, добавляются в конец списка fields
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    # Отображение панели с кнопкой сохранить сверху
    save_on_top = True

    # Пример показывает как можно менять стандартный код в полях админ-панели на свой собственный

    # Метод для отображения миниатюр в админ панели, возвращает html-код
    # Параметр object ссылается на текущую запись списка (обьект модели Women)
    # Обращаемся к полю photo и берем url
    def get_html_photo(self, object):
        if object.photo:  # Если фото существует
            # Функция mark_safe указывает не экранировать символы
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    # Меняем имя фото в админ панели
    get_html_photo.short_description = "Миниатюра"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# Изменение названия админ панели и имени страницы
admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах 2'