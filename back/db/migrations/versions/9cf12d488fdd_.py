"""empty message

Revision ID: 9cf12d488fdd
Revises: e3c68f8570fc
Create Date: 2022-10-22 17:30:06.043615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9cf12d488fdd"
down_revision = "e3c68f8570fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("notification_user_id_fkey", "notification", type_="foreignkey")
    op.create_foreign_key(
        None, "notification", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_index("ix_user_username", table_name="user")
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.create_index("ix_user_username", "user", ["username"], unique=False)
    op.drop_constraint(None, "notification", type_="foreignkey")
    op.create_foreign_key(
        "notification_user_id_fkey", "notification", "user", ["user_id"], ["id"]
    )
    # ### end Alembic commands ###
