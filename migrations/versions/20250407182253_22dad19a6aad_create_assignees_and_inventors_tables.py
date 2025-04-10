"""create assignees and inventors tables

Revision ID: 22dad19a6aad
Revises: d8329ebcf507
Create Date: 2025-04-07 18:22:53.262817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22dad19a6aad'
down_revision: Union[str, None] = 'd8329ebcf507'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignees',
    sa.Column('assignee_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('assignee_name', sa.String(length=50), nullable=False),
    sa.Column('assignee_type', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('assignee_id')
    )
    op.create_table('inventors',
    sa.Column('inventor_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patent_number', sa.String(length=55), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=2), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['patent_number'], ['patents.patent_number'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('inventor_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventors')
    op.drop_table('assignees')
    # ### end Alembic commands ###
