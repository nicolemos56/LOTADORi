from decimal import Decimal

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    photo_url: Mapped[str | None] = mapped_column(String(500))
    languages: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    trips_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1))
    base_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    specialties: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )
    location: Mapped[WKBElement | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )
