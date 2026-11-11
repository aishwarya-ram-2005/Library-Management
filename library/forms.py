from django import forms
from .models import Book, Member, Category

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'total_copies', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

    def clean_total_copies(self):
        value = self.cleaned_data['total_copies']
        if value < 1:
            raise forms.ValidationError('At least one copy is required.')
        return value

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'student_id']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
