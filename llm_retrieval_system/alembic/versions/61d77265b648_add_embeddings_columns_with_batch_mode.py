"""add embeddings columns

Revision ID: abc123
Revises: b6430a559b9f
Create Date: 2025-08-04 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123'  # Keep the generated ID
down_revision = 'b6430a559b9f'
branch_labels = None
depends_on = None

def upgrade():
    # Use batch mode for safe column additions
    with op.batch_alter_table('embeddings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pinecone_id', sa.String(length=64), nullable=False, server_default='placeholder'))
        batch_op.add_column(sa.Column('model_name', sa.String(length=100), nullable=True, server_default='text-embedding-ada-002'))
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True, server_default='completed'))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.create_unique_constraint('uq_embeddings_pinecone_id', ['pinecone_id'])

def downgrade():
    with op.batch_alter_table('embeddings', schema=None) as batch_op:
        batch_op.drop_constraint('uq_embeddings_pinecone_id', type_='unique')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('status')
        batch_op.drop_column('model_name')
        batch_op.drop_column('pinecone_id')
