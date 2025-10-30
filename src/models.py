from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class Characters(db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    specie_id: Mapped[int] = mapped_column(ForeignKey("species.id"))

    vehicles: Mapped[List["Vehicles"]] = relationship(back_populates="owner")
    planet: Mapped["Planets"] = relationship(back_populates="characters")
    specie: Mapped["Species"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "planet_id": self.planet_id,
            "specie_id": self.specie_id
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # zmieniamy nazwę w Pythonie, ale w DB zostaje "type"
    vehicle_type: Mapped[str] = mapped_column("type", nullable=False)
    max_speed: Mapped[str] = mapped_column(nullable=False)
    charac_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    owner: Mapped["Characters"] = relationship(back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.vehicle_type,  # w serializacji trzymamy nazwę logiczną
            "max_speed": self.max_speed,
            "charac_id": self.charac_id
        }


class Planets(db.Model):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    characters: Mapped[List["Characters"]] = relationship(
        back_populates="planet")
    species: Mapped[List["Species"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Species(db.Model):
    __tablename__ = 'species'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    species_type: Mapped[str] = mapped_column("type", nullable=False)  # j.w.
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    characters: Mapped[List["Characters"]] = relationship(
        back_populates="specie")
    planet: Mapped["Planets"] = relationship(back_populates="species")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.species_type,
            "planet_id": self.planet_id
        }


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)  # poprawione
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped["Characters"] = relationship()
    planet: Mapped["Planets"] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }
