import os
from datetime import timedelta

from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect,reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Quiz, Lesson
from .forms import (
                    QuizQuestionForm, 
                    QuestionCreateForm, 
                    QuestionUpdateForm,
                    QuizQuestionCreateForm
                    )

class QuestionListView(ListView):
    model = Question
    template_name = "exam/quiz/quiz_list.html"



class QuizListView(ListView):
    # model = Quiz
    template_name = "exam/quiz/quiz_list.html"
    context_object_name = "quiz_list"

    def get_queryset(self) -> QuerySet[Any]:
        return Quiz.objects.filter(is_deleted=False)


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "exam/quiz/quiz_detail.html"
    context_object_name = "quiz"


class QuizQuestionUpdateView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "exam/quiz/quiz_detail.html"

    # change new answers for every question  
    def post(self, request, *args, **kwargs):
        posted_data = self.request.POST
        quiz = get_object_or_404(Quiz, id=self.kwargs["pk"])

        delete_question_id = posted_data.get('delete_question')
        if delete_question_id :
            question = Question.objects.get(pk=delete_question_id)
            quiz.questions.remove(question)
            return redirect(reverse('quiz_question_update', args=[quiz.id]))
        # for every question check new data and last-answer. if data was new then change it.
        for question in quiz.questions.all():
            question_new_answer = posted_data.get(str(question.id))
            if posted_data.get('last-answer') != question_new_answer:
                question.answer = question_new_answer
                question.save()
        
        return super().get(request, *args, **kwargs)


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    template_name = "exam/question/question_create.html"
    form_class = QuestionCreateForm

    def post(self, request, *args, **kwargs):
        posted_data = request.POST
        posted_files = request.FILES

        question_create_form = QuestionCreateForm(posted_data, posted_files)

        if question_create_form.is_valid() : 
            created_obj = question_create_form.save()
            created_obj.question_maker = request.user
            created_obj.save()
        return redirect(reverse('question_create'))
    success_url = reverse_lazy('question_create')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "exam/question/question_update.html"
    form_class = QuestionUpdateForm
    context_object_name = "question"

    def get_form_kwargs(self) -> dict[str, Any]:
        obj = self.get_object()
        posted_data = self.request.POST

        kwargs =  super(QuestionUpdateView, self).get_form_kwargs()
        kwargs['user'] = obj.question_maker

        return kwargs
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        posted_data = self.request.POST

        # delete image path and image file
        if obj.image is not None and  posted_data.get('delete_image') == 'on':
            if os.path.isfile(obj.image.path):
                os.remove(obj.image.path)
            obj.image = None
            obj.save()
        return super().post(request, *args, **kwargs)
    
    # success_url = reverse_lazy('home')
    def get_success_url(self) -> str:
        return reverse('question_update', args=[self.get_object().id])
    

class QuestionDetailView(DetailView):
    model = Question
    template_name = "exam/question/question_detail.html"
    context_object_name = "question"

    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.get_not_deleted(pk=self.pk_url_kwarg)

    # change new answers for  question  
    def post(self, request, *args, **kwargs):
        posted_data = self.request.POST
        question = get_object_or_404(Question, id=self.kwargs["pk"])
        print(posted_data.get('id'))

        # for every question check new data and last-answer. if data was new then change it.
        question_new_answer = posted_data.get(str(question.id))
        if posted_data.get('last-answer') != question_new_answer:
            question.answer = question_new_answer
            question.save()

        if posted_data['button-name'] == 'delete_question':
            return redirect(reverse('question_delete', args=[question.id]))

        return super().get(request, *args, **kwargs)
    

def question_delete_view(request, pk):
    question = get_object_or_404(Question, pk=pk)

    question.is_deleted = True
    question.save()

    return redirect('home')


class QuestionListView(ListView):
    # model = Question
    template_name = "exam/question/question_list.html"
    context_object_name = "questions"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return Question.objects.filter(question_maker=user, is_deleted=False)


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = "exam/quiz/quiz_create.html"
    fields = ('name', 'lesson', 'quiz_maker')
    
    def post(self, request, *args, **kwargs):
        posted_data = self.request.POST
        quiz_time = timedelta(minutes=int(posted_data.get('quiz_time')))
        quiz_image = self.request.FILES.get('quiz_image')
        user = self.request.user
        obj = Quiz.objects.create(
            name=posted_data['quiz_name'],
            lesson=Lesson.objects.get(pk=posted_data['lesson_id']),
            quiz_maker=user,
            time=quiz_time,
            image=quiz_image
            )
        return redirect(reverse('quiz_question_create', args=[obj.id]))


    def form_valid(self, form: BaseModelForm) -> HttpResponse:


        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.all()
        return context
    
    def get_success_url(self) -> str:
        return reverse('quiz_question_create', args=[self.get_object().id])


class QuizQuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "exam/quiz/quiz_question_create.html"
    fields = ['text']
    
    def get_success_url(self) -> str:
        return reverse('home')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['quiz_pk'] = self.kwargs['pk']
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        posted_data = request.POST
        posted_file = request.FILES
        user = request.user
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])

        num = 0
        while(posted_data.get(f'text-{num}')):
            ques_val = multi_question_maker(num)
            # quiz_question_create_form = QuizQuestionCreateForm()

            # quiz_question_create_form.text = posted_data.get(ques_val['text'])
            # quiz_question_create_form.choice_1 = posted_data.get(ques_val['choice_1'])
            # quiz_question_create_form.choice_2 = posted_data.get(ques_val['choice_2'])
            # quiz_question_create_form.choice_3 = posted_data.get(ques_val['choice_3'])
            # quiz_question_create_form.choice_4 = posted_data.get(ques_val['choice_4'])
            # quiz_question_create_form.answer = posted_data.get(ques_val['answer'])
            # quiz_question_create_form.image = posted_data.get(ques_val['image'])
            # quiz_question_create_form.explanation = posted_data.get(ques_val['explanation'])

            # chech for no problems in submited form
            # if quiz_question_create_form.is_valid():
            new_question = Question.objects.create(
                text=posted_data.get(ques_val['text']),
                choice_1=posted_data.get(ques_val['choice_1']),
                choice_2=posted_data.get(ques_val['choice_2']),
                choice_3=posted_data.get(ques_val['choice_3']),
                choice_4=posted_data.get(ques_val['choice_4']),
                answer=posted_data.get(ques_val['answer']),
                image=posted_file.get(ques_val['image']),
                explanation=posted_data.get(ques_val['explanation']),
                question_maker = user,

                                    )
                
            quiz.questions.add(new_question)
            
            num += 1

        
        return redirect(reverse('quiz_detail', args=[quiz.id]))
    


    


    
def multi_question_maker(num=0):
    text = f'text-{num}'
    choice_1 = f'choice_1-{num}'
    choice_2 = f'choice_2-{num}'
    choice_3 = f'choice_3-{num}'
    choice_4 = f'choice_4-{num}'
    answer = f'answer-{num}'
    image = f'image-{num}'
    explanation = f'explanation-{num}'
    context = {
        'text': text, 
        'choice_1': choice_1, 
        'choice_2': choice_2, 
        'choice_3': choice_3, 
        'choice_4': choice_4, 
        'answer': answer, 
        'image': image ,
        'explanation': explanation 
    }

    return context


def quiz_delete(request):
    if request.method == "POST":
        posted_data = request.POST

        quiz = get_object_or_404(Quiz, pk=posted_data.get('delete_quiz'))
        quiz.is_deleted = True
        quiz.save()
    return redirect(reverse('quiz_list'))
