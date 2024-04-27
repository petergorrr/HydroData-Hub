import streamlit as st

# Set page configuration with the globe emoji as the page icon
st.set_page_config(
    page_title="HydroDataHub",  # Set a title for the web page
    page_icon="🌏",             # Set the emoji or path to an image file as the page icon
    layout="wide",              # Optional: Use the "wide" layout for the app, which uses the full screen width
    initial_sidebar_state="expanded"  # Optional: Expand the sidebar by default
)

# Define the member information with LinkedIn profiles
members = [
    {
        "name": "Tan Peng Teck",
        "major": "Artificial Intelligence",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Tan Peng Teck.jpg",
        "linkedin": "https://www.linkedin.com/in/peng-teck-tan-573a201b8/"
    },
    {
        "name": "Lim Heng Hoe",
        "major": "Artificial Intelligence",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Lim Heng Hoe.jpg",
        "linkedin": "https://www.linkedin.com/in/limhenghoe/"
    },
    {
        "name": "Agnes Saul",
        "major": "Marine Biology",
        "university": "University Malaysia Terengganu",
        "image": "images/Agnes Saul.jpg",
        "linkedin": "https://www.linkedin.com/in/agnes-saul/"
    },
    {
        "name": "Peggy Lee Pooi Qi",
        "major": "Marine Biology",
        "university": "University Malaysia Terengganu",
        "image": "images/Peggy Lee Pooi Qi.jpg",
        "linkedin": "https://www.linkedin.com/in/peggy-lee-47013422b/"
    }
]

# Enhanced CSS for overall modern styling
st.markdown("""
<style>
    /* Main page container */
    .main-container {
        background-color: #f0f2f6;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        font-family: 'Arial', sans-serif;
        color: #333;
        margin-bottom: 20px;
    }

    /* Headers and Titles */
    .header, .sub-header, h3 {
        text-align: center;
        color: #2a9d8f;
    }

    .header {
        margin-bottom: 20px;
    }

    .sub-header {
        color: #264653;
        font-size: 18px;
    }

    /* Content Sections */
    .content-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    .content-title {
        color: #e76f51;
        font-weight: bold;
    }

    .content-text {
        color: #666;
        line-height: 1.6;
    }

    /* Video description styling */
    .video-description {
        background-color: #f8f9fa;
        border-left: 5px solid #2a9d8f;
        padding: 15px;
        margin-top: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Profile styling */
    .member-info {
        background-color: #ffffff;
        margin: 10px 0px;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 16px;
    }
    .member-name {
        font-weight: bold;
        color: #2a9d8f;
    }
</style>
""", unsafe_allow_html=True)

# Centering the logo image using columns
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/app_logo.jpg", use_column_width=True)

# Main content within styled container
st.markdown("""
<div class="main-container">
    <h1 class="header">Welcome to HydroDataHub</h1>
    <h2 class="sub-header">The Future of Environmental Data Analysis and Management</h2>
    <div class="content-section">
        <h3 class="content-title">Landslide Risk Assessment System</h3>
        <p class="content-text">
            Our Landslide Risk Assessment System uses the concept of fuzzy logic to figure out the risk of landslides. It looks at many factors like how much rain there is, how wet the soil is, the shape of the land, and if landslides happened there before. It then gives each place a score to show how safe it is. You can also upload pictures of the site, and the system will check for safety measures like protective netting or anchoring in the soil. The final report breaks down all these details and shows a map that points out the risky areas. This helps people who plan cities, build things, or study the environment make good choices to keep everyone safe.
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
            Explore our systems and harness the power of data to take action towards a sustainable future.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.write("This application is for authorized use only.")
    st.markdown("Copyright © Make Water OK Malaysia")

# Add the Meet Our Team section with LinkedIn profiles in an expander
with st.expander("Meet Our Team", expanded=False):
    for member in members:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(member["image"], width=150)
        with col2:
            st.markdown(f"<p class='member-name'>{member['name']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Major:** {member['major']}")
            st.markdown(f"**University:** {member['university']}")
        with col3:
            # Add a clickable LinkedIn icon that leads to the member's LinkedIn profile
            st.markdown(f"[![LinkedIn](https://img.icons8.com/color/48/000000/linkedin.png)]({member['linkedin']})", unsafe_allow_html=True)
    st.image("images/group_photo.jpg", use_column_width=True)

# Nature Walk / Heritage Walk video
st.header("Nature Walk / Heritage Walk Trip")
st.markdown("""
<div class="video-description">
    <p>This video captures our nature walk and heritage walk at Penang Hill, highlighting our interactions with the environment and efforts to integrate these experiences into our project.</p>
</div>
""", unsafe_allow_html=True)
st.video('https://www.youtube.com/watch?v=uRb5tdTx1eE')

# Stakeholder Engagement Trip video
st.header("Stakeholder Engagement Trip at Penang Hill")
st.markdown("""
<div class="video-description">
    We also visited the Penang Hill Biosphere Reserve office and met with the personnel there to gain insights that would help improve our prototype.</p>
</div>
""", unsafe_allow_html=True)
st.video('https://www.youtube.com/watch?v=kGcKlLym9J0')
