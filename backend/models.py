import os

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    LargeBinary,
    Text,
    create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
engine = create_engine(os.getenv('DBURL'), echo=True)
db = sessionmaker(bind=engine)()
Base = declarative_base()


class Sheet(Base):
    __tablename__ = 'sheets'
    id = Column(Text, primary_key=True)
    link = Column(Text)
    title = Column(Text)
    abc = Column(Text)
    abc_link = Column(Text)
    musicxml = Column(LargeBinary)
    musicxml_link = Column(Text)
    has_midi = Column(Boolean, default=False)
    midi_link = Column(Text)

    def __repr__(self):
        return f"<Sheet title={self.title}>"
