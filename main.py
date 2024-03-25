import streamlit as st
import plotly.express as px
from backend import get_data
import requests

# Add title, sub header, place, forecast days and data to view
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        # Get the Temperature / Sky data
        filtered_data = get_data(place, days)

        dates = [dict["dt_txt"] for dict in filtered_data]

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]

            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        elif option == "Sky":
            #  --- Solution 01
            # images_dict = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
            #                        "Rain": "images/rain.png", "Snow": "images/snow.png"}
            # sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            # image_paths = [images_dict[condition] for condition in sky_conditions]

            # st.image(image_paths, width=115)
            # st.write(dates)

            # --- Solution 02
            # images_dict = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
            #                        "Rain": "images/rain.png", "Snow": "images/snow.png"}
            # sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            # for index, condition in enumerate(sky_conditions):
            # image_path = images_dict[condition]
            # st.image(image_path, width=115, caption=dates[index])
            # st.write(condition)
            # st.write(dates[index])

            # --- Solution 03
            item_no = 0
            current_row = 0
            cols = st.columns(4)
            weather_dict = [dict["weather"][0] for dict in filtered_data]

            for index, weather_item in enumerate(weather_dict):
                if item_no == 4:
                    item_no = 0

                with cols[item_no]:
                    weather_icon = weather_item["icon"]
                    image = requests.get(f"http://openweathermap.org/img/wn/{weather_icon}@2x.png")
                    st.image(image.content, width=115, caption=dates[index])
                    st.write(weather_item["description"].title())
                    item_no = item_no + 1
    except KeyError:
        st.write("That place does not exist.")
