"""Added image link to course

Revision ID: 69a4cb5004e3
Revises: 52fa6929cb47
Create Date: 2023-07-11 13:16:52.793300

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '69a4cb5004e3'
down_revision = '52fa6929cb47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('course', sa.Column('image_link', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('course', 'image_link')
    pass
