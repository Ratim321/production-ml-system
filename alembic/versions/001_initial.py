"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=True),
        sa.Column('prediction', sa.Float(), nullable=True),
        sa.Column('probability', sa.Float(), nullable=True),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('features', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_churn', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_predictions_customer_id'), 'predictions', ['customer_id'], unique=False)
    op.create_index(op.f('ix_predictions_id'), 'predictions', ['id'], unique=False)

    op.create_table(
        'model_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_version', sa.String(), nullable=True),
        sa.Column('metric_name', sa.String(), nullable=True),
        sa.Column('metric_value', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_metrics_model_version'), 'model_metrics', ['model_version'], unique=False)

    op.create_table(
        'model_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('model_type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('traffic_percent', sa.Integer(), nullable=True),
        sa.Column('mlflow_run_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('performance_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('version')
    )
    op.create_index(op.f('ix_model_versions_version'), 'model_versions', ['version'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_model_versions_version'), table_name='model_versions')
    op.drop_table('model_versions')
    op.drop_index(op.f('ix_model_metrics_model_version'), table_name='model_metrics')
    op.drop_table('model_metrics')
    op.drop_index(op.f('ix_predictions_id'), table_name='predictions')
    op.drop_index(op.f('ix_predictions_customer_id'), table_name='predictions')
    op.drop_table('predictions')


