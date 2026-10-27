"""create post table

Revision ID: 36226de4e0f4
Revises: 
Create Date: 2026-10-27 13:57:36.722674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36226de4e0f4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.column('id',sa.Integer(),nullable= False,primary_key= True),sa.Column('title',sa.String(),nullable= False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
