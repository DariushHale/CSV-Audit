import pandas as pd
import streamlit as st

@st.cache
def read_files(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)

bar = st.sidebar

with st.sidebar:

    with st.form('c'):

        uploaded_file = st.file_uploader("Choose a file")

        done = st.form_submit_button('Upload File')

        if done:
            st.write('Start Audit')

    if 'Upload File' not in st.session_state:
        df = read_files(uploaded_file)
        df1 = df.copy()
        df1['OK?']=0


with st.container():
    for n, row in df.iterrows():

        st.write(f"Attribute: {row['MAPPED_ATTRIBUTE']}")
        st.write(f"")

        col1,col2 = st.columns(2)
        with col1:
            st.image(row['IMAGE_1'])

        with col2:
            # choice = st.radio(f"{n+1}.- Is this a {row['MAPPED_VALUE']} {row['MAPPED_ATTRIBUTE']}?",['Yes','No'])
            st.write(f"{n+1}.- Is this {row['MAPPED_VALUE']}?")
            yes = st.checkbox(f'{n}.- Yes')
            no  = st.checkbox(f'{n}.- No')

            if yes: df1.loc[n,'OK?'] = 1
            if no: df1.loc[n,'OK?'] = 0

# st.sidebar.write(f'Quality: {(df1["OK?"].sum()/len(df1))*100}')
st.sidebar.write('Status:')
st.sidebar.write(f'General quality: {(df1["OK?"].sum()/len(df1))*100}%')
st.sidebar.dataframe(pd.DataFrame(df1.groupby(['MAPPED_ATTRIBUTE','MAPPED_VALUE'])['OK?'].agg(lambda x: x.sum()/len(x))))


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df1)

st.sidebar.download_button(
   "Press to Download the CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

        


