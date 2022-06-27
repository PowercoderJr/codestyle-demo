from dummies import DrawSettings
from modules.abstract_module.structures import (
    AbstractModuleSettings,
    AbstractModuleResult,
)


class ObjectDetectorSettings(AbstractModuleSettings):
    """Настройки модуля "Детектор объектов"."""

    def __init__(self):
        super().__init__()

        self.draw_settings = None
        """Настройки графики."""

        self.target_classes = []
        """Список классов для обнаружения."""

        self.obj_confidence = 1
        """Минимальный показатель уверенности для обнаружения объекта."""

    def set_silently(self, settings):
        super().set_silently(settings)
        self.draw_settings = ObjectDetectorDrawSettings(
            settings['draw_settings'])

    def merge(self, other_settings):
        super().merge(other_settings)
        if type(other_settings) in [ObjectDetectorSettings]:
            self.target_classes = list(set(
                self.target_classes + other_settings.target_classes))
            if other_settings.obj_confidence < self.obj_confidence:
                self.obj_confidence = other_settings.obj_confidence


class ObjectDetectorResult(AbstractModuleResult):
    """Результат модуля "Детектор объектов".

    Представляет один обнаруженный объект.
    """

    def __init__(self, class_id, label, obj_confidence, box):
        """Конструктор.

        :param class_id: Идентификатор класса.
        :param label: Лейбл класса.
        :param obj_confidence: Показатель уверенности нейронной сети.
        :param box: Координаты рамки в формате ltrb (x0, y0, x1, y1).
        """
        super().__init__()

        self.class_id = class_id
        """Идентификатор класса."""

        self.label = label
        """Лейбл класса."""

        self.obj_confidence = obj_confidence
        """Показатель уверенности нейронной сети."""

        self.box = box
        """Координаты рамки в формате ltrb (x0, y0, x1, y1)."""


class ObjectDetectorDrawSettings(DrawSettings):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)

        self.draw_name = True
        """Флаг "писать лейбл класса на кадре"."""

        self.draw_confid = False
        """Флаг "писать показатель уверенности на кадре"."""

        if settings_dict is not None:
            self.draw_name = settings_dict['draw_name']
            self.draw_confid = settings_dict['draw_confid']
