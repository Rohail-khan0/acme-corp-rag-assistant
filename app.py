import streamlit as st
import backend
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Acme Nexus | Corporate Intelligence",
    page_icon="🕸️",
    layout="centered"
)

# --- Custom CSS (Acme Nexus Theme) ---
st.markdown("""
<style>
    /* Hide standard Streamlit header/footer/toolbar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* Global Settings */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 6rem;
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Header Styling */
    .nexus-header {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 40px 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .nexus-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 0;
    }
    .nexus-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
        margin-top: 10px;
        letter-spacing: 0.5px;
    }
    
    /* Thread Styles */
    .thread-item {
        margin-bottom: 30px;
        animation: fadeIn 0.4s ease-out;
    }
    
    /* User Query Styling */
    .query-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
        margin-bottom: 5px;
    }
    .user-query {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a2a3a; /* Dark Blue-Black */
        margin-bottom: 15px;
        border-left: 4px solid #1a2a3a;
        padding-left: 15px;
    }
    
    /* Answer Card Styling */
    .answer-card {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #2c3e50;
        font-size: 1.05rem;
        line-height: 1.7;
        position: relative;
    }
    .answer-card::before {
        content: "NEXUS INTELLIGENCE";
        position: absolute;
        top: 0;
        right: 0;
        background-color: #f8f9fa;
        padding: 4px 12px;
        font-size: 0.6rem;
        color: #999;
        border-bottom-left-radius: 12px;
        border-top-right-radius: 12px;
        font-weight: bold;
    }
    
    .loading-status {
        color: #2c5364;
        font-style: italic;
        margin-bottom: 20px;
    }

    /* Animation */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Initialization ---
try:
    with st.spinner("Connecting to Nexus Core..."):
        rag_components = backend.initialize_rag_system()
except Exception as e:
    st.error(f"Nexus Setup Failed: {str(e)}")
    st.stop()

# --- Header Section ---
st.markdown("""
<div class="nexus-header">
    <div class="nexus-title">ACME NEXUS</div>
    <div class="nexus-subtitle">Corporate Intelligence & Search Platform</div>
</div>
""", unsafe_allow_html=True)

# --- Render History ---
# Prompt placeholder if empty
if not st.session_state.history:
    st.markdown("""
    <div style="text-align: center; color: #a0a0a0; margin-top: 50px;">
        <p style="font-size: 1.2rem;">Begin your search by typing below.</p>
        <p style="font-size: 0.9rem;">Try: <em>"What are our sustainability goals?"</em> or <em>"List the engineering team."</em></p>
    </div>
    """, unsafe_allow_html=True)

# Iterate through history
for i, (q, a) in enumerate(st.session_state.history):
    st.markdown(f"""
    <div class="thread-item">
        <div class="query-label">Query Log #{i+1}</div>
        <div class="user-query">{q}</div>
        <div class="answer-card">
            {a}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Input Area (Sticky Footer) ---
query = st.chat_input("Access Nexus Database...")

if query:
    # 1. Process
    try:
        # We can add a small "Thinking" indicator if needed, but st.chat_input handles some UI
        with st.status("Analyzing Corporate Data...", expanded=False) as status:
            response = backend.get_rag_response(query, rag_components)
            status.update(label="Analysis Complete", state="complete", expanded=False)
        
        # 2. Update State
        st.session_state.history.append((query, response))
        
        # 3. Rerun to display
        st.rerun()
        
    except Exception as e:
        st.error(f"Processing Error: {e}")
