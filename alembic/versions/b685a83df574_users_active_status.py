"""users active status 

Revision ID: b685a83df574
Revises: 29952d73c0e7
Create Date: 2024-10-28 23:15:55.731486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b685a83df574'
down_revision: Union[str, None] = '29952d73c0e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
