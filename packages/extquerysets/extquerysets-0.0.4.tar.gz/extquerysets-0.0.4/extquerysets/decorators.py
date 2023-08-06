import functools

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def _use_decorator(decorator_name, function, args):
    """Флаг, указывающий применим ли данный декоратор."""
    queryset = args[0]
    queryset_attrs = queryset.__dict__
    manager_attrs = queryset.model.objects.__dict__

    attr_sets = (queryset_attrs, manager_attrs)

    decorator_attr = '{name}_{postfix}'.format(name=function.__name__,
                                               postfix=decorator_name)

    return any([decorator_attr in attr_set for attr_set in attr_sets])


def or_404(function):
    """Возвращает Объект or raise Http404."""
    def do_action(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if _use_decorator(decorator_name='or_404', function=function,
                          args=args):
            return do_action(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    return wrapper


def or_none(function):
    """Возвращает Объект or None"""
    def do_action(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if _use_decorator(decorator_name='or_none', function=function,
                          args=args):
            return do_action(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    return wrapper


"""Маппинг постфиксов и соответсвуюих им декораторов."""
POSTFIX_MAP = {
    '_or_none': or_none,
    '_or_404': or_404
}
