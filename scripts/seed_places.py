import pandas as pd
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal  # Importa a sessão de BD configurada
from backend.app.models.place import Place        # Importa o modelo SQLAlchemy que já têm

def executar_seeding(caminho_csv: str = "locais_turisticos_tratados.csv"):
    print("A iniciar o processo de seeding...")
    
    # 1. Ler o ficheiro tratado pela equipa de dados com o pandas
    try:
        df = pd.read_csv(caminho_csv)
    except FileNotFoundError:
        print(f"Erro: O ficheiro '{caminho_csv}' não foi encontrado. Certifique-se de que foi exportado pelo Jupyter.")
        return

    # 2. Abrir sessão na base de dados
    db: Session = SessionLocal()
    
    try:
        contador_inseridos = 0
        
        # 3. Percorrer cada linha do DataFrame e inserir na BD
        for _, row in df.iterrows():
            # Verificar se o local já existe pelo nome para evitar duplicados
            existe = db.query(Place).filter(Place.name == row['name']).first()
            
            if not existe:
                novo_local = Place(
                    name=row.get('name'),
                    category=row.get('category'),
                    province=row.get('province'),
                    latitude=row.get('latitude'),
                    longitude=row.get('longitude'),
                    description=row.get('description')
                )
                db.add(novo_local)
                contador_inseridos += 1
                
        # 4. Gravar as alterações permanentemente na base de dados (Commit)
        db.commit()
        print(f"Sucesso! Foram inseridos {contador_inseridos} novos locais turísticos na base de dados.")
        
    except Exception as e:
        db.rollback()
        print(f"Ocorreu um erro durante o seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    executar_seeding()