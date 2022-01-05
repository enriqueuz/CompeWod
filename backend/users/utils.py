""" Users utils. """

# Django
from django.contrib.sessions.models import Session

# Utils
from django.utils import timezone

def delete_user_sessions(user_id):
    all_sessions = Session.objects.filter(
                                expire_date__gte=timezone.now()
                                )
    if all_sessions.exists():
        for session in all_sessions:
            session_data = session.get_decoded()
            if user_id == int(session_data.get('_auth_user_id')):
                session.delete()