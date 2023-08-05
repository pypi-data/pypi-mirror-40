# -*- coding: utf-8 -*-
import traceback
import logging
from functools import wraps

from typing import Any, Callable, Dict, Tuple, Union

"""errs.errs module"""


class ErrorResult(object):
    '''Result indicator of function or method execution.'''
    def __init__(self): # type: () -> None 
        self.is_error = False

    def check(self): # type: () -> bool
        '''Check if it is an error.

        Returns:
            bool: True, if it is an error. False, if it is no error.
        '''
        if self.is_error:
            return True
        return False


class NoError(ErrorResult):
    '''Indicates that no error occurred.'''
    def __init__(self): # type: () -> None
        self.is_error = False


class Error(ErrorResult):
    '''Indicates an error occurred.

    Args:
        error (Exception):
            Exception that was raised inside of the function or method
    '''
    def __init__(self, error): # type: (Exception) -> None
        self.is_error = True
        self.traceback = traceback.format_exc()
        self.error = error


def errs(func): #type: (Callable[..., Any]) -> Callable[..., Any] 
    '''Convenient error handling decorator for functions and methods
    
    Args:
        func (Callable):
            any function or method that raises an Exception

    This decorator will catch all exceptions raised inside of a function
    or method that reach the end of control flow for that function or method.
    It will then package the error result, presenting the output of the
    function or method and an inspectable ErrorResult object as an
    immutable tuple. The purpose of this decorator is to signal when a
    function or method produces errors and then to change the error
    handling behavior so all errors are handled by the type system.

    This decorator calls the default logger at the error level in order
    to log the Exception and message that was raised inside of function
    or method.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs): # type: (*Any, **Any) -> Tuple[Union[Any, None], ErrorResult]
        try:
            out = func(*args, **kwargs)
            return out, NoError()
        except Exception as e:
            err = Error(e)
            logging.getLogger(__name__).error(err.traceback)
            return None, err
    return wrapper
