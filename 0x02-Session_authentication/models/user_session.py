#!/usr/bin/env python3
""" A module that contains the UserSession class """
from models.base import Base


class UserSession(Base):
    """ A class for UserSession"""
    def __init__(self, *args: list, **kwargs: dict):
        """It initializes a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
