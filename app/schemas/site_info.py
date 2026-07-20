from pydantic import BaseModel, Field
from typing import List
from app.schemas.base_site_info import CreateSlogans, CreateLocation, CreatePhone, CreateLink, CreateTodaySuggestions, CreateSection, UpdateSlogans, UpdateLocation, UpdatePhone, UpdateLink, UpdateTodaySuggestions, UpdateWorkingHours, UpdateSetting, UpdateSection, DeleteById, DeleteSection

class CreateSiteInfo(BaseModel):
    name: str | None = Field(None, min_length=1)
    slogans: List[CreateSlogans] | None = None
    logo: str | None = Field(None, pattern=r"^/media/uploads/site_info/[A-Za-z0-9_\-./]+\.(jpg|jpeg|png|webp)$")

    address: str | None = Field(None, min_length=1)
    location: CreateLocation | None = None

    phones: List[CreatePhone] | None = None

    links: List[CreateLink] | None = None

    today_suggestions: List[CreateTodaySuggestions] | None = None

    table_reservation_time: int | None = Field(None, gt=0)
    
    hero: CreateSection | None = None
    footer: CreateSection | None = None
    about_us: CreateSection | None = None
    contact_us: CreateSection | None = None



class UpdateSiteInfo(BaseModel):
    name: str | None = Field(None, min_length=1)
    slogans: List[UpdateSlogans] | None = None
    logo: str | None = Field(None, pattern=r"^/media/uploads/site_info/[A-Za-z0-9_\-./]+\.(jpg|jpeg|png|webp)$")

    address: str | None = Field(None, min_length=1)
    location: UpdateLocation | None = None

    phones: List[UpdatePhone] | None = None

    links: List[UpdateLink] | None = None

    working_hours: List[UpdateWorkingHours] | None = None

    today_suggestions: List[UpdateTodaySuggestions] | None = None

    settings: List[UpdateSetting] | None = None

    table_reservation_time: int | None = Field(None, gt=0)
    
    hero: UpdateSection | None = None
    footer: UpdateSection | None = None
    about_us: UpdateSection | None = None
    contact_us: UpdateSection | None = None



class DeleteSiteInfo(BaseModel):
    name: bool | None = None
    slogans: List[DeleteById] | None = None
    logo: bool | None = None

    address: bool | None = None
    location: bool | None = None

    phones: List[DeleteById] | None = None

    links: List[DeleteById] | None = None

    today_suggestions: List[DeleteById] | None = None

    hero: DeleteSection | None = None
    footer: DeleteSection | None = None
    about_us: DeleteSection | None = None
    contact_us: DeleteSection | None = None