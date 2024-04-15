from django import forms

from .models import QuizHistory

class QuizHistoryForm(forms.ModelForm):

    class Meta:
        model = QuizHistory
        fields = ('quiz', 'question','user', 'user_answer')