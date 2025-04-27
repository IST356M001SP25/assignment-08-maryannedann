import pandas as pd
import streamlit as st

def top_locations(df: pd.DataFrame, min_total: int = 1000) -> pd.DataFrame:
    summary = df.groupby('location', as_index=False)['amount'].sum()
    summary = summary.sort_values('amount', ascending=False)
    return summary[summary['amount'] >= min_total]

def top_locations_mappable(df: pd.DataFrame, min_total: int = 1000) -> pd.DataFrame:
    top_locs = top_locations(df, min_total)
    location_coords = df[['location', 'lat', 'lon']].drop_duplicates(subset=['location'])
    merged = pd.merge(top_locs, location_coords, on='location')
    return merged

def tickets_in_top_locations(df: pd.DataFrame, min_total: int = 1000) -> pd.DataFrame:
    top_locs = top_locations(df, min_total)
    return df[df['location'].isin(top_locs['location'])]

if __name__ == "__main__":
    st.title("Parking Violations ETL Process")
    st.caption("Extracting top violation locations in Syracuse...")
    
    st.write("Loading data...")
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    st.success("Data loaded successfully.")

    st.write("Processing top locations...")
    top_locations_df = top_locations(violations_df)
    top_locations_df.to_csv('./cache/top_locations.csv', index=False)
    st.success("Top locations written to ./cache/top_locations.csv")

    st.write("Processing mappable top locations...")
    mappable_locations_df = top_locations_mappable(violations_df)
    mappable_locations_df.to_csv('./cache/top_locations_mappable.csv', index=False)
    st.success("Mappable locations written to ./cache/top_locations_mappable.csv")

    st.write("Processing tickets issued at top locations...")
    tickets_top_locations_df = tickets_in_top_locations(violations_df)
    tickets_top_locations_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)
    st.success("Tickets for top locations written to ./cache/tickets_in_top_locations.csv")
