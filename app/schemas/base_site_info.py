from pydantic import BaseModel, Field
from datetime import time
from typing import List
from app.models.site_info import DaysWeek, SiteInfoSettings

class BaseImages(BaseModel):
    url: str = Field(..., pattern=r"^/media/uploads/[A-Za-z0-9_\-./]+\.(jpg|jpeg|png|webp)$")
    position: str | None = Field(None, min_length=1)

class BaseImage(BaseModel):
    url: str = Field(..., pattern=r"^/media/uploads/[A-Za-z0-9_\-./]+\.(jpg|jpeg|png|webp)$")

class BaseButton(BaseModel):
    text: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)

class BaseLocation(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class BasePhone(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    phone: str = Field(..., pattern=r"^09\d{9}$")
    order: int = Field(..., gt=0)
    is_visible: bool = True

class BaseLink(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    icon: str = Field(..., min_length=1)
    order: int = Field(..., gt=0)
    is_visible: bool = True

class BaseWorkingHours(BaseModel):
    id: str = Field(..., min_length=1)
    day: DaysWeek
    open_time: time
    close_time: time
    is_closed: bool | None = None

class BaseSetting(BaseModel):
    capability: SiteInfoSettings
    enabled: bool = True

class BaseSection(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: str | None = Field(None, min_length=1)
    content: str = Field(..., min_length=1)
    images: List[BaseImages] = Field(default_factory=list)
    buttons: List[BaseButton] = Field(default_factory=list)

class BaseHero(BaseSection): pass

class BaseFooter(BaseSection): pass

class BaseAboutUs(BaseSection): pass

class BaseContactUs(BaseSection): pass
