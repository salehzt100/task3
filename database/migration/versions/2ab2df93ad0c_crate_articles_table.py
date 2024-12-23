"""crate articles table

Revision ID: 2ab2df93ad0c
Revises: e34b905b81cd,
Create Date: 2024-11-24 07:28:09.600711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ab2df93ad0c'
down_revision: Union[str, None] = 'e34b905b81cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('articles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=60), nullable=False),
                    sa.Column('body', sa.Text(), nullable=False),
                    sa.Column('status', sa.Enum('DRAFT', 'IN_REVIEW', 'PUBLISHED', 'REJECTED', name='STATUS'),
                              server_default='DRAFT', nullable=False),
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('category_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )



def downgrade() -> None:
    op.drop_table('articles')

    # Drop ENUM type
    status_enum = sa.Enum('DRAFT','SUBMITTED', 'IN_REVIEW', 'PUBLISHED', 'REJECTED', name='STATUS')
    status_enum.drop(op.get_bind(), checkfirst=True)
