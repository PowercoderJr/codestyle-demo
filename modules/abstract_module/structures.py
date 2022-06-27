import copy
import logging
from abc import ABC, abstractmethod
from typing import List, Callable, Dict

from dummies import Logger

logger: Logger = logging.getLogger('Module.Abstract')


class AbstractModuleSettings(ABC):
    """Настройки модуля."""

    def __init__(self):
        """Настройки модуля.
        """
        super().__init__()

        self.is_active: bool = False
        """Флаг "модуль включен пользователем"."""

        self.on_change_callbacks: List[
            Callable[[AbstractModuleSettings], None]
        ] = []
        """Функции-коллбэки подписчиков события изменения настроек. Аргументы:
        old_settings - Прежние настройки."""

    @abstractmethod
    def set_silently(self, settings: Dict):
        """Запоминает все настройки этого модуля из словаря settings без
        вызова коллбэков события on_change.

        :param settings: Словарь с настройками.
        """
        for k in settings:
            if k in self.__dict__:
                self.__dict__[k] = settings[k]
            else:
                logger.warning(f'Key {k} is not defined in '
                               f'{self.__class__.__name__}')

        if __debug__:
            keys = (
                set(self.__dict__.keys())
                - set(settings.keys())
                - {'on_change_callbacks', }  # <- игнор список
            )
            if len(keys) > 0:
                logger.debug(
                    f'{self.__class__.__name__} has these keys but didn\'t '
                    f'get them in set_silently func: {", ".join(keys)}'
                )

    @abstractmethod
    def merge(self, other_settings: 'AbstractModuleSettings') -> None:
        """Добавляет в этот объект настроек другие настройки модуля. Для каждой
        пары модулей алгоритм слияния свой.

        :param other_settings: Настройки другого модуля.
        """
        pass

    def subscribe_on_change(
        self, callback: Callable[['AbstractModuleSettings'], None]
    ):
        """Добавляет подписчика на событие изменения настроек.
        
        :param callback: Коллбэк. Аргументы:
            old_settings - Прежние настройки.
        """
        self.on_change_callbacks.append(callback)

    def set(self, settings: Dict):
        """Запоминает все настройки этого модуля из словаря settings через
         self.set_silently() и вызывает коллбэки события on_change.

        :param settings: Словарь с настройками.
        """
        if len(self.on_change_callbacks) > 0:
            old_settings = copy.deepcopy(self)
            self.set_silently(settings)
            for callback in self.on_change_callbacks:
                callback(old_settings)
        else:
            self.set_silently(settings)
        logger.debug(f'{type(self).__name__} are set')

    def __deepcopy__(self, memodict):
        new_copy = type(self)()
        for k in self.__dict__:
            if k not in ['on_change_callbacks']:
                new_copy.__dict__[k] = copy.deepcopy(self.__dict__[k])
        return new_copy


class AbstractModuleResult(ABC):
    """Результат модуля."""

    def __init__(self):
        """Результат модуля.
        """
        super().__init__()
        pass
