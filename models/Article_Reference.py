from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

class Article_Reference(Base):
    __tablename__ = "Articles_References"
    __table_args__ = {'extend_existing': True}

    ID_Article_Reference : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Article : Mapped[int] = mapped_column(ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE'))
    ID_Reference : Mapped[int] = mapped_column(ForeignKey('References.ID_Reference', ondelete='CASCADE', onupdate='CASCADE'))