import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configuração da conexão com o banco de dados PostgreSQL
engine = create_engine('postgresql://postgres:sua_senha@localhost:5432/postgres')

# Função para carregar dados de uma view
def load_data(view_name):
    try:
        data = pd.read_sql(f"SELECT * FROM {view_name}", engine)
        return data
    except SQLAlchemyError as e:
        st.error(f"Erro ao carregar a view '{view_name}': {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Título do dashboard
st.title('Dashboard de Temperaturas IoT')

# Gráfico 1: Média de temperatura por dispositivo
st.header('Média de Temperatura por Dispositivo')
df_avg_temp = load_data('avg_temp_por_dispositivo')
if not df_avg_temp.empty:
    fig1 = px.bar(df_avg_temp, x='device_id', y='avg_temp', title="Média de Temperatura por Dispositivo")
    st.plotly_chart(fig1)
else:
    st.warning("Dados não disponíveis para 'Média de Temperatura por Dispositivo'.")

# Gráfico 2: Contagem de leituras por hora
st.header('Leituras por Hora do Dia')
df_leituras_hora = load_data('leituras_por_hora')
if not df_leituras_hora.empty:
    fig2 = px.line(df_leituras_hora, x='hora', y='contagem', title="Leituras por Hora do Dia")
    st.plotly_chart(fig2)
else:
    st.warning("Dados não disponíveis para 'Leituras por Hora do Dia'.")

# Gráfico 3: Temperaturas máximas e mínimas por dia
st.header('Temperaturas Máximas e Mínimas por Dia')
df_temp_max_min = load_data('temp_max_min_por_dia')
if not df_temp_max_min.empty:
    fig3 = px.line(df_temp_max_min, x='data', y=['temp_max', 'temp_min'], title="Temperaturas Máximas e Mínimas por Dia")
    st.plotly_chart(fig3)
else:
    st.warning("Dados não disponíveis para 'Temperaturas Máximas e Mínimas por Dia'.")
