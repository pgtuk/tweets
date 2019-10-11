"""Create User and Twit tables

Revision ID: 8364977c14b1
Revises: 
Create Date: 2019-10-09 16:29:16.813792

"""

from src.utils import db_engine
from src.tweets.tables import metadata

# revision identifiers, used by Alembic.
revision = '8364977c14b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    metadata.create_all(db_engine, checkfirst=True)


def downgrade():
    metadata.drop_all(db_engine, checkfirst=True)
