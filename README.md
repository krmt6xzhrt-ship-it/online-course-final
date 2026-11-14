# Online Course App — Django final assessment

A complete standalone Django application for the Online Course App assessment.

## Quick start — macOS / Linux

```bash
cd online-course-final
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ to see the course and http://127.0.0.1:8000/admin/ to see the administration site.

For exam demo, log in using the superuser you created and choose the correct options:
1. def
2. models.py
3. POST
4. `{{ variable }}`
5. A route to a view

You will see the **Congratulations!** exam result with a score of **100 / 100**.

Run tests:

```bash
python manage.py test
python manage.py check
```

## Assignment files

- Task 1: `onlinecourse/models.py` — Question, Choice and Submission models.
- Task 2: `onlinecourse/admin.py` — seven model imports, QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin.
- Task 3: Screenshot of `/admin/` displaying Authentication and Authorization and Onlinecourse sections.
- Task 4: `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`.
- Task 5: `onlinecourse/views.py` — submit and show_exam_result views.
- Task 6: `onlinecourse/urls.py` — routes for submit and results.
- Task 7: Screenshot of exam result page with Congratulations, score and detailed results.

**Submission guide in Russian:** read `ИНСТРУКЦИЯ_СДАЧА.md`.

## Note

This is an independent standalone implementation of the assignment requirements. It is not a modification of the IBM course starter code. Check against any additional private rubric details before submission.
