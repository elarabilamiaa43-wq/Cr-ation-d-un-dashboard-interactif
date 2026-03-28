import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données préparées
df = pd.read_csv("data_dashboard.csv")

#Donner titre pour dashboard
st.title("Dashboard des ventes")

#  Filtres interactifs
# filtre région
region = st.sidebar.multiselect(
    "Region",
    df["region"].unique(),
    default=df["region"].unique()
)
# filtre catégorie
category = st.sidebar.multiselect(
    "Category",
    df["category"].unique(),
    default=df["category"].unique()
)
# filtre année
year = st.sidebar.multiselect(
    "Year",
    df["annee"].unique(),
    default=df["annee"].unique()
)
###Appliquer les filtres au dataframe
df_filtered = df[
    (df["region"].isin(region)) &
    (df["category"].isin(category)) &
    (df["annee"].isin(year))
]


#  KPIs

total_sales = df_filtered["sales"].sum()
total_profit = df_filtered["marge"].sum()
avg_profit_margin = (df_filtered["marge"] / df_filtered["sales"]).mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", round(total_sales,2))
col2.metric("Total Profit", round(total_profit,2))
col3.metric("Profit Margin", f"{avg_profit_margin:.2%}")


#  Graphiques


#  Ventes par région (bar)
sales_region = df_filtered.groupby("region")["sales"].sum()
fig1, ax1 = plt.subplots()
sales_region.plot(kind="bar", color="#FFD3D3", ax=ax1)
ax1.set_title("Ventes par région")

st.pyplot(fig1)

#  Evolution des ventes dans le temps (line)
sales_time = df_filtered.groupby("annee")["sales"].sum()
fig2, ax2 = plt.subplots()
sales_time.plot(kind="line", color="#195C5C", ax=ax2)
ax2.set_title("Evolution des ventes")
st.pyplot(fig2)

#  Répartition des ventes par catégorie (pie)
# Calcul des ventes par catégorie
sales_category = df_filtered.groupby("category")["sales"].sum()

# Couleurs personnalisées pour chaque catégorie
colors = ["#99BEFF", "#66FFA8", "#99FF99", "#FFCC99", "#C2C2F0"]  

# Création du graphique
fig3, ax3 = plt.subplots()
sales_category.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax3,
    colors=colors,
    startangle=90,  # pour rotation initiale
    shadow=True     # optionnel
)

ax3.set_ylabel("")
ax3.set_title("Répartition des ventes par catégorie")
ax3.axis("equal")  # pour un cercle parfait

st.pyplot(fig3)

#  Top 10 produits (bar horizontal)
top_products = df_filtered.groupby("product_name")["sales"].sum().sort_values(ascending=True).tail(10)
fig4, ax4 = plt.subplots()
top_products.plot(kind="barh", color="#d3e3ff", ax=ax4)
ax4.set_title("Top 10 produits")
st.pyplot(fig4)

#  Heatmap Ventes par Région et Catégorie
pivot = df_filtered.pivot_table(index="region", columns="category", values="sales", aggfunc="sum")
fig5, ax5 = plt.subplots(figsize=(8,5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax5)
ax5.set_title("Ventes par Région et Catégorie")
st.pyplot(fig5)

#  Scatter Ventes vs Profit
fig6, ax6 = plt.subplots(figsize=(9,6))
sns.set(style="whitegrid")

sns.scatterplot(
    x="sales",
    y="marge",
    data=df_filtered,
    alpha=0.5,
    color="purple",
    ax=ax6
)

ax6.set_title("Ventes vs Profit", fontsize=16)
st.pyplot(fig6)

