# Trabalho-de-IOT
Trabalho da faculdade 

Projeto de Monitoramento de Temperaturas IoT
Este projeto utiliza dados de temperatura de dispositivos IoT e realiza a ingestão desses dados em um banco de dados PostgreSQL, onde são criadas views SQL para análise. A visualização dos dados é feita por meio de um dashboard com gráficos que permitem explorar diferentes aspectos dos dados coletados.

Sumário
Introdução
Configuração do Ambiente
Ingestão de Dados
Criação das Views SQL
Visualização com Streamlit
Explicação das Views SQL
Possíveis Insights dos Dados
Introdução
O objetivo deste projeto é coletar, armazenar e visualizar dados de temperatura de dispositivos IoT para monitorar as condições ao longo do tempo. O sistema é composto por um pipeline de dados que realiza as seguintes tarefas:

Leitura dos dados a partir de um arquivo CSV.
Armazenamento dos dados no banco de dados PostgreSQL.
Criação de views SQL para realizar cálculos agregados.
Visualização dos dados usando um dashboard interativo no Streamlit.
Configuração do Ambiente
Pré-requisitos:

Python 3.x
PostgreSQL instalado e configurado
Pacotes Python: pandas, sqlalchemy, psycopg2, streamlit, e plotly
Instalação dos Pacotes: Execute o seguinte comando para instalar os pacotes necessários:

pip install pandas sqlalchemy psycopg2-binary streamlit plotly
Configuração do Banco de Dados:

Certifique-se de que o PostgreSQL está em execução.
Crie um banco de dados PostgreSQL chamado postgres (ou use o banco padrão).
Defina as credenciais de acesso no código.
Estrutura de Arquivos:

Coloque o arquivo de dados CSV no caminho correto, por exemplo:

C:/Users/José Augusto/Downloads/archive 3/IOT-temp.csv
Ingestão de Dados
O código lê um arquivo CSV contendo dados de temperatura e insere os dados na tabela temperature_readings do banco de dados PostgreSQL. Cada linha do arquivo representa uma leitura de temperatura de um dispositivo IoT em um horário específico.

Criação das Views SQL
Após a ingestão dos dados, três views SQL são criadas para agregar e organizar as informações para análises específicas.

Código de Ingestão e Criação de Views
python

import pandas as pd
from sqlalchemy import create_engine

# Configurações
csv_file = r'C:\Users\José Augusto\Downloads\archive 3\IOT-temp.csv'
db_url = 'postgresql+psycopg2://postgres:sua_senha@localhost:5432/postgres'
engine = create_engine(db_url)

# Carregar dados e inserir no banco
data = pd.read_csv(csv_file)
with engine.connect() as connection:
    data.to_sql('temperature_readings', con=connection, if_exists='replace', index=False)

# Criação das views
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

with engine.connect() as connection:
    for query in sql_queries:
        connection.execute(query)
print("Views criadas com sucesso.")
Visualização com Streamlit
O dashboard é criado com a biblioteca Streamlit e utiliza plotly para a visualização dos gráficos. Para executar o dashboard, use o comando:



streamlit run dashboard.py
O dashboard apresenta os seguintes gráficos:

Média de Temperatura por Dispositivo: um gráfico de barras mostrando a média das temperaturas medidas por cada dispositivo.
Leituras por Hora do Dia: um gráfico de linha que mostra o número de leituras de temperatura em cada hora do dia.
Temperaturas Máximas e Mínimas por Dia: um gráfico de linha com as temperaturas máxima e mínima registradas a cada dia.
Explicação das Views SQL
1. avg_temp_por_dispositivo
Objetivo: Esta view calcula a média de temperatura registrada por cada dispositivo.
Consulta:
sql

CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;
Propósito: Avaliar o comportamento de cada dispositivo em termos de média de temperatura registrada.
2. leituras_por_hora
Objetivo: Esta view calcula a contagem de leituras feitas em cada hora do dia.
Consulta:
sql

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM timestamp_column) AS hora, COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;
Propósito: Identificar padrões de coleta de dados ao longo do dia, o que pode ajudar a otimizar a frequência das medições.
3. temp_max_min_por_dia
Objetivo: Esta view calcula a temperatura máxima e mínima registradas em cada dia.
Consulta:
sql

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT DATE(timestamp_column) AS data,
       MAX(temperature) AS temp_max,
       MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;
Propósito: Acompanhar as variações diárias de temperatura, útil para observar tendências sazonais ou padrões de mudanças climáticas.
Possíveis Insights dos Dados
Análise de Performance dos Dispositivos: A view avg_temp_por_dispositivo permite verificar se algum dispositivo está registrando valores anormais em relação à média, podendo indicar problemas de calibração ou mau funcionamento.

Padrões de Coleta de Dados: A view leituras_por_hora ajuda a entender o comportamento da coleta de dados ao longo do dia, o que pode indicar momentos de maior ou menor atividade e sugerir ajustes na frequência de coleta.

Variação Diária de Temperatura: A view temp_max_min_por_dia é útil para monitorar tendências diárias, que podem ajudar na identificação de padrões sazonais, flutuações de temperatura e detecção de eventos fora do normal.

Observação: Certifique-se de que o arquivo CSV está corretamente formatado e que a coluna timestamp_column existe e está configurada para as operações de extração de hora e data.

Autor: [José Augusto Ferreira] Data de Criação: [14/11/2024]
