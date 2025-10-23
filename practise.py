import streamlit as st

st.title("Chai making app")

col1 , col2, col3 = st.columns(3)

with col1:
    st.write("Vote for Adrak Chai")
    vote1 = st.button("Adrak Chai")
    
with col2:
    st.write("Vote for Masala Chai")
    vote2 = st.button("Masala Chai")
    
with col3:
    st.write("Vote for Elaichi Chai")
    vote3 = st.button("Elaichi Chai")
    
if vote1:
    st.success("Your Adrak chai is on way")
elif vote2:
    st.success("Your Masala chai is on way")
elif vote3:
    st.success("Your Elaichi chai is on way")
    
st.sidebar.text_input("Enter you name: ")
st.sidebar.selectbox("Enter you chai type: ",['Adrak', 'masala', 'elaichi'])
