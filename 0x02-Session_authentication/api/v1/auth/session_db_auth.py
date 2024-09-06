#!/usr/bin/env python3
""" A module """
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """It defines a class for SessionDBAuth """
    def create_session(self, user_id=None) -> str:
        """It creates and stores new instance of UserSession and
           returns the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ It returns the User ID by requesting UserSession in
        the database based on session_id"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        current_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expired_time = sessions[0].created_at + time_span
        if expired_time < current_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """It destroys the UserSession based on the
        Session ID from the request cookie"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
