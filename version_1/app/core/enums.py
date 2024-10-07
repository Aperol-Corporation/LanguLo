from enum import Enum


class PlatformEnum(str, Enum):
    ZOOM = 'Zoom'
    DISCORD = 'Discord'
    TELEGRAM = 'Telegram'
    KAKAOTALK = 'KakaoTalk'


class RoleEnum(str, Enum):
    STUDENT = 'Student'
    TEACHER = 'Teacher'
