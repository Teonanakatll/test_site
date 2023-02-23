from django import forms
from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

# class AddPostForm(forms.Form):
#     # wiget=forms.TextInput(attrs={'class': 'form-input'} - добавление сss класса к полю формы
#     title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}, ), label='Контент')
#     # required=False необязательно заполнять
#     # initial=True по умолчанию делает поле отмеченным
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     # Читает все записи из модели Category и выводит в выпадающий список
#     # empty_label='text' отображает текст по умолчанию
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')