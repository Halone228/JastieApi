"""operations_recreate

Revision ID: 70bb9c6da6a1
Revises: 25f2872aa7cc
Create Date: 2024-05-03 18:43:35.341225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '70bb9c6da6a1'
down_revision: Union[str, None] = '25f2872aa7cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('operations_table')
    op.create_table(
        'initiator_table',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('descriptor', sa.String(length=255), unique=True, nullable=False)
    )
    op.create_table(
        'action_table',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('descriptor', sa.String(length=255), unique=True, nullable=False)
    )
    op.create_table(
        'operations_table',
        sa.Column('id', sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column('action_id', sa.Integer(), sa.ForeignKey('action_table.id')),
        sa.Column('initiator_id', sa.Integer(), sa.ForeignKey('initiator_table.id')),
        sa.Column('user_id', sa.BigInteger(), sa.ForeignKey('users_table.id')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('points', sa.Float(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False)
    )


def downgrade() -> None:
    pass
