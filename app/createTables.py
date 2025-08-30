from database import Base, engine
import models

# Cria todas as tabelas definidas nas models
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
