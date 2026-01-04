"""create phone number for user coloumn

Revision ID: 1751cb9c7277
Revises: 
Create Date: 2026-01-04 00:31:19.079348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1751cb9c7277'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    


def downgrade() -> None:
    op.drop_column('users','phone_number')
