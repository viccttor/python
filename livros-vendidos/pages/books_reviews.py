import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Reviews", page_icon="📚", layout="wide")

# Carregamento dos dados
df_reviews = pd.read_csv('./datasets/customer reviews.csv')
df_top100_books = pd.read_csv('./datasets/Top-100 Trending Books.csv')

# Padroniza nome de coluna para fazer join mais simples
df_reviews = df_reviews.rename(columns={'book name': 'book title'})

# Lista de livros para seleção
books = df_top100_books['book title'].unique()
book = st.sidebar.selectbox('📖 Selecione um livro', sorted(books))

# Filtra dados do livro e review
df_book = df_top100_books[df_top100_books['book title'] == book]
df_reviews_f = df_reviews[df_reviews['book title'] == book]

st.write("Colunas disponíveis nas avaliações:", df_reviews_f.columns.tolist())

if not df_book.empty:
    book_info = df_book.iloc[0]

    # Cabeçalho com informações
    st.markdown(f"""
    ## {book_info['book title']}
    **Autor:** {book_info['author']}  
    **Gênero:** {book_info['genre']}  
    **Ano de Publicação:** {book_info['year of publication']}  
    """)

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Preço", f"R$ {book_info['book price']:.2f}")
    col2.metric("⭐ Rating", book_info['rating'])
    col3.metric("📅 Ano", int(book_info['year of publication']))
    col4.metric("💬 Avaliações", df_reviews_f.shape[0])

    st.divider()

    # Gráfico de distribuição de avaliações
    if not df_reviews_f.empty and 'rating' in df_reviews_f.columns:
        fig = px.histogram(df_reviews_f, x='rating', nbins=5,
                           title='Distribuição de Avaliações',
                           labels={'rating': 'Nota'})
        fig.update_layout(template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

    # Avaliações dos usuários
    st.subheader("🗣 Avaliações dos Leitores")

    if df_reviews_f.empty:
        st.info("Este livro ainda não possui avaliações.")
    else:
        for _, row in df_reviews_f.iterrows():
            with st.expander(f"{row['review title']} - por {row['reviewer']}"):
                st.write(row['review description'])
else:
    st.warning("Livro não encontrado nos dados.")