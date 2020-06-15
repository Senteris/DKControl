from django.shortcuts import render

from main.models import StudySession
from main.views.functionsAndClasses.setModel import setModel


def get_session(request, session):
    session = StudySession.objects.get(id=session)
    setModel(session, request)
    return render(request, 'study_session.html', {'session': session})
