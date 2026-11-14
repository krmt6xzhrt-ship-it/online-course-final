from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help='Create a demo course and exam questions (safe to run more than once).'
    def handle(self, *args, **kwargs):
        course, _ = Course.objects.get_or_create(name='Python & Django Fundamentals', defaults={
            'description':'Learn the basics of Python web development, Django models, views, and templates.'})
        lessons = [
            ('Getting started with Python','Python uses indentation to define code blocks, and functions are created with def.'),
            ('Django Models','Models represent database tables. Each model field represents a column.'),
            ('Views and URLs','URL patterns connect routes to view functions, which return HTTP responses.'),
            ('Templates and Forms','Django templates render dynamic HTML. Forms can submit data using POST and CSRF protection.'),
        ]
        for index,(title,content) in enumerate(lessons,1):
            Lesson.objects.update_or_create(course=course,title=title,defaults={'content':content,'order':index})
        questions = [
            ('Which keyword defines a Python function?', ['func','def','function'], 1),
            ('Which Django file normally contains database models?', ['models.py','urls.py','settings.py'], 0),
            ('Which HTTP method is typically used to submit an exam?', ['GET','PUT','POST'], 2),
            ('Which template syntax outputs a Django variable?', ['{{ variable }}','[variable]','<variable>'], 0),
            ('What does a Django URL pattern connect?', ['A route to a view','A model to a database server','A CSS file to a template'], 0),
        ]
        for index,(title,options,correct_index) in enumerate(questions,1):
            question, _ = Question.objects.update_or_create(course=course,question_text=title,defaults={'grade':20,'order':index})
            for choice_index,option in enumerate(options):
                Choice.objects.update_or_create(question=question,choice_text=option,
                    defaults={'is_correct':choice_index==correct_index})
        self.stdout.write(self.style.SUCCESS(f'Demo ready: course ID {course.pk}. Create a superuser with python manage.py createsuperuser.'))
