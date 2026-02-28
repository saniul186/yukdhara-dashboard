st.divider()
st.subheader("District-wise Progress Map")

fig_map = px.choropleth(
    data_frame=data,
    geojson=geojson_data,
    featureidkey="properties.District",
    locations="District",
    color="Category",
    color_discrete_map={
        "100%": "#2ca02c",      # Green
        "85-99%": "#ffd700",    # Yellow
        "50-84%": "#ff9800",    # Orange
        "<50%": "#d62728"       # Red
    }
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(
    fig_map,
    use_container_width=True,
    config={
        "scrollZoom": False,
        "displayModeBar": False
    }
)
