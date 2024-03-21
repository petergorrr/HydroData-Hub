import streamlit as st

# Using columns to center the logo image
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/app_logo.jpg", use_column_width="always")

# Define the HTML content with CSS embedded for styling
st.markdown("""
    <style>
        .main-container {
            background-color: lightblue;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        .header {
            color: #333;
            text-align: center;
            margin-bottom: 40px;
        }
        .sub-header {
            color: #555;
            text-align: center;
            margin-top: 0;
        }
        .content-section {
            margin-top: 20px;
        }
        .content-title {
            color: #2c3e50;
            font-weight: bold;
        }
        .content-text {
            color: #666;
            line-height: 1.6;
        }
        .mission-statement {
            margin-top: 40px;
            text-align: center;
        }
        .mission-statement h3 {
            color: #2c3e50;
            font-weight: bold;
        }
        .mission-statement p {
            color: #666;
            line-height: 1.6;
        }
    </style>
    <div class="main-container">
        <h1 class="header">Welcome to HydroDataHub</h1>
        <h2 class="sub-header">The Future of Environmental Data Analysis and Management</h2>
        <div class="content-section">
            <h3 class="content-title">Landslide Risk Assessment System</h3>
            <p class="content-text">
                Our Landslide Risk Assessment System utilizes AI and machine learning to predict landslide risks accurately. It provides dynamic risk maps, predictive alerts, and data-driven insights to help urban planners, researchers, and emergency response teams make informed decisions.
            </p>
        </div>
        <div class="content-section">
            <h3 class="content-title">Smart Water Meter System</h3>
            <p class="content-text">
                Our Smart Water Meter System leverages IoT-enabled meters and analytics for efficient water management. It features real-time usage monitoring, insights for water conservation, and customizable alerts to help utilities, managers, and households optimize water usage.
            </p>
        </div>
        <div class="mission-statement">
            <h3>Join Us in Our Mission</h3>
            <p>
                Explore our systems and harness the power of data to take action towards a sustainable future. Welcome to HydroDataHub.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.write("This application is for authorized use only.")
    st.markdown("Copyright © Make Water OK Malaysia")

# Define the member information
members = [
    {
        "name": "Tan Peng Teck",
        "major": "Artificial Intelligence",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Tan Peng Teck.jpg"
    },
    {
        "name": "Lim Heng Hoe",
        "major": "Artificial Intelligence",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Lim Heng Hoe.jpg"
    },
    {
        "name": "Agnes Saul",
        "major": "Marine Biology",
        "university": "University Terengganu Malaysia",
        "image": "images/Agnes Saul.jpg"
    },
    {
        "name": "Peggy Lee Pooi Qi",
        "major": "Marine Biology",
        "university": "University Terengganu Malaysia",
        "image": "images/Peggy Lee Pooi Qi.jpg"
    }
]

# Title of the group profile page
st.title("Meet Our Team")

# Styling for member profiles
st.markdown("""
<style>
.member-info {
    margin: 10px 0px;
    padding: 10px;
}
.member-name {
    font-weight: bold;
    color: #0078AA;
}
</style>
""", unsafe_allow_html=True)

# Create profile cards for each member
for member in members:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(member["image"], width=150)
    with col2:
        st.markdown(f"<div class='member-info'>", unsafe_allow_html=True)
        st.markdown(f"<p class='member-name'>{member['name']}</p>", unsafe_allow_html=True)
        st.markdown(f"**Major:** {member['major']}")
        st.markdown(f"**University:** {member['university']}")
        st.markdown("</div>", unsafe_allow_html=True)

# Description section
st.markdown("""
## Our Mission

In the wake of escalating environmental challenges, **HydroDataHub** emerges as a beacon of innovation and sustainability. Our dedicated team, comprised of experts in **Artificial Intelligence** and **Marine Biology**, is committed to leveraging cutting-edge technology to address critical water-related issues.

### Why We're Here

Our journey is fueled by a shared vision to make a meaningful impact on the world's water resources management practices. We understand the intricate balance of ecosystems and the pressing need for sustainable solutions. Through HydroDataHub, we aim to:

- **Empower Decision Making:** Provide actionable insights to policymakers, scientists, and communities.
- **Promote Conservation:** Utilize AI and data analytics to foster efficient water use and protect marine life.
- **Drive Innovation:** Challenge the status quo with breakthrough technologies and research.

Together, we are not just a team; we are pioneers on a mission to safeguard our planet's most precious resource. Join us as we embark on this vital journey towards a more sustainable and water-wise future.
""", unsafe_allow_html=True)
