"""referrer referrer_id

Revision ID: b472b360fa68
Revises: 181f598a6c6e
Create Date: 2024-02-10 22:28:01.837311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b472b360fa68'
down_revision: Union[str, None] = '181f598a6c6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'user_info_table',
        'referrer',
        new_column_name='referrer_id'
    )


def downgrade() -> None:
    pass
