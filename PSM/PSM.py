
# import

import re
import streamlit as st
import secrets
import string

# Set page configuration
st.set_page_config(page_title="Password Strength Meter", layout='centered')

# Initialize session state for button visibility
if "show_generate" not in st.session_state:
    st.session_state.show_generate = False

# Custom CSS Styling
st.markdown("""
    <style>
        .main {text-align: center;}
        div[data-testid="stTextInput"] {
            width: 80% !important; 
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        div.stButton {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        div.stButton > button {
             border-radius: 10px;
             background-image: linear-gradient(to right, #141E30 0%, #243B55 51%, #141E30 100%);
             padding: 10px 30px;
             text-align: center;
             text-transform: uppercase;
             transition: 0.5s;
             background-size: 200% auto;
             color: white;            
             width: 30% !important;
             box-shadow: 0 0 20px #eee;
             font-size: 14px;
             border: none;
            cursor: pointer;}
            

        div.stButton > button:hover {
            background-position: right center;
        }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-image: linear-gradient(171.8deg,  
                rgba(10, 10, 10, 1) 10%,  
                rgba(50, 50, 50, 1) 30%,  
                rgba(5, 111, 146, 1) 50%,  
                rgba(6, 57, 84, 1) 70%,   
                rgba(20, 20, 20, 1) 90%   
            );
            color: white;
        }
        h1 {
            font-family: Georgia, serif !important;
            font-size: 34px;
            font-weight: bold;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            color: white !important;
            font-size: 18px;
            font-weight: bold;
        }
        .custom-warning {
            background-color: rgba(202, 255, 190, 0.42);
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        .weak-text {
            font-size: 22px;
            font-weight: bold;
            color: red;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50px;
        }
    </style>           
""", unsafe_allow_html=True)

# Function to generate a strong password
def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(12))

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) < 8:
        return '<p class="weak-text">Weak: Too short</p>', "red", 0.2, ["⚠️ Increase password length to at least 8 characters."]
    
    if re.search(r"[A-Z]", password):
        score += 0.2
    else:
        feedback.append("🔴 Add at least one uppercase letter.")
    
    if re.search(r"[a-z]", password):
        score += 0.2
    else:
        feedback.append("🔴 Add at least one lowercase letter.")
    
    if re.search(r"[0-9]", password):
        score += 0.2
    else:
        feedback.append("🔴 Add at least one digit.")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 0.2
    else:
        feedback.append("🔴 Add at least one special character (!@#$%^&*).")
    
    common_passwords = ["password123", "12345678", "qwerty", "abcdefg", "12345"]
    if password.lower() in common_passwords:
        return '<p class="weak-text">Weak: Common password, choose another</p>', "red", 0.2, ["⚠️ Avoid common passwords!"]
    
    if score == 1.0:
        return "✅ Strong: Your password is strong!", "green", score, []
    elif score < 0.6:
        return "❌ Weak", "red", score, feedback
    else:
        return "⚠️ Moderate", "blue", score, feedback

# Title
st.title("Password Strength Meter")

# Input field
password = st.text_input("🔑 Enter password", type="password", help="Make sure your password is strong.")

# Button to check password strength
if st.button("🔍 Check Strength"):
    if password:
        strength_msg, color, progress, suggestions = check_password_strength(password)
        
        st.progress(progress)
        
        if color == "green":
            st.success(strength_msg)
        elif color == "blue":
            st.info(strength_msg)
        else:
            st.markdown(strength_msg, unsafe_allow_html=True)

        if suggestions:
            with st.expander("💡 Improve Your Password"):
                for item in suggestions:
                    st.markdown(item, unsafe_allow_html=True)

        # Enable "Generate Password" button after checking strength
        st.session_state.show_generate = True
    else:
        st.markdown('<div class="custom-warning">⚠️ Please enter a password first.</div>', unsafe_allow_html=True)

# Show "Generate Strong Password" button only after checking strength
if st.session_state.show_generate:
    if st.button("🔄 Generate Strong Password"):
        generated_password = generate_strong_password()
        st.text_input("🔑 Generated Password", value=generated_password, disabled=True)
