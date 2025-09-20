from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, AnswerOption, UserAnswer, Score
from .forms import ExamForm, QuestionForm, AnswerOptionForm, UserAnswerForm

def exam_list(request):
    exams = Exam.objects.filter(active=True)
    return render(request, 'exams/exam_list.html', {'exams': exams})

@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'exams/exam_form.html', {'form': form})

@login_required
def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = QuestionForm()
    return render(request, 'exams/question_form.html', {'form': form, 'exam': exam})

@login_required
def answer_option_create(request, exam_id, question_id):
    question = get_object_or_404(Question, id=question_id, exam_id=exam_id)
    if request.method == 'POST':
        form = AnswerOptionForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('exam_detail', exam_id=exam_id)
    else:
        form = AnswerOptionForm()
    return render(request, 'exams/answer_option_form.html', {'form': form, 'question': question, 'exam': question.exam})

@login_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.question_set.all().order_by('order')
    return render(request, 'exams/exam_detail.html', {'exam': exam, 'questions': questions})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.question_set.all().order_by('order')
    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        for question in questions:
            form = UserAnswerForm(request.POST, prefix=str(question.id))
            if form.is_valid():
                user_answer = form.save(commit=False)
                user_answer.user = request.user
                user_answer.question = question
                user_answer.save()
                if question.question_type in ['mcq', 'tf']:
                    correct_option = question.answeroption_set.filter(is_correct=True).first()
                    if correct_option and user_answer.answer == correct_option.text:
                        score += 1
        if total_questions > 0:
            score_percentage = (score / total_questions) * 100
            Score.objects.create(user=request.user, exam=exam, score=score_percentage)
        return redirect('exam_results', exam_id=exam.id)
    forms = {q.id: UserAnswerForm(prefix=str(q.id)) for q in questions}
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions, 'forms': forms})

@login_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    scores = Score.objects.filter(user=request.user, exam=exam)
    return render(request, 'exams/exam_results.html', {'exam': exam, 'scores': scores})

@login_required
def grade_short_answers(request, exam_id):
    if not request.user.is_staff:
        return redirect('exam_list')
    exam = get_object_or_404(Exam, id=exam_id)
    answers = UserAnswer.objects.filter(question__exam=exam, question__question_type='short')
    if request.method == 'POST':
        total_score = 0
        total_questions = exam.question_set.count()
        for answer in answers:
            score = request.POST.get(f'score_{answer.id}')
            if score:
                answer.score = int(score)
                answer.save()
                total_score += int(score)
        if total_questions > 0:
            score_percentage = (total_score / (total_questions * 10)) * 100  # Assuming 10 points per question
            Score.objects.update_or_create(
                user=answers[0].user, exam=exam,
                defaults={'score': score_percentage, 'completed_at': timezone.now()}
            )
        return redirect('exam_results', exam_id=exam.id)
    return render(request, 'exams/grade_short_answers.html', {'exam': exam, 'answers': answers})
