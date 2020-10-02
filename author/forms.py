from django import forms

from author.models import Author


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    patronymic = forms.CharField(max_length=20)

    name.widget.attrs.update({'class': 'form-control'})
    surname.widget.attrs.update({'class': 'form-control'})
    patronymic.widget.attrs.update({'class': 'form-control'})

    def save(self):
        new_author = Author.create(self.cleaned_data['name'], self.cleaned_data['surname'],
                                   self.cleaned_data['patronymic'])
        return new_author
