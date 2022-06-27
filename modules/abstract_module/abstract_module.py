import logging
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, TypeVar, Generic, Tuple

from dummies import Analytics, DrawScript, Frame, Logger
from modules.abstract_module.structures import (
    AbstractModuleSettings,
    AbstractModuleResult,
)

logger: Logger = logging.getLogger('Module.Abstract')

TModuleSettings = TypeVar('TModuleSettings', bound=AbstractModuleSettings)
"""Обобщённый тип настроек модуля."""
TModuleResult = TypeVar('TModuleResult', bound=AbstractModuleResult)
"""Обобщённый тип результата модуля."""


class AbstractModule(ABC, Generic[TModuleSettings, TModuleResult]):
    """Модуль обработки кадров с камеры."""

    leaders_names = []
    """Список имён модулей, от которых непосредственно зависит данный модуля."""

    def __init__(self, settings: TModuleSettings, module_name: str):
        """Модуль обработки кадров с камеры.

        :param settings: Настройки модуля.
        :param module_name: Имя модуля.
        """
        super().__init__()

        self.logger: Logger = logging.getLogger(f'Module.{module_name}')
        """Логгер."""

        self.logger.info('Init...')

        self.settings: TModuleSettings = settings
        """Настройки модуля."""

        self.compiled_settings: TModuleSettings = settings
        """Скомпилированные настройки модуля."""

        self.module_name: str = module_name
        """Строковое название модуля."""

        self.is_processing_now: bool = False
        """Флаг "модуль сейчас выполняет обработку"."""

        self.settings.subscribe_on_change(self.on_settings_changed)

    @abstractmethod
    def process_silently(
        self,
        frame: Frame,
        modules_outputs: Dict[str, Tuple[Frame, List[AbstractModuleResult]]],
    ) -> Tuple[Frame, List[TModuleResult]]:
        """Запускает обработку кадра и данных других модулей.

        :param frame: Кадр.
        :param modules_outputs: Словарь сырых результатов других модулей.
        :return: Кортеж из кадра и списка результатов обработки.
        """
        pass

    @abstractmethod
    def generate_draw_script(
        self, raw_data: List[TModuleResult]
    ) -> DrawScript:
        """Генерирует DrawScript.

        :param raw_data: Сырые результаты обработки.
        :return: Объект DrawScript с инструкциями для рисования графики.
        """
        pass

    @abstractmethod
    def generate_analytic_journal(
        self, raw_data: List[TModuleResult],
    ) -> List[Analytics]:
        """Генерирует журнал событий аналитики.

        :param raw_data: Сырые результаты обработки.
        :return: Список объектов Analytics.
        """
        pass

    @abstractmethod
    def filter_raw_data(
        self,
        raw_data: List[TModuleResult],
        module_settings: TModuleSettings = None,
    ) -> List[TModuleResult]:
        """Фильтрует сырые результаты обработки в соответствии с настройками
         модуля.

        :param raw_data: Сырые результаты обработки.
        :param module_settings: Настройки модуля. Если None, то будут
            использованы текущие настройки этого модуля.
        :return: Отфильтрованные сырые результаты обраобтки.
        """
        pass

    def process(
        self,
        frame: Frame,
        modules_outputs: Dict[str, Tuple[Frame, List[AbstractModuleResult]]],
        processing_done_callback: Callable[
            [str, Frame, List[TModuleResult]], None
        ],
    ):
        """Запускает обработку кадра и данных других модулей через
        self.process_silently(), после чего вызывает коллбэк
        processing_done_callback.

        :param frame: Кадр.
        :param modules_outputs: Словарь сырых результатов других модулей.
        :param processing_done_callback: Функция-коллбэк, которая будет вызвана
            по завершении обработки кадра. Аргументы:
                module_name - Имя модуля.
                frame - Кадр.
                raw_output - Сырые результаты обработки.
        """
        self.logger.debug(
            f'Frame processing (time {frame.time:.7f}) has begun'
        )
        self.logger.start_timer('process')
        frame, raw_output = self.process_silently(frame, modules_outputs)
        self.logger.debug(
            f'Frame processing (time {frame.time:.7f}) has done '
            f'({self.logger.stop_timer("process") * 1000:.0f} ms, '
            f'{len(raw_output)} results returned)'
        )
        processing_done_callback(self.module_name, frame, raw_output)

    def on_settings_changed(self, old_settings: TModuleSettings):
        pass
