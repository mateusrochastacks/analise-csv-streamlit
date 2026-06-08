import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analisador de ID", layout="centered")

st.image("logo.png", width="stretch")

st.title("Sistema de Auditoria de IDs - BRASILCARD")

def tratar_df(arquivo, nome_csv):
    try:
        df = pd.read_csv(arquivo)

        # padroniza colunas
        df.columns = df.columns.str.strip().str.lower()

        # valida ID
        if 'id' not in df.columns:
            st.error(f"❌ O arquivo {nome_csv} não possui a coluna 'id'")
            st.stop()

        # padroniza valores
        df['id'] = df['id'].astype(str).str.strip().str.upper()

        return df

    except Exception as e:
        st.error(f"Erro ao processar {nome_csv}: {e}")
        st.stop()

# verificados de duplicatas 
st.header("🔍 Verificar duplicados em um CSV")

arquivo_unico = st.file_uploader("Envie um CSV", type=["csv"], key="single")

if arquivo_unico:
    df = tratar_df(arquivo_unico, "CSV único")

    st.subheader("Prévia")
    st.dataframe(df.head())

    duplicados = df[df.duplicated(subset=['id'], keep=False)]

    st.subheader("IDs duplicados (contagem)")
    st.write(duplicados['id'].value_counts())

    st.subheader("Linhas completas duplicadas")
    st.dataframe(duplicados.sort_values(by='id'))

    # download
    csv = duplicados.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Baixar relatório de duplicados",
        data=csv,
        file_name="duplicados.csv",
        mime="text/csv"
    )

st.header("🔄 Comparar dois CSVs")

arquivo1 = st.file_uploader("CSV 1", type=["csv"], key="csv1")
arquivo2 = st.file_uploader("CSV 2", type=["csv"], key="csv2")

if arquivo1 and arquivo2:
    df1 = tratar_df(arquivo1, "CSV 1")
    df2 = tratar_df(arquivo2, "CSV 2")

    st.subheader("Prévia CSV 1")
    st.dataframe(df1.head())

    st.subheader("Prévia CSV 2")
    st.dataframe(df2.head())

    # 🔹 IDs em comum
    comuns = set(df1['id']) & set(df2['id'])
    df_comuns = pd.DataFrame({'id': list(comuns)})

    st.subheader("IDs presentes nos dois arquivos")
    st.dataframe(df_comuns)

    # 🔹 linhas completas
    st.subheader("Linhas do CSV 1 com IDs em comum")
    st.dataframe(df1[df1['id'].isin(comuns)])

    st.subheader("Linhas do CSV 2 com IDs em comum")
    st.dataframe(df2[df2['id'].isin(comuns)])

    # 🔴 duplicados cruzados
    dup1 = set(df1[df1.duplicated(subset=['id'])]['id'])
    dup2 = set(df2[df2.duplicated(subset=['id'])]['id'])

    duplicados_cruzados = dup1 & dup2
    df_cruzado = pd.DataFrame({'id': list(duplicados_cruzados)})

    st.subheader("IDs duplicados em ambos os arquivos")
    st.dataframe(df_cruzado)

    # download comparação
    csv_comp = df_comuns.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Baixar IDs em comum",
        data=csv_comp,
        file_name="comparacao.csv",
        mime="text/csv"
    )