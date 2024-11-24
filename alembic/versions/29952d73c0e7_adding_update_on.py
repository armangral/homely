"""adding update on 

Revision ID: 29952d73c0e7
Revises: dc770112cd74
Create Date: 2024-10-28 18:13:20.044323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29952d73c0e7'
down_revision: Union[str, None] = 'dc770112cd74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('properties', 'updated_on',
               existing_type=sa.DATE(),
               type_=sa.String(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('properties', 'updated_on',
               existing_type=sa.String(),
               type_=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###
