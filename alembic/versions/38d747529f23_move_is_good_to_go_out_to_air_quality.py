"""move is_good_to_go_out to air_quality

Revision ID: 38d747529f23
Revises: c9289c136733
Create Date: 2026-11-16 19:33:02.988203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38d747529f23'
down_revision: Union[str, Sequence[str], None] = 'c9289c136733'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('air_quality', sa.Column('is_good_to_go_out', sa.Boolean(), nullable=True))

    op.execute("""
        UPDATE air_quality
        SET is_good_to_go_out = (COALESCE(air_quality_pm2_5, 0) < 35.0);
    """)

    op.alter_column('air_quality', 'is_good_to_go_out', existing_type=sa.Boolean(), nullable=False)
    op.drop_column('weather_data', 'is_good_to_go_out')


def downgrade() -> None:
    op.add_column('weather_data', sa.Column('is_good_to_go_out', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.execute("""
        UPDATE weather_data
        SET is_good_to_go_out = aq.is_good_to_go_out
        FROM air_quality AS aq
        WHERE weather_data.id = aq.weather_id;
    """)
    op.alter_column('weather_data', 'is_good_to_go_out', existing_type=sa.BOOLEAN(), nullable=False)
    op.drop_column('air_quality', 'is_good_to_go_out')