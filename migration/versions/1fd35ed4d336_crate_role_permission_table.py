"""crate role_permission table

Revision ID: 1fd35ed4d336
Revises: d4f91465fa6d
Create Date: 2024-11-24 06:13:25.446948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fd35ed4d336'
down_revision: Union[str, None] = 'd4f91465fa6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('role_permission',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    op.drop_constraint('permissions_name_key', 'permissions', type_='unique')



def downgrade() -> None:

    op.create_unique_constraint('permissions_name_key', 'permissions', ['name'])
    op.drop_table('role_permission')

