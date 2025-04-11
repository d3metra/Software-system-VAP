"""create an index for assignee name

Revision ID: c2bcbef0084a
Revises: 56e4dc061ebc
Create Date: 2025-04-11 19:11:50.862961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2bcbef0084a'
down_revision: Union[str, None] = '56e4dc061ebc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_assignee_name', 'assignees', ['assignee_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_assignee_name', table_name='assignees')
    # ### end Alembic commands ###
