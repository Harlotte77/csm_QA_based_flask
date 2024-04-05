"""empty message

Revision ID: 78cb2a22a47f
Revises: 8c7c27201fff
Create Date: 2024-04-05 11:57:09.048944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78cb2a22a47f'
down_revision = '8c7c27201fff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_captcha', schema=None) as batch_op:
        batch_op.add_column(sa.Column('used', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('email_captcha', schema=None) as batch_op:
        batch_op.drop_column('used')

    # ### end Alembic commands ###