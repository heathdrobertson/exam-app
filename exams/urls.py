from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='splash'),
    path('create/', views.exam_create, name='exam_create'),
    path('<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('<int:exam_id>/question/create/', views.question_create, name='question_create'),
    path('<int:exam_id>/question/<int:question_id>/answer/create/', views.answer_option_create, name='answer_option_create'),
    path('<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('<int:exam_id>/results/', views.exam_results, name='exam_results'),
    path('<int:exam_id>/grade/', views.grade_short_answers, name='grade_short_answers'),
    path('logout/', views.logout_view, name='logout'),
]
