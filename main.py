from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Blip.database import Persona, SessionLocal  
from datetime import date

app = FastAPI()
app.title = "Veterinaria"
app.version = "0.0.1"

class PersonaCreate(BaseModel):
    nombre: str
    fecha_nacimiento: date 
    sexo: str
    correo: str
    telefono: str
    domicilio: str

class PersonaRead(BaseModel):
    persona_id: int
    nombre: str
    fecha_nacimiento: date
    sexo: str
    correo: str
    telefono: str
    domicilio: str

def get_db():
    db = SessionLocal()  # Usa SessionLocal
    try:
        yield db
    finally:
        db.close()

@app.post("/personas/", response_model=PersonaRead)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    try:
        nueva_persona = Persona(**persona.dict())
        db.add(nueva_persona)
        db.commit()
        db.refresh(nueva_persona)
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la persona"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas/", response_model=list[PersonaRead])
def leer_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Persona).offset(skip).limit(limit).all()

@app.get("/personas/{persona_id}", response_model=PersonaRead)
def leer_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.persona_id == persona_id).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.put("/personas/{persona_id}", response_model=PersonaRead)
def actualizar_persona(persona_id: int, persona: PersonaCreate, db: Session = Depends(get_db)):
    persona_db = db.query(Persona).filter(Persona.persona_id == persona_id).first()
    if persona_db is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    for key, value in persona.dict().items():
        setattr(persona_db, key, value)
    
    db.commit()
    db.refresh(persona_db)
    return persona_db

@app.delete("/personas/{persona_id}", response_model=PersonaRead)
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    persona_db = db.query(Persona).filter(Persona.persona_id == persona_id).first()
    if persona_db is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    db.delete(persona_db)
    db.commit()
    return persona_db
