# colors.py

import streamlit as st

def set_colors(primary_color='#4CAF50', secondary_color='#2196F3'):
    # Apply the colors to specific elements
    st.markdown(
        f"""
        <style>
        .primary-text {{
            color: {primary_color};
        }}
        .secondary-background {{
            background-color: {secondary_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
