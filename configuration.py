from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class CONFIG:
    require_auth: bool = True

    @staticmethod
    def load_env():
        if not load_dotenv() and CONFIG.require_auth:
            raise RuntimeError(".env must exist and contain 'AUTH_TOKEN'")
