__module_name__ = "mock_profiles"


mock_linkedin_urls = {
    "johnsmith": "https://www.linkedin.com/in/johnsmith",
    "alicejohnson": "https://www.linkedin.com/in/alicejohnson",
    "boblee": "https://www.linkedin.com/in/boblee",
    "janedoe": "https://www.linkedin.com/in/janedoe"
}
    

profile_a = {
    "name": "John Smith",
    "about": "Experienced software engineer with a passion for AI and machine learning.",
    "experience": [
        {"title": "Software Engineer", "company": "Tech Innovations", "description": "Developed scalable applications."},
        {"title": "AI Research Intern", "company": "Future Tech Labs", "description": "Worked on NLP models."}
    ],
    "skills": ["Python", "Machine Learning", "Cloud Computing"]
}

profile_b = {
    "name": "Alice Johnson",
    "about": "Marketing specialist with expertise in digital campaigns and brand strategy.",
    "experience": [
        {"title": "Marketing Manager", "company": "Brand Builders", "description": "Led successful marketing campaigns."},
        {"title": "Content Strategist", "company": "Creative Minds", "description": "Developed content strategies for clients."}
    ],
    "skills": ["Digital Marketing", "SEO", "Content Creation"]
}

profile_c = {
    "name": "Bob Lee",
    "about": "Financial analyst with a strong background in data analysis and investment strategies.",
    "experience": [
        {"title": "Financial Analyst", "company": "Wealth Advisors", "description": "Analyzed market trends and investment opportunities."},
        {"title": "Junior Analyst", "company": "Finance Corp", "description": "Assisted in financial reporting and forecasting."}
    ],
    "skills": ["Financial Analysis", "Excel", "Data Visualization"]
}

profile_d = {
    "name": "Jane Doe",
    "about": "Aspiring data scientist with strong foundations in ML and Python.",
    "experience": [
        {"title": "Data Analyst", "company": "Acme Corp", "description": "Worked on dashboards and reporting."}
    ],
    "skills": ["Python", "SQL", "Data Visualization"]
}


def get_mock_profile(linkedin_url: str) -> dict:
    if "johnsmith" in linkedin_url:
        return profile_a
    elif "alicejohnson" in linkedin_url:
        return profile_b
    elif "boblee" in linkedin_url:
        return profile_c
    elif "janedoe" in linkedin_url:
        return profile_d
    else:
        return {
            "name": "Unknown User",
            "about": "No profile information available.",
            "experience": [],
            "skills": []
        }

