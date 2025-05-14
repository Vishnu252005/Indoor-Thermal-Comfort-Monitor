import socket
import json
from datetime import datetime

def get_local_ip():
    """Get local IP address for QR code"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "localhost"

def save_session_data(session_data):
    """Save session data to JSON"""
    return json.dumps(session_data)

def load_session_data(uploaded_file):
    """Load session data from JSON"""
    if uploaded_file is not None:
        return json.load(uploaded_file)
    return None

def get_current_time():
    """Get formatted current time"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S') 