from django.shortcuts import render

from main.models import StudySession


def get_session(request, session):
    session = StudySession.objects.get(id=session)
    return render(request, 'study_session.html', {'session': session})
