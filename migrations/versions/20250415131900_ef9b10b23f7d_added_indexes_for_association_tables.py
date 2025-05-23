"""added indexes for association tables

Revision ID: ef9b10b23f7d
Revises: 0bea285a1cb4
Create Date: 2025-04-15 13:19:00.056499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef9b10b23f7d'
down_revision: Union[str, None] = '0bea285a1cb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_assignees_groups_assignee_id', 'assignees_groups', ['assignee_id'], unique=False)
    op.create_index('ix_assignees_groups_patent_number', 'assignees_groups', ['patent_number'], unique=False)
    op.create_index('ix_cpc_classifications_code', 'cpc_classifications', ['cpc_code'], unique=False)
    op.create_index('ix_cpc_classifications_patent_number', 'cpc_classifications', ['patent_number'], unique=False)
    op.create_index('ix_ipc_classifications_code', 'ipc_classifications', ['ipc_code'], unique=False)
    op.create_index('ix_ipc_classifications_patent_number', 'ipc_classifications', ['patent_number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ipc_classifications_patent_number', table_name='ipc_classifications')
    op.drop_index('ix_ipc_classifications_code', table_name='ipc_classifications')
    op.drop_index('ix_cpc_classifications_patent_number', table_name='cpc_classifications')
    op.drop_index('ix_cpc_classifications_code', table_name='cpc_classifications')
    op.drop_index('ix_assignees_groups_patent_number', table_name='assignees_groups')
    op.drop_index('ix_assignees_groups_assignee_is', table_name='assignees_groups')
    # ### end Alembic commands ###
