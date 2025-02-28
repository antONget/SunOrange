from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: str
    support_id: int


@dataclass
class UOn:
    key_uon: str



@dataclass
class Config:
    tg_bot: TgBot
    u_on: UOn


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=env('ADMIN_IDS'),
                               support_id=env('SUPPORT_ID')),
                  u_on=UOn(key_uon=env('KEY_UON')))

