#!/usr/bin/env python3
"""A module that provides functions  for encrypting passwords and
checking validity"""
import bcrypt


def hash_password(password: str) -> bytes:
    """It returns  hashed password, which is a byte string """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """It checks if hashed password matches the provided password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
