import streamlit as st
import os

# Set page configuration with the globe emoji as the page icon
st.set_page_config(
    page_title="HydroDataHub",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the member information with LinkedIn profiles
members = [
    {
        "name": "Tan Peng Teck",
        "major": "Artificial Intelligence 🤖",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Tan Peng Teck.jpg",
        "linkedin": "https://www.linkedin.com/in/peng-teck-tan-573a201b8/"
    },
    {
        "name": "Lim Heng Hoe",
        "major": "Artificial Intelligence 🤖 / Psychology 💭",
        "university": "Asia Pacific University of Technology and Innovation",
        "image": "images/Lim Heng Hoe.jpg",
        "linkedin": "https://www.linkedin.com/in/limhenghoe/"
    },
    {
        "name": "Agnes Saul",
        "major": "Marine Biology 🐚",
        "university": "University Malaysia Terengganu",
        "image": "images/Agnes Saul.jpg",
        "linkedin": "https://www.linkedin.com/in/agnes-saul/"
    },
    {
        "name": "Peggy Lee Pooi Qi",
        "major": "Marine Biology 🦭",
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


# Directory containing the images
image_directory = "images/casual_group_photos"

# List to store the image paths
image_paths = []

# Loop through the directory and get all image paths
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg"):  # Check for .jpg files
        image_paths.append(os.path.join(image_directory, filename))

# Centering the logo image using columns
col1, col2, col3 = st.columns([1, 2, 1])
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
    st.markdown("<h2 style='font-size: 24px;'>Who are We?😎</h2>", unsafe_allow_html=True)
    for member in members:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(member["image"], width=150)
        with col2:
            st.markdown(f"<p class='member-name'>{member['name']}</p>", unsafe_allow_html=True)
            st.markdown(f"**Major:** {member['major']}")
            st.markdown(f"**University:** {member['university']}")
        with col3:
            st.markdown(f"[![LinkedIn](https://img.icons8.com/color/48/000000/linkedin.png)]({member['linkedin']})", unsafe_allow_html=True)

# Gallery Header
st.markdown("<h2 style='text-align: center; color:black;'>Note + Gallery 📝🖼️</h2>", unsafe_allow_html=True)

st.markdown("""
<div style="
    border: 2px solid black;
    border-radius: 10px;
    background-color: #f4f4f4;
    margin: 10px;
    padding: 20px;
    text-align: justify;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
">
    <p>
        Throughout these five months, our team has gone through many experiences together while working for UNESCO Water Resilience Challenge. 
        These invaluable experiences, in various forms, have shaped our bond in many ways. 
        Be it bitterness 😥, sourness 🍋, frustration 😩, or a little bit of sadness sometimes 😢, 
        what we truly remember at the end of the day is an abundance of joy and happiness. 
        <br><br>Those memories will forever stay in our hearts.
        <br><br><strong>Team Make Water OK (Malaysia) - 2024 </strong>
    </p>
</div>
""", unsafe_allow_html=True)


# Define the number of columns you want to show the images in.
columns = st.columns(3)
for index, image_path in enumerate(image_paths):
    with columns[index % 4]:  # Modulo the number of columns to create a grid
        st.image(image_path)
        
# Nature Walk / Heritage Walk video section
st.markdown('<h1 class="header">Nature Walk / Heritage Walk Trip</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="video-description">
    <p>This video captures our nature walk and heritage walk at Penang Hill, highlighting our interactions with the environment and efforts to integrate these experiences into our project.</p>
</div>
""", unsafe_allow_html=True)
st.video('https://www.youtube.com/watch?v=uRb5tdTx1eE')

# Stakeholder Engagement Trip video section
st.markdown('<h1 class="header">Stakeholder Engagement Trip at Penang Hill</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="video-description">
    <p>We visited the Penang Hill Biosphere Reserve office and met with the personnel there to gain insights that would help improve our prototype.</p>
</div>
""", unsafe_allow_html=True)
st.video('https://www.youtube.com/watch?v=kGcKlLym9J0')

st.markdown("""
<div style="
    border: 2px solid blue;
    border-radius: 10px;
    background-color: #f4f4f4;
    margin: 10px;
    padding: 20px;
    text-align: justify;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
">
    <h2 style="text-align: center;">Acknowledgements</h2>
    <p>
        We extend our deepest gratitude to <u><strong>Dr. Yang Kok Lee</strong></u>, Senior Project Officer at the Penang Hill Biosphere Reserve (PHBR) Office. Dr. Yang's unwavering support and assistance in organizing our stakeholder engagement trip and site visits have been invaluable to our project's progress.
        <br><br>
        We also wish to express our sincere thanks to the <u><strong>PHBR Landslide Rehabilitation Team</strong></u> for their technical expertise and professional advice throughout this project. Their insights have been crucial in guiding our initiatives.
        <br><br>
        Additionally, we are immensely thankful to <u><strong>Dr. Vazeerudeen Hameed</strong></u>, a senior lecturer at Asia Pacific University of Technology and Innovation, whose profound knowledge in the field of computing and invaluable help with the technical aspects of the application have been vital to our progress.
        <br><br>
        Lastly, a special thanks to <u><strong>Dr. Abe Woo Sau Pinn</strong></u>, Senior Lecturer and Marine Biologist at Universiti Sains Malaysia (USM). Dr. Woo's moral support and assistance have been instrumental in helping us navigate the challenges of this project.
        <br><br>
        We are immensely grateful to all who have contributed their time and expertise to make this project fruitful.
    </p>
</div>
""", unsafe_allow_html=True)
