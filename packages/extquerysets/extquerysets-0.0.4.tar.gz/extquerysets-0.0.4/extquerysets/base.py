from django.db.models import Manager
from django.db.models import QuerySet

from .decorators import POSTFIX_MAP


class BaseQuerySetManagerMixin(object):
    def __getattr__(self, item):
        for postfix in POSTFIX_MAP.keys():
            if item.endswith(postfix):
                # Если обращаемся через RelatedManager
                # (напр.: campaign.phases), то сохраняем dummy в Manager,
                # тк словарь RelatedManager в декораторе не доступен.
                if self.__class__.__name__ == 'RelatedManager':
                    self.model.objects.__dict__[item] = self.dummy
                else:
                    self.__dict__[item] = self.dummy

                return getattr(self, item.split(postfix)[0])

        return super().__getattribute__(item)

    def __getattribute__(self, item):
        for postfix in POSTFIX_MAP.keys():
            if item.endswith(postfix):
                delattr(self, item)

        return super().__getattribute__(item)

    def dummy(self, *args, **kwargs):
        pass


class CustomManager(BaseQuerySetManagerMixin, Manager):
    """
    Manager позволяющий наследникам выполнять запросы:
    ModelClass.objects.active_or_none()

    active_or_none состоит из:
        active = <manager_method>
        _or_none = <ключ декоратора из POSTFIX_MAP>

    Необходимо, чтобы метод active имел декоратор or_none

    Несколько декораторов можно указать один за другим:

    @or_404
    @or_none
    def active(self):
        ...

    """
    pass


class CustomQuerySet(BaseQuerySetManagerMixin, QuerySet):
    """
    QuerySet позволяющий наследникам выполнять запросы:
    ModelClass.objects.all().active_or_none()

    active_or_none состоит из:
        active = <queryset_method>
        _or_none = <ключ декоратора из POSTFIX_MAP>

    Необходимо, чтобы метод active имел декоратор or_none

    Несколько декораторов можно указать один за другим:

    @or_404
    @or_none
    def active(self):
        ...


    Также Manager, построенный методом as_manager(),
    будет обладать данным функционалом.
    Доп. см.: CustomManager
    """

    def as_manager(cls):
        manager = CustomManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)
