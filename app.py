import streamlit as st
import google.generativeai as genai
from scraper import scrape_page, BASE_URLS  

# API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key not found! Please fill in the Secrets section in Streamlit Cloud settings.")
    st.stop()



# Scrape the information from the METU Summer Practice website
general_info = scrape_page(BASE_URLS["general_info"])
steps_info = scrape_page(BASE_URLS["steps_follow"])
faq_info = scrape_page(BASE_URLS["faq"])

# FAQ data: You can add more questions and answers here

faq_data = {
    "Can IE 300 and IE 400 be completed in the same summer?": "No, the two mandatory summer practices cannot be performed during the same summer period.",
    "What is the submission deadline for the Summer Practice Report?": "Reports must be submitted by the end of the add-drop week of the academic semester following the internship.",
    "Do Saturdays count as work days for the internship?": "Saturdays can be counted as work days only if the company officially documents that they have a full-time working schedule on Saturdays.",
    "Is it mandatory to have an Industrial Engineer at the company?": "Yes, there must be at least one full-time Industrial Engineer working in the department who will act as the student's supervisor.",
    "How many work days are required for IE 300?": "IE 300 requires a minimum of 20 consecutive work days, excluding public holidays.",
    "How many work days are required for IE 400?": "IE 400 requires a minimum of 20 consecutive work days, excluding public holidays.",
    "In which language should the report be written?": "In accordance with METU's medium of instruction, all summer practice reports must be written in English.",
    "Can I start my internship before getting approval?": "No, the company and the specific department must be officially approved by the Summer Practice Committee before you start.",
    "Is it possible to do the summer practice abroad?": "Yes, provided that the company and the scope of work meet the IE 300/400 requirements and are approved by the committee in advance.",
    "Who covers the insurance for the internship?": "For mandatory summer practices within Turkey, the Social Security (SGK) insurance is covered by METU."
}

prompt = f"""
**Persona:** You are the "IE 300/400 Summer Practice Virtual Advisor," specialized for the METU Industrial Engineering Department. Your mission is to provide students with precise, reliable information regarding internship procedures based strictly on official resources.

**Information Sources & Constraints:**
* **Primary Source:** Use only the data provided in the following sections: {{general_info}}, {{steps_info}}, {{faq_info}}, and {{faq_data}}.
* **No Speculation:** Never guess or provide information not found in these documents. If information is missing, direct the student to the Summer Practice Committee or https://sp-ie.metu.edu.tr/en.
* **Out-of-Scope:** Politely decline non-internship questions (e.g., weather, general chat) and state that you can only assist with METU-IE internship matters.

**Operational Rules:**
1. **Language:** Respond in the same language used by the student (Turkish or English).
2. **Format:** Maintain a professional, clear, and readable tone. Use bullet points for complex processes.
3. **Token Limit:** Responses must not exceed 200 tokens. Avoid unnecessary pleasantries; be direct and information-oriented.

**Dataset:**
---General Info---
{general_info}
---Steps Info---
{steps_info}
---FAQ Info---
{faq_info}
---Additional Q&A---
{faq_data} """

#Function to get responses from Gemini
def ask_gemini(user_question):
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=prompt
    )
   
    response = model.generate_content(user_question)
    return response.text

# Function to get responses from OpenAI's GPT (Updated for new API)
"""def get_gpt_response(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to gpt-3.5-turbo if gpt-4 is not available
    messages=[{"role": "system","content":prompt},{"role": "user", "content": query}],  # Format the message as a list
        max_tokens=200
    )
    return response['choices'][0]['message']['content']  # Extract and return the response message"""

# Streamlit App Layout
st.title("METU IE Summer Practice Chatbot - Group 2")
st.write("Welcome! Ask me any questions regarding METU IE Summer Practice.")

# Create an input field for the user to ask questions
user_query = st.text_input("Your Question")

if user_query:
    # Get response based on user input
    response = ask_gemini(user_query)
    st.write(f"**Answer**: {response}")

    # Optionally, store the user query and bot response for logs (could be saved to a file or database)
    st.write(f"**Log**: You asked: '{user_query}'")
