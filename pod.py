import streamlit as st
import google.generativeai as genai

# Predefined API key
api_key = "AIzaSyCl2DDXFdXy09KZCfiR2kYO-NT4Rpsbc8w"

# Configure the API
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# Custom CSS for neon background and styling
st.markdown("""
    <style>
    body {
        background-color: #222; /* Dark background for contrast */
        color: #fff;  /* White text for readability */
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #222;
        color: #fff;
    }
    .stTextInput, .stTextArea, .stSelectbox, .stSlider {
        background-color: #333; /* Dark input fields */
        color: #fff;
        border: 1px solid #0f0; /* Neon green border */
        box-shadow: 0 0 10px #0f0; /* Neon green shadow */
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .stTextInput:focus, .stTextArea:focus, .stSelectbox:focus, .stSlider:focus {
        border: 1px solid #00ff00; /* Bright neon green on focus */
        box-shadow: 0 0 10px #00ff00;
    }
    .stButton > button {
        background-color: #ff00ff; /* Neon pink button */
        color: #fff;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff1493; /* Slightly darker pink when hovered */
    }
    .output-box {
        background-color: #333; /* Dark background for the output box */
        color: #0f0;  /* Neon green text */
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 10px #0f0; /* Neon green shadow */
        font-size: 16px;
        max-height: 400px;
        overflow-y: scroll;
        margin-top: 20px;
    }
    h1 {
        color: #FFA500;  /* Orange color for the title */
        font-weight: bold;
        text-align: center;
        text-shadow: 0 0 10px #FFA500; /* Orange glow effect */
    }
    .container {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
    }
    .input-box {
        margin-bottom: 30px;
    }
    .section-header {
        color: #ff00ff;
        font-weight: bold;
        margin-top: 30px;
        text-shadow: 0 0 10px #ff00ff; /* Neon glow effect */
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for conversation history and other data
if "responses" not in st.session_state:
    st.session_state["responses"] = []  # Stores responses

# Title
st.title("Tushar")

# Main container for user input
with st.container():
    # Display the generated script at the top if available
    if st.session_state["responses"]:
        latest_response = st.session_state["responses"][-1]
        st.subheader("Generated Podcast Script:")
        st.markdown(f'<div class="output-box">{latest_response["response"]}</div>', unsafe_allow_html=True)

    # User Input Fields
    st.subheader("Enter the topic for the podcast:")
    topic = st.text_area(
        "E.g., The Future of AI in Healthcare", 
        key="topic_input", 
        placeholder="Type the topic here...",
        label_visibility="collapsed",
        height=100
    )

    # Select Tone of the Podcast
    st.subheader("Select the tone of the podcast:")
    tone = st.selectbox(
        "Select the tone of the podcast:",
        ["Informative", "Casual", "Educational", "Entertainment"]
    )

    # Select Target Audience
    st.subheader("Select the target audience:")
    audience = st.selectbox(
        "Select the target audience:",
        ["General Audience", "Tech Enthusiasts", "Professionals", "Students"]
    )

    # Select Length of Podcast
    st.subheader("Select the approximate length of the script (in minutes):")
    length = st.slider(
        "Length of the podcast (minutes):",
        min_value=5,
        max_value=60,
        step=5,
    )

    # Generate Button with Loading Indicator
    generate_button = st.button("Generate Podcast Script")

    if generate_button:
        if not topic.strip():
            st.warning("Please enter a topic before generating the podcast script.")
        else:
            with st.spinner("Generating your podcast script..."):
                try:
                    # Generate content for the podcast
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"Generate a {tone.lower()} podcast script about {topic}. The target audience is {audience}, and the length should be approximately {length} minutes."
                    response = model.generate_content(prompt)

                    # Append the response to session state
                    st.session_state["responses"].append(
                        {"prompt": topic, "response": response.text}
                    )

                    # Display the generated podcast script in a textbox
                    st.subheader("Generated Podcast Script:")
                    st.markdown(f'<div class="output-box">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating content: {e}")
