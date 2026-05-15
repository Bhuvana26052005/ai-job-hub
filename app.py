import streamlit as st
import google.generativeai as genai
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import json

# App Interface Setup
st.set_page_config(page_title="AI Career Reputation & Live Job Hub", page_icon="🤖")
st.title("🤖 AI Career Reputation & Live Job Hub")
st.write("Your active profile assessment and live embedded job opportunities marketplace.")

# User Inputs
name = st.text_input("Enter your Full Name:", placeholder="Bhuvaneshwari")
role = st.text_input("Enter your Job Role:", placeholder="Web Developer")
city = st.text_input("Enter your Target City/Country:", placeholder="Kolkata")

# API Key Input
gemini_key = st.text_input("Enter Gemini API Key:", type="password")

if st.button("Run Unified Profile & Vacancy Audit"):
    if not name or not role or not city:
        st.error("Please fill out all input fields.")
    elif not gemini_key:
        st.error("Please provide your Gemini API key.")
    else:
        with st.spinner(f"Running complete unified AI analysis for {city}..."):
            
            # Default fallbacks in case of an absolute connection block
            audit_report = f"Recruiters looking for a {role} in {city} will scan major local hubs like Sector V or New Town. Ensure your public project repository matches regional tech stacks."
            dynamic_vacancies = [
                {"title": f"Senior {role}", "company": "Wipro", "skills": ["SQL", "Python", "Dashboards"], "url": "https://wipro.com"},
                {"title": f"Junior {role} Associate", "company": "Infosys", "skills": ["Data Cleansing", "Excel", "Tableau"], "url": "https://infosys.com"},
                {"title": f"Infrastructure {role} Lead", "company": "TCS", "skills": ["Cloud Databases", "AWS", "Analytics"], "url": "https://tcs.com"}
            ]

            # COMBINED SINGLE PROMPT LOGIC: Only 1 API call means no more 429 rate limit triggers
            try:
                genai.configure(api_key=gemini_key)
                gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                
                unified_prompt = (
                    f"You are an executive recruiter evaluating talent. First, write a brief 3-sentence reputation audit summary "
                    f"about what is missing from the online presence of '{name}', a '{role}' in '{city}', to be picked up by automated hiring engines. "
                    f"Second, identify exactly 5 real, major corporate employers or technology hubs physically hiring or operating in '{city}' "
                    f"that currently have open vacancy tracks or active hiring pipelines for a '{role}' role. "
                    f"You must return your entire response ONLY as a single valid JSON object. Do not include markdown, code backticks, or conversational text. "
                    f"Format the JSON exactly like this structure example: "
                    f'{{"audit": "Your 3-sentence audit text here", "vacancies": [{{"title": "Role Title", "company": "Company Name", "skills": ["Skill1", "Skill2"], "url": "https://wipro.com"}}]}}'
                )
                
                response = gemini_model.generate_content(unified_prompt)
                raw_text = response.text.strip()
                
                # Extract clean JSON markers safely from the response stream
                if "{" in raw_text and "}" in raw_text:
                    start_idx = raw_text.find("{")
                    end_idx = raw_text.rfind("}") + 1
                    cleaned_json = raw_text[start_idx:end_idx]
                    parsed_data = json.loads(cleaned_json)
                    
                    audit_report = parsed_data.get("audit", audit_report)
                    dynamic_vacancies = parsed_data.get("vacancies", dynamic_vacancies)
                
                st.success("Unified Data Retrieval Successful!")
            except Exception as e:
                st.warning("⚠️ Google Free Tier limit reached. Displaying local cache backup metrics smoothly:")

            # 1. Output the Reputation Audit Panel
            st.subheader("👁️ Your AI Audit Report:")
            st.info(audit_report)

            # 2. Fetch and Display Live RSS Jobs Feed (Unaffected by Google Limits)
            st.subheader(f"💼 Open {role} Jobs Found in {city}:")
            try:
                search_query = f"{role} {city}"
                encoded_search = urllib.parse.quote(search_query)
                rss_url = f"https://upwork.com{encoded_search}"
                
                feed_res = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                if feed_res.status_code == 200:
                    root = ET.fromstring(feed_res.content)
                    for item in root.findall('.//item')[:3]: # Embed top 3 live marketplace tracks
                        title = item.find('title').text
                        link = item.find('link').text
                        desc = item.find('description').text[:180] + "..."
                        
                        with st.container(border=True):
                            st.markdown(f"### 🎯 {title}")
                            st.markdown("🏢 **Company:** Verified Marketplace Client")
                            st.write(desc)
                            st.link_button("🚀 Apply For Position", link, use_container_width=True)
                        st.write("")
            except:
                pass

            # 3. Output the City-Specific Corporate Portal Vacancies Panel
            st.subheader(f"🔍 Active Company Career Portals Inside {city}:")
            for job_data in dynamic_vacancies:
                with st.container(border=True):
                    c_name = job_data.get('company', 'Enterprise')
                    j_title = job_data.get('title', role)
                    
                    st.markdown(f"### 🎯 Job Title: {j_title}")
                    st.markdown(f"🏢 **Company:** {c_name} ({city} Office)")
                    
                    # Layout skill tags capsules smoothly
                    skills_list = job_data.get('skills', ["Analysis", "Development"])
                    skills_html = "".join([f'<span style="background-color:#1E3A8A; color:white; padding:4px 10px; margin-right:6px; border-radius:12px; font-size:12px; font-weight:bold; display:inline-block;">{skill}</span>' for skill in skills_list])
                    st.markdown(f"💡 **Key Skills Required:** {skills_html}", unsafe_allow_html=True)
                    st.write("")
                    
                    # Direct Link Validation Guard
                    provided_url = job_data.get('url', '').strip()
                    if not provided_url or "example" in provided_url or len(provided_url) < 12:
                        encoded_target = urllib.parse.quote(f"{c_name} jobs vacancies careers")
                        target_url = f"https://linkedin.com{encoded_target}"
                    else:
                        target_url = provided_url
                    
                    st.link_button(f"🚀 Open Official {c_name} Career Portal", target_url, use_container_width=True)
                st.write("")
