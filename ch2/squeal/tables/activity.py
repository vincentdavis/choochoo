
from sqlalchemy import Column, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from .source import Source, SourceType
from ..support import Base
from ..types import Time, Sort
from ...lib.date import format_time


class ActivityGroup(Base):

    __tablename__ = 'activity_group'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, server_default='')
    description = Column(Text, nullable=False, server_default='')
    sort = Column(Sort, nullable=False, server_default='')

    def __str__(self):
        return 'ActivityGroup "%s"' % self.name


class ActivityJournal(Source):

    __tablename__ = 'activity_journal'

    id = Column(Integer, ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    activity_group_id = Column(Integer, ForeignKey('activity_group.id'), nullable=False)
    activity_group = relationship('ActivityGroup')
    name = Column(Text, unique=True)
    fit_file = Column(Text, nullable=False, unique=True)
    finish = Column(Time, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': SourceType.ACTIVITY
    }

    def __str__(self):
        return 'ActivityJournal from %s' % format_time(self.time)


class ActivityTimespan(Base):

    __tablename__ = 'activity_timespan'

    id = Column(Integer, primary_key=True)
    activity_journal_id = Column(Integer, ForeignKey('source.id', ondelete='cascade'),
                                 nullable=False)
    activity_journal = relationship('ActivityJournal',
                                    backref=backref('timespans', cascade='all, delete-orphan',
                                                    passive_deletes=True,
                                                    order_by='ActivityTimespan.start'))
    start = Column(Time, nullable=False)
    finish = Column(Time, nullable=False)
    UniqueConstraint('activity_journal_id', 'start')
