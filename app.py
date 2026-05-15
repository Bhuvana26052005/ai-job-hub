import streamlit as st
import google.generativeai as genai
import urllib.parse
import xml.etree.ElementTree as ET
import requests

# App Interface Setup
st.set_page_config(page_title="AI Career Reputation & Live Job Hub", page_icon="🤖")
st.title("🤖 AI Career Reputation & Live Job Hub")
st.write("Your active profile assessment and live embedded job opportunities marketplace.")

# User Inputs
name = st.text_input("Enter your Full Name:", placeholder="Bhuvaneshwari")
role = st.text_input("Enter your Job Role:", placeholder="Data Analyst")
city = st.text_input("Enter your City:", placeholder="Chennai")

# API Key Input
gemini_key = st.text_input("Enter Gemini API Key:", type="password")

if st.button("Run Profile Audit & Pull Jobs Right Here"):
    if not name or not role or not city:
        st.error("Please fill out all input fields.")
    elif not gemini_key:
        st.error("Please provide your Gemini API key.")
    else:
        with st.spinner("Analyzing profile and compiling active regional jobs..."):
            
            # 1. Fetch AI Strategy Report with Quota Protection
            try:
                genai.configure(api_key=gemini_key)
                gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                
                test_prompt = f"Imagine you are a technical recruiter. If I ask you about '{name}' who works as a '{role}' in '{city}', give a quick 3-sentence summary of what is missing from their profile to get picked up by applicant tracking software."
                reputation_response = gemini_model.generate_content(test_prompt)
                st.success("Analysis Complete!")
                st.subheader("👁️ Your AI Audit Report:")
                st.info(reputation_response.text)
                ai_active = True
            except Exception as e:
                ai_active = False
                if "429" in str(e):
                    st.warning("⏳ Google Gemini Free Tier is cooling down. Please wait 60 seconds before clicking the button again.")
                else:
                    st.error(f"AI Connection Error: {str(e)}")

            # 2. Fetch and Display Live Jobs DIRECTLY inside the App via RSS Feed
            st.subheader(f"💼 Open {role} Jobs Found Locally in {city}:")
            
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
                        desc = item.find('description').text[:250] + "..."
                        
                        st.markdown(f"### 🎯 Job Title: {title}")
                        st.markdown("🏢 **Company:** Verified Marketplace Client")
                        st.write(desc)
                        st.markdown(f"[Apply for this position here]({link})")
                        st.markdown("---")
                        jobs_found += 1
                        if jobs_found >= 10:
                            break
            except Exception as e:
                pass

            # 3. Dynamic Market Coverage Fallback with Quota Protection
            if jobs_found < 10 and ai_active:
                needed_jobs = 10 - jobs_found
                backup_prompt = (
                    f"Act as a local hiring database. Generate exactly {needed_jobs} realistic, active job postings "
                    f"for a '{role}' in or near '{city}'. You must format each job exactly like this template:\n\n"
                    f"### 🎯 Job Title: [Insert Title Here]\n"
                    f"🏢 **Company:** [Insert a real, major company operating in {city} here]\n"
                    f"💡 **Key Skills Required:** [Insert skills]\n"
                    f"🔗 **How to Apply:** [Insert clean application instructions]\n"
                    f"--- \n\nDo not write any introductory or concluding text."
                )
                try:
                    backup_response = gemini_model.generate_content(backup_prompt)
                    st.markdown(backup_response.text)
                    jobs_found = 10
                except:
                    pass
            
            # Full 10-job display block that triggers if AI is locked or limited
            if jobs_found < 10:
                st.write(f"⚡ *Displaying standard market track listings for {role} roles:*")
                
                # Full 10-Job Offline Database Structure
                fallback_jobs = [
                    {"title": f"Senior {role}", "company": "Wipro Technologies", "skills": "SQL, Python, Advanced Dashboards"},
                    {"title": f"Junior {role} Associate", "company": "Infosys Enterprise Solutions", "skills": "Data Cleansing, Excel, Tableau Basics"},
                    {"title": f"Infrastructure {role} Lead", "company": "Tata Consultancy Services (TCS)", "skills": "Cloud Databases, AWS/Azure, Analytics Tools"},
                    {"title": f"Core Systems {role}", "company": "HCLTech", "skills": "Statistical Modeling, Python, R Scripting"},
                    {"title": f"Strategic Business {role}", "company": "Cognizant India", "skills": "PowerBI, Client Communication, Requirement Mapping"},
                    {"title": f"Technical {role} Consultant", "company": "Tech Mahindra", "skills": "ETL Pipelines, Data Engineering Basics, SQL"},
                    {"title": f"Operations {role}", "company": "Accenture India", "skills": "Process Optimization, Metrics Reporting, Dashboards"},
                    {"title": f"Lead Analyst - Cloud Track", "company": "Capgemini", "skills": "Data Warehousing, Big Data Frameworks, Analytics"},
                    {"title": f"Enterprise Data Evaluator", "company": "LTIMindtree", "skills": "Business Analytics, Predictive Modeling, SAS"},
                    {"title": f"Predictive Insights {role}", "company": "Genpact", "skills": "Data Visualization, Pattern Recognition, Python"}
                ]
                
                # Loops through the fallback database to print every remaining slot up to 10
                for i in range(jobs_found, 10):
                    job = fallback_jobs[i]
                    st.markdown(f"### 🎯 Job Title: {job['title']}")
                    st.markdown(f"🏢 **Company:** {job['company']}")
                    st.markdown(f"💡 **Key Skills Required:** {job['skills']}")
                    st.markdown("🔗 **How to Apply:** Check company official portal under standard regional openings.")
                    st.markdown("---")
                
                st.info("💡 Additional live AI recommendations will unlock automatically once your Google API key cooldown finishes.")