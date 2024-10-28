from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./veterinaria.db')

Base = declarative_base()


class Persona(Base):
    __tablename__ = 'personas'

    persona_id = Column(Integer(), primary_key = True)
    nombre = Column(String(50), nullable = False, unique = True)
    fecha_nacimiento = Column(Date(), nullable = False, unique = False)
    sexo = Column(String(20), nullable = False, unique = False)
    correo = Column(String(50), nullable = False, unique = True)
    telefono = Column(String(20), nullable = False, unique = True)
    domicilio = Column(String(50), nullable = False, unique = True)


class Mascota(Base):
    __tablename__ = 'mascotas'

    mascota_id = Column(Integer(), primary_key = True)
    persona_id = Column(Integer(), ForeignKey('personas.persona_id'))
    especie_id = Column(Integer(), ForeignKey('especies.especie_id'))
    nombre = Column(String(50), nullable = False, unique = False)
    edad = Column(Integer(), nullable = False, unique = False)
    sexo = Column(String(20), nullable = False, unique = False)
    peso = Column(Float(), nullable = False, unique = False)

class Especie(Base):
    __tablename__ = 'especies'

    especie_id = Column(Integer(), primary_key = True)
    nombre_especie = Column(String(20), nullable = False, unique = True)
    descripcion = Column(String(100), nullable = False, unique = False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)