from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.place import Place

router = APIRouter(prefix="/test", tags=["Testes Base de Dados"])

@router.get("/locais-turisticos")
def test_consultar_locais(db: Session = Depends(get_db)):
    # Faz uma query simples à tabela de locais turísticos
    locais = db.query(Place).all()
    
    return {
        "status": "sucesso",
        "total_registos": len(locais),
        "dados": locais
    }