from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, Table

# Base must be created first
Base = declarative_base()

# the association table between watch_list and assets (where watch_list is the parent)
association_table = Table('watch_list_assets', Base.metadata,
                          Column('watch_list_id', Integer, ForeignKey('watch_list.id')),
                          Column('asset_id', Integer, ForeignKey('assets.id'))
                          )