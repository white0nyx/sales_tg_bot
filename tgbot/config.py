# Классы для формирования конфига и метод для его загрузки

from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    """Класс конфига для базы данных"""
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    """Класс бота"""
    token: str
    admin_ids: list[int]


@dataclass
class Miscellaneous:
    """Класс прочих параметров"""
    other_params: str = None


@dataclass
class Config:
    """Класс конфига бота"""
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str = None):
    """Загрузка конфига"""
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
        ),
        misc=Miscellaneous()
    )
