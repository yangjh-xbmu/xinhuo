"""Initial migration: create users, courses, knowledge_points, quiz_records tables

Revision ID: bac93e8c4f86
Revises: 
Create Date: 2025-09-15 03:55:54.686479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bac93e8c4f86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create courses table
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('cover_image_url', sa.String(length=255), nullable=True),
    sa.Column('difficulty_level', sa.String(length=20), nullable=False),
    sa.Column('estimated_duration', sa.Integer(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_index(op.f('ix_courses_title'), 'courses', ['title'], unique=False)
    
    # Create knowledge_points table
    op.create_table('knowledge_points',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.Column('quiz_question', sa.Text(), nullable=True),
    sa.Column('quiz_options', sa.JSON(), nullable=True),
    sa.Column('quiz_correct_answer', sa.String(length=10), nullable=True),
    sa.Column('quiz_explanation', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_points_id'), 'knowledge_points', ['id'], unique=False)
    op.create_index(op.f('ix_knowledge_points_course_id'), 'knowledge_points', ['course_id'], unique=False)
    op.create_index(op.f('ix_knowledge_points_title'), 'knowledge_points', ['title'], unique=False)
    
    # Create quiz_records table
    op.create_table('quiz_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('knowledge_point_id', sa.Integer(), nullable=False),
    sa.Column('user_answer', sa.String(length=10), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('time_spent', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['knowledge_point_id'], ['knowledge_points.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_records_id'), 'quiz_records', ['id'], unique=False)
    op.create_index(op.f('ix_quiz_records_user_id'), 'quiz_records', ['user_id'], unique=False)
    op.create_index(op.f('ix_quiz_records_knowledge_point_id'), 'quiz_records', ['knowledge_point_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_quiz_records_knowledge_point_id'), table_name='quiz_records')
    op.drop_index(op.f('ix_quiz_records_user_id'), table_name='quiz_records')
    op.drop_index(op.f('ix_quiz_records_id'), table_name='quiz_records')
    op.drop_table('quiz_records')
    
    op.drop_index(op.f('ix_knowledge_points_title'), table_name='knowledge_points')
    op.drop_index(op.f('ix_knowledge_points_course_id'), table_name='knowledge_points')
    op.drop_index(op.f('ix_knowledge_points_id'), table_name='knowledge_points')
    op.drop_table('knowledge_points')
    
    op.drop_index(op.f('ix_courses_title'), table_name='courses')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
