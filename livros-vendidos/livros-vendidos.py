import streamlit as st
import pandas as pd
import plotly.express as px  

st.set_page_config(page_title="Livros Vendidos", page_icon="📚", layout="wide")

# Carregamento dos dados
df_reviews = pd.read_csv('./datasets/customer reviews.csv')
df_top100_books = pd.read_csv('./datasets/Top-100 Trending Books.csv')

#Data frame com as colunas 
df_books = df_top100_books[['book title', 'author', 'book price', 'rating', 'genre', 'year of publication']].copy()

# Filtro por faixa de preço
price_max = df_top100_books['book price'].max()
price_min = df_top100_books['book price'].min()   
price_range  = st.sidebar.slider('Preço', price_min, price_max, (price_min, price_max))
df_books = df_books[df_books['book price'].between(price_range[0], price_range[1])]

# Renomear colunas para exibição
df_books_display = df_books.rename(columns={
    'book title': 'Título',
    'author': 'Autor',
    'book price': 'Preço',
    'rating': 'Avaliação',
    'genre': 'Gênero',
    'year of publication': 'Ano'
})

# Gráfico por ano de publicação
year_counts1 = df_books["year of publication"].value_counts().reset_index()
year_counts1.columns = ['Ano de Publicação', 'Quantidade']
year_counts1 = year_counts1.sort_values('Ano de Publicação')
fig = px.bar(year_counts1, x='Ano de Publicação', y='Quantidade', title='Quantidade de Livros por Ano')
fig.update_layout(template='plotly_white')

# Gráfico por preço
year_counts2 = df_books["book price"].value_counts().reset_index()
year_counts2.columns = ['Preço', 'Quantidade']
year_counts2 = year_counts2.sort_values('Preço')
fig2 = px.bar(year_counts2, x='Preço', y='Quantidade', title='Quantidade de Livros por Preço')
fig2.update_layout(template='plotly_white')

# Exibição lado a lado
col1, col2 = st.columns(2)
with col1:
    st.header("Livros mais vendidos por Ano")
    st.dataframe(df_books_display.head(10))
    col1.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Livros mais vendidos por Preço")
    st.dataframe(df_books_display.sort_values('Preço', ascending=False).head(10))
    col2.plotly_chart(fig2, use_container_width=True)

#df_reviews
df_books