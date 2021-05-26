"""empty message

Revision ID: 9cc7599d222e
Revises: 
Create Date: 2021-05-26 21:09:04.321383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cc7599d222e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviewer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('verification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('valid', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('institution', sa.String(length=255), nullable=False),
    sa.Column('journal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journal_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('journal_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('reviewer_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['reviewer_id'], ['reviewer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('journal_id'),
    sa.UniqueConstraint('journal_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('journal_log')
    op.drop_table('author')
    op.drop_table('verification')
    op.drop_table('reviewer')
    # ### end Alembic commands ###
