"""
Streamlit UI for Groq + PDF RAG with User Context
Upload PDF, select user profile, ask questions, get personalized Groq-powered responses.
"""

import streamlit as st
import os
from rag_groq import SimpleRAG
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="📄 Groq + PDF RAG with User Context", layout="wide")

# Show warning if GROQ API key is missing
if not os.getenv("GROQ_API_KEY"):
    st.warning(
        "⚠️ GROQ_API_KEY is not set. Set the environment variable or add it to `.env` to enable Groq generation.\n"
        "Example (PowerShell): `$env:GROQ_API_KEY = 'your_key_here'`"
    )

# Initialize session state
if "rag" not in st.session_state:
    # Do not hard-code a decommissioned model; let SimpleRAG pick from env or fallback.
    # Use the previous requested model explicitly across the app.
    st.session_state.rag = SimpleRAG(model="openai/gpt-oss-20b", users_file="users.json")
    users_count = len(st.session_state.rag.list_users())
    if users_count > 0:
        print(f"✓ Loaded {users_count} users from users.json")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = None

st.title("📄 Groq + PDF RAG with User Context")
st.markdown("Upload a PDF, select a user profile, and get personalized responses based on user context.")

# Sidebar for PDF upload and user management
with st.sidebar:
    st.header("⚙️ Configuration")

    # Tab for PDF Management and User Management
    tab1, tab2 = st.tabs(["📁 PDF & Docs", "👤 Users"])

    with tab1:
        st.subheader("Upload PDF(s)")
        st.write("Upload one or more PDF files. The LLM will use context from all of them.")
        
        # Multiple file uploader
        uploaded_files = st.file_uploader("Choose PDF file(s)", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Load PDF
                with st.spinner(f"Loading {uploaded_file.name}..."):
                    text = st.session_state.rag.load_pdf(temp_path)
                    st.success(f"✓ {uploaded_file.name} loaded ({len(text)} characters)")

                # Clean up temp file
                os.remove(temp_path)
        
        # Show loaded documents
        st.write("---")
        st.subheader("📚 Loaded Documents")
        docs = st.session_state.rag.list_documents()
        
        if docs:
            st.info(f"✓ {len(docs)} document(s) loaded")
            for i, doc in enumerate(docs):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.text(f"📄 {doc['name']}")
                with col2:
                    st.text(f"{doc['pages']} pages")
                with col3:
                    # Ensure each button has a unique key to avoid Streamlit DuplicateElementKey
                    btn_key = f"remove_{i}_{doc['name']}"
                    if st.button("🗑️", key=btn_key):
                        st.session_state.rag.remove_document(doc["name"])
                        # Use experimental_rerun to immediately refresh the UI
                        try:
                            st.experimental_rerun()
                        except Exception:
                            # Fallback to st.rerun for older Streamlit versions
                            st.rerun()
            
            # Clear all button
            if st.button("🗑️ Clear All Documents"):
                st.session_state.rag.clear_documents()
                st.session_state.messages = []
                st.success("All documents cleared")
                try:
                    st.experimental_rerun()
                except Exception:
                    st.rerun()
        else:
            st.info("ℹ️ No documents loaded yet. Upload a PDF to get started.")

    with tab2:
        st.subheader("User Profiles")

        # Section 1: Existing Users (Pre-loaded from users.json)
        st.write("**📋 Existing Users**")
        users = st.session_state.rag.list_users()

        if users:
            # Display user count badge
            st.info(f"✓ {len(users)} user(s) loaded from users.json")

            # User selection dropdown
            user_names = {user["user_id"]: f"👤 {user['name']} ({user['user_id']})" for user in users}
            selected_user_id = st.selectbox(
                "Select a user for this conversation",
                options=list(user_names.keys()),
                format_func=lambda x: user_names[x],
                key="user_selector",
            )
            st.session_state.current_user_id = selected_user_id

            # Show selected user details (expanded)
            if st.session_state.current_user_id:
                user = st.session_state.rag.get_user(st.session_state.current_user_id)
                if user:
                    with st.expander("👤 User Details", expanded=True):
                        st.markdown(f"**Name:** {user['name']}")
                        st.markdown(f"**User ID:** `{user['user_id']}`")
                        if user["preferences"]:
                            st.markdown(f"**Preferences:** {', '.join(user['preferences'])}")
                        if user["purchase_history"]:
                            st.markdown(
                                f"**Recent Interactions:** {', '.join(user['purchase_history'][-5:])}"
                            )
        else:
            st.info("ℹ️ No users found. Run `python setup_users.py` to create default users.")

        # Section 2: Create New User
        st.write("---")
        st.write("**➕ Create New User**")

        with st.form("create_user_form", clear_on_submit=True):
            new_user_id = st.text_input("User ID", placeholder="e.g., user_001")
            new_user_name = st.text_input("User Name", placeholder="e.g., John Doe")
            new_user_prefs = st.text_area(
                "Preferences (comma-separated)",
                placeholder="e.g., vegetarian, likes_coffee, tech_enthusiast",
                height=60,
            )
            new_user_history = st.text_area(
                "Purchase/Interaction History (comma-separated)",
                placeholder="e.g., bought_coffee, attended_event, read_article",
                height=60,
            )

            submit_button = st.form_submit_button("➕ Create User")

            if submit_button:
                if new_user_id:
                    prefs_list = [p.strip() for p in new_user_prefs.split(",") if p.strip()]
                    history_list = [h.strip() for h in new_user_history.split(",") if h.strip()]
                    st.session_state.rag.create_user(
                        new_user_id, new_user_name, prefs_list, history_list
                    )
                    st.success(f"✓ User '{new_user_id}' created and saved to users.json!")
                    st.session_state.current_user_id = new_user_id
                    st.rerun()
                else:
                    st.error("User ID is required")

# Main chat interface
st.header("💬 Ask Questions")

# Display current user badge (prominent)
if st.session_state.current_user_id:
    user = st.session_state.rag.get_user(st.session_state.current_user_id)
    if user:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"💬 **Chatting as:** {user['name']} ({user['user_id']})")
        with col2:
            if st.button("🔄 Switch User"):
                st.session_state.current_user_id = None
                st.rerun()
else:
    st.warning("⚠️ No user selected. Select a user from the sidebar to personalize responses.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Ask a question about the PDF..."):
    if not st.session_state.current_user_id:
        st.warning("Please select a user first!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate personalized response
        with st.chat_message("assistant"):
            with st.spinner("Generating personalized response..."):
                response = st.session_state.rag.generate_response(
                    prompt, user_id=st.session_state.current_user_id
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
