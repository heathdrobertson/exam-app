from django.contrib import admin
from .models import Exam, Question, AnswerOption, UserAnswer, Score

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'active']
    search_fields = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'question_type', 'order']
    list_filter = ['question_type', 'exam']

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer', 'submitted_at']
    list_filter = ['user', 'question__exam']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'completed_at']
    list_filter = ['user', 'exam']
