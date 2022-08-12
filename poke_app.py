import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('pokemon.csv')
df = df[df.pokedex_number <= 150]
cols = ['pokedex_number', 'name', 'defense', 'experience_growth', 'height_m', 'hp', 
        'percentage_male','sp_attack', 'sp_defense', 'speed', 
        'type1', 'type2', 'weight_kg', 'generation', 'is_legendary']
df = df[cols]

header = st.container()


def get_data():
    cols = ['pokedex_number', 'name', 'attack', 'defense', 'experience_growth', 'height_m', 'hp', 
        'percentage_male','sp_attack', 'sp_defense', 'speed', 
        'type1', 'type2', 'weight_kg', 'generation', 'is_legendary']
    df = pd.read_csv('pokemon.csv')
    df = df[df.pokedex_number <= 150]
    df = df[cols]
    return df

source = get_data()

def get_chart(data):
    data = pd.DataFrame(data.type1.value_counts()).reset_index()
    bars = alt.Chart(data).mark_bar().encode(
        x='index',
        y='type1'
    )
    return bars

chart = get_chart(source)
col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    image = Image.open('./images/pokemon_logo.png')
    w = 300
    size = (w, w)
    image = image.resize(size)
    st.image(image, use_column_width=False)

with col3:
    st.write("")

#st.markdown("<h1 style='text-align: center; ;'>Pokedex</h1>", unsafe_allow_html=True)
st.subheader('Introducción')
st.markdown('Bienvenido a la visualización de los 150 pokemones de la primera temporada de Pokemon. Por si no lo sabías Pokemon fue una serie de anime estrenada el 1 de abril de 1997. La serie creaba una especie de animales que eran capaces de peliar unos con otros.')
st.subheader('Datos')
st.markdown('Este dataframe contiene las estadísticas y descriptores de todos los pokemones existentes. Para efectos de esta visualización se tomó únicamente a los 150 pokemones originales (primera temporada).')
st.markdown('Algunas variables son las siguientes:')
lst = ['Nombre pokemon ***(str)***', 'Número en la lista ***(int)***', 'Ataque ***(int)***', 'Defensa ***(int)***', 'velocidad ***(int)***', 'tipo ***(str)***']
s = ''
for i in lst:
    s += "- " + i + "\n"

st.markdown(s)
st.subheader('Descripción')
st.markdown('El público objetivo son personas que sean fanáticos tanto de la serie como de los juegos de pokemon. En el juego o en la serie los pokemones poseen estadísticas, las cuales determinan qué tan fuerte es un pokemon.')
st.markdown('Dado esto, la visualización permite observar los valores de las estadísticas y también comparar las estadísticas contra la **media** del **tipo** del pokemon. ')
st.markdown('Ejemplo: Si eliges a Bulbasaur verás sus estadísticas y como Bulbasaur es de tipo planta , comparará a Bulbasaur con la media de todos los tipo plantas.')
st.subheader('Visualicemos!')
st.markdown('Puedes **seleccionar** en el **dropdown de la izquierda** algun pokemon y visualizar sus estadísticas.')

with st.sidebar:
    st.title('Selecciona un Pokemon!')
    #st.checkbox("da", list(source.type1))
    pokemon = st.selectbox("", (source.name.unique()))
    cols_set = ['name', 'defense', 'attack', 'sp_attack', 'sp_defense', 'speed']
    pk = source[source.name == pokemon][cols_set]
    type = list(source[source.name == pokemon]['type1'])[0]
    pk = pk.melt(id_vars='name', var_name='stats', value_name='value_stats')
    pk = pk.sort_values(by='stats')

    over_all = source[source.type1 == type][cols_set]
    over_all = over_all.melt(id_vars='name', var_name='stats', value_name='value_stats').groupby('stats').mean().reset_index()
    over_all['value_stats'] = over_all.value_stats.astype(int)
    over_all = over_all.sort_values(by='stats')

st.markdown(f'Tu pokemón elegido es **{pokemon}** y es de tipo **{type}**.')
st.markdown(f'Ahora puedes visualizar las estadísticas de {pokemon} versus el promedio de las stats de todos los pokemon del tipo {type}. Con esto puedes saber qué tan buen pokemon es {pokemon} versus la media de los tipo {type}.')

col1, col2 = st.columns(2)

with col1:
    idx = source[source.name == pokemon]['pokedex_number'].values[0]
    image = Image.open(f'./images/{idx}.png')
    st.image(image, caption=pokemon)

with col2:

    #fig = px.line_polar(pk, r='value_stats', theta='stats', line_close=True)
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=pk.value_stats,
        theta=pk.stats,
        name=pokemon,
        fill='toself'
    ))
    fig.add_trace(go.Scatterpolar(
        r=over_all.value_stats,
        theta=over_all.stats,
        name=f'Promedio de los tipo: {type}',
        fill='toself',
        #color='green'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 200]
        )),
    showlegend=True
        )

#fig.show()
    st.plotly_chart(fig)