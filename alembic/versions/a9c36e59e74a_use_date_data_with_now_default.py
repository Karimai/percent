"""use Date data with now default

Revision ID: a9c36e59e74a
Revises: 396bddedb767
Create Date: 2023-07-09 20:00:41.587457

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "a9c36e59e74a"
down_revision = "396bddedb767"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_residence_id", table_name="residence")
    op.drop_table("residence")
    op.drop_index("ix_user_id", table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('user_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "username", sa.VARCHAR(length=25), autoincrement=False, nullable=False
        ),
        sa.Column(
            "password", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("date_of_birth", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("email", name="user_email_key"),
        sa.UniqueConstraint("username", name="user_username_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.create_table(
        "residence",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "start_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "end_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "status",
            postgresql.ENUM(
                "motherland", "travel", "study", "work", "other", name="status"
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("country", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name="residence_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="residence_pkey"),
    )
    op.create_index("ix_residence_id", "residence", ["id"], unique=False)
    # ### end Alembic commands ###
