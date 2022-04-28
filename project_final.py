import altair as alt
import streamlit as st
import pandas as pd 
import numpy as np
from PIL import Image
import plotly.express as px
from vega_datasets import data

@st.cache
def load():
    df = pd.read_excel('owid-co2-data.xlsx')
    result = pd.read_csv('merged.csv')
    return df, result
    
    


#st.title('Greenhouse Gas Emissions')
st.markdown("<h1 style='text-align: center; color: white;'>Greenhouse Gas Emissions</h1>", unsafe_allow_html=True)
st.sidebar.title("Selectors")
image = Image.open("dims.jpeg")


#loading countries
countries_map = alt.topo_feature(data.world_110m.url, 'countries')



#load data 
# df = pd.read_excel('owid-co2-data.xlsx')
# result = pd.read_csv('merged.csv')
df, result = load()
countries = df['country'].unique()



#Choose the type of visualization
visualization = st.sidebar.radio('Navigation', ('Home','Co2 World Distribution','Co2 Emission by year','Co2 vs Population Vs GDP', 'Distribution of emission sources'),index=0)

#drop down selection
country_selection = st.sidebar.selectbox(
    "Select Country",countries
)


max_year = max(df['year'])
min_year = min(df['year'])
years_range = df['year'].unique()

# year range selection
start_year, end_year = st.sidebar.select_slider(
     'Select a range Years for visulization',
     options=sorted(years_range),
     value=(min_year, max_year))





st.sidebar.write('Selected Year range is between', start_year, 'and', end_year)
st.sidebar.markdown("<i>Note: These filters does not apply for Co2 World Distribution</i>",unsafe_allow_html=True)


if visualization == 'Co2 vs Population Vs GDP':
    country_selected = df[(df['country']==country_selection )&(df['year']>=start_year)&(df['year']<=end_year)]

    #population vs co2
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Co2 vs Population and GDP<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>This graph tells us if there is drirect relationship between Co2 emissions and population growith, Co2 emission and GDP growth of a particular contry. </p>", unsafe_allow_html=True)
    
    
    source = country_selected
    source['year']=pd.to_datetime(source['year'], format='%Y')

    base = alt.Chart(source).encode(
        alt.X('year:T', axis=alt.Axis(title='Years'))
    )

    co2_grpah = base.mark_line().encode(
        alt.Y('co2',
              axis=alt.Axis(title='CO2 Emission', titleColor='#57A44C')),color=alt.value("#57A44C")
    )

    poppulation_graph = base.mark_line().encode(
        alt.Y('population',
              axis=alt.Axis(title='Population', titleColor='#5276A7')),color=alt.value("#5276A7")
    )


    graph1 = alt.layer(co2_grpah, poppulation_graph).resolve_scale(y = 'independent',color='independent').properties(
        width=400,
        height=400
    )
    #co2 vs GDP
    gdp = base.mark_line().encode(
        alt.Y('gdp',
              axis=alt.Axis(title='GDP', titleColor='#5276A7')),color=alt.value("#5276A7")
    )
    graph2 = alt.layer(co2_grpah, gdp).resolve_scale(y = 'independent',color='independent').properties(
        width=400,
        height=400
    )
    
    
    st.write(alt.hconcat(graph1,graph2))

elif visualization == 'Distribution of emission sources':
    country_selected = df[(df['country']==country_selection )&(df['year']>=start_year)&(df['year']<=end_year)]

    # distribution of sources
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Distribution of Co2 sources of emission<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>This graph indicates the various sources of Co2 emissions and tells us the percentage of contribution. This can help policymakers decide on which policy could drastically reduce Co2 emission based on source. </p>", unsafe_allow_html=True)

    value  = country_selected[['coal_co2', 'cement_co2', 'flaring_co2','gas_co2', 'oil_co2']].sum().values
    df_new =  pd.DataFrame({'Source':['Coal','Cement','Falring','Gas','Oil'],'Quantity':value})

    #Function to display the chart depending on the selection
    display = px.pie(df_new, values= 'Quantity', names= 'Source')
    st.plotly_chart(display)

    
    
elif visualization == 'Co2 Emission by year':
    
    country_selected = df[(df['country']==country_selection )&(df['year']>=start_year)&(df['year']<=end_year)]
    country_selected['year']=pd.to_datetime(country_selected['year'], format='%Y')
    
    #co2 yearly emission
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Co2 Emission over the years<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>This grpahs gives us an idea about how Co2 emission has increased through the years. This can be an indicator of how much Co2 emission would increase in the near future.  </p>", unsafe_allow_html=True)
    source = country_selected

    base = alt.Chart(source).encode(
        alt.X('year:T', axis=alt.Axis(title=None))
    )

    co2_grpah = base.mark_line().encode(
        alt.Y('co2',
              axis=alt.Axis(title='CO2 Emission', titleColor='#57A44C'))
    )
    
    co2_grpah_p = base.mark_point().encode(
        alt.Y('co2',
              axis=alt.Axis(title='CO2 Emission', titleColor='#57A44C'))
    )
    
    st.write(alt.layer(co2_grpah,co2_grpah_p).interactive().properties(width=700,height=500))
    
    
    
elif visualization == 'Home': 
    st.image(image, use_column_width=True)
    
    st.markdown("<br><p style='text-align: center; color: white;'>This Project Team 17 presenting on the final project for ITCS 4122/5122 - Telsi Tamuzi, Vishwath Kamalanathan, Divya Sri Sanaganapalli, Snigdha Bhagat </p>", unsafe_allow_html=True)
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> About<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Climate change is one of the biggest challenges faced by humans in the 21st century. Co2 plays an important role in the greenhouse effect and it is the primary gas emitted through human activities. The idea of this project is to visualize and better understand the greenhouse gas emissions over time by individual countries, enabling us to better design frameworks that could help contain the emissions.</p>", unsafe_allow_html=True)
    
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> About the data <p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>The data represents historical greenhouse gas emission values along with GDP and population growth from each country. The data set was taken from Global Carbonm Project which releases the data annually.</p>", unsafe_allow_html=True)
    
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Findings<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>The main takeaway is that there is a direct rel;ationship betwwen Population and GDP. China is the largest contributor for Co2 emissions whereas spain has the lowest Co2 emission. The visulaizations is tailored to understand individual contribution of each contry over the years. The dashboard could be leveraged by the policymakers to understand past patterns in order to contain future Co2 emissions. </p>", unsafe_allow_html=True)
    
else: 
    


    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Co2 Emission worldwide<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'> The visualization helps us understand the contribution of each country to Co2 emission over the years. <i>Note: You can select the type of chart i.e emission by each year and cummulative emission till the selected year.</p>", unsafe_allow_html=True)
    select = st.radio('Select the type of chart',('Emssions by each year','Cummulative emssions till the selected year'))
    var = 'co2'

    if select == 'Emssions by each year':
        var = 'co2'
    elif select == 'Cummulative emssions till the selected year':
        var = 'cumulative_co2'
    else:
        var = 'co2'

    #result.to_csv('./merged.csv', index = False)

    year = st.slider("Choose a year", min_value=min_year, max_value=max_year, step = 1)
    d = result[result['year'] == year]
    map1 = alt.Chart(countries_map).mark_geoshape(stroke = 'grey').encode(
        color  = f'{var}:Q',
        tooltip = ['country:N', f'{var}:Q']
    ).transform_lookup(
        lookup = 'id',
        from_ = alt.LookupData(d, 'id', [f'{var}', 'country'])
    ).project(
        type = 'equalEarth'
    ).properties(
        width = 700, height = 500
    )  
    #source = alt.topo_feature(data.world_110m.url, 'countries')

    base = alt.Chart(countries_map).mark_geoshape(
        fill='#666666',
        stroke='white'
    ).properties(
        width=700,
        height=500
    )
    a = base.project('equalEarth').properties(title='')
    st.write(a+map1)

    
    
    


