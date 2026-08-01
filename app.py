# =========== Step 1: Load Modules =============

import os
import time
import langchain
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

#============ STEP 2: API KEYS AND ENV VARIABLES ============
TAVILY_API_KEY = st.sidebar.text_input("Tavily_API", type = "password")
GOOGLE_API_KEY = st.sidebar.text_input("Google_API", type = "password")
GROQ_API_KEY =  st.sidebar.text_input("Groq_API", type = "password")

st.title("Agentic PPT Generator")
st.header("User can generate, PPT, Images, and fetch Latest News")

st.sidebar.title("Give API KEYS")

all_API = [TAVILY_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY]
if not all(all_API):
    st.sidebar.error("Must give API keys")
    
    url = "https://aistudio.google.com/api-keys"
    st.markdown(f"Get Google API key-{url}")

    url ="https://app.tavily.com/playground"
    st.markdown(f"Get Tavily API key-{url}")

    url = "https://console.groq.com/keys"
    st.markdown(f"Get Groq API key-{url}")

elif all(all_API):
    st.success("API KEYS LOADED SUCCESSFULLY")
    options = ["gemini-3.5-flash-lite", "gemini-3.5-flash",
              "gemini-2.5-flash-lite", "gemini-2.5-flash"]

    selected_model = st.selectbox("Select-Model", options = options)
  
    model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
    )
else:
    st.info("TRY VALID API_KEYS")

# ================ STEP 3: BACKEND =================

def search_latest_info(query):
  """This function helps to give lastest
  search using tavily based on given user query
  related research or contents"""

  client = TavilyClient(
      api_key  = TAVILY_API_KEY)

  response = client.search(query)
  return response

# Tool 2
def generate_image(img_prompt,slide_no = 1):
  """This function helps user to generate
  image using free api, with given
  img_prompt, with slide no"""

  url = f"https://image.pollinations.ai/{img_prompt}"

  import requests as r
  content = r.get(url).content
  with open(f"ai_image_{slide_no}.jpeg",'wb') as f:
    f.write(content)
  return url

def run_agent(agent, query):
  """This is the main agent, or leader agent
  orchestrate sub agents"""

  # Giving prompt to create detailed prompt
  # for code generation
  prompt = f"""Based on Below given Query,
  your task is to call specific tool, first to
  promptify user prompt, than call image tool, or
  latest search if required.give slide dynamic, ui ux,
  with creative design, keep help of function to generate image
  based on given topic,
  Generate image using
  with number of slide asked, and use time sleep to hit image request on server
  and using file handling embed this in output html, use java script function
  give Final response output in HTML, no markdowns
  user query given below:
  """
  prompt = prompt+query

  # prompt = agent_prompt(prompt)

  response = leader_agent. invoke({'messages' : [ {'role':'user',
                                                   'content' :prompt} ]})
  code = response['messages'][-1].content[-1]['text']
  return code


# Agent Creation
if all(all_API):
    leader_agent = create_agent(
        model = model,
        tools = [search_latest_info,
                 #generate_image
                 ])
    leader_agent

else:
    st.info("Give API-Keys first to load Agent")

# ============== STEP 4: STREAMLIT NAVBARS ===============

tab1, tab2, tab3 = st.tabs(["Generate Image", 
                           "Fetch News", 
                           "Generate PPT"])

user_input = st.text_area("Write Prompt & click Enter")

if (user_input) & (leader_agent):
    with tab1:
        if st.button("Click To Generate Image", key = "Image-Button"):
            with st.spinner("Running Agent"):
                try:
                    url = generate_image(user_input)
                    import requests as r 
                    img_data = r.get(url)
                    st.image(url)
                except Exception as err:
                    st.error("Error Code: ", err)

    with tab2:
        if st.button("Fetch Latest News", key = "News-Button"):
            with st.spinner("Running Agent"):
                try:
                    prompt = """Give Latest News related to given user query
                    in dynamic HTML, output with cards design format,
                    strict HTML output, no any markdowns response
                    user query: """ + user_input
                    
                    response = leader_agent.invoke({'messages' : [ {'role':'user',
                                                   'content' :prompt} ]})
                    code = response['messages'][-1].content[-1]['text']
                    st.html(code, width="stretch",unsafe_allow_javascript=True)

                except Exception as err:
                    st.error("Error Code: ", err)

    with tab3:
        if st.button("Click To Generate PPT", key = "PPT-Button"):
            with st.spinner("Running Agent"):
                try:
                    code = run_agent(leader_agent, user_input)
                    st.html(code, width="stretch",unsafe_allow_javascript=True)

                    if st.download_button(label = "DOWNLOAD PPT", data = code, file_name = 'ppt.html', mime = 'text/html'):
                        st.success("PPT Downloaded Successfully")
                        
                except Exception as err:
                    st.error("Error Code: ", err)
                    
