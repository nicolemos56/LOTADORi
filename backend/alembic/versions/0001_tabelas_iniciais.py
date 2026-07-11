"""tabelas iniciais: tourists, places, drivers

Revision ID: 0001
Revises:
Create Date: 2026-07-10

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "tourists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=True),
        sa.Column("nationality", sa.String(length=80), nullable=True),
        sa.Column("current_city", sa.String(length=80), nullable=True),
        sa.Column(
            "interests",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "places",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=60), nullable=True),
        sa.Column("photo_url", sa.String(length=500), nullable=True),
        sa.Column("rating", sa.Numeric(2, 1), nullable=True),
        sa.Column("visit_duration_minutes", sa.Integer(), nullable=True),
        sa.Column("avg_cost", sa.Numeric(10, 2), nullable=True),
        sa.Column("best_time", sa.String(length=120), nullable=True),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT", srid=4326, spatial_index=False
            ),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_places_location", "places", ["location"], postgresql_using="gist"
    )

    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("photo_url", sa.String(length=500), nullable=True),
        sa.Column(
            "languages",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column("trips_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rating", sa.Numeric(2, 1), nullable=True),
        sa.Column("base_price", sa.Numeric(10, 2), nullable=True),
        sa.Column(
            "specialties",
            postgresql.ARRAY(sa.String()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT", srid=4326, spatial_index=False
            ),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_drivers_location", "drivers", ["location"], postgresql_using="gist"
    )


def downgrade() -> None:
    op.drop_index("idx_drivers_location", table_name="drivers")
    op.drop_table("drivers")
    op.drop_index("idx_places_location", table_name="places")
    op.drop_table("places")
    op.drop_table("tourists")
