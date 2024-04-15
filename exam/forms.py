from django import forms

from .models import Question, Quiz


class QuizQuestionForm(forms.ModelForm):
    class Meta :
        model = Question
        fields = ['answer']


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'text', 'image',
            'choice_1', 'choice_2', 'choice_3', 'choice_4', 
            'answer', 'explanation', 'question_maker'
        ]


class QuestionUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question_maker = kwargs.pop('user')
        super(QuestionUpdateForm, self).__init__(*args, **kwargs)
        self.fields['question_maker'].initial = question_maker
    class Meta:
        model = Question
        fields = [
            'text', 'image', 'question_maker',
            'choice_1', 'choice_2', 'choice_3', 'choice_4', 
            'answer', 'explanation'
        ]


class QuizQuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'text', 'image',
            'choice_1', 'choice_2', 'choice_3', 'choice_4', 
            'answer', 'question_maker', 'explanation'
        )