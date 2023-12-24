from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean
from database import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from models.Auteur import Auteur
from models.Reference import Reference
from models.Mot_Cle import Mot_Cle

class Article(Base):
    __tablename__ = "Articles"
    __table_args__ = {'extend_existing': True}

    ID_Article : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Titre : Mapped[str] = mapped_column(String(1000))
    Resume : Mapped[str] = mapped_column(LONGTEXT)
    Texte : Mapped[str] = mapped_column(LONGTEXT)
    Date_Publication : Mapped[str] = mapped_column(String(100))
    Valide : Mapped[bool] = mapped_column(Boolean)

    Auteurs : Mapped[list["Auteur"]] = relationship("Auteur", back_populates="Articles", secondary="Auteurs_Articles")
    References : Mapped[list["Reference"]] = relationship("Reference", back_populates="Article", secondary="References_Articles")
    Mots_Cles : Mapped[list["Mot_Cle"]] = relationship("Mot_Cle", back_populates="Article", secondary="Mots_Cles_Articles")

    def __init__(self, Titre, Resume, Texte, Date_Publication, Valide):
        self.Titre = Titre
        self.Resume = Resume
        self.Texte = Texte
        self.Date_Publication = Date_Publication
        self.Valide = Valide

    def get_Obj(self):
        return {
            "ID_Article" : self.ID_Article,
            "Titre" : self.Titre,
            "Resume" : self.Resume,
            "Texte" : self.Texte,
            "Date_Publication" : self.Date_Publication,
            "Valide" : self.Valide,
            "Auteurs" : [*self.Auteurs(lambda x: x.Nom)],
            "Mots_Cles" : [*self.Mots_Cles(lambda x: x.Mot_Cle)],
            "References" : [*self.References(lambda x: x.Reference)]
        }