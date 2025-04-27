import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

df = pd.read_csv('./cache/tickets_in_top_locations.csv')

st.title('Top Parking Ticket Locations in Syracuse')
st.caption('Displaying tickets issued at locations that generated $1,000 or more in total fines.')

locations = df['location'].unique()
selected_location = st.selectbox('Choose a location:', locations)

if selected_location:
    loc_data = df[df['location'] == selected_location]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total Tickets", value=loc_data.shape[0])
        fig, ax = plt.subplots()
        ax.set_title('Tickets by Hour')
        sns.barplot(data=loc_data, x='hourofday', y='count', estimator='sum', ax=ax)
        st.pyplot(fig)

    with col2:
        st.metric(label="Total Amount Collected", value=f"$ {loc_data['amount'].sum():,.2f}")
        fig2, ax2 = plt.subplots()
        ax2.set_title('Tickets by Day of Week')
        sns.barplot(data=loc_data, x='dayofweek', y='count', estimator='sum', ax=ax2)
        st.pyplot(fig2)

    st.map(loc_data[['lat', 'lon']])
