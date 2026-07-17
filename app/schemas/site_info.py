from pydantic import BaseModel, Field
from typing import List
from app.schemas.base_site_info import BaseLocation, BasePhone, BaseLink, BaseWorkingHours, BaseSetting, BaseHero, BaseFooter, BaseAboutUs, BaseContactUs

class UpdateSiteInfo(BaseModel):
    name: str | None = Field(None, min_length=1)
    slogan: List[str] | None = None
    logo: str | None = Field(None, pattern=r"^/media/uploads/[A-Za-z0-9_\-./]+\.(jpg|jpeg|png|webp)$")

    address: str | None = Field(None, min_length=1)
    location: BaseLocation | None = None

    phones: List[BasePhone] | None = None

    links: List[BaseLink] | None = None

    working_hours: List[BaseWorkingHours] | None = None

    today_suggestions: List[str] | None = None

    settings: List[BaseSetting] | None = None

    table_reservation_time: int | None = Field(None, gt=0)
    
    hero: BaseHero | None = None
    footer: BaseFooter | None = None
    about_us: BaseAboutUs | None = None
    contact_us: BaseContactUs | None = None