"""crack

Revision ID: 859e8df1f7b9
Revises: 
Create Date: 2020-12-20 11:24:19.477456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '859e8df1f7b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_uid'), 'user', ['uid'], unique=False)
    op.create_table('instrument',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_uid', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_instrument_uid'), 'instrument', ['uid'], unique=False)
    op.create_table('strategy',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_uid', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_strategy_uid'), 'strategy', ['uid'], unique=False)
    op.create_table('study',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_study_uid'), 'study', ['uid'], unique=False)
    op.create_table('style',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_uid', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_style_uid'), 'style', ['uid'], unique=False)
    op.create_table('task',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_task_uid'), 'task', ['uid'], unique=False)
    op.create_table('tradingplan',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_tradingplan_uid'), 'tradingplan', ['uid'], unique=False)
    op.create_table('watchlist',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_watchlist_uid'), 'watchlist', ['uid'], unique=False)
    op.create_table('attribute',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('study_uid', sa.Integer(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['study_uid'], ['study.uid'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_attribute_uid'), 'attribute', ['uid'], unique=False)
    op.create_table('strategyimage',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('alt', sa.String(length=128), nullable=True),
    sa.Column('public_uid', sa.String(), nullable=True),
    sa.Column('asset_uid', sa.String(), nullable=True),
    sa.Column('signature', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('version_uid', sa.String(), nullable=True),
    sa.Column('strategy_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['strategy_uid'], ['strategy.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_strategyimage_uid'), 'strategyimage', ['uid'], unique=False)
    op.create_table('studyitem',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('study_uid', sa.Integer(), nullable=False),
    sa.Column('instrument_uid', sa.Integer(), nullable=True),
    sa.Column('position', sa.Boolean(), nullable=True),
    sa.Column('outcome', sa.Boolean(), nullable=True),
    sa.Column('pips', sa.Integer(), nullable=True),
    sa.Column('rrr', sa.Float(), nullable=True),
    sa.Column('style_uid', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_uid'], ['instrument.uid'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['study_uid'], ['study.uid'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['style_uid'], ['style.uid'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_studyitem_uid'), 'studyitem', ['uid'], unique=False)
    op.create_table('trade',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('instrument_uid', sa.Integer(), nullable=False),
    sa.Column('strategy_uid', sa.Integer(), nullable=False),
    sa.Column('position', sa.Boolean(), nullable=True),
    sa.Column('outcome', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('pips', sa.Integer(), nullable=True),
    sa.Column('rr', sa.Float(), nullable=True),
    sa.Column('style_uid', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('sl', sa.Integer(), nullable=True),
    sa.Column('tp', sa.Integer(), nullable=True),
    sa.Column('tp_reached', sa.Boolean(), nullable=True),
    sa.Column('tp_exceeded', sa.Boolean(), nullable=True),
    sa.Column('full_stop', sa.Boolean(), nullable=True),
    sa.Column('entry_price', sa.Float(), nullable=True),
    sa.Column('sl_price', sa.Float(), nullable=True),
    sa.Column('tp_price', sa.Float(), nullable=True),
    sa.Column('scaled_in', sa.Boolean(), nullable=True),
    sa.Column('scaled_out', sa.Boolean(), nullable=True),
    sa.Column('correlated_position', sa.Boolean(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_uid'], ['instrument.uid'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['owner_id'], ['user.uid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['strategy_uid'], ['strategy.uid'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['style_uid'], ['style.uid'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_trade_uid'), 'trade', ['uid'], unique=False)
    op.create_table('studyitemattribute',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('studyitem_uid', sa.Integer(), nullable=False),
    sa.Column('attribute_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['attribute_uid'], ['attribute.uid'], ),
    sa.ForeignKeyConstraint(['studyitem_uid'], ['studyitem.uid'], ),
    sa.PrimaryKeyConstraint('uid', 'studyitem_uid', 'attribute_uid')
    )
    op.create_index(op.f('ix_studyitemattribute_uid'), 'studyitemattribute', ['uid'], unique=False)
    op.create_table('studyitemimage',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('alt', sa.String(length=128), nullable=True),
    sa.Column('public_uid', sa.String(), nullable=True),
    sa.Column('asset_uid', sa.String(), nullable=True),
    sa.Column('signature', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('version_uid', sa.String(), nullable=True),
    sa.Column('studyitem_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['studyitem_uid'], ['studyitem.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_studyitemimage_uid'), 'studyitemimage', ['uid'], unique=False)
    op.create_table('tradeimage',
    sa.Column('uid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('alt', sa.String(length=128), nullable=True),
    sa.Column('public_uid', sa.String(), nullable=True),
    sa.Column('asset_uid', sa.String(), nullable=True),
    sa.Column('signature', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('version_uid', sa.String(), nullable=True),
    sa.Column('trade_uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trade_uid'], ['trade.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_tradeimage_uid'), 'tradeimage', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tradeimage_uid'), table_name='tradeimage')
    op.drop_table('tradeimage')
    op.drop_index(op.f('ix_studyitemimage_uid'), table_name='studyitemimage')
    op.drop_table('studyitemimage')
    op.drop_index(op.f('ix_studyitemattribute_uid'), table_name='studyitemattribute')
    op.drop_table('studyitemattribute')
    op.drop_index(op.f('ix_trade_uid'), table_name='trade')
    op.drop_table('trade')
    op.drop_index(op.f('ix_studyitem_uid'), table_name='studyitem')
    op.drop_table('studyitem')
    op.drop_index(op.f('ix_strategyimage_uid'), table_name='strategyimage')
    op.drop_table('strategyimage')
    op.drop_index(op.f('ix_attribute_uid'), table_name='attribute')
    op.drop_table('attribute')
    op.drop_index(op.f('ix_watchlist_uid'), table_name='watchlist')
    op.drop_table('watchlist')
    op.drop_index(op.f('ix_tradingplan_uid'), table_name='tradingplan')
    op.drop_table('tradingplan')
    op.drop_index(op.f('ix_task_uid'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_style_uid'), table_name='style')
    op.drop_table('style')
    op.drop_index(op.f('ix_study_uid'), table_name='study')
    op.drop_table('study')
    op.drop_index(op.f('ix_strategy_uid'), table_name='strategy')
    op.drop_table('strategy')
    op.drop_index(op.f('ix_instrument_uid'), table_name='instrument')
    op.drop_table('instrument')
    op.drop_index(op.f('ix_user_uid'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###