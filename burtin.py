import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("burtin.csv")

# Sidebar filters
genus_filter = st.sidebar.multiselect("Select Genus:", options=df["Genus"].unique(), default=df["Genus"].unique())
gram_filter = st.sidebar.multiselect("Gram Staining:", options=df["Gram_Staining"].unique(), default=df["Gram_Staining"].unique())

filtered_df = df[(df["Genus"].isin(genus_filter)) & (df["Gram_Staining"].isin(gram_filter))]

# Chart 1: Penicillin effectiveness
pen_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('Bacteria:N', sort='-y', title='Bacteria'),
    y=alt.Y('Penicillin:Q', title='Penicillin MIC (μg/mL)'),
    color='Genus:N',
    tooltip=['Bacteria', 'Penicillin', 'Genus']
).properties(title="Penicillin Effectiveness")

# Chart 2: Streptomycin vs Neomycin Scatter
scatter = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x='Streptomycin:Q',
    y='Neomycin:Q',
    color='Gram_Staining:N',
    tooltip=['Bacteria', 'Streptomycin', 'Neomycin']
).properties(title="Streptomycin vs Neomycin Resistance")

# Chart 3: Faceted Bar Charts per Antibiotic
melted = pd.melt(filtered_df, id_vars=['Bacteria', 'Genus'], value_vars=['Penicillin', 'Streptomycin', 'Neomycin'], var_name='Antibiotic', value_name='MIC')
facet_chart = alt.Chart(melted).mark_bar().encode(
    x='Bacteria:N',
    y='MIC:Q',
    color='Genus:N',
    column='Antibiotic:N',
    tooltip=['Bacteria', 'Antibiotic', 'MIC']
).properties(title="MIC by Antibiotic").configure_axis(labelAngle=45)

# Layout
st.title("Antibiotic Resistance Dashboard")
st.altair_chart(pen_chart, use_container_width=True)
st.altair_chart(scatter, use_container_width=True)
st.altair_chart(facet_chart, use_container_width=True)
