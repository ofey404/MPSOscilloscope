import os
import json
from pathlib import Path
from typing import List


_DEFAULT_CONFIG_PATH = Path.home() / ".mpsoscilloscope.json"


_DEFAULT_PLUGIN_LIST = [
    "plugin.builtin.linearInterpolation",
    "plugin.builtin.basicAnalysis",
    "plugin.builtin.fastFourierTranformation",
]


def pluginListFromConfigFile() -> List[str]:
    if not os.path.exists(_DEFAULT_CONFIG_PATH):
        with open(_DEFAULT_CONFIG_PATH, "wt") as f:
            json.dump(_DEFAULT_PLUGIN_LIST, f)

    with open(_DEFAULT_CONFIG_PATH, "rt") as f:
        pluginList = json.load(f)

    return pluginList
