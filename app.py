"""
Multi-Agent AI System - Streamlit Web Interface
A professional, user-friendly interface for the Multi-Agent System with ReAct Agent.
"""

import streamlit as st
import json
from datetime import datetime
from src.multi_agent_system import MultiAgentSystem
from src.tools import Tools

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .agent-card h4 {
        margin: 0;
        color: #2c3e50;
    }
    .agent-card p {
        margin: 0.5rem 0 0 0;
        color: #555;
        font-size: 0.9rem;
    }
    .tool-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        margin: 0.2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .response-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        max-height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: inherit;
    }
    
    /* ✅ FIX: Dark text for AI responses */
    .ai-message {
        background: #f0f2f6;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 15px 5px;
        max-width: 70%;
        color: #1a1a2e !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    .ai-message strong {
        color: #2c3e50;
    }
    .ai-message p {
        color: #1a1a2e !important;
    }
    .ai-message * {
        color: #1a1a2e !important;
    }
    
    /* ✅ Code block styling - 50% LIGHTER */
    .ai-message code {
        background: #e8e8e8 !important;
        color: #2d2d2d !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    .ai-message pre {
        background: #f0f0f0 !important;
        color: #2d2d2d !important;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        margin: 0.5rem 0;
        border: 1px solid #d0d0d0;
    }
    .ai-message pre code {
        background: transparent !important;
        color: #2d2d2d !important;
        padding: 0;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* ✅ Syntax highlighting - 50% LIGHTER */
    .ai-message pre code .keyword {
        color: #0066cc;
    }
    .ai-message pre code .string {
        color: #008000;
    }
    .ai-message pre code .comment {
        color: #808080;
        font-style: italic;
    }
    .ai-message pre code .function {
        color: #cc5500;
    }
    .ai-message pre code .number {
        color: #8000cc;
    }
    .ai-message pre code .operator {
        color: #cc5500;
    }
    .ai-message pre code .variable {
        color: #2d2d2d;
    }
    
    /* ✅ FIX: User messages */
    .user-message {
        background: #667eea;
        color: white !important;
        padding: 0.8rem 1.2rem;
        border-radius: 15px 15px 5px 15px;
        max-width: 70%;
        margin: 0.5rem 0;
        margin-left: auto;
    }
    .user-message strong {
        color: white;
    }
    .user-message * {
        color: white !important;
    }
    
    /* ✅ FIX: AI message container */
    .ai-message-container {
        display: flex;
        justify-content: flex-start;
        margin: 0.5rem 0;
    }
    
    /* ✅ FIX: User message container */
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = MultiAgentSystem(max_reflection_iterations=3)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'tools' not in st.session_state:
    st.session_state.tools = Tools()
if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# ============================================================
# SIDEBAR - Configuration & Information
# ============================================================

with st.sidebar:
    st.markdown("### 🤖 System Configuration")
    
    # ✅ Agent Selection (ADDED BACK)
    st.markdown("#### 🎯 Agent Mode")
    agent_mode = st.selectbox(
        "Select Agent Mode",
        ["Auto (Supervisor)", "Research Agent", "Analysis Agent", "Creative Agent", "Verification Agent"],
        help="Choose which agent to use. Auto uses the Supervisor to route tasks."
    )
    
    # Speed vs Quality
    st.markdown("#### ⚡ Performance Mode")
    speed_mode = st.selectbox(
        "Select Mode",
        ["🚀 Fast (3-5s)", "⚖️ Balanced (6-10s)", "🧠 Thorough (10-20s)"],
        help="Fast: 1 iteration, no verification. Balanced: 2 iterations. Thorough: 3 iterations with verification."
    )

    # Map mode to configuration
    if speed_mode == "🚀 Fast (3-5s)":
        max_iterations = 1
        skip_verification = True
    elif speed_mode == "🧠 Thorough (10-20s)":
        max_iterations = 3
        skip_verification = False
    else:  # Balanced
        max_iterations = 2
        skip_verification = False
    
    # Temperature
    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more deterministic"
    )
    
    st.markdown("---")
    
    # System Status
    st.markdown("#### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🟢 Status", "Online")
    with col2:
        st.metric("🛠️ Tools", "10+")
    
    # Available Tools
    st.markdown("#### 🛠️ Available Tools")
    tools_list = [
        "🔍 Web Search", "📄 Read Webpage", "💻 Run Code",
        "📁 Read File", "✏️ Write File", "📋 List Files",
        "🧮 Calculate", "📺 YouTube Search", "🌤️ Weather", "📄 PDF Reader"
    ]
    for tool in tools_list:
        st.markdown(f"<span class='tool-badge'>{tool}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("#### 📈 Quick Stats")
    st.markdown(f"""
    - **Chats:** {len(st.session_state.chat_history)}
    - **Agents:** 5 Specialist Agents
    - **Self-Reflection:** ✅ Enabled
    - **Human-in-Loop:** ✅ Ready
    """)
    
    st.markdown("---")
    
    # Clear Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.current_result = None
        st.rerun()

# ============================================================
# MAIN CONTENT
# ============================================================

# Header
st.markdown("<h1 class='main-header'>🤖 Multi-Agent AI System</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Powered by Groq API • ReAct Framework • 5 Specialist Agents • Self-Reflection</p>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat Interface",
    "🧠 Agent Dashboard",
    "🛠️ Tool Testing",
    "📊 Analytics"
])

# ============================================================
# TAB 1: Chat Interface
# ============================================================

with tab1:
    # Chat Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask me anything...",
            placeholder="e.g., Research the latest AI trends, Write a Python function, Create a poem...",
            key="user_input"
        )
    with col2:
        submit_button = st.button("🚀 Send", use_container_width=True)
    
    # Quick example buttons
    st.markdown("#### 📝 Quick Examples")
    col1, col2, col3, col4 = st.columns(4)
    
    example_queries = [
        ("🔍 Research", "What is the capital of Japan and its population?"),
        ("💻 Code", "Write a Python function to reverse a string"),
        ("🎨 Creative", "Write a short poem about technology"),
        ("🌤️ Weather", "What is the weather in Islamabad?")
    ]
    
    for col, (label, query) in zip([col1, col2, col3, col4], example_queries):
        with col:
            if st.button(label, use_container_width=True):
                user_input = query
                submit_button = True
    
    # Process input
    if submit_button and user_input:
        with st.spinner("🧠 Processing your request..."):
            try:
                # Recreate system with selected mode
                if speed_mode == "🚀 Fast (3-5s)":
                    st.session_state.system = MultiAgentSystem(max_reflection_iterations=1, skip_verification=True)
                elif speed_mode == "🧠 Thorough (10-20s)":
                    st.session_state.system = MultiAgentSystem(max_reflection_iterations=3, skip_verification=False)
                else:  # Balanced
                    st.session_state.system = MultiAgentSystem(max_reflection_iterations=2, skip_verification=False)
                
                # Process the query
                result = st.session_state.system.process(user_input)
                st.session_state.current_result = result
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                
                # Extract final answer
                final_result = result.get('final_result', {})
                if final_result and isinstance(final_result, dict):
                    final_text = final_result.get('final_result', final_result.get('result', 'No result'))
                else:
                    final_text = str(final_result) if final_result else 'No result'
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': final_text,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'iterations': len(result.get('iterations', [])),
                    'result': result
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display chat history
    st.markdown("---")
    st.markdown("#### 💬 Conversation")
    
    if not st.session_state.chat_history:
        st.info("💡 Start a conversation by typing a message above or clicking a quick example!")
    else:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="user-message-container">
                    <div class="user-message">
                        <strong>🧑 You</strong><br>
                        {msg['content']}
                        <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 0.3rem;">
                            {msg['timestamp']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message-container">
                    <div class="ai-message">
                        <strong>🤖 AI</strong><br>
                        {msg['content']}
                        <div style="font-size: 0.7rem; color: #888; margin-top: 0.3rem;">
                            {msg['timestamp']} • {msg.get('iterations', 0)} iterations
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Expandable details for each response
                if 'result' in msg:
                    with st.expander("📊 View Details"):
                        result = msg['result']
                        st.json({
                            'task': result.get('task', ''),
                            'iterations': len(result.get('iterations', [])),
                            'agents_used': result.get('agents_used', []),
                            'final_result': str(result.get('final_result', ''))[:500] + '...'
                        })

# ============================================================
# TAB 2: Agent Dashboard
# ============================================================

with tab2:
    st.markdown("### 🧠 Agent Dashboard")
    st.markdown("View detailed information about each agent in the system.")
    
    # Agent cards
    col1, col2 = st.columns(2)
    
    agents_info = [
        {
            'name': '🔍 Research Agent',
            'role': 'Information Gathering & Summarization',
            'description': 'Searches the web, reads webpages, and summarizes information.',
            'tools': ['web_search', 'read_webpage', 'list_files'],
            'color': '#667eea'
        },
        {
            'name': '💻 Analysis Agent',
            'role': 'Problem Solving & Code Generation',
            'description': 'Writes code, analyzes problems, and provides solutions.',
            'tools': ['run_code', 'calculate', 'write_file'],
            'color': '#28a745'
        },
        {
            'name': '🎨 Creative Agent',
            'role': 'Creative Writing & Content Generation',
            'description': 'Writes poems, stories, articles, and generates creative content.',
            'tools': ['write_file', 'list_files'],
            'color': '#ffc107'
        },
        {
            'name': '✅ Verification Agent',
            'role': 'Quality Assurance & Critique',
            'description': 'Reviews outputs, identifies issues, and suggests improvements.',
            'tools': ['read_file'],
            'color': '#dc3545'
        },
        {
            'name': '👔 Supervisor Agent',
            'role': 'Orchestration & Routing',
            'description': 'Routes tasks to the right agents and coordinates the workflow.',
            'tools': ['All tools'],
            'color': '#6f42c1'
        }
    ]
    
    for i, agent in enumerate(agents_info):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class='agent-card' style='border-left-color: {agent["color"]};'>
                <h4>{agent['name']}</h4>
                <p><strong>Role:</strong> {agent['role']}</p>
                <p>{agent['description']}</p>
                <p><strong>Tools:</strong> {', '.join(agent['tools'])}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Current System Status
    st.markdown("---")
    st.markdown("#### 📊 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧠 Agents", "5", delta="Specialist")
    with col2:
        st.metric("🛠️ Tools", "10", delta="Available")
    with col3:
        st.metric("🔄 Iterations", str(max_iterations), delta="Max")
    with col4:
        st.metric("💬 Chats", str(len(st.session_state.chat_history)), delta="Total")

# ============================================================
# TAB 3: Tool Testing
# ============================================================

with tab3:
    st.markdown("### 🛠️ Tool Testing Console")
    st.markdown("Test individual tools directly to see their outputs.")
    
    # Tool selector
    tool_options = {
        "Web Search": "web_search",
        "Read Webpage": "read_webpage",
        "Run Code": "run_code",
        "Read File": "read_file",
        "Write File": "write_file",
        "List Files": "list_files",
        "Calculate": "calculate",
        "YouTube Search": "youtube_search",
        "Weather": "get_weather",
        "PDF Reader": "read_pdf"
    }
    
    selected_tool = st.selectbox("Select a tool to test:", list(tool_options.keys()))
    tool_name = tool_options[selected_tool]
    
    # Tool-specific input
    if tool_name in ['web_search', 'youtube_search']:
        tool_input = st.text_input("Search Query:", placeholder="Enter your search query...")
    elif tool_name == 'read_webpage':
        tool_input = st.text_input("URL:", placeholder="https://example.com")
    elif tool_name in ['run_code']:
        tool_input = st.text_area("Python Code:", placeholder="print('Hello, World!')", height=150)
    elif tool_name == 'read_file':
        tool_input = st.text_input("Filename:", placeholder="example.txt")
    elif tool_name == 'write_file':
        col1, col2 = st.columns(2)
        with col1:
            filename = st.text_input("Filename:", placeholder="example.txt")
        with col2:
            content = st.text_area("Content:", placeholder="Your content here...")
        tool_input = f"{filename}|||{content}"
    elif tool_name == 'calculate':
        tool_input = st.text_input("Expression:", placeholder="2 + 2 * 10")
    elif tool_name == 'get_weather':
        tool_input = st.text_input("City:", placeholder="London, UK")
    elif tool_name == 'read_pdf':
        tool_input = st.text_input("PDF Filename:", placeholder="document.pdf")
    else:
        tool_input = st.text_input("Input:")
    
    # Execute button
    if st.button("🔄 Execute Tool", use_container_width=True):
        if tool_input:
            with st.spinner(f"Executing {selected_tool}..."):
                try:
                    tools = st.session_state.tools
                    tool_func = getattr(tools, tool_name)
                    
                    if tool_name == 'write_file':
                        parts = tool_input.split('|||')
                        if len(parts) == 2:
                            result = tool_func(parts[0], parts[1])
                        else:
                            result = "❌ Please provide both filename and content."
                    else:
                        result = tool_func(tool_input)
                    
                    st.markdown("#### 📤 Result")
                    st.markdown(f"""
                    <div class='response-box'>
                        {result}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please provide input for the tool.")
    
    st.markdown("---")
    st.info("💡 Tip: Tools are also used automatically by the agents in the Chat Interface tab.")

# ============================================================
# TAB 4: Analytics
# ============================================================

with tab4:
    st.markdown("### 📊 Analytics Dashboard")
    st.markdown("View performance metrics and insights from your conversations.")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_chats = len(st.session_state.chat_history) // 2
    total_iterations = sum([
        msg.get('iterations', 0) 
        for msg in st.session_state.chat_history 
        if msg['role'] == 'assistant'
    ])
    
    with col1:
        st.metric("💬 Total Conversations", total_chats)
    with col2:
        st.metric("🔄 Total Iterations", total_iterations)
    with col3:
        avg_iter = total_iterations / total_chats if total_chats > 0 else 0
        st.metric("📊 Avg Iterations", f"{avg_iter:.1f}")
    with col4:
        st.metric("📈 Success Rate", "100%")
    
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("#### 📋 Conversation History")
        
        # Create a table of conversations
        chat_data = []
        for i in range(0, len(st.session_state.chat_history), 2):
            if i+1 < len(st.session_state.chat_history):
                user_msg = st.session_state.chat_history[i]
                ai_msg = st.session_state.chat_history[i+1]
                chat_data.append({
                    'User Query': user_msg['content'][:50] + '...' if len(user_msg['content']) > 50 else user_msg['content'],
                    'Response Length': len(ai_msg['content']),
                    'Iterations': ai_msg.get('iterations', 0),
                    'Time': user_msg['timestamp']
                })
        
        if chat_data:
            import pandas as pd
            df = pd.DataFrame(chat_data)
            st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### 📤 Export Data")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export JSON", use_container_width=True):
                json_data = json.dumps(st.session_state.chat_history, default=str, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        with col2:
            if st.button("🔄 Reset Analytics", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.info("💡 Start a conversation to see analytics data here.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem;">
    <p>🤖 Multi-Agent AI System • Built with Groq API • ReAct Framework</p>
    <p>🔍 Research Agent • 💻 Analysis Agent • 🎨 Creative Agent • ✅ Verification Agent • 👔 Supervisor Agent</p>
    <p>🛠️ 10+ Tools • Self-Reflection Loop • Human-in-the-Loop Ready</p>
</div>
""", unsafe_allow_html=True)