def get_custom_css():
    return """
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: white;
        transition: all 0.3s ease;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    .stAlert {
        border-radius: 0.5rem;
    }
    </style>
    """ 