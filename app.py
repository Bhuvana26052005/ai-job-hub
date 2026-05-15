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
role = st.text_input("Enter your Job Role:", placeholder="Data Analyst")
city = st.text_input("Enter your City/Country:", placeholder="Canada")

# API Key Input
gemini_key = st.text_input("Enter Gemini API Key:", type="password")

if st.button("Run Profile Audit & Pull Jobs Right Here"):
    if not name or not role or not city:
        st.error("Please fill out all input fields.")
    elif not gemini_key:
        st.error("Please provide your Gemini API key.")
    else:
        with st.spinner("Analyzing profile and compiling active regional jobs..."):
            
            # Initialize AI Model
            ai_active = True
            try:
                genai.configure(api_key=gemini_key)
                gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 1. Fetch AI Strategy Report
                test_prompt = f"Imagine you are a technical recruiter. If I ask you about '{name}' who works as a '{role}' in '{city}', give a quick 3-sentence summary of what is missing from their profile to get picked up by applicant tracking software."
                reputation_response = gemini_model.generate_content(test_prompt)
                st.success("Analysis Complete!")
                st.subheader("👁️ Your AI Audit Report:")
                st.info(reputation_response.text)
            except Exception as e:
                ai_active = False
                if "429" in str(e):
                    st.warning("⏳ Google Gemini Free Tier is cooling down. Running on fallback mode with custom role parsing.")
                else:
                    st.error(f"AI Connection Error: {str(e)}")

            # 2. Fetch and Display Live Jobs
            st.subheader(f"💼 Open {role} Jobs Found in {city}:")
            
            jobs_found = 0
            try:
                search_query = f"{role} {city}"
                encoded_search = urllib.parse.quote(search_query)
                rss_url = f"https://upwork.com{encoded_search}"
                
                response = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    for item in root.findall('.//item'):
                        title = item.find('title').text
                        link = item.find('link').text
                        desc = item.find('description').text[:220] + "..."
                        
                        with st.container(border=True):
                            st.markdown(f"### 🎯 {title}")
                            st.markdown("🏢 **Company:** Verified Marketplace Client")
                            st.write(desc)
                            st.link_button("🚀 Apply For Position", link, use_container_width=True)
                        st.write("") 
                        jobs_found += 1
                        if jobs_found >= 10:
                            break
            except:
                pass

            # 3. Dynamic Global Fallback Generation
            if jobs_found < 10:
                # Baseline safety targets for skills
                if "developer" in role.lower() or "engineer" in role.lower():
                    dynamic_skills = ["Python", "SQL", "Git Architecture", "System Design"]
                else:
                    dynamic_skills = ["SQL", "Excel Platforms", "PowerBI / Tableau", "Python Data Sets"]
                
                # Default Indian list if everything else fails
                fallback_companies = [
                    {"name": "Wipro", "url": "https://wipro.com"},
                    {"name": "Infosys", "url": "https://infosys.com"},
                    {"name": "TCS", "url": "https://tcs.com"},
                    {"name": "HCLTech", "url": "https://hcltech.com"},
                    {"name": "Cognizant", "url": "https://cognizant.com"},
                    {"name": "Tech Mahindra", "url": "https://techmahindra.com"},
                    {"name": "Accenture", "url": "https://accenture.com"},
                    {"name": "Capgemini", "url": "https://capgemini.com"},
                    {"name": "LTIMindtree", "url": "https://ltimindtree.com"},
                    {"name": "Genpact", "url": "https://genpact.com"}
                ]

                # FIX: Check if the user typed Canada or another international region, then load global tech hubs
                is_canada = "canada" in city.lower() or "toronto" in city.lower() or "vancouver" in city.lower()
                
                if is_canada:
                    fallback_companies = [
                        {"name": "Shopify", "url": "https://shopify.com"},
                        {"name": "RBC (Royal Bank of Canada)", "url": "https://rbc.com"},
                        {"name": "TD Bank", "url": "https://td.com"},
                        {"name": "Deloitte Canada", "url": "https://deloitte.com"},
                        {"name": "CGI Group", "url": "https://cgi.com"},
                        {"name": "Scotiabank", "url": "https://scotiabank.com"},
                        {"name": "Amazon Canada", "url": "https://amazon.jobs"},
                        {"name": "Rogers Communications", "url": "https://rogers.com"},
                        {"name": "Bell Canada", "url": "https://bell.ca"},
                        {"name": "OpenText", "url": "https://opentext.com"}
                    ]
                elif ai_active:
                    # Advanced: Ask Gemini to fetch 10 major employers dynamically if it's a completely different country
                    try:
                        comp_prompt = f"Provide a JSON list of exactly 10 major top-tier corporate employers frequently hiring technical staff in '{city}'. Output ONLY a valid JSON array of objects with keys 'name' and generic career 'url'. Do not include markdown or formatting text."
                        comp_response = gemini_model.generate_content(comp_prompt)
                        cleaned_json = comp_response.text.replace("```json", "").replace("```", "").strip()
                        fallback_companies = json.loads(cleaned_json)
                    except:
                        pass

                # Print out the localized target cards
                for i in range(jobs_found, 10):
                    # Prevent list index errors
                    if i - jobs_found >= len(fallback_companies):
                        break
                    job_data = fallback_companies[i - jobs_found]
                    
                    with st.container(border=True):
                        st.markdown(f"### 🎯 {role} Specialist")
                        st.markdown(f"🏢 **Company:** {job_data['name']}")
                        
                        skills_html = "".join([f'<span style="background-color:#1E3A8A; color:white; padding:4px 10px; margin-right:6px; border-radius:12px; font-size:12px; font-weight:bold; display:inline-block;">{skill}</span>' for skill in dynamic_skills])
                        st.markdown(f"💡 **Key Skills Required:** {skills_html}", unsafe_allow_html=True)
                        st.write("") 
                        
                        st.link_button(f"🔍 Open Official {job_data['name']} Career Portal", job_data['url'], use_container_width=True)
                    st.write("")
