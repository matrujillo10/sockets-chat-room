"""empty message

Revision ID: 7e0ddd763344
Revises: d2912d862adb
Create Date: 2020-10-23 14:14:24.042997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e0ddd763344"
down_revision = "d2912d862adb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("password", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint("_id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "message",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("sent_on", sa.DateTime(), nullable=True),
        sa.Column("message", sa.String(length=1000), nullable=True),
        sa.Column("room", sa.String(length=100), nullable=True),
        sa.Column("sender_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["user._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(length=100), autoincrement=False, nullable=True),
        sa.Column(
            "password", sa.VARCHAR(length=100), autoincrement=False, nullable=True
        ),
        sa.Column("name", sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("_id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    op.drop_table("message")
    op.drop_table("user")
    # ### end Alembic commands ###
