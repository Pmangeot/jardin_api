"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2022-10-18 11:12:22.253864

"""

import sqlalchemy as sa # type: ignore
from alembic import op # type: ignore


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("firstname", sa.String(length=128), nullable=False, unique=True),
        sa.Column("lastname", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=128), default=False),
        sa.Column("password", sa.String(length=128), default=False),
        sa.Column("admin", sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "type",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "state",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "season",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("active", sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reservation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("articles_total", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("state_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),      
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["state_id"], ["state.id"]),
        sa.ForeignKeyConstraint(["season_id"], ["season.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),        
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("total_stock", sa.Integer(), nullable=False),
        sa.Column("remaining_quantity", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),   
        sa.ForeignKeyConstraint(["type_id"], ["type.id"]),
        sa.ForeignKeyConstraint(["season_id"], ["season.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reservation_articles",
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["reservation_id"], ["reservation.id"]),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.PrimaryKeyConstraint("reservation_id", "article_id"),
    )

def downgrade() -> None:
    op.drop_table("reservation_articles")
    op.drop_table("articles")
    op.drop_table("reservation")
    op.drop_table("season")
    op.drop_table("state")
    op.drop_table("type")
    op.drop_table("user")

