from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
