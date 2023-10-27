# HSL Bike Planner

This repository contains all the code and data for the HSL Bike Planner: a tool for planning bike trips in Helsinki. This project is a part of the course "Introduction to Data Science" at the University of Helsinki.

In this project, we wanted to help Helsinki city bike users plan their trips. Our machine learning model predicts the busyness of each bike station in the Helsinki/Espoo region for the upcoming 5 days, by using weather data as well as historical bike usage data for each station. The model is then used to create a map that shows the predicted busyness of each station for the next 5 days. The user can then use this map to plan their bike trips accordingly.

This repository contains the following sections:
1. data - contains all the data used in the project, including weather data and HSL bike usage data. Also includes finalized data used in the machine learning model, as well as the predictions made by the model.
2. notebooks - contains the notebooks that were used for data collection and cleaning, as well as the notebook used for visualizing the data.
3. src - contains the code for the machine learning model and its predictions, as well as the code for the creation of the map for our website.
4. The code for the website.
5. The final HSL bike planner report.

Below we have the link to our website, where you will find an interactive map of the Helsinki/Espoo region. The map contains a pin for each HSL bike station, where, by clicking on a pin, will show the predicted busyness of the station for the next 5 days.

Link to website: https://jessehantula.github.io/data_science_project.github.io/
*Disclaimer: This website can be used only during the city bike season from April to October, and exceptionally during November 2023 for course grading purposes.*
