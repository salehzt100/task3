"""crate article_tag table

Revision ID: 929a9cb7647b
Revises: 3cd3df94bd0d
Create Date: 2024-11-24 09:05:03.547377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '929a9cb7647b'
down_revision: Union[str, None] = '3cd3df94bd0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('article_tag',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False,server_default=sa.text('now()')),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('article_id', 'tag_id')
    )


def downgrade() -> None:

    op.drop_table('article_tag')

