# app/core/exceptions.py

class NLToSQLBaseException(Exception):
    """Base exception for this project"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class SchemaRetrievalError(NLToSQLBaseException):
    """schema not found from Qdrant"""
    pass


class IntentParsingError(NLToSQLBaseException):
    """LLM could not extract intent"""
    pass


class SQLGenerationError(NLToSQLBaseException):
    """SQL build not done"""
    pass


class SQLValidationError(NLToSQLBaseException):
    """SQL is unsafe or invalid"""
    pass


class DatabaseExecutionError(NLToSQLBaseException):
    """MySQL query failed"""
    pass


class EntityResolutionError(NLToSQLBaseException):
    """Entity not resolved (e.g. User 101 does not exist)"""
    pass