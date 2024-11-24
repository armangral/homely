"""adding user last login col update

Revision ID: c9d25e356bfb
Revises: ab2839a49b82
Create Date: 2024-11-24 17:02:06.873243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9d25e356bfb'
down_revision: Union[str, None] = 'ab2839a49b82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Modify 'last_login' column to include both date and time
    op.alter_column("users", "last_login", type_=sa.DateTime, existing_type=sa.Date)


def downgrade():
    # Revert 'last_login' column back to date-only
    op.alter_column("users", "last_login", type_=sa.Date, existing_type=sa.DateTime)