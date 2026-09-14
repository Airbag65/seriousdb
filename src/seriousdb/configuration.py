from dataclasses import dataclass, fields
import json
import os
from typing import Any, Self
import warnings


@dataclass
class Configuration:
    port: int = 8000
    debug: bool = True
    require_auth: bool = False
    db_file: str = ".sdb"

    @classmethod
    def _known_fields(cls):
        return {f.name: f for f in fields(cls)}

    @staticmethod
    def warning_message() -> str:
        message = "\nConfiguration-file is malformed. The supported fields are:"
        for name, item in Configuration._known_fields().items():
            message += f"\n\t{name}: {item.type.__name__}"
        return message

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self:
        try:
            conf = cls(**json_data)
            return conf
        except:
            warnings.warn(
                Configuration.warning_message(), MalformedConfigurationWarning
            )

        valid_kwargs = {}
        for name, item in Configuration._known_fields().items():
            if name in json_data:
                val = json_data[name]
                if item.type is int and isinstance(val, bool):
                    continue
                elif isinstance(val, item.type):
                    valid_kwargs[name] = val
        return cls(**valid_kwargs)


class MalformedConfigurationWarning(UserWarning):
    pass


def get_configuration(file_path: str = "config.json") -> Configuration:
    if not os.path.isfile(file_path):
        return Configuration()
    with open(file_path, "r") as config_file:
        json_data = json.loads(config_file.read())
    config = Configuration.from_json(json_data)
    return config
