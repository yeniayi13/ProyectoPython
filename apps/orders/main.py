from src.common.infrastructure.config.database.init_db import create_tables

def main():
    # Inicializar la base de datos y crear las tablas
    create_tables()
    print("Database initialized and tables created.")

if __name__ == "__main__":
    main()
