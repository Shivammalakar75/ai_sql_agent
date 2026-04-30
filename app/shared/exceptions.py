# app/shared/exceptions.py

class NLToSQLBaseException(Exception):
    """Base exception for this project"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class SchemaRetrievalError(NLToSQLBaseException):
    """Qdrant se schema nahi mila"""
    pass


class IntentParsingError(NLToSQLBaseException):
    """LLM intent extract nahi kar paya"""
    pass


class SQLGenerationError(NLToSQLBaseException):
    """SQL build nahi hui"""
    pass


class SQLValidationError(NLToSQLBaseException):
    """SQL unsafe hai ya invalid hai"""
    pass


class DatabaseExecutionError(NLToSQLBaseException):
    """MySQL query fail hui"""
    pass


class EntityResolutionError(NLToSQLBaseException):
    """Entity resolve nahi hui (jaise user 101 exist nahi karta)"""
    pass