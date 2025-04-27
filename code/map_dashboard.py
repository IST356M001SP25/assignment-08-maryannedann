import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd

# Syracuse coordinates and zoom settings
CENTER_COORDS = (43.0481, -76.1474)
DEFAULT_ZOOM = 14
AMOUNT_MIN = 1000
AMOUNT_MAX = 5000

df = pd.read_csv('./cache/top_locations_mappable.csv')

st.title('Parking Violations Heatmap - Syracuse')
st.caption('Mapped visualization of locations with $1,000+ in total fines.')

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

map_obj = folium.Map(location=CENTER_COORDS, zoom_start=DEFAULT_ZOOM)

gdf.explore(
    column='amount',
    cmap='magma',
    vmin=AMOUNT_MIN,
    vmax=AMOUNT_MAX,
    m=map_obj,
    legend=True,
    legend_kwds={'caption': 'Total Amount ($)'},
    marker_type="circle",
    marker_kwds={"radius": 10, "fill": True}
)

sf.folium_static(map_obj, width=800, height=600)
