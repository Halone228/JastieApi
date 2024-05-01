"""referral_primary

Revision ID: 25f2872aa7cc
Revises: 0033b33c6e97
Create Date: 2024-05-01 22:43:05.522031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '25f2872aa7cc'
down_revision: Union[str, None] = '0033b33c6e97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        'referrers_table_pkey',
        'referrers_table'
    )
    op.create_primary_key(
        'referrers_table_pkey',
        'referrers_table',
        ['referral_id', 'referrer_id']
    )


def downgrade() -> None:
    pass
