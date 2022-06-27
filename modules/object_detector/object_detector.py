from typing import cast, List, Dict, Tuple
from warnings import simplefilter

from dummies import Analytics, Box, DrawScript, Frame, Label, NnStaff
from modules.abstract_module.abstract_module import AbstractModule
from modules.abstract_module.structures import AbstractModuleResult
from modules.consts import ModuleName
from modules.object_detector.structures import (
    ObjectDetectorSettings,
    ObjectDetectorResult,
)

simplefilter(action='ignore', category=DeprecationWarning)


class ObjectDetector(
    AbstractModule[ObjectDetectorSettings, ObjectDetectorResult]
):
    """Модуль "Детектор объектов"."""

    def __init__(self, module_name=ModuleName.object_detector):
        """Модуль "Детектор объектов".
        """
        super().__init__(ObjectDetectorSettings(), module_name)

        self.logger.info('OK')

    def process_silently(
        self,
        frame: Frame,
        modules_outputs: Dict[str, Tuple[Frame, List[AbstractModuleResult]]]
    ) -> Tuple[Frame, List[ObjectDetectorResult]]:
        super().process_silently(frame, modules_outputs)

        if (
            len(self.compiled_settings.target_classes) <= 0
            or self.compiled_settings.obj_confidence > 1
        ):
            return frame, []

        boxes, scores, classes_ids = NnStaff.run(frame.orig_image)
        height, width = frame.orig_image.shape[:2]
        raw_output = []
        for i in range(len(boxes)):
            if (
                classes_ids[i] in self.compiled_settings.target_classes
                and scores[i] >= self.compiled_settings.obj_confidence
            ):
                eff_box = [
                    int(boxes[i][0] * width),
                    int(boxes[i][1] * height),
                    int(boxes[i][2] * width),
                    int(boxes[i][3] * height),
                ]

                label = None
                if classes_ids[i] < len(NnStaff.classes_disp):
                    label = NnStaff.classes_disp[classes_ids[i]].name
                else:
                    label = '?'
                    self.logger.warning(f'No class #{classes_ids[i]}')
                eff_score = scores[i]
                raw_output.append(ObjectDetectorResult(
                    classes_ids[i], label, eff_score, eff_box
                ))
        return frame, raw_output

    def generate_draw_script(
        self, raw_data: List[ObjectDetectorResult],
    ) -> DrawScript:
        super().generate_draw_script(raw_data)
        draw_script = DrawScript(self.settings.draw_settings)
        for item in raw_data:
            color = NnStaff.classes_disp[item.class_id].color
            draw_script.add_box(Box(
                (item.box[0], item.box[1]),
                (item.box[2], item.box[3]),
                color=color,
            ))
            obj_label = (
                f'{item.label}'
                if self.settings.draw_settings.draw_name
                else None
            )
            confidence_label = (
                f'{item.obj_confidence * 100:.0f}%'
                if self.settings.draw_settings.draw_confid
                else None
            )
            label = ' '.join(
                [x for x in [obj_label, confidence_label] if x is not None]
            )
            if len(label) > 0:
                draw_script.add_label(Label(
                    label, (item.box[0] + 10, item.box[1] + 35), color=color,
                ))
        return draw_script

    def generate_analytic_journal(
        self, raw_data: List[ObjectDetectorResult]
    ) -> List[Analytics]:
        super().generate_analytic_journal(raw_data)
        # для данного модуля не подразумевается
        return []

    def filter_raw_data(
        self, raw_data: List[ObjectDetectorResult],
        module_settings: ObjectDetectorSettings = None,
    ) -> List[ObjectDetectorResult]:
        super().filter_raw_data(raw_data, module_settings)
        if module_settings is None:
            module_settings = self.settings
        return list(filter(
            lambda item: (
                item.class_id in module_settings.target_classes
                and item.obj_confidence >= module_settings.obj_confidence
            ), raw_data
        ))


class ConcreteObjectDetector(ObjectDetector):
    """Модуль "Детектор объектов"."""

    leaders_names = [ModuleName.object_detector]

    def __init__(self, module_name):
        super().__init__(module_name)

    def process_silently(
        self,
        frame: Frame,
        modules_outputs: Dict[str, Tuple[Frame, List[AbstractModuleResult]]]
    ) -> Tuple[Frame, List[ObjectDetectorResult]]:
        return (
            modules_outputs[ModuleName.object_detector][0],
            cast(
                List[ObjectDetectorResult],
                modules_outputs[ModuleName.object_detector][1]
            )
        )
