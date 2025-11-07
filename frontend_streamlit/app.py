import os
import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000/api")

st.set_page_config(page_title="PerplexiPlay", layout="wide")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

st.title("PerplexiPlay ? Agent Playground")

menu = st.sidebar.radio("Navigation", ["Auth", "Agents", "Experiments"]) 


def auth_headers():
    if not st.session_state["access_token"]:
        return {}
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}

if menu == "Auth":
    st.subheader("Register")
    with st.form("register"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            r = requests.post(f"{API_BASE}/auth/register", json={"username": username, "email": email, "password": password})
            if r.status_code == 200:
                st.success("Registered. You can now login.")
            else:
                st.error(r.text)

    st.subheader("Login")
    with st.form("login"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.form_submit_button("Login"):
            r = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
            if r.status_code == 200:
                data = r.json()
                st.session_state["access_token"] = data["access_token"]
                st.session_state["refresh_token"] = data["refresh_token"]
                st.success("Logged in")
            else:
                st.error(r.text)

    if st.session_state["refresh_token"]:
        if st.button("Refresh Token"):
            r = requests.post(f"{API_BASE}/auth/refresh", json={"refresh_token": st.session_state["refresh_token"]})
            if r.status_code == 200:
                data = r.json()
                st.session_state["access_token"] = data["access_token"]
                st.session_state["refresh_token"] = data["refresh_token"]
                st.success("Token refreshed")
            else:
                st.error(r.text)
        if st.button("Logout"):
            r = requests.post(f"{API_BASE}/auth/logout", json={"refresh_token": st.session_state["refresh_token"]})
            st.session_state["access_token"] = None
            st.session_state["refresh_token"] = None
            st.success("Logged out")

elif menu == "Agents":
    st.subheader("Your Agents")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Create Agent")
        name = st.text_input("Name")
        framework = st.selectbox("Framework", ["openai", "langchain", "crewai"]) 
        params = st.text_area("Params (JSON)", value="{}")
        if st.button("Create"):
            try:
                payload = {"name": name, "framework": framework, "params": eval(params)}
            except Exception:
                st.error("Params must be a JSON-like dict, e.g., {'model': 'gpt-4o-mini'}")
                payload = None
            if payload:
                r = requests.post(f"{API_BASE}/agents/", json=payload, headers=auth_headers())
                if r.status_code == 200:
                    st.success("Agent created")
                else:
                    st.error(r.text)
    with col2:
        st.markdown("### List Agents")
        r = requests.get(f"{API_BASE}/agents/", headers=auth_headers())
        if r.status_code == 200:
            for a in r.json():
                st.write(a)
        else:
            st.info("Login to view agents")

elif menu == "Experiments":
    st.subheader("Run Experiment")
    # Load agents
    r = requests.get(f"{API_BASE}/agents/", headers=auth_headers())
    agents = r.json() if r.status_code == 200 else []
    agent_options = {f"{a['name']} (#{a['id']})": a['id'] for a in agents}
    if not agent_options:
        st.info("Create an agent first in Agents tab.")
    else:
        agent_label = st.selectbox("Agent", list(agent_options.keys()))
        agent_id = agent_options[agent_label]
        input_json = st.text_area("Input JSON", value="{'prompt': 'Hello world'}")
        if st.button("Run"):
            try:
                input_data = eval(input_json)
            except Exception:
                st.error("Input must be a JSON-like dict.")
                input_data = None
            if input_data is not None:
                r = requests.post(f"{API_BASE}/experiments/", json={"agent_id": agent_id, "input_data": input_data}, headers=auth_headers())
                if r.status_code == 200:
                    exp = r.json()
                    st.success(f"Experiment {exp['id']} status: {exp['status']}")
                    r = requests.get(f"{API_BASE}/experiments/{exp['id']}", headers=auth_headers())
                    if r.status_code == 200:
                        st.json(r.json())
                else:
                    st.error(r.text)
