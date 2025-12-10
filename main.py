# # import streamlit as st
# # from langchain_openai import ChatOpenAI
# # from langchain_community.tools import DuckDuckGoSearchRun
# # # from langchain.agents import AgentExecutor, create_react_agent
# # # Nayi Lines (Correct fix)
# # from langchain.agents import create_react_agent
# # from langchain.agents.agent_executor import AgentExecutor
# # from langchain.prompts import PromptTemplate
# # from langchain.memory import ConversationBufferMemory

# # # --- Page Config ---
# # st.set_page_config(page_title="Conversational Knowledge Bot", page_icon="🤖")

# # st.title("🤖 Conversational Knowledge Bot")
# # st.markdown("I can remember our chat and search the web for answers!")

# # # --- Sidebar for API Key ---
# # # Assignment ke liye user se API key lena best practice hai
# # api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
# # # api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")


# # if not api_key:
# #     st.info("⚠️ Please enter your OpenAI API Key in the sidebar to start.")
# #     st.stop()

# # # --- Initialization (Run once) ---
# # if "memory" not in st.session_state:
# #     # Memory setup: Yeh bot ko pichli baatein yaad dilata hai
# #     st.session_state.memory = ConversationBufferMemory(
# #         memory_key="chat_history",
# #         return_messages=True
# #     )

# # if "messages" not in st.session_state:
# #     # UI Chat history setup
# #     st.session_state.messages = [
# #         {"role": "assistant", "content": "Hello! Ask me anything. I can search the web too!"}
# #     ]

# # # --- Setup Tools & Agent ---
# # def setup_agent():
# #     # 1. LLM Setup
# #     llm = ChatOpenAI(
# #         model="gpt-3.5-turbo", 
# #         temperature=0, 
# #         api_key=api_key
# #     )
    
# #     # 2. Tools Setup (Web Search)
# #     search_tool = DuckDuckGoSearchRun()
# #     tools = [search_tool]
    
# #     # 3. Prompt Template (ReAct style)
# #     # Hum agent ko bata rahe hain ki tools kaise use karne hain aur memory kaise check karni hai.
# #     template = """
# #     Answer the following questions as best you can. You have access to the following tools:

# #     {tools}

# #     Use the following format:

# #     Question: the input question you must answer
# #     Thought: you should always think about what to do
# #     Action: the action to take, should be one of [{tool_names}]
# #     Action Input: the input to the action
# #     Observation: the result of the action
# #     ... (this Thought/Action/Action Input/Observation can repeat N times)
# #     Thought: I now know the final answer
# #     Final Answer: the final answer to the original input question

# #     Begin!

# #     Previous conversation history:
# #     {chat_history}

# #     Question: {input}
# #     Thought:{agent_scratchpad}
# #     """
    
# #     prompt = PromptTemplate.from_template(template)

# #     # 4. Create Agent
# #     agent = create_react_agent(llm, tools, prompt)
    
# #     # 5. Create Executor (Jo agent ko run karega aur memory sambhalega)
# #     agent_executor = AgentExecutor(
# #         agent=agent, 
# #         tools=tools, 
# #         memory=st.session_state.memory, # Yahan hum memory connect kar rahe hain
# #         verbose=True, # Terminal mein details dikhayega
# #         handle_parsing_errors=True
# #     )
# #     return agent_executor

# # # --- Chat Interface ---

# # # Display chat messages from history on app rerun
# # for message in st.session_state.messages:
# #     with st.chat_message(message["role"]):
# #         st.markdown(message["content"])

# # # React to user input
# # if prompt := st.chat_input("What is on your mind?"):
# #     # Display user message
# #     st.chat_message("user").markdown(prompt)
# #     st.session_state.messages.append({"role": "user", "content": prompt})

# #     # Run the Agent
# #     try:
# #         agent_executor = setup_agent()
        
# #         with st.chat_message("assistant"):
# #             with st.spinner("Thinking & Searching..."):
# #                 response = agent_executor.invoke({"input": prompt})
# #                 output_text = response["output"]
# #                 st.markdown(output_text)
                
# #         # Add assistant response to chat history
# #         st.session_state.messages.append({"role": "assistant", "content": output_text})
        
# #     except Exception as e:
# #         st.error(f"An error occurred: {e}")


# import streamlit as st
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Check for API Key
# if not os.getenv("GEMINI_API_KEY"):
#     st.error("⚠️ GEMINI_API_KEY not found in .env file.")
#     st.stop()

# # --- Imports for Logic ---
# # Updated Imports for LangChain 0.1+
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain.memory import ConversationBufferMemory
# from langchain_core.prompts import PromptTemplate  # PromptTemplate ab core me hai
# # from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain.agents import AgentExecutor, create_react_agent
# # from langchain.prompts import PromptTemplate
# # from langchain.memory import ConversationBufferMemory
# # Updated Imports for LangChain 0.1+
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.memory import ConversationBufferMemory
# from langchain_core.prompts import PromptTemplate  # PromptTemplate ab core me hai

# # --- Page Config ---
# st.set_page_config(page_title="Gemini Knowledge Bot", page_icon="🧠")
# st.title("🧠 Gemini Conversational Bot")
# st.caption("Powered by Google Gemini + LangChain Memory + Web Search")

# # --- Initialization (Session State) ---
# # Memory setup: Ye previous conversations ko store karega
# if "memory" not in st.session_state:
#     st.session_state.memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=True
#     )

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hi! I'm connected to Google Gemini. Ask me about current events or factual topics!"}
#     ]

# # --- Core Logic: Agent Setup ---
# def setup_agent():
#     # 1. LLM Setup (Google Gemini)
#     # Hum 'gemini-1.5-flash' use kar rahe hain jo fast aur capable hai.
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0,
#         google_api_key=os.getenv("GEMINI_API_KEY"),
#         convert_system_message_to_human=True # Gemini specific tweak
#     )
    
#     # 2. Tools (Web Search)
#     search_tool = DuckDuckGoSearchRun()
#     tools = [search_tool]
    
#     # 3. Prompt Template (ReAct Logic)
#     # Ye prompt bot ko batata hai ki Tools kaise use karne hain.
#     template = """
#     Answer the following questions as best you can. You have access to the following tools:

#     {tools}

#     Use the following format:

#     Question: the input question you must answer
#     Thought: you should always think about what to do
#     Action: the action to take, should be one of [{tool_names}]
#     Action Input: the input to the action
#     Observation: the result of the action
#     ... (this Thought/Action/Action Input/Observation can repeat N times)
#     Thought: I now know the final answer
#     Final Answer: the final answer to the original input question

#     Begin!

#     Previous conversation history:
#     {chat_history}

#     Question: {input}
#     Thought:{agent_scratchpad}
#     """
    
#     prompt = PromptTemplate.from_template(template)

#     # 4. Create Agent
#     # Ye LLM, Tools aur Prompt ko jodta hai
#     agent = create_react_agent(llm, tools, prompt)
    
#     # 5. Agent Executor
#     # Ye runtime hai jo loop chalata hai (Think -> Act -> Observe)
#     agent_executor = AgentExecutor(
#         agent=agent, 
#         tools=tools, 
#         memory=st.session_state.memory,
#         verbose=True, # Terminal me logs dikhayega
#         handle_parsing_errors=True # Agar Gemini format gadbad kare to crash na ho
#     )
#     return agent_executor

# # --- Chat UI Interface ---

# # 1. Display Chat History
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # 2. Handle User Input
# if user_input := st.chat_input("Ask me anything..."):
#     # User message show karein
#     st.chat_message("user").markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Agent Run karein
#     try:
#         agent_executor = setup_agent()
        
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 # Agent ko invoke karte hain
#                 response = agent_executor.invoke({"input": user_input})
#                 output_text = response["output"]
#                 st.markdown(output_text)
                
#         # Assistant response save karein
#         st.session_state.messages.append({"role": "assistant", "content": output_text})
        
#     except Exception as e:
#         st.error(f"Error: {e}")


import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for API Key
if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ GEMINI_API_KEY not found in .env file.")
    st.stop()

# --- IMPORTS (Yeh hain wo lines jo maine fix ki hain) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# FIX: AgentExecutor ko alag se import kar rahe hain taaki error na aaye
from langchain.agents import create_react_agent
from langchain.agents.agent_executor import AgentExecutor

# --- Page Config ---
st.set_page_config(page_title="Gemini Knowledge Bot", page_icon="🧠")
st.title("🧠 Gemini Conversational Bot")
st.caption("Powered by Google Gemini + LangChain Memory + Web Search")

# --- Initialization ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm connected to Google Gemini. Ask me anything!"}
    ]

# --- Core Logic ---
def setup_agent():
    # 1. LLM Setup (Google Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        convert_system_message_to_human=True
    )
    
    # 2. Tools (Web Search)
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool]
    
    # 3. Prompt Template
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Previous conversation history:
    {chat_history}

    Question: {input}
    Thought:{agent_scratchpad}
    """
    
    prompt = PromptTemplate.from_template(template)

    # 4. Create Agent
    agent = create_react_agent(llm, tools, prompt)
    
    # 5. Create Executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=st.session_state.memory,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor

# --- Chat Interface ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask me anything..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        agent_executor = setup_agent()
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent_executor.invoke({"input": user_input})
                output_text = response["output"]
                st.markdown(output_text)
                
        st.session_state.messages.append({"role": "assistant", "content": output_text})
        
    except Exception as e:
        st.error(f"Error: {e}")