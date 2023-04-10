import streamlit as st


class MyException(Exception):
    """Generic exception to handle program flow exits"""
    def __init__(self, message):
        self.message = message
        st.error(self.message)
