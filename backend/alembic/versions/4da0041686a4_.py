"""

Revision ID: 4da0041686a4
Revises: d880bfb9bc13
Create Date: 2020-10-09 07:13:37.531077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4da0041686a4'
down_revision = 'd880bfb9bc13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('studyitem_study_id_fkey', 'studyitem', type_='foreignkey')
    op.create_foreign_key(None, 'studyitem', 'study', ['study_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'studyitem', type_='foreignkey')
    op.create_foreign_key('studyitem_study_id_fkey', 'studyitem', 'trade', ['study_id'], ['id'])
    # ### end Alembic commands ###