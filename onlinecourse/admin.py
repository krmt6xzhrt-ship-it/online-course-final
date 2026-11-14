from django.contrib import admin
from .models import Course, Lesson, Learner, Enrollment, Question, Choice, Submission

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('question_text', 'grade', 'order')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'grade')
    list_filter = ('course',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [QuestionInline]

admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Submission)
admin.site.register(Choice)
admin.site.site_header = 'OnlineCourse Administration'
