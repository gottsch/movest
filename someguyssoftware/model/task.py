from someguyssoftware.model.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

#
# class Task
# used to store the state of a automated task
#


class Task(Base):
    def __init__(self, name, active=1, status="idle"):
        self.name = name
        self.active = active
#     self.lastRun = lastRun
#     self.lastSuccess = lastSuccess
        self.status = status

    # db mapping/properties
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    active = Column(Boolean)
    lastRun = Column("last_run", DateTime)
    lastSuccess = Column("last_success", DateTime)
    status = Column(String(45))

    # java-style
    def tostring(self):
        return "Task = [name: '" + self.name \
            + "', active: " + str(self.active) \
            + ", status: '" + self.status \
            + "']"

    # python-style
    def __repr__(self):
        return "<Task(name='%s')>" % self.name

# ---------------------------------------------------------------------
