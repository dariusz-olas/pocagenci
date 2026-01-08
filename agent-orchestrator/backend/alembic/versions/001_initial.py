"""Initial migration - create tasks, subtasks, executions tables.

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'decomposing', 'ready', 'in_progress', 'completed', 'failed', name='taskstatus'), nullable=False),
        sa.Column('decomposition_data', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )

    # SubTasks table
    op.create_table(
        'subtasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('complexity', sa.Enum('simple', 'medium', 'complex', name='subtaskcomplexity'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'decomposing', 'ready', 'in_progress', 'completed', 'failed', name='taskstatus'), nullable=False),
        sa.Column('dependencies', postgresql.JSON(), default=[]),
        sa.Column('acceptance_criteria', postgresql.JSON(), default=[]),
        sa.Column('order_index', sa.Integer(), default=0),
    )

    # Executions table
    op.create_table(
        'executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id'), nullable=False),
        sa.Column('status', sa.Enum('queued', 'running', 'completed', 'failed', 'cancelled', name='executionstatus'), nullable=False),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('logs', postgresql.JSON(), default=[]),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('execution_time_seconds', sa.Float(), nullable=True),
        sa.Column('adapter_name', sa.String(50), default='crewai'),
        sa.Column('cost_usd', sa.Float(), default=0.0),
    )

    # Indexes
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_subtasks_task_id', 'subtasks', ['task_id'])
    op.create_index('ix_executions_task_id', 'executions', ['task_id'])


def downgrade() -> None:
    op.drop_index('ix_executions_task_id')
    op.drop_index('ix_subtasks_task_id')
    op.drop_index('ix_tasks_status')
    op.drop_table('executions')
    op.drop_table('subtasks')
    op.drop_table('tasks')
    op.execute('DROP TYPE IF EXISTS executionstatus')
    op.execute('DROP TYPE IF EXISTS subtaskcomplexity')
    op.execute('DROP TYPE IF EXISTS taskstatus')
