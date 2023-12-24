from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

class Article_Favori(Base):
    __tablename__ = "Articles_Favoris"
    __table_args__ = {'extend_existing': True}

    ID_Article_Favori : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Article : Mapped[int] = mapped_column(ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE'))
    ID_Compte : Mapped[int] = mapped_column(ForeignKey('Comptes.ID_Compte', ondelete='CASCADE', onupdate='CASCADE'))