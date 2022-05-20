from typing import List
from plugin.helpers.pluginType import ProcessorType
class LinearInterpolationProcessor(ProcessorType):
    def process(self, data: List[float]) -> List[float]:
        # print("LinearInterpolationProcessor")
        return data
