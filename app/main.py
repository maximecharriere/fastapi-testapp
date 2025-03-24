from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from lxml import etree

from app.database import SessionLocal, engine
from app.models import Base, Client
from app.schemas import ClientInput, ClientResponse

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency pour obtenir une session de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload-xml")
async def upload_xml(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()

    # Parser le XML
    try:
        tree = etree.fromstring(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid XML format")

    # Lire et valider les données client
    clients_data = []
    errors = []
    for i, client_elem in enumerate(tree.findall("client"), start=1):
        try:
            client_id = int(client_elem.find("id").text)
            age = int(client_elem.find("age").text)
            revenue = float(client_elem.find("revenue").text)

            # Validation Pydantic
            client = ClientInput(id=client_id, age=age, revenue=revenue)
            clients_data.append(client)
        except Exception as e:
            errors.append(f"Ligne {i}: {str(e)}")
            continue

    if not clients_data:
        raise HTTPException(status_code=400, detail="No valid clients found in the uploaded XML.")

    # Enregistrer dans la base avec merge (insert or update)
    for client in clients_data:
        db.merge(Client(id=client.id, age=client.age, revenue=client.revenue))
    db.commit()
    
    # Convertir en DataFrame
    df = pd.DataFrame([client.dict() for client in clients_data])
    
    # Calcul des statistiques
    avg_age = df["age"].mean()
    avg_revenue = df["revenue"].mean()
    total_clients = len(df)

    return {
        "message": "Clients inserted successfully",
        "total_clients": total_clients,
        "average_age": avg_age,
        "average_revenue": avg_revenue,
        "invalid_entries": errors
    }


@app.get("/clients", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients
