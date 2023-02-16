from django.contrib import admin

from women.models import Women, Category

class WomenAdmin(admin.ModelAdmin):
    # Поля которые будут отображаться в админ панели
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')

    # Поля на которые мы можем кликнуть и перейти
    list_display_links = ('id', 'title')

    # По каким полям можно будет производить поиск
    search_fields = ('title', 'content')

    # Список полей которые можно редактировать в админ панели
    list_editable = ('is_published',)

    # Поля по которым можно фильтровать список статей (сайт-бар)
    list_filter = ('is_published', 'time_create')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)