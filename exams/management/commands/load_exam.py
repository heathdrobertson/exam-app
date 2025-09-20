from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from exams.models import Exam, Question, AnswerOption

class Command(BaseCommand):
    help = 'Loads the 6th Grade Linux Command Line Basics exam'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User "admin" does not exist. Please create a superuser with "python3 manage.py createsuperuser".'))
            return
        exam, created = Exam.objects.get_or_create(
            title="6th Grade Linux Command Line Basics",
            defaults={'description': "Based on LinuxHandbook course", 'created_by': user, 'active': True}
        )
        questions = [
            {
                'text': "What is the terminal in Linux?",
                'type': 'mcq', 'order': 1,
                'options': [
                    ('A program for drawing pictures', False),
                    ('A text window where you type commands', True),
                    ('A game you play in the browser', False),
                    ('A tool for editing photos', False),
                ]
            },
            {
                'text': "What does the 'ls' command do?",
                'type': 'mcq', 'order': 2,
                'options': [
                    ('Lists all files and folders in your current location', True),
                    ('Changes your password', False),
                    ('Opens a web browser', False),
                    ('Shuts down the computer', False),
                ]
            },
            {
                'text': "Which command shows you exactly where you are in the computer's folders?",
                'type': 'mcq', 'order': 3,
                'options': [
                    ('cd', False),
                    ('pwd', True),
                    ('mkdir', False),
                    ('rm', False),
                ]
            },
            {
                'text': "What happens if you type 'cd Documents' in the terminal?",
                'type': 'mcq', 'order': 4,
                'options': [
                    ('It deletes the Documents folder', False),
                    ('It moves you into the Documents folder', True),
                    ('It creates a new file called Documents', False),
                    ('It copies all files to Documents', False),
                ]
            },
            {
                'text': "Why does Linux care about uppercase and lowercase letters?",
                'type': 'mcq', 'order': 5,
                'options': [
                    ("It doesn't—it's not case-sensitive", False),
                    ("Because 'File' and 'file' are treated as different things", True),
                    ("Only for passwords, not for files", False),
                    ("To make typing harder for kids", False),
                ]
            },
            {
                'text': "The bash shell is the program that reads and runs the commands you type in the terminal.",
                'type': 'tf', 'order': 6,
                'options': [
                    ('True', True),
                    ('False', False),
                ]
            },
            {
                'text': "To get help on a command like 'ls', you can type 'man ls' to open a guide called a man page.",
                'type': 'tf', 'order': 7,
                'options': [
                    ('True', True),
                    ('False', False),
                ]
            },
            {
                'text': "The 'rm' command is used to safely backup your files.",
                'type': 'tf', 'order': 8,
                'options': [
                    ('True', False),
                    ('False', True),
                ]
            },
            {
                'text': "Explain what a superuser or root is, and why it has special powers on a Linux computer.",
                'type': 'short', 'order': 9,
                'options': []
            },
            {
                'text': "Describe how the 'mkdir' and 'cp' commands work. Give an example of when you might use each one.",
                'type': 'short', 'order': 10,
                'options': []
            },
        ]
        for q in questions:
            question, _ = Question.objects.get_or_create(
                exam=exam, text=q['text'], question_type=q['type'], order=q['order']
            )
            for opt_text, is_correct in q['options']:
                AnswerOption.objects.get_or_create(question=question, text=opt_text, is_correct=is_correct)
        self.stdout.write(self.style.SUCCESS('Exam loaded successfully'))
