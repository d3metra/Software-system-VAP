"""create assignees_groups table

Revision ID: 56e4dc061ebc
Revises: 22dad19a6aad
Create Date: 2025-04-09 12:09:27.214767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56e4dc061ebc'
down_revision: Union[str, None] = '22dad19a6aad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignees_groups',
    sa.Column('group_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patent_number', sa.String(length=55), nullable=False),
    sa.Column('assignee_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assignee_id'], ['assignees.assignee_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patent_number'], ['patents.patent_number'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignees_groups')
    # ### end Alembic commands ###
