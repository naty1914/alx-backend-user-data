#!/usr/bin/env python3
""" A module for SessionExpAuth class"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """It inherits from SessionAuth class and initializes
        the session expiration time
    """
    def __init__(self) -> None:
        """It intizializes the session expiration"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ It creates a Session ID for a user_id and
            return None if super() can’t create a Session ID
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """It returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        created_time = session_dictionary.get('created_at')
        if created_time + timedelta(seconds=self.session_duration
                                    ) < datetime.now():
            return None
        return session_dictionary.get('user_id')
