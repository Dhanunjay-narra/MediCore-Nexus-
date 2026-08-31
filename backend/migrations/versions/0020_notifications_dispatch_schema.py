"""
Alembic Database Migration: Multi-Channel Communications (notifications)
Revision ID: 0020_notifications_dispatch_schema
Revises: '0019_staff_roster_schema'
Create Date: 2026-08-31 20:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql, sqlite

revision = "0020_notifications_dispatch_schema"
down_revision = '0019_staff_roster_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Execute schema upgrades for Multi-Channel Communications."""
    op.create_table(
        "notifications_master",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("entity_code", sa.String(length=64), unique=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=128), server_default="General", nullable=False),
        sa.Column("status", sa.String(length=64), server_default="Active", nullable=False),
        sa.Column("hospital_id", sa.String(length=64), server_default="hosp-001", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("base_cost", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("standard_price", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("quantity_capacity", sa.Integer(), server_default="100", nullable=False),
        sa.Column("extended_attributes", sa.JSON(), nullable=True),
        sa.Column("compliance_audit_flags", sa.String(length=255), server_default="HIPAA_COMPLIANT"),
        sa.Column("version_number", sa.Integer(), server_default="1", nullable=False),
        sa.Column("last_modified_by", sa.String(length=128), server_default="SYSTEM"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_notifications_entity_code", "notifications_master", ["entity_code"], unique=True)
    op.create_index("ix_notifications_status", "notifications_master", ["status"], unique=False)
    op.create_index("ix_notifications_hospital", "notifications_master", ["hospital_id"], unique=False)

    op.create_table(
        "notifications_transactions",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("master_id", sa.String(length=64), sa.ForeignKey("notifications_master.id"), nullable=False),
        sa.Column("transaction_code", sa.String(length=128), unique=True, nullable=False),
        sa.Column("transaction_type", sa.String(length=64), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.Column("unit_rate", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("total_amount", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_notifications_txn_code", "notifications_transactions", ["transaction_code"], unique=True)


def downgrade() -> None:
    """Revert schema changes."""
    op.drop_table("notifications_transactions")
    op.drop_table("notifications_master")
