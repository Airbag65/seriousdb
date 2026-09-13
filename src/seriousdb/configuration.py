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

    @staticmethod
    def warning_message() -> str:
        message = "\nConfiguration-file is malformed. The supported fields are:"
        message += "\n\tport: int"
        message += "\n\tdebug: bool"
        message += "\n\trequire_auth: bool"
        message += "\n\tdb_file: str"
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
        known_fields = {f.name: f for f in fields(cls)}

        valid_kwargs = {}
        for name, field in known_fields.items():
            if name in json_data:
                val = json_data[name]
                if field.type is int and isinstance(val, bool):
                    continue
                elif isinstance(val, field.type):
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
