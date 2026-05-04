from enum import Enum
from pydantic import BaseModel

from app.schemas.settings import UserSettingsUpdateRequest


class DetoxModeType(str, Enum):
    EASY = "EASY"
    NORMAL = "NORMAL"
    HARD = "HARD"


class ModePreset(BaseModel):
    mode: DetoxModeType
    title: str
    description: str
    settingsPreset: UserSettingsUpdateRequest


class ModeListResponse(BaseModel):
    presets: list[ModePreset]