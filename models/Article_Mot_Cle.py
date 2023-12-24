from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

class Article_Mot_Cle(Base):
    __tablename__ = "Articles_Mots_Cles"
    __table_args__ = {'extend_existing': True}

    ID_Article_Mot_Cle : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Article : Mapped[int] = mapped_column(ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE'))
    ID_Mot_Cle : Mapped[int] = mapped_column(ForeignKey('Mots_Cles.ID_Mot_Cle', ondelete='CASCADE', onupdate='CASCADE'))