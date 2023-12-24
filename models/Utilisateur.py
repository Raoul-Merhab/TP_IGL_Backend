from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from database import Base
from models.Article import Article

class Utilisateur(Base):
    __tablename__ = "Utilisateurs"
    __table_args__ = {'extend_existing': True}

    ID_Utilisateur : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nom : Mapped[str] = mapped_column(String(200))
    Email : Mapped[str] = mapped_column(String(200))
    Password : Mapped[str] = mapped_column(String(200))

    Articles_Favoris : Mapped["Article"] = relationship("Article", back_populates="Utilisateurs", secondary="Articles_Favoris")