import streamlit as st
import requests
import pandas as pd

# TODO: Move API functions to another file
@st.cache
def get_data():
    return pd.read_json('http://0.0.0.0:8000/data')

@st.cache
def get_aggregate_data(field):
    return pd.read_json(f'http://0.0.0.0:8000/aggregate?field={field}')

@st.cache
def get_by_field(field, value):
    data = requests.get(f'http://0.0.0.0:8000/by_field?field={field}&name={value}').json()
    return pd.DataFrame(data)

# -------------------- Main Streamlit page -------------------------------

def main():
    header = st.container()
    dataset = st.container()
    model = st.container()

    with header:
        st.title('Migration data for Barcelona city')
        st.text('Dashboard showing data exploring migratory tendencies in the city of Barcelona')

    with dataset:
        st.header('Raw dataset')
        data_load_state = st.text("Loading")
        bcn_data = get_data()
        data_load_state.text("Done! (using st.cache)")
        st.write(bcn_data)

        st.subheader('Total inmigration in the last 3 years')
        yearly = bcn_data.groupby('Year').agg({ 'Number': sum })
        st.line_chart(yearly)

    
    with model:
        st.subheader('Visualize inmigrants by:')
        filter = st.radio('Geographical unit', ['District','Neighborhood'])

        # Load data from API
        agg_data = get_aggregate_data(filter).sort_values(by='total',ascending=False)

        # Setup filters 
        agg_data_max = int(agg_data.max()['total'])
        max_limit = st.slider('Min migrant limit to visualize', min_value=500, max_value=agg_data_max, step=1000, value=500)
        agg_filtered = agg_data[agg_data.total-1 >= max_limit]

        # Plot chart
        st.bar_chart(pd.DataFrame(agg_filtered.rename(columns={ '_id': 'index' })))
        
        # Setup user input/filters
        nationalities = bcn_data['Nationality'].unique()
        selected_nat = st.selectbox('Select Nationality', nationalities)

        # Load data from API
        country_raw = get_by_field('Nationality',selected_nat)

        #Set filters
        country_data = country_raw.groupby(filter).agg({ 'Number': sum })
        country_max = int(country_data.max()['Number'])
        max_limit_country = st.slider('Min migrant limit to visualize', min_value=10, max_value=country_max, step=10, value=10)
        country = country_data[country_data.Number-1 >= max_limit_country]

        # Plot chart
        st.bar_chart(country)

if __name__ == '__main__':
    main()