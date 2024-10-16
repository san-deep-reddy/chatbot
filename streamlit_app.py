import fitz
import streamlit as st
import google.generativeai as genai
import variables

# Configure the API key for the generative model
genai.configure(api_key=variables.api_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from the resume PDF
resume_text = extract_text_from_pdf(variables.local_cv_path)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    system_message = f"You are an AI assistant named Rocky, representing {variables.name}. Use the following resume information to answer questions about {variables.name}'s professional background: {resume_text}"
    st.session_state.chat_history = [
        {"role": "user", "parts": [system_message]},
        {"role": "model", "parts": ["Understood. I'm Rocky, an AI assistant representing " + variables.name + ". I'm ready to answer questions about their professional background based on the resume information provided. How can I help you today?"]}
    ]

def setup_sidebar():
    # Center the image and download button in the sidebar
    st.sidebar.image(variables.picture)
    
    # Display name centered
    st.sidebar.markdown(f'<h2 style="text-align: center;">{variables.name}</h2>', unsafe_allow_html=True)

    # Oval Download Resume Button centered
    st.sidebar.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="{variables.google_drive_cv_url}" target="_blank">
            <button style="
                background-color:#4CAF50; 
                color:white; 
                padding:10px 25px; 
                font-size:16px; 
                border:none; 
                border-radius:50px; 
                outline:none;
                cursor:pointer;
                ">
                Download Resume
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True)
    
    # About the Developer
    st.sidebar.markdown("### About the Developer")
    st.sidebar.markdown(
        f"This app was created by Sandeep D, leveraging the power of LLMs. For any inquiries or feedback, feel free to reach out via email at {variables.email}. You can also connect with me on [LinkedIn]({variables.url_linkedin}) to stay in touch."
    )
    
    # Privacy
    st.sidebar.markdown(
    """
    <div style="font-size: 1px; margin-top: 50px;">
        <p>Privacy: We do not retain or store user data from the chat session.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

def display_intro():
    st.markdown(f"<h1 style='font-size:30px;'>Welcome to Rocky, {variables.name.split()[0]}'s AI assistant! 🚀</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size:22px;'>I'm here to help you explore his skills, experience, and more.</h2>", unsafe_allow_html=True)

def display_messages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def generate_response(model, user_input, chat_history):
    # Append the new user message to the chat history
    chat_history.append({"role": "user", "parts": [user_input]})
    
    # Generate the response
    response = model.generate_content(chat_history)
    
    # Append the model's response to the chat history
    chat_history.append({"role": "model", "parts": [response.text]})
    
    return response.text, chat_history

# Show title and description
display_intro()

# Create a generative model client
model = genai.GenerativeModel("gemini-1.5-flash")

# Setup sidebar
setup_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the chat with a system message containing the resume context
if "chat" not in st.session_state:
    system_message = f"You are an AI assistant named Rocky, representing {variables.name}. Use the following resume information to answer questions about {variables.name}'s professional background: {resume_text}"
    st.session_state.chat = model.start_chat(history=[{"role": "system", "parts": [system_message]}])

# Display the existing chat messages
display_messages(st.session_state.messages)

# Create a chat input field to allow the user to enter a message
if prompt := st.chat_input(f"Hi, please ask any questions that you want to know about {variables.name.split()[0]} professionally."):
    # Store and display the current prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the Gemini model
    response_text, st.session_state.chat_history = generate_response(model, prompt, st.session_state.chat_history)

    # Display and store the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
