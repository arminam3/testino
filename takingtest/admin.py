from django.contrib import admin

from .models import QuizHistory, QuizResult

@admin.register(QuizHistory)
class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ('quiz','datetime_created')


@admin.register(QuizResult)
class QuizResultyAdmin(admin.ModelAdmin):
    list_display = ('quiz','user')
    # list