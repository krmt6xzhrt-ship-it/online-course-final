from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ['order', 'id']
    def __str__(self):
        return self.title

class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['learner', 'course'], name='unique_enrollment')]
    def __str__(self):
        return f'{self.learner} in {self.course}'

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ['order', 'id']
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    possible_score = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'{self.enrollment.learner} — {self.enrollment.course} ({self.score}/{self.possible_score})'
    @property
    def percentage(self):
        return round(self.score * 100 / self.possible_score, 1) if self.possible_score else 0
    @property
    def passed(self):
        return self.possible_score > 0 and self.percentage >= 70
