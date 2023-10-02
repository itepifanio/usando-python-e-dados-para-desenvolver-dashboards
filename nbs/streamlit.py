import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_pie_chart(data):
    contagem_descricao = data['descricao'].value_counts()
    porcentagens = (contagem_descricao / contagem_descricao.sum()) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(porcentagens, labels=porcentagens.index, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
    ax.axis('equal')

    for text, autotext in zip(texts, autotexts):
        text.set(size=10)
        autotext.set(size=10)

    legend_labels = [f"{label}: {value}" for label, value in zip(contagem_descricao.index, contagem_descricao.values)]
    ax.legend(wedges, legend_labels, title="Descrições", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    st.pyplot(fig)

df = pd.read_csv('turma_matricula_docente_filtrados.csv')

st.title("Taxa de Aprovação por Curso, Componente e Docente")

# Dropdowns
unidade_selecionada = st.selectbox(
    'Selecione o Curso:',
    df[['unidade_responsavel', 'unidade_responsavel']].drop_duplicates().values.tolist(),
    format_func=lambda x: x[0]
)

df_unidade = df[df['unidade_responsavel'] == unidade_selecionada[1]]

componente_selecionado = st.selectbox(
    'Selecione o Componente Curricular:',
    df_unidade[['nome_x', 'id_componente']].drop_duplicates().values.tolist(),
    format_func=lambda x: x[0]
)

df_componente = df_unidade[df_unidade['id_componente'] == componente_selecionado[1]]

docente_selecionado = st.selectbox(
    'Selecione o Docente:',
    df_componente[['nome_y', 'siape']].drop_duplicates().values.tolist(),
    format_func=lambda x: x[0]
)

if unidade_selecionada and componente_selecionado and docente_selecionado:
    # Filtra o dataframe com base nas seleções
    df_filtrado = df[(df['unidade_responsavel'] == unidade_selecionada[1]) & 
                    (df['id_componente'] == componente_selecionado[1]) &
                    (df['siape'] == docente_selecionado[1])]
    
    df_filtrado = df_componente.drop_duplicates(subset='discente')

    plot_pie_chart(df_filtrado)