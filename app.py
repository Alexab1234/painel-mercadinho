import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mercadinho Dashboard", layout="wide")
st.title("🛒 Painel do Mercadinho")

# CONEXÃO COM O BANCO DE DADOS
def get_data(query):
    # Conecta no MySQL (A senha está vazia "", se tiver senha, coloque dentro das aspas)
    conn = mysql.connector.connect(
        host="localhost", user="root", password="709017ab?", database="mercadinho"
    )
    return pd.read_sql(query, conn)

try:
    # 1. INDICADORES (KPIs)
    st.header("Resumo Financeiro")
    df_kpi = get_data("SELECT SUM(total_venda) as fat, COUNT(id) as qtd FROM vendas")
    
    # Tratamento de erro caso o banco esteja vazio
    faturamento = df_kpi['fat'][0] if df_kpi['fat'][0] else 0
    vendas = df_kpi['qtd'][0] if df_kpi['qtd'][0] else 0

    col1, col2 = st.columns(2)
    col1.metric("💰 Faturamento Total", f"R$ {faturamento:,.2f}")
    col2.metric("📦 Total de Vendas", vendas)

    st.markdown("---")

    # 2. GRÁFICO
    st.header("🏆 Produtos Mais Vendidos")
    df_prod = get_data("""
        SELECT p.nome, SUM(i.quantidade) as qtd 
        FROM vendas_itens i 
        JOIN produtos p ON i.produto_id = p.id 
        GROUP BY p.nome 
        ORDER BY qtd DESC 
        LIMIT 5
    """)
    
    # Exibe o gráfico
    fig = px.bar(df_prod, x='qtd', y='nome', orientation='h', title="Top 5 Itens", text='qtd')
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao conectar ou ler dados: {e}")