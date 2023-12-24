from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

class Auteur_Article(Base):
    __tablename__ = "Auteurs_Articles"
    __table_args__ = {'extend_existing': True}

    ID_Auteur_Article : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_Auteur : Mapped[int] = mapped_column(ForeignKey('Articles.ID_Article', ondelete='CASCADE', onupdate='CASCADE'))
    ID_Article : Mapped[int] = mapped_column(ForeignKey('Auteurs.ID_Auteur', ondelete='CASCADE', onupdate='CASCADE'))