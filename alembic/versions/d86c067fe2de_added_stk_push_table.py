"""added stk push table

Revision ID: d86c067fe2de
Revises: 9f8e8b6df2b1
Create Date: 2025-06-16 23:32:44.765105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd86c067fe2de'
down_revision: Union[str, None] = '9f8e8b6df2b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stk_push',
    sa.Column('stk_id', sa.Integer(), nullable=False),
    sa.Column('merchant_request_id', sa.String(), nullable=False),
    sa.Column('checkout_request_id', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT', name='mpesa_status_enum'), nullable=False),
    sa.Column('result_code', sa.String(), nullable=True),
    sa.Column('result_desc', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('stk_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stk_push')
    # ### end Alembic commands ###
