import streamlit as st

def app():
    st.title('Data Filter')

    if st.session_state['dataframe'] is not None:
        df = st.session_state['dataframe']
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select column to filter", columns)
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox("Select value to filter", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)
    else:
        st.write("No data uploaded yet. Please upload data on the Data Uploader page.")