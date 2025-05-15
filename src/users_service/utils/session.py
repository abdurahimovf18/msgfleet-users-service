
"""
This utils file declares various utilities related to database actions,
such as decorators and helper functions for managing database sessions.
"""
from typing import Callable, Coroutine, TypeVar, ParamSpec, Callable
from functools import wraps
from enum import Enum

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.users_service.infrastructure.db.setup import session_factory
from src.users_service.utils.misc import signature, memorize


P = ParamSpec("P")
R = TypeVar("R")


class SessionMode(Enum):
    """
    Enum to specify the session mode.
    - `transaction`: Opens a session with an active transaction.
    - `session`: Opens a regular session without an active transaction.
    """
    transaction = "transaction"
    session = "session"


class SessionDecorator:
    """
    A decorator class for managing database sessions in FastAPI-based applications.
    This class injects an `AsyncSession` object into the decorated function,
    allowing seamless database transactions.
    
    Attributes:
        mode (str): Defines the type of session (`transaction` or `session`).
        autorollback (bool): Determines whether the session should rollback on exceptions.
        autocommit (bool): Determines whether the session should commit automatically.
        param_name (str): The keyword argument name under which the session is passed.
        context_manager (Callable): Function to generate session contexts.
    """
    def __init__(self,
                 mode: SessionMode | str = SessionMode.session,
                 autorollback: bool = True,
                 autocommit: bool = False,
                 param_name: str = "session",
                 context_manager_builder: sessionmaker[AsyncSession] = session_factory):
        """
        Initializes the session factory.

        Args:
            mode (SessionMode | str): The session mode (`transaction` or `session`).
            autorollback (bool): If True, rolls back transactions on exceptions.
            autocommit (bool): If True, commits the session after function execution.
            param_name (str): The keyword argument name for passing the session.
            context_manager_builder (sessionmaker[AsyncSession]): A session factory.
        """
        self.mode: str = self.get_normalized_mode(mode=mode)
        self.autorollback: bool = autorollback
        self.autocommit: bool = autocommit
        self.param_name: str = param_name
        self.context_manager: Callable[[], AsyncSession] = (
            self.get_context_manager(context_manager_builder, self.mode)
        )

    def get_normalized_mode(self, mode: SessionMode | str) -> str:
        """
        Normalizes the session mode input, ensuring it is valid.

        Args:
            mode (SessionMode | str): The session mode value.

        Returns:
            str: The normalized session mode as a string.

        Raises:
            ValueError: If the mode is not valid.
        """
        if isinstance(mode, SessionMode):
            return mode.value
        elif isinstance(mode, str):
            return mode
        else:
            raise ValueError(f"{mode} is not a valid value for mode")
        
    @memorize
    def is_session_param_exists(self, fn: Callable) -> bool:
        """
        This function checks whatever the function is waiting for the
        session or not. This can be more fixeble in some case where the session is not using
        yet, or there is some logic not require the session.

        Params:
            fn (Callable): the actual function which should be checked

        Returns:
            bool: the result of the function check
        """
        sig = signature(fn)
        return self.param_name in sig.parameters.keys()

    @staticmethod
    def get_context_manager(builder: sessionmaker[AsyncSession], mode: str) -> Callable[[], AsyncSession]:
        """
        Returns the appropriate session context manager based on the selected mode.

        Args:
            builder (sessionmaker[AsyncSession]): The session factory.
            mode (str): The session mode (`transaction` or `session`).

        Returns:
            Callable: A callable that generates session contexts.

        Raises:
            ValueError: If an invalid mode is provided.
        """
        match mode:
            case "transaction":
                return builder.begin 
            case "session":
                return builder
            case _:
                raise ValueError(f"Invalid session mode: {mode}")
    
    def __call__(self, function: Callable[P, Coroutine[None, None, R]]) -> Callable[P, Coroutine[None, None, R]]:
        """
        Allows the class instance to be used as an asynchronous decorator, injecting a database session
        into the decorated function if it's not already provided.

        The wrapper function:
        - Automatically opens and closes an `AsyncSession`
        - Injects the session into the decorated function via `self.param_name`
        - Optionally commits or rolls back the session based on config flags

        Args:
            function (Callable[P, Coroutine[None, None, R]]): 
                The asynchronous function to decorate. It must accept `self.param_name` as a keyword argument 
                unless `is_session_param_exists` returns False.

        Returns:
            Callable[P, Coroutine[None, None, R]]: 
                The decorated asynchronous function with automatic session handling.
        """
        @wraps(function)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # If session already provided or not needed, call directly
            if self.param_name in kwargs or not self.is_session_param_exists(function):
                return await function(*args, **kwargs)

            # Otherwise, inject session via context manager
            async with self.context_manager() as session:
                try:
                    kwargs[self.param_name] = session
                    result = await function(*args, **kwargs)
                    if self.autocommit:
                        await session.commit()
                    return result
                except Exception as exc:
                    if self.autorollback:
                        await session.rollback()
                    raise exc

        return wrapper


# Predefined decorators for session handling.
# `session` provides a standard session context.
# `transaction` provides a transaction-bound session context.
session = SessionDecorator()
transaction = SessionDecorator(mode=SessionMode.transaction)
