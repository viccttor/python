import streamlit as st
import pandas as pd

st.set_page_config(page_title="Livros Vendidos", page_icon="📚", layout="wide")

df_reviews = pd.read_csv('./datasets/customer reviews.csv')
df_top100_books = pd.read_csv('./datasets/Top-100 Trending Books.csv')


df_reviews
