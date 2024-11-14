import pandas as pd
from sqlalchemy import create_engine

# Configurações do banco de dados
csv_file = r'C:\Users\José Augusto\Downloads\archive 3\IOT-temp.csv'  # Certifique-se de incluir ".csv" no final do nome do arquivo
db_url = 'postgresql+psycopg2://postgres:sua_senha@localhost:5432/postgres'

# Lê o CSV
data = pd.read_csv(csv_file)

# Conecta ao banco de dados
engine = create_engine(db_url)

# Insere os dados no PostgreSQL
with engine.connect() as connection:
    data.to_sql('temperature_readings', con=connection, if_exists='replace', index=False)

# Criação das views SQL
sql_queries = [
    """
    CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
    SELECT device_id, AVG(temperature) AS avg_temp
    FROM temperature_readings
    GROUP BY device_id;
    """,
    
    """
    CREATE OR REPLACE VIEW leituras_por_hora AS
    SELECT EXTRACT(HOUR FROM timestamp_column) AS hora, COUNT(*) AS contagem
    FROM temperature_readings
    GROUP BY hora
    ORDER BY hora;
    """,
    
    """
    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
    SELECT DATE(timestamp_column) AS data,
           MAX(temperature) AS temp_max,
           MIN(temperature) AS temp_min
    FROM temperature_readings
    GROUP BY data
    ORDER BY data;
    """
]

# Conecta ao banco e executa cada consulta SQL para criar as views
with engine.connect() as connection:
    for query in sql_queries:
        connection.execute(query)

print("Dados e views criados com sucesso.")
