from typing import List
from plugin.helpers.pluginType import ProcessorType


class LinearInterpolationProcessor(ProcessorType):
    def process(self, data: List[float]) -> List[float]:
        """Simple and dumb linear interpolation.
           Don't take care of the edge condition.
        """
        ans = []
        d0 = data[0]
        for d in data:
            ans.append((d+d0) / 2)
            ans.append(d)
            d0 = d
        return ans

    def displayName(self) -> str:
        return "Linear Interpolation"
