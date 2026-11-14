from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Enrollment, Learner, Submission


def index(request):
    return render(request, 'onlinecourse/index.html', {'courses': Course.objects.all()})


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lessons', 'questions__choices'), pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'onlinecourse/signup.html', {'form': form})


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    learner, _ = Learner.objects.get_or_create(user=request.user)
    enrollment, _ = Enrollment.objects.get_or_create(learner=learner, course=course)
    questions = list(course.questions.prefetch_related('choices'))
    if not questions:
        return redirect('onlinecourse:course_details', course_id=course.id)
    selected_choices = []
    points = 0
    possible_points = sum(question.grade for question in questions)
    for question in questions:
        raw_id = request.POST.get(f'question_{question.pk}')
        choice = Choice.objects.filter(pk=raw_id, question=question).first() if raw_id else None
        if choice:
            selected_choices.append(choice)
            if choice.is_correct:
                points += question.grade
    submission = Submission.objects.create(
        enrollment=enrollment, score=points, possible_score=possible_points
    )
    submission.choices.set(selected_choices)
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.pk)


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission.objects.select_related('enrollment__learner').prefetch_related('choices'),
        pk=submission_id, enrollment__course=course, enrollment__learner__user=request.user
    )
    selected_ids = set(submission.choices.values_list('id', flat=True))
    results = []
    for question in course.questions.prefetch_related('choices'):
        choices = list(question.choices.all())
        chosen = next((c for c in choices if c.pk in selected_ids), None)
        correct = next((c for c in choices if c.is_correct), None)
        results.append({'question': question, 'selected': chosen,
                        'correct': correct, 'is_correct': bool(chosen and chosen.is_correct)})
    return render(request, 'onlinecourse/exam_result_bootstrap.html',
                  {'course':course,'submission':submission,'results':results})
