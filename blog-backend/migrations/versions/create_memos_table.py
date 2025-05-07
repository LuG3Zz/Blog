"""创建备忘录表

Revision ID: create_memos_table
Revises: 
Create Date: 2023-11-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_memos_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 创建备忘录表
    op.create_table(
        'memos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_encrypted', sa.Boolean(), nullable=False, default=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index(op.f('ix_memos_id'), 'memos', ['id'], unique=False)
    op.create_index(op.f('ix_memos_title'), 'memos', ['title'], unique=False)


def downgrade():
    # 删除索引
    op.drop_index(op.f('ix_memos_title'), table_name='memos')
    op.drop_index(op.f('ix_memos_id'), table_name='memos')
    
    # 删除表
    op.drop_table('memos')
