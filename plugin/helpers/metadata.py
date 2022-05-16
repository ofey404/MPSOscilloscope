from dataclasses import dataclass


@dataclass
class PluginMetaData:
    id: str = "SHOULD_BE_UNIQUE"
    display_name: str = "Placeholder."
    description: str = "A longer discription."
    tab_title: str = "Placeholder Title"
    freeze_on_switch_away: bool = False
