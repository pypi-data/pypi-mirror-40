#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"Annotation" decorators that can be applied to functions and classes as a way of tagging the object with
some form of metadata. This is designed to function in a similar way to Java 6 annotation interfaces.

Note:
    It is imperative to remember that remark decorators hand must be invoked with an argument list. An example being
    `@remark()` or `@remark(foo, bar)` or `@remark(f='foo', b='bar')`. These will add metadata to the decorated
    function or class that specifies the presence of that decorator on the object, and this can be
    queried at runtime, which requires marginally more resources than if we were to not use it at all.
    Calling *without* parenthesis `()` is invalid.

    Hints (provided by :mod:`metabeyond.hints`), on the other hand, are purely descriptive notes added to the docstring.
    They *must not* be called with arguments, for example `@hint`. Calling *with* parenthesis `()` will produce an
    invalid result, not decorating the given object correctly.

    Using the presence of parenthesis is a good way to determine if it is a documentation hint or a
    metadata remark. Metadata remarks are much more complicated than hints.

    To document parameter types and return types, one should use type annotations or comment-based
    annotations as per PEP 3107: `def foo(bar: int, baz: int) -> float:`. Utilities for this are in the
    Python :mod:`typing` module.
"""
__all__ = [
    'Remark',
    'quick_remark',
    'get_remarks_for',
    'has_remarks',
    'get_remark',
    'get_remarks_by_type',
]

import collections
import logging
from typing import Any, Callable, FrozenSet, Iterator, Optional, Type, Union

from . import hints

#: Used for logging debugging information about checks.
_logger = logging.getLogger('metabeyond.remarks')

#: Name of the hidden dunder attribute storing remarks.
_REMARK_COLLECTION_ATTR = '__metabeyond_remarks__'

#: Used internally to hold constraints dynamically.
_CONSTRAINT_ATTR = '_constraints'

#: Used internally to hold predicates dynamically.
_PREDICATE_ATTR = '_predicates_'

#: Single constraint
_CONSTRAINT_ARG = 'constraint'

#: Multiple constraints.
_CONSTRAINTS_ARG = 'constraints'

#: Single predicate
_PREDICATE_ARG = 'predicate'

#: Multiple predicates
_PREDICATES_ARG = 'predicates'

#: Type hint for valid things to decorate.
_ToDecorate = Union[Callable[..., Any], Type[Any]]

#: Frozen set that is reused internally.
# noinspection NonAsciiCharacters
_Ø = frozenset()


@hints.decorator
class Remark:
    # noinspection PyUnresolvedReferences
    """
    Class that can be subclassed to produce remark decorators that behave similar to Java 6 annotations::

    >>> class Foo(Remark): ...

    >>> @Foo()
    ... def bar():
    ...     pass

    You may also make it accept other parameters.

    >>> class Baz(Remark):
    >>>     def __init__(self, *, x: int, y: int):
    ...         super().__init__()
    ...         self.x = x
    ...         self.y = y

    And decorating with multiple remarks is also supported.

    >>> @Foo()
    ... @Baz(x=122, y=34)  # kwargs work too
    ... def bork():
    ...     pass

    Constraints
    ~~~~~~~~~~~

    You can add a single runtime constraint onto a class in order to limit what it is allowed to decorate when used.
    These will be inherited regardless of whether you specify one or not.

    >>> import asyncio
    >>> class SomeRemark(Remark, constraint=asyncio.iscoroutinefunction):
    ...     ...

    >>> @SomeRemark()
    ... async def whatever():
    ...      "This is acceptable!"

    >>> @SomeRemark()
    ... def something_else():
    ...     "This will cause a type error..."

    Or supply multiple constraints in a collection type.

    >>> import asyncio
    >>> import inspect
    >>> class SomeOtherRemark(Remark,
    ...                       constraints=[
    ...                           asyncio.iscoroutinefunction,
    ...                           lambda o: bool(inspect.getdoc(o).strip())
    ...                       ]):
    ...    ...

    Constraints should be callable type `Callable[[ToDecorate], bool]`, meaning they take the decorated
    item as a sole parameter and return True if it is acceptable or False otherwise. They may alternatively
    raise their own exceptions for a more custom interface. Multiple constraints will all have to be True to enable
    the entire check suite to pass.

    Warning:
        Passing the `constraint` and `constraints` arguments together in the class definition will cause an error,
        because I deemed it a stupid thing to be doing. You have no need to use both. It is designed to be readable.

    Predicates
    ~~~~~~~~~~

    Since v0.1.0, predicates have also been supported in remarks. Predicates are similar to constraints in that they
    are executed across the decorated item when you decorate an object with the remark.

    The distinguishing feature is that whereas constraints will create an error when they fail, a predicate will
    only result in the object not being decorated by the remark if it fails.


    This is useful if you wish to only decorate an object based on some runtime condition, environment variable, or
    flag.

    As the name suggests, a predicate that returns True is considered to be successful, whereas a predicate that returns
    False or raises an :class:`Exception`-derived exception will be considered to have failed.

    Like constraints, a single predicate is provided with the `predicate` kwarg, or multiple predicates can be provided
    with the `predicates` kwarg.

    For example, adding a single predicate:

    >>> import os
    >>> class SomeRemark(Remark, predicate=lambda _: os.getenv('ADD_REMARKS', False)):
    ...    ...

    ... or multiple predicates with the following syntax:

    >>> import os
    >>> class SomeRemark(Remark, predicates=[lambda _: os.getenv('ADD_REMARKS', False), something_else]):
    ...    ...

    This remark would only apply to an object if the `ADD_REMARKS` environment variable was applied at the time
    the object was decorated.

    Warning:
        Passing the `predicate` and `predicates` arguments together in the class definition will cause an error,
        because I deemed it a stupid thing to be doing. You have no need to use both. It is designed to be readable.

    ------------

    Note:
        As this functionality is fairly difficult to debug due to its dynamic nature, enabling the `DEBUG` logging
        level for `metabeyond.remarks` in the standard Python logging module will enable exposing information regarding
        what is happening internally, such as the predicates and constraints that are failing, etc.
    """

    def __init__(self) -> None:
        if type(self) is Remark:
            raise TypeError('Please subclass this class first')

    def __init_subclass__(cls, **kwargs) -> None:
        Remark.__init_constraints(cls, **kwargs)
        Remark.__init_predicates(cls, **kwargs)

    @staticmethod
    def __init_constraints(cls, **kwargs):
        if not hasattr(cls, _CONSTRAINT_ATTR):
            _logger.debug('Applying new constraint mapping to %s', cls)
            constraints = collections.defaultdict(list)
            setattr(cls, _CONSTRAINT_ATTR, constraints)
        else:
            constraints = getattr(cls, _CONSTRAINT_ATTR)

        if _CONSTRAINT_ARG in kwargs and _CONSTRAINTS_ARG in kwargs:
            raise TypeError(f'Please specify either {_CONSTRAINTS_ARG} or {_CONSTRAINT_ARG}')
        if _CONSTRAINTS_ARG in kwargs:
            _logger.debug('Adding %s constraints to %s', len(kwargs[_CONSTRAINTS_ARG]), cls)
            constraints[cls].extend(kwargs[_CONSTRAINTS_ARG])
        elif _CONSTRAINT_ARG in kwargs:
            _logger.debug('Adding one constraint to %s', cls)
            constraints[cls].append(kwargs[_CONSTRAINT_ARG])

    @staticmethod
    def __init_predicates(cls, **kwargs):
        if not hasattr(cls, _PREDICATE_ATTR):
            _logger.debug('Applying new predicate mapping to %s', cls)
            predicates = collections.defaultdict(list)
            setattr(cls, _PREDICATE_ATTR, predicates)
        else:
            predicates = getattr(cls, _PREDICATE_ATTR)

        if _PREDICATE_ARG in kwargs and _PREDICATES_ARG in kwargs:
            raise TypeError(f'Please specify either {_PREDICATES_ARG} or {_PREDICATE_ARG}')
        if _PREDICATES_ARG in kwargs:
            _logger.debug('Adding %s predicates to %s', len(kwargs[_PREDICATES_ARG]), cls)
            predicates[cls].extend(kwargs[_PREDICATES_ARG])
        elif _PREDICATE_ARG in kwargs:
            _logger.debug('Adding one predicate to %s', cls)
            predicates[cls].append(kwargs[_PREDICATE_ARG])

    def __call__(self, item_to_wrap: _ToDecorate) -> _ToDecorate:
        # Apply constraints first.
        self._perform_constraint_checking(item_to_wrap)

        if self._perform_predicate_checking(item_to_wrap):
            if not hasattr(item_to_wrap, _REMARK_COLLECTION_ATTR):
                setattr(item_to_wrap, _REMARK_COLLECTION_ATTR, set())
            getattr(item_to_wrap, _REMARK_COLLECTION_ATTR).add(self)

        return item_to_wrap

    def __repr__(self):
        middle_bit = ' '.join(
            f'{k!s}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')
        )
        return f'{type(self).__name__}({middle_bit})'

    def __hash__(self):
        """
        We hash the class object, this means each class may only be annotated once per remark type.

        This does not take into account transitive inheritance.

        Warning:
             Do not overload this method, otherwise it may cause this framework to misbehave.
        """
        return hash(type(self))

    def __eq__(self, other):
        """
        Compares the class.

        This may seem counter intuitive, but we hash on the class ID anyway. The reason for this is to allow
        a single remark of each type to be allowed on an object only. We must apply an ``__eq__`` overload as
        per https://docs.python.org/3.7/glossary.html#term-hashable

        There is not really a use case for comparing by content value, remark instances usually would be compared
        by their identity with the ``is`` operator instead.

        Warning:
             Do not overload this method, otherwise it may cause this framework to misbehave.
        """
        return hash(self) == hash(other)

    def _perform_constraint_checking(self, item_to_wrap) -> None:
        """
        Checks any constraints on the object and fails if any are not met.
        """
        for enforcing_class, check_list in getattr(self, _CONSTRAINT_ATTR).items():
            for check in check_list:
                if not check(item_to_wrap):
                    friendly_item = getattr(item_to_wrap, "__name__", item_to_wrap)
                    friendly_check = getattr(check, '__name__', check)
                    # This error should explain exactly what failed to work...
                    raise TypeError(
                        f'"{type(self).__name__}" cannot be used to decorate "{friendly_item}" because '
                        f'check "{friendly_check}" failed on it, and is required to pass by '
                        f'remark "{enforcing_class.__name__}"'
                    )

    def _perform_predicate_checking(self, item_to_wrap):
        """
        Checks any predicates on this object against the wrapped item. If any
        fail, we return False, else, we return True.
        """
        for enforcing_class, predicate_list in getattr(self, _PREDICATE_ATTR).items():
            for predicate in predicate_list:
                try:
                    if not predicate(item_to_wrap):
                        self._log_failed_predicate(item_to_wrap, enforcing_class, predicate, None)
                        return False
                except Exception as ex:
                    self._log_failed_predicate(item_to_wrap, enforcing_class, predicate, ex)
                    return False
        else:
            return True

    @staticmethod
    def _log_failed_predicate(item_to_wrap, enforcing_class, predicate, exception):
        """
        Logs a failed predicate if the logger is enabled for this module.
        """
        if exception is not None:
            _logger.debug(
                'Predicate %s failed on class %s from exception %s: %r, the object '
                '%s will not be marked with this remark.',
                predicate,
                enforcing_class,
                type(exception).__qualname__,
                exception,
                item_to_wrap,
            )
        else:
            _logger.debug(
                'Predicate %s enforced by %s failed, the object %s will not be marked with '
                'this remark',
                predicate,
                enforcing_class,
                item_to_wrap,
            )


def quick_remark(name: str) -> Type[Remark]:
    """
    Creates a remark quickly.

    >>> foo = quick_remark('foo')

    >>> @foo()
    ... def bar(): ...

    Args:
        name:
            The name of the remark to use

    Returns:
        The remark type generated from the given name.
    """
    cls: Type[Remark] = type(name, (Remark,), {})
    return cls


def get_remarks_for(object: Any) -> FrozenSet[Remark]:
    """
    Returns a frozen set of remarks for the given object at the time of calling, or an empty set if none exist.

    Args:
        object:
            The object to get the remarks applied to. This might be any type of object, but usually will be a function
            or class reference.

    Returns:
        Frozen set of any remarks found.
    """
    return frozenset(getattr(object, _REMARK_COLLECTION_ATTR, _Ø))


def has_remarks(object: Any) -> bool:
    """
    Returns true if the object has any remarks applied to it.
    """
    return bool(get_remarks_for(object))


def get_remark(class_: Type[Remark], object: Any) -> Optional[Remark]:
    """
    Get the remark of the given type that is applied to the object.

    This will not consider subtypes/covariants.

    Args:
        class_:
            The type of remark to look for.
        object:
            The object with remarks applied to it to inspect.

    Returns:
        The first remark found, or None if no remarks matching this type were discovered.
    """
    remarks = get_remarks_for(object)
    for remark in remarks:
        if type(remark) == class_:
            return remark
    return None


def get_remarks_by_type(base_class: Type[Remark], object: Any) -> Iterator[Remark]:
    """
    Gets any remarks that are instances of the given base class which are applied to the given object.

    Args:
        base_class:
            The base class of remark to filter by. Set to `remark.Remark` to get all remarks, or just
            call :meth:`get_remarks_for`.
        object:
            The object with remarks applied to it to consider.

    Returns:
        An iterator of each matching remark discovered. Order is undefined.
    """
    remarks = get_remarks_for(object)
    for remark in remarks:
        if isinstance(remark, base_class):
            yield remark
