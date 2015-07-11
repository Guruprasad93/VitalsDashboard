from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
device = Table('device', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=25)),
    Column('type', String(length=25)),
    Column('user_id', Integer),
)

vital = Table('vital', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('tempinternal', Float(precision=4), default=ColumnDefault(0)),
    Column('tempexternal', Float(precision=4), default=ColumnDefault(0)),
    Column('heartrate', Float(precision=4), default=ColumnDefault(0)),
    Column('bloodoxy', Float(precision=4), default=ColumnDefault(0)),
    Column('baro', Float(precision=4), default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['device'].create()
    post_meta.tables['vital'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['device'].drop()
    post_meta.tables['vital'].drop()
