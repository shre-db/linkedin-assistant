import streamlit as st

def show_footer():
    st.markdown("---")
    st.markdown("Built with ❤️ for LearnTube.ai | [GitHub](https://github.com/shre-db/linkedin-genie)")

def get_mock_profile():
    return {
        "name": "Jane Doe",
        "about": "Aspiring data scientist with strong foundations in ML and Python.",
        "experience": [
            {"title": "Data Analyst", "company": "Acme Corp", "description": "Worked on dashboards and reporting."}
        ],
        "skills": ["Python", "SQL", "Data Visualization"]
    }
