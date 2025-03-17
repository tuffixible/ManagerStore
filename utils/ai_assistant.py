import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def analisar_tendencias_vendas(df_financeiro):
    """Analisa tendências de vendas dos últimos 30 dias"""
    if df_financeiro.empty:
        return None, None
    
    df = df_financeiro.copy()
    df['data'] = pd.to_datetime(df['data'])
    df = df[df['tipo'] == 'entrada']
    
    # Agrupa por data e soma os valores
    vendas_diarias = df.groupby(df['data'].dt.date)['valor'].sum().reset_index()
    if len(vendas_diarias) < 2:
        return None, None
    
    # Prepara dados para regressão
    X = np.array(range(len(vendas_diarias))).reshape(-1, 1)
    y = vendas_diarias['valor'].values
    
    # Ajusta o modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Calcula tendência
    tendencia = "crescente" if model.coef_[0] > 0 else "decrescente"
    variacao = abs(model.coef_[0])
    
    return tendencia, variacao

def analisar_estoque_critico(df_produtos):
    """Identifica produtos com estoque crítico"""
    if df_produtos.empty:
        return []
    
    estoque_critico = df_produtos[df_produtos['quantidade'] <= 5].copy()
    return estoque_critico.to_dict('records')

def gerar_sugestoes(df_produtos, df_financeiro):
    """Gera sugestões baseadas na análise dos dados"""
    sugestoes = []
    
    # Análise de vendas
    tendencia, variacao = analisar_tendencias_vendas(df_financeiro)
    if tendencia:
        sugestoes.append({
            'tipo': 'vendas',
            'mensagem': f"Tendência de vendas {tendencia}. "
                       f"Variação média diária: R$ {variacao:.2f}"
        })
    
    # Análise de estoque
    produtos_criticos = analisar_estoque_critico(df_produtos)
    if produtos_criticos:
        sugestoes.append({
            'tipo': 'estoque',
            'mensagem': f"Há {len(produtos_criticos)} produtos com estoque crítico:",
            'produtos': produtos_criticos
        })
    
    return sugestoes

def formatar_sugestoes(sugestoes):
    """Formata as sugestões para exibição"""
    texto_sugestoes = []
    
    for sugestao in sugestoes:
        if sugestao['tipo'] == 'vendas':
            texto_sugestoes.append(f"📈 {sugestao['mensagem']}")
        
        elif sugestao['tipo'] == 'estoque':
            texto = f"⚠️ {sugestao['mensagem']}\n"
            for produto in sugestao['produtos']:
                texto += f"   • {produto['nome']}: {produto['quantidade']} unidades\n"
            texto_sugestoes.append(texto)
    
    return texto_sugestoes
