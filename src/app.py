import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import os

st.set_page_config(
    page_title="FarmTech Dashboard",
    page_icon="🌱",
    layout="wide"
)

def create_sample_data():
    """Cria dados de exemplo para demonstração"""
    np.random.seed(42)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    timestamps = pd.date_range(start=start_date, end=end_date, freq='30min')
    
    data = []
    for ts in timestamps:
        hour = ts.hour
        
        base_humidity = 45 + 15 * np.sin(2 * np.pi * (hour - 6) / 24)
        humidity = max(20, min(80, base_humidity + np.random.normal(0, 5)))
        
        ph = 6.5 + np.random.normal(0, 0.5)
        ph = max(4.0, min(9.0, ph))
        
        p = np.random.choice([0, 1], p=[0.3, 0.7])
        k = np.random.choice([0, 1], p=[0.4, 0.6])
        
        irrigou = 1 if (humidity < 40.0 and (p == 1 or k == 1)) else 0
        
        data.append({
            'timestamp': ts,
            'umidade': round(humidity, 1),
            'ph': round(ph, 2),
            'p': p,
            'k': k,
            'irrigou': irrigou
        })
    
    return pd.DataFrame(data)

def load_data():
    """Carrega dados do banco SQLite ou cria dados de exemplo"""
    if os.path.exists('db/farmtech.db'):
        try:
            conn = sqlite3.connect('db/farmtech.db')
            df = pd.read_sql_query("SELECT * FROM medicoes ORDER BY ts DESC LIMIT 500", conn)
            conn.close()
            df['timestamp'] = pd.to_datetime(df['ts'])
            return df
        except:
            pass
    
    return create_sample_data()

def main():
    """Função principal do dashboard"""
    
    st.title("🌱 FarmTech Solutions - Dashboard")
    st.markdown("**Sistema de Irrigação Inteligente - Monitoramento em Tempo Real**")
    
    st.sidebar.header("⚙️ Configurações")
    
    df = load_data()
    
    if df.empty:
        st.error("❌ Nenhum dado disponível")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_humidity = df['umidade'].mean()
        st.metric(
            label="🌊 Umidade Média",
            value=f"{avg_humidity:.1f}%",
            delta=f"{df['umidade'].iloc[0] - avg_humidity:.1f}%" if len(df) > 1 else None
        )
    
    with col2:
        avg_ph = df['ph'].mean()
        st.metric(
            label="⚗️ pH Médio",
            value=f"{avg_ph:.2f}",
            delta=f"{df['ph'].iloc[0] - avg_ph:.2f}" if len(df) > 1 else None
        )
    
    with col3:
        p_deficiency = (df['p'] == 1).sum() / len(df) * 100
        st.metric(
            label="🧪 Deficiência P",
            value=f"{p_deficiency:.1f}%"
        )
    
    with col4:
        irrigation_rate = (df['irrigou'] == 1).sum() / len(df) * 100
        st.metric(
            label="💧 Taxa de Irrigação",
            value=f"{irrigation_rate:.1f}%"
        )
    
    st.header("📊 Análise Temporal")
    
    fig_humidity = px.line(
        df.tail(100), 
        x='timestamp', 
        y='umidade',
        title='📈 Umidade do Solo (Serial Plotter)',
        labels={'umidade': 'Umidade (%)', 'timestamp': 'Tempo'}
    )
    fig_humidity.add_hline(y=40, line_dash="dash", line_color="red", 
                          annotation_text="Limite de Irrigação (40%)")
    fig_humidity.update_layout(height=400)
    st.plotly_chart(fig_humidity, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ph = px.line(
            df.tail(50), 
            x='timestamp', 
            y='ph',
            title='⚗️ Nível de pH',
            labels={'ph': 'pH', 'timestamp': 'Tempo'}
        )
        fig_ph.add_hline(y=6.5, line_dash="dash", line_color="green", 
                        annotation_text="pH Ideal")
        st.plotly_chart(fig_ph, use_container_width=True)
    
    with col2:
        irrigation_data = df.tail(50).copy()
        irrigation_data['status'] = irrigation_data['irrigou'].map({0: 'Desligada', 1: 'Ligada'})
        
        fig_irrigation = px.scatter(
            irrigation_data, 
            x='timestamp', 
            y='status',
            color='status',
            title='💧 Status da Irrigação',
            labels={'status': 'Bomba', 'timestamp': 'Tempo'}
        )
        st.plotly_chart(fig_irrigation, use_container_width=True)
    
    st.header("🔍 Análise de Correlações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            df, 
            x='umidade', 
            y='irrigou',
            color='irrigou',
            title='Relação Umidade × Irrigação',
            labels={'umidade': 'Umidade (%)', 'irrigou': 'Irrigação Ativa'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        nutrients_data = pd.DataFrame({
            'Nutriente': ['Fósforo (P)', 'Potássio (K)'],
            'Deficiência (%)': [
                (df['p'] == 1).sum() / len(df) * 100,
                (df['k'] == 1).sum() / len(df) * 100
            ]
        })
        
        fig_nutrients = px.bar(
            nutrients_data,
            x='Nutriente',
            y='Deficiência (%)',
            title='📊 Deficiência de Nutrientes',
            color='Nutriente'
        )
        st.plotly_chart(fig_nutrients, use_container_width=True)
    
    st.header("📋 Dados Recentes")
    st.dataframe(
        df.head(20)[['timestamp', 'umidade', 'ph', 'p', 'k', 'irrigou']],
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("**FarmTech Solutions** - Sistema de Irrigação Inteligente | Fase 4 - FIAP")

if __name__ == "__main__":
    main()
