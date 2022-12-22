

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
import plotly.express as px
from streamlit_player import st_player
from streamlit_plotly_events import plotly_events

#make wide layout
st.set_page_config(layout="wide")

data = pd.read_csv("1998_final_dataset.csv")
df = pd.DataFrame(data)
df = df.drop("Unnamed: 0",axis=1)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False)
# .encode('utf-8')

#definition of the interactive plot
def interactive_plot(dataframe):
    #make a dropdown menu for the x and y axis
    x_axis_value =  st.selectbox('Select x-axis', options = dataframe.columns, index= 7)
    y_axis_value =  st.selectbox('Select y-axis', options = dataframe.columns, index= 40)
    
    plot= px.scatter(dataframe, x=x_axis_value, y=y_axis_value)
    #st.plotly_chart(plot, use_container_width=True)
    
        # Writes a component similar to st.write()
    #use plotly_events to create an event if a datapoint is clicked
    selected_points = plotly_events(plot, click_event=True, hover_event=False)
    #print selected points
    if not selected_points == []:
        #print pointIndex of selected_points
        id = selected_points[0]['pointIndex']
        
        #locate the id inside the dataframe and print the row
        st.write('Clicked Datapoint:')
        st.write(df.iloc[id])


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridoptions = gb.build()

response = AgGrid(
    df,
    height=200,
    gridOptions=gridoptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
    header_checkbox_selection_filtered_only=True,
    use_checkbox=True)

# st.write(type(response))
# st.write(response.keys())
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')  

v = response['selected_rows'] 
# print(v)
for entry in v:
    
   #  st.write(entry['participant_id'])
   # print(entry['participant_id'])
   #  data = [[entry['participant_id'],entry['demo_age']]]
   #  df2 = pd.DataFrame(data, columns=['Numbers',"demo"])




    # df2 = pd.DataFrame().assign(Courses=entry['participant_id'], Duration=entry['participant_id'])

    
    
    col1, col2, col3 = st.columns(3)

    # data = df[["demo_sex","demo_age"]].values
    # df2 = pd.DataFrame(data, columns=['Gender','Age'])
    # st.table(df2)
    

    with col1:
        st.write("- Age:",entry["demo_age"])
        st.write("- Gender:",entry["demo_sex"])
        st.write("- Ethnicity:",entry["demo_ethnicity"])
        st.write("- Status:",entry["demo_status"])
        st.write("- Education level:",entry["demo_education"])
        st.write("- Employment status:",entry["demo_employment"])
        st.write("- Video URL:",entry["video_link"])
        
    with col2:
        interactive_plot(data)

        # s = df["demo_age"]
        # p = s.plot(kind='hist', bins=100, color='orange')

        # bar_value_to_label = entry["demo_age"]
        # # print(entry["demo_age"],'-----')
        # min_distance = float("inf")  # initialize min_distance with infinity
        # index_of_bar_to_label = 0
        # for i, rectangle in enumerate(p.patches):  # iterate over every bar
        #     tmp = abs(  # tmp = distance from middle of the bar to bar_value_to_label
        #         (rectangle.get_x() +
        #             (rectangle.get_width() * (1 / 2))) - bar_value_to_label)
        #     if tmp < min_distance:  # we are searching for the bar with x cordinate
        #                             # closest to bar_value_to_label
        #         min_distance = tmp
        #         index_of_bar_to_label = i
        # p.patches[index_of_bar_to_label].set_color('r')

        # st.pyplot(plt)






    with col3:
        #extract id from phonic url
        entry_session_ID = entry.copy()
        splitted_URL = entry_session_ID['video_link'].split("/")
        entry_session_ID['session_ID'] = splitted_URL[4]

        
                
        #find video location based on the session ID
        video_location = './data/Videos_compressed_15fps/' + entry_session_ID['session_ID'] + '-0.m4v'


        st.video(video_location)
      

        #attempt to embed video directly from web(unsuccesful)
        #     #entry_session_ID['session_ID']
        #     video_direct_link = ("https://survey-audio.s3.amazonaws.com/surveys/6149002a446a704c03e00648/quesitons/614a4caa306e9a0ecd47b861/responses/" + entry_session_ID['session_ID'] + "/response_video.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAX3R45OUYDGGR4EY7%2F20221222%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Date=20221222T091040Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=9b5c6a39223f93cb2e00949c7e120bc31a951225e7dd9a3a82e58b893ddebbe0")
        #     st_player(video_direct_link)
            

                
if v:

    # for entry in v:
      # print(entry['participant_id'])
      
      
      

    # st.dataframe(v)
    # st.write(v)
    #for i in range(v[0]):
    #    print(i)
    # for i in range(2):
    #    st.write(v[0]["participant_id"])

    dfs = pd.DataFrame(v)
    csv = convert_df(dfs)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='selected.csv',
        mime='text/csv',
    )