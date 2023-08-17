"""split country column values

Revision ID: e5fe48b2286b
Revises: 9749b607229c
Create Date: 2023-08-16 16:34:20.635225

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "e5fe48b2286b"
down_revision = "9749b607229c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    result = connection.execute("SELECT id, country FROM residence")

    for row in result:
        id_, country = row
        if "," in country:
            country_name, country_code = country.split(",")
            connection.execute(
                "UPDATE residence SET country = %s, country_code = %s WHERE id = %s",
                (country_name.strip(), country_code.strip(), id_),
            )
