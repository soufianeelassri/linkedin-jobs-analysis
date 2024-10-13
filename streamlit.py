import streamlit as st
import mysql.connector  # To connect to your MySQL database
import pandas as pd
import plotly.express as px  # Import Plotly for dynamic plotting


def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aaaa',
        database='jobs'
    )
    return conn

# Define a function to fetch unique values from a table
def fetch_unique_countries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT country_name FROM Country")
    countries = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return countries

# Fetch unique contract types based on selected country
def fetch_unique_contract_types(selected_country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT ct.contract_type 
        FROM ContractTypes ct
        JOIN Jobs j ON j.contract_type_id = ct.contract_type_id
        JOIN Country c ON j.country_id = c.country_id
        WHERE c.country_name = %s
    """, (selected_country,))
    contract_types = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return contract_types

# Fetch unique experience levels based on selected country
def fetch_unique_experience_levels(selected_country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT el.experience_level 
        FROM ExperienceLevels el
        JOIN Jobs j ON j.experience_level_id = el.experience_level_id
        JOIN Country c ON j.country_id = c.country_id
        WHERE c.country_name = %s
    """, (selected_country,))
    experience_levels = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return experience_levels

# Fetch unique titles based on selected country
def fetch_unique_titles(selected_country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT t.title 
        FROM Titles t
        JOIN Jobs j ON j.title_id = t.title_id
        JOIN Country c ON j.country_id = c.country_id
        WHERE c.country_name = %s
    """, (selected_country,))
    titles = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return titles


def fetch_top_skills(selected_title,):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Query to get top 5 skills for the selected title
    query = """
        SELECT count(j.skill_id), s.skill FROM jobs j, titles t, skills s
        WHERE j.skill_id = s.skill_id AND t.title = %s AND j.title_id = t.title_id
        GROUP BY s.skill
        ORDER BY count(j.skill_id) DESC
        LIMIT 5;
    """
    cursor.execute(query, (selected_title,))
    results = cursor.fetchall()
    connection.close()
    
    # Return the results as a pandas DataFrame
    return pd.DataFrame(results, columns=['Skill', 'Count'])

# Configure sidebar to have a red background
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: red;
    }
    .centered-title {
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        margin-top: -85px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="centered-title">Linkedin Jobs Dashboard (DATA & SECURITY)</h1>', unsafe_allow_html=True)

# Sidebar Title
st.sidebar.title("Filters")

selected_country = st.sidebar.selectbox(
        "Select a country", fetch_unique_countries()
)

selected_contract_type = st.sidebar.selectbox(
    "Select a Contract Type", fetch_unique_contract_types(selected_country)
)

selected_experience_level = st.sidebar.selectbox(
    "Select an Experience Level", fetch_unique_experience_levels(selected_country)
)

selected_title = st.sidebar.selectbox(
    "Select a Title", fetch_unique_titles(selected_country)
)
if selected_title:
    st.subheader(f"Top 5 Skills for {selected_title}")

    # Fetch top skills
    top_skills_df = fetch_top_skills(selected_title)

    if not top_skills_df.empty:
        # Plotting the top 5 skills using Plotly
        fig = px.bar(top_skills_df, 
                     x='Skill', 
                     y='Count', 
                     color='Count', 
                     title=f'Top 5 Skills for {selected_title}', 
                     labels={'Number of Skills': 'Count', 'Skill': 'Skills'},
                     color_continuous_scale=px.colors.sequential.Oranges)

        st.plotly_chart(fig)  # Display the Plotly plot in Streamlit
    else:
        st.write("No skills found for this job title.")
