from decimal import Decimal

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(60))
    photo_url: Mapped[str | None] = mapped_column(String(500))
    rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1))
    visit_duration_minutes: Mapped[int | None] = mapped_column(Integer)
    avg_cost: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    best_time: Mapped[str | None] = mapped_column(String(120))
    location: Mapped[WKBElement | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )
