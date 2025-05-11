from django import forms
from .models import Course, Student, Grade, GradeItem


class CourseForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Course
        fields = ['name', 'students']  # 確保包含課程名稱和學生
        
class GradeItemForm(forms.ModelForm):
    class Meta:
        model = GradeItem
        fields = ['name', 'category']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']

