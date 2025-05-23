"""added foreign key main_cpc to Patent model

Revision ID: 08dbdb6586c1
Revises: ef9b10b23f7d
Create Date: 2025-04-16 18:23:24.996733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08dbdb6586c1'
down_revision: Union[str, None] = 'ef9b10b23f7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'patents', 'cpc', ['main_cpc'], ['cpc_code'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'patents', type_='foreignkey')
    # ### end Alembic commands ###
