import altair as alt
import streamlit as st
import pandas as pd 
import numpy as np
from PIL import Image
import plotly.express as px
from vega_datasets import data
#@st.cache

#st.title('Greenhouse Gas Emissions')
st.markdown("<h1 style='text-align: center; color: white;'>Greenhouse Gas Emissions</h1>", unsafe_allow_html=True)
st.sidebar.title("Selectors")
image = Image.open("dims.jpeg")


#loading countries
countries_map = alt.topo_feature(data.world_110m.url, 'countries')

#data loading
df_m = pd.read_csv('co2.csv')
country_codes = pd.read_csv("codes.csv")

#preprocessing

df_m = df_m.drop(columns = [ 'consumption_co2',
       'co2_growth_prct', 'co2_growth_abs', 'trade_co2', 'co2_per_capita',
       'consumption_co2_per_capita', 'share_global_co2', 
       'share_global_cumulative_co2', 'co2_per_gdp', 'consumption_co2_per_gdp',
       'co2_per_unit_energy', 'coal_co2', 'cement_co2', 'flaring_co2',
       'gas_co2', 'oil_co2', 'other_industry_co2', 'cement_co2_per_capita',
       'coal_co2_per_capita', 'flaring_co2_per_capita', 'gas_co2_per_capita',
       'oil_co2_per_capita', 'other_co2_per_capita', 'trade_co2_share',
       'share_global_cement_co2', 'share_global_coal_co2',
       'share_global_flaring_co2', 'share_global_gas_co2',
       'share_global_oil_co2', 'share_global_other_co2',
       'cumulative_cement_co2', 'cumulative_coal_co2',
       'cumulative_flaring_co2', 'cumulative_gas_co2', 'cumulative_oil_co2',
       'cumulative_other_co2', 'share_global_cumulative_cement_co2',
       'share_global_cumulative_coal_co2',
       'share_global_cumulative_flaring_co2',
       'share_global_cumulative_gas_co2', 'share_global_cumulative_oil_co2',
       'share_global_cumulative_other_co2', 'total_ghg', 'ghg_per_capita',
       'methane', 'methane_per_capita', 'nitrous_oxide',
       'nitrous_oxide_per_capita', 'population', 'gdp',
       'primary_energy_consumption', 'energy_per_capita', 'energy_per_gdp'])

country_codes = country_codes.drop(columns = ['name'])
country_codes.rename(columns={'alpha-3': 'alpha_3', 'country-code': 'id'}, inplace=True)
df_m = df_m.dropna(subset = ['iso_code'])
df_m['iso_code'] = df_m['iso_code'].astype(str)
df_m['iso_code'] = df_m['iso_code'].str.strip()
country_codes['alpha_3'] = country_codes['alpha_3'].astype(str)
country_codes['alpha_3'] = country_codes['alpha_3'].str.strip()
country_codes['id'] = country_codes['id'].astype(str)
country_codes['id'] = country_codes['id'].str.strip()

#merge two tables
result = pd.merge(df_m, country_codes, how="outer", left_on = "iso_code", right_on = 'alpha_3')
result = result.dropna(subset = ['iso_code'])
result = result.dropna(subset = ['alpha_3'])




#load data 
df = pd.read_excel('owid-co2-data.xlsx')

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



country_selected = df[(df['country']==country_selection )&(df['year']>=start_year)&(df['year']<=end_year)]


st.sidebar.write('Selected Year range is between', start_year, 'and', end_year)
st.sidebar.markdown("<i>Note: These filters does not apply for Co2 World Distribution</i>",unsafe_allow_html=True)


if visualization == 'Co2 vs Population Vs GDP':
    #population vs co2
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Co2 vs Population and GDP<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>This graph tells us if there is drirect relationship between Co2 emissions and population growith, Co2 emission and GDP growth of a particular contry. </p>", unsafe_allow_html=True)
    
    
    source = country_selected

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
    # distribution of sources
    st.markdown("<b><p style='text-align: center; color: white;font-size:150%;'> Distribution of Co2 sources of emission<p></b>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>This graph indicates the various sources of Co2 emissions and tells us the percentage of contribution. This can help policymakers decide on which policy could drastically reduce Co2 emission based on source. </p>", unsafe_allow_html=True)

    value  = country_selected[['coal_co2', 'cement_co2', 'flaring_co2','gas_co2', 'oil_co2']].sum().values
    df_new =  pd.DataFrame({'Source':['Coal','Cement','Falring','Gas','Oil'],'Quantity':value})

    #Function to display the chart depending on the selection
    display = px.pie(df_new, values= 'Quantity', names= 'Source')
    st.plotly_chart(display)

    
    
elif visualization == 'Co2 Emission by year':
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
    source = alt.topo_feature(data.world_110m.url, 'countries')

    base = alt.Chart(source).mark_geoshape(
        fill='#666666',
        stroke='white'
    ).properties(
        width=700,
        height=500
    )
    a = base.project('equalEarth').properties(title='')
    st.write(a+map1)

    
    
    


