# styles.py
def get_css():
    return """
    <style>
    /* Import custom font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');

    /* Global styling */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #e0f7e9;
    }
    /* Main header styling */
    h1.header {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5rem;
        color: #2c6e49;
        text-align: center;
    }
    /* Input elements styling */
    input, textarea, .stSelectbox select {
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #c4e7d4;
        width: 100%;
        font-size: 1rem;
    }
    /* Button styling */
    button, .stButton button {
        background-color: #64c2a6;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover, .stButton button:hover {
        background-color: #4da489;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #a3e4d7, #e8f8f5);
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        color: black;
    }
    /* (Optional) Enlarge tables or add spacing for the data editor */
    .stDataEditor {
        font-size: 1.1rem;
        padding: 1rem;
    }
    </style>
    """
