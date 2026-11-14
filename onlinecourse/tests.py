from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Enrollment, Submission

class OnlineCourseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('student', password='secret12345')
        self.course = Course.objects.create(name='Test course', description='Testing')
        Lesson.objects.create(course=self.course,title='Intro',content='Hello')
        self.question = Question.objects.create(course=self.course,question_text='2 + 2?',grade=10)
        self.yes = Choice.objects.create(question=self.question,choice_text='4',is_correct=True)
        self.no = Choice.objects.create(question=self.question,choice_text='5')
    def test_course_and_admin(self):
        self.assertEqual(self.client.get(reverse('onlinecourse:index')).status_code,200)
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk]))
        self.assertContains(response,'Test course')
        self.assertContains(response,'Intro')
    def test_correct_exam(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('onlinecourse:submit',args=[self.course.pk]),
                                    {f'question_{self.question.pk}':str(self.yes.pk)})
        self.assertEqual(response.status_code,302)
        submission = Submission.objects.get()
        self.assertEqual(submission.score,10)
        self.assertEqual(submission.percentage,100)
        self.assertEqual(Enrollment.objects.count(),1)
        self.assertContains(self.client.get(response.url),'Congratulations!')
    def test_wrong_exam(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('onlinecourse:submit',args=[self.course.pk]),
                                    {f'question_{self.question.pk}':str(self.no.pk)})
        self.assertEqual(Submission.objects.get().score,0)
        self.assertContains(self.client.get(response.url),'Keep learning!')
    def test_requires_auth(self):
        response=self.client.post(reverse('onlinecourse:submit',args=[self.course.pk]),{})
        self.assertEqual(response.status_code,302)
        self.assertIn('/login/', response.url)
