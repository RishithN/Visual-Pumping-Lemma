"""
Main Streamlit application for Visual Pumping Lemma Demonstrator
"""
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any, List

from language_parser import LanguageParser
from pumping_engine import PumpingEngine
from visualizer import PumpingVisualizer
from utils import generate_test_strings, validate_language_input
import config

# Set page configuration
st.set_page_config(
    page_title="Visual Pumping Lemma Demonstrator",
    page_icon="🔁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def get_components():
    return LanguageParser(), PumpingEngine(), PumpingVisualizer()

parser, engine, visualizer = get_components()

def styled_success(message: str):
    """Display a styled success message"""
    st.markdown(f"""
    <div class="success-box">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">✅</span>
            <span style="font-weight: 600; font-size: 1.1rem;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def styled_error(message: str):
    """Display a styled error message"""
    st.markdown(f"""
    <div class="error-box">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">❌</span>
            <span style="font-weight: 600; font-size: 1.1rem;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def styled_info(message: str):
    """Display a styled info message"""
    st.markdown(f"""
    <div class="info-box">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">ℹ️</span>
            <span style="font-weight: 600; font-size: 1.1rem;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(title: str, description: str, icon: str):
    """Create a feature card with icon"""
    st.markdown(f"""
    <div class="custom-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <span style="font-size: 2rem;">{icon}</span>
            <h3 style="margin: 0; color: #4B0082;">{title}</h3>
        </div>
        <p style="margin: 0; color: #666; line-height: 1.6;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Enhanced Custom CSS with Pale Purple Background
    st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #e6e6fa 0%, #d8bfd8 100%) !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #e6e6fa 0%, #d8bfd8 100%) !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #4B0082 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(75, 0, 130, 0.2);
        border: 3px solid #9370DB;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #4B0082;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-left: 5px solid #9370DB;
        padding-left: 15px;
        background: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #9370DB 0%, #8A2BE2 100%) !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #9370DB 0%, #8A2BE2 100%) !important;
    }
    
    /* Sidebar Header - Black Color */
    .sidebar-header {
        color: #000000 !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #9370DB, #8A2BE2);
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 4px 15px 0 rgba(147, 112, 219, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #8A2BE2, #9370DB);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(147, 112, 219, 0.4);
    }
    
    /* Secondary Button */
    .stButton>button.kind-secondary {
        background: linear-gradient(45deg, #20B2AA, #48D1CC) !important;
    }
    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #9370DB;
        backdrop-filter: blur(10px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, #9370DB, #8A2BE2) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border: none !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 0 0 10px 10px !important;
        padding: 20px !important;
        border: 2px solid #9370DB;
        border-top: none !important;
    }
    
    /* Radio Buttons */
    .st-bb {
        background-color: rgba(255,255,255,0.9);
    }
    
    .st-bc {
        background-color: #9370DB;
    }
    
    /* Select Box Styling */
    .stSelectbox>div>div {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        border: 2px solid #9370DB;
    }
    
    /* Text Input Styling */
    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        border: 2px solid #9370DB;
        padding: 10px;
    }
    
    /* Text Area Styling */
    .stTextArea>div>div>textarea {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        border: 2px solid #9370DB;
        padding: 15px;
    }
    
    /* Slider Styling - WHITE SLIDER */
    .stSlider>div>div>div {
        background: #FFFFFF !important;
        border: 2px solid #9370DB !important;
        border-radius: 10px !important;
    }
    
    .stSlider>div>div>div>div {
        background: #9370DB !important;
        border-radius: 50% !important;
    }
    
    /* Slider track - the line */
    .stSlider div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFFFFF !important;
    }
    
    /* Slider Labels - Remove purple highlight, keep black */
    .stSlider label {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Remove purple background from slider value labels */
    .stSlider div[data-baseweb="slider"] div div div {
        color: #000000 !important;
        background: transparent !important;
        padding: 0px !important;
    }
    
    /* Specifically target the min and max value labels */
    .stSlider div[data-baseweb="slider"] > div > div > div:first-child,
    .stSlider div[data-baseweb="slider"] > div > div > div:last-child {
        background: transparent !important;
        color: #000000 !important;
    }
    
    /* Success/Error/Info Boxes */
    .success-box {
        background: linear-gradient(45deg, #E8F5E8, #C8E6C9) !important;
        color: #2E7D32 !important;
        border: 2px solid #81C784 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 6px 20px rgba(200, 230, 201, 0.3) !important;
    }
    
    .error-box {
        background: linear-gradient(45deg, #FFEBEE, #FFCDD2) !important;
        color: #C62828 !important;
        border: 2px solid #E57373 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 6px 20px rgba(255, 205, 210, 0.3) !important;
    }
    
    .info-box {
        background: linear-gradient(45deg, #E3F2FD, #BBDEFB) !important;
        color: #1565C0 !important;
        border: 2px solid #64B5F6 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 6px 20px rgba(187, 222, 251, 0.3) !important;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        border: 2px solid #9370DB !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(45deg, #9370DB, #8A2BE2) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Custom Cards */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid #9370DB;
        backdrop-filter: blur(10px);
    }
    
    /* Animation for headers */
    @keyframes gentle-glow {
        0% { box-shadow: 0 0 10px rgba(147, 112, 219, 0.5); }
        50% { box-shadow: 0 0 20px rgba(147, 112, 219, 0.8); }
        100% { box-shadow: 0 0 10px rgba(147, 112, 219, 0.5); }
    }
    
    .glow-card {
        animation: gentle-glow 3s ease-in-out infinite;
    }
    
    /* Loading Spinner */
    .stSpinner>div>div {
        border-color: #9370DB !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #4B0082;
        font-size: 0.9rem;
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        border: 2px solid #9370DB;
    }
    
    /* Info Metric Styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: bold !important;
        color: #4B0082 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #4B0082 !important;
        font-weight: 600 !important;
    }
    
    /* Slider value labels - ensure no background */
    .stSlider [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        background: transparent !important;
    }
    
    /* Remove any background from slider tick labels */
    .stSlider div[role="slider"] ~ div div {
        background: transparent !important;
        color: #000000 !important;
    }
    
    /* Target the specific elements that show min and max values */
    div[data-baseweb="slider"] > div:first-child > div:first-child,
    div[data-baseweb="slider"] > div:first-child > div:last-child {
        background: transparent !important;
        color: #000000 !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .sub-header {
            font-size: 1.4rem;
        }
    }
    
    /* Block Container Styling */
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Header with Features
    st.markdown("""
    <div class="main-header glow-card">
        🔁 Visual Pumping Lemma Demonstrator
        <div style="font-size: 1.2rem; color: #666; margin-top: 10px; font-weight: normal;">
            An Interactive Educational Tool for Theory of Computation
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_feature_card(
            "Interactive Visualization", 
            "Watch pumping lemma in action with animated decompositions and color-coded segments",
            "🎨"
        )
    
    with col2:
        create_feature_card(
            "Dual Lemma Support", 
            "Supports both Regular and Context-Free pumping lemmas with detailed analysis",
            "🔀"
        )
    
    with col3:
        create_feature_card(
            "Educational Tool", 
            "Perfect for students and researchers to understand formal language theory",
            "📚"
        )
    
    # Enhanced Sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #000000; margin-bottom: 30px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);" class="sidebar-header">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Lemma type selection
    lemma_type = st.sidebar.radio(
        "Select Pumping Lemma Type:",
        ["Regular Languages", "Context-Free Languages"],
        help="Choose between regular and context-free pumping lemmas"
    )
    
    # Language input method
    input_method = st.sidebar.radio(
        "Language Input Method:",
        ["Predefined Examples", "Custom Language"]
    )
    
    # Main content area
    if input_method == "Predefined Examples":
        render_predefined_interface(lemma_type)
    else:
        render_custom_interface(lemma_type)
    
    # Additional features in expanders
    with st.expander("📚 Educational Resources", expanded=False):
        render_educational_resources(lemma_type)
    
    with st.expander("📊 Advanced Analysis", expanded=False):
        render_advanced_analysis()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🔬 <strong>Visual Pumping Lemma Demonstrator</strong> - Theory of Computation Project</p>
        <p>Built with ❤️ using Streamlit | An educational tool for formal language theory</p>
    </div>
    """, unsafe_allow_html=True)

def render_predefined_interface(lemma_type: str):
    """Render interface for predefined language examples"""
    
    st.markdown('<div class="sub-header">🎯 Predefined Language Examples</div>', 
                unsafe_allow_html=True)
    
    # Filter examples based on lemma type
    if lemma_type == "Regular Languages":
        lang_category = {**config.PREDEFINED_LANGUAGES['regular'], 
                        **config.PREDEFINED_LANGUAGES['non_regular']}
    else:
        lang_category = config.PREDEFINED_LANGUAGES['context_free']
    
    # Language selection
    selected_lang_key = st.selectbox(
        "Select a language:",
        options=list(lang_category.keys()),
        format_func=lambda x: f"{x}: {lang_category[x]['description']}"
    )
    
    selected_lang = lang_category[selected_lang_key]
    
    # Display language info
    col1, col2, col3 = st.columns(3)
    with col1:
        styled_info(f"**Pattern:** {selected_lang['pattern']}")
    with col2:
        styled_info(f"**Type:** {selected_lang['type']}")
    with col3:
        styled_info(f"**Description:** {selected_lang['description']}")
    
    # Generate sample strings
    sample_strings = parser.generate_sample_strings(selected_lang['pattern'])
    
    # String selection
    selected_string = st.selectbox(
        "Select or enter a test string:",
        options=sample_strings,
        index=min(2, len(sample_strings) - 1)
    )
    
    # Custom string input
    custom_string = st.text_input("Or enter custom string:", value="")
    if custom_string:
        selected_string = custom_string
    
    # Pumping length
    st.markdown("<div style='margin-bottom: 10px;'><strong>Pumping Length (p):</strong></div>", unsafe_allow_html=True)
    p = st.slider(
        "Pumping Length (p):",
        min_value=1,
        max_value=10,
        value=config.calculate_pumping_length(selected_lang['type'], selected_lang['pattern']),
        help="The pumping length constant",
        label_visibility="collapsed"  # Hide the default label since we added our own
    )
    
    # Analyze button
    if st.button("🔍 Analyze with Pumping Lemma", type="primary"):
        perform_analysis(lemma_type, selected_lang, selected_string, p)

def render_custom_interface(lemma_type: str):
    """Render interface for custom language input"""
    
    st.markdown('<div class="sub-header">🛠️ Custom Language Analysis</div>', 
                unsafe_allow_html=True)
    
    # Language input
    lang_input = st.text_area(
        "Enter your language pattern:",
        value="a^n b^n",
        help="Examples: a^n b^n, a*b*, ww, w w_reverse, (ab)*, a^n b^n c^n"
    )
    
    if st.button("Validate Language Pattern", type="secondary"):
        is_valid, message, lang_info = validate_language_input(lang_input)
        
        if is_valid:
            styled_success(f"Valid pattern: {message}")
            st.session_state['custom_lang'] = lang_info
        else:
            styled_error(f"{message}")
            return
    
    if 'custom_lang' in st.session_state:
        lang_info = st.session_state['custom_lang']
        
        # Display language info
        col1, col2 = st.columns(2)
        with col1:
            styled_info(f"**Detected Pattern:** {lang_info['pattern']}")
        with col2:
            styled_info(f"**Inferred Type:** {lang_info['type']}")
        
        # Complexity analysis
        complexity = parser.analyze_language_complexity(lang_info['pattern'])
        if complexity:
            with st.expander("🔬 Language Complexity Analysis"):
                st.write(f"**Level:** {complexity.get('level', 'Unknown')}")
                st.write(f"**Automaton:** {complexity.get('automaton', 'Unknown')}")
                st.write(f"**Grammar:** {complexity.get('grammar', 'Unknown')}")
        
        # String input
        test_string = st.text_input("Test string:", value="aaabbb")
        
        # Pumping length
        st.markdown("<div style='margin-bottom: 10px;'><strong>Pumping Length (p):</strong></div>", unsafe_allow_html=True)
        p = st.slider(
            "Pumping Length (p):",
            min_value=1,
            max_value=10,
            value=config.calculate_pumping_length(lang_info['type'], lang_info['pattern']),
            label_visibility="collapsed"  # Hide the default label since we added our own
        )
        
        if st.button("🔍 Analyze Custom Language", type="primary"):
            perform_analysis(lemma_type, lang_info, test_string, p)

def perform_analysis(lemma_type: str, language_info: Dict, test_string: str, p: int):
    """Perform pumping lemma analysis and display results"""
    
    st.markdown('<div class="sub-header">📊 Analysis Results</div>', 
                unsafe_allow_html=True)
    
    # Perform analysis based on lemma type
    if lemma_type == "Regular Languages":
        result = engine.apply_regular_pumping_lemma(
            language_info['pattern'], test_string, p
        )
    else:
        result = engine.apply_cfl_pumping_lemma(
            language_info['pattern'], test_string, p
        )
    
    # Display results
    if "error" in result:
        styled_error(f"Error: {result['error']}")
        return
    
    # Result summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("String", result["string"])
    with col2:
        st.metric("Length", len(result["string"]))
    with col3:
        st.metric("Pumping Length", p)
    with col4:
        status_color = "🟢" if result["lemma_holds"] else "🔴"
        st.metric("Lemma Result", f"{status_color} {result['language_type']}")
    
    # Visualization
    st.subheader("🎨 Visualization")
    
    if lemma_type == "Regular Languages":
        fig = visualizer.create_regular_pumping_visualization(
            result["decomposition"], result["iterations"], result
        )
    else:
        fig = visualizer.create_cfl_pumping_visualization(
            result["decomposition"], result["iterations"], result
        )
    
    st.pyplot(fig)
    
    # Detailed results
    st.subheader("🔍 Detailed Analysis")
    
    # Create results table
    results_data = []
    for iteration in result["iterations"]:
        results_data.append({
            "i": iteration["i"],
            "Pumped String": iteration["pumped_string"],
            "Length": len(iteration["pumped_string"]),
            "In Language": "✅ Yes" if iteration["in_language"] else "❌ No"
        })
    
    st.table(pd.DataFrame(results_data))
    
    # Decomposition details
    with st.expander("🧩 Decomposition Details"):
        if lemma_type == "Regular Languages":
            decomp = result["decomposition"]
            st.write(f"**x:** '{decomp.get('x', '')}' (length: {len(decomp.get('x', ''))})")
            st.write(f"**y:** '{decomp.get('y', '')}' (length: {len(decomp.get('y', ''))})")
            st.write(f"**z:** '{decomp.get('z', '')}' (length: {len(decomp.get('z', ''))})")
            st.write(f"**|xy|:** {len(decomp.get('x', '') + decomp.get('y', ''))} ≤ p = {p}")
            st.write(f"**|y|:** {len(decomp.get('y', ''))} > 0")
        else:
            decomp = result["decomposition"]
            st.write(f"**u:** '{decomp.get('u', '')}'")
            st.write(f"**v:** '{decomp.get('v', '')}'")
            st.write(f"**w:** '{decomp.get('w', '')}'")
            st.write(f"**x:** '{decomp.get('x', '')}'")
            st.write(f"**y:** '{decomp.get('y', '')}'")
            st.write(f"**|vwx|:** {len(decomp.get('v', '') + decomp.get('w', '') + decomp.get('x', ''))} ≤ p = {p}")
            st.write(f"**|vx|:** {len(decomp.get('v', '') + decomp.get('x', ''))} > 0")
    
    # Conclusion
    st.subheader("🎯 Conclusion")
    
    if result["lemma_holds"]:
        styled_success(
            f"The Pumping Lemma **holds** for this decomposition. "
            f"The language is **{result['language_type']}**."
        )
    else:
        styled_error(
            f"The Pumping Lemma **fails** for this string. "
            f"The language is **{result['language_type']}**."
        )
        
        # Show counterexample
        counterexample = next(
            (iter for iter in result["iterations"] if not iter["in_language"]), 
            None
        )
        if counterexample:
            st.warning(
                f"Counterexample found at i={counterexample['i']}: "
                f"'{counterexample['pumped_string']}' is not in the language."
            )

def render_educational_resources(lemma_type: str):
    """Render educational content"""
    
    st.write("### Pumping Lemma Overview")
    
    if lemma_type == "Regular Languages":
        st.latex(r"""
        \text{For any regular language } L, \exists p \geq 1 \text{ such that } \\
        \forall s \in L \text{ with } |s| \geq p, \exists x,y,z \text{ with:} \\
        s = xyz \\
        |y| > 0, |xy| \leq p \\
        \forall i \geq 0, xy^iz \in L
        """)
        
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #4B0082; margin-bottom: 10px;">Key Points:</h4>
            <ul style="color: #666; line-height: 1.6;">
                <li>Applies to <strong>all regular languages</strong></li>
                <li>Used to prove languages are <strong>not regular</strong></li>
                <li>If lemma fails ⇒ language is <strong>not regular</strong></li>
                <li>If lemma holds ⇒ language <strong>might be regular</strong> (but not guaranteed)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.latex(r"""
        \text{For any CFL } L, \exists p \geq 1 \text{ such that } \\
        \forall s \in L \text{ with } |s| \geq p, \exists u,v,w,x,y \text{ with:} \\
        s = uvwxy \\
        |vx| > 0, |vwx| \leq p \\
        \forall i \geq 0, uv^iwx^iy \in L
        """)
        
        st.markdown("""
        <div class="custom-card">
            <h4 style="color: #4B0082; margin-bottom: 10px;">Key Points:</h4>
            <ul style="color: #666; line-height: 1.6;">
                <li>Applies to <strong>all context-free languages</strong></li>
                <li>Used to prove languages are <strong>not context-free</strong></li>
                <li>More complex than regular pumping lemma</li>
                <li>Both <strong>v and x are pumped simultaneously</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### Common Language Patterns")
    patterns_df = pd.DataFrame([
        {"Language": "aⁿbⁿ", "Type": "Context-Free", "Regular": "No", "CFL": "Yes"},
        {"Language": "aⁿbᵐ", "Type": "Regular", "Regular": "Yes", "CFL": "Yes"},
        {"Language": "aⁿbⁿcⁿ", "Type": "Context-Sensitive", "Regular": "No", "CFL": "No"},
        {"Language": "ww", "Type": "Context-Sensitive", "Regular": "No", "CFL": "No"},
        {"Language": "wwᴿ", "Type": "Context-Free", "Regular": "No", "CFL": "Yes"},
    ])
    st.table(patterns_df)
    
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: #4B0082; margin-bottom: 15px;">🎯 How to Use This Tool</h3>
        <div style="display: grid; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</span>
                <span><strong>Select Lemma Type</strong>: Choose between Regular or Context-Free</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</span>
                <span><strong>Choose Language</strong>: Pick from examples or enter custom pattern</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">3</span>
                <span><strong>Select Test String</strong>: Use suggested strings or enter your own</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">4</span>
                <span><strong>Adjust Pumping Length</strong>: Modify p value if needed</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">5</span>
                <span><strong>Analyze</strong>: Click the analyze button to see results</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #9370DB; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold;">6</span>
                <span><strong>Interpret</strong>: Check if pumping lemma holds or fails</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_advanced_analysis():
    """Render advanced analysis features"""
    
    st.write("### Batch Analysis")
    
    st.markdown("""
    <div class="custom-card">
        <h4 style="color: #4B0082; margin-bottom: 10px;">Batch Analysis Feature</h4>
        <p style="color: #666; margin: 0;">
            Test multiple strings simultaneously to see patterns in pumping behavior.
            This helps identify whether the language consistently satisfies or violates the pumping lemma conditions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Multiple string analysis
    st.write("#### Test Multiple Strings")
    test_strings_input = st.text_area(
        "Enter multiple test strings (one per line):",
        value="ab\naabb\naaabbb\naaaabbbb",
        help="Enter one string per line"
    )
    
    if st.button("Run Batch Analysis"):
        strings = [s.strip() for s in test_strings_input.split('\n') if s.strip()]
        
        if strings:
            st.write("**Batch Results:**")
            results = []
            
            for test_str in strings:
                # Simple analysis for demonstration
                if test_str.count('a') == test_str.count('b') and 'a' in test_str and 'b' in test_str:
                    lang_type = "Possibly aⁿbⁿ"
                    status = "⚠️ Check carefully"
                elif 'a' in test_str and 'b' in test_str:
                    lang_type = "Possibly aⁿbᵐ" 
                    status = "✅ Likely regular"
                else:
                    lang_type = "Other pattern"
                    status = "🔍 Needs analysis"
                
                results.append({
                    "String": test_str,
                    "Length": len(test_str),
                    "a-count": test_str.count('a'),
                    "b-count": test_str.count('b'),
                    "Type": lang_type,
                    "Status": status
                })
            
            st.table(pd.DataFrame(results))
    
    st.write("### Language Family Classification")
    
    classification_data = {
        "Language Family": ["Regular", "Context-Free", "Context-Sensitive", "Recursively Enumerable"],
        "Automaton": ["DFA/NFA", "PDA", "LBA", "Turing Machine"],
        "Grammar": ["Regular", "Context-Free", "Context-Sensitive", "Unrestricted"],
        "Closed Under": ["Union, Concatenation, Kleene*", "All regular operations", "All CFL operations", "All CSL operations"]
    }
    
    st.table(pd.DataFrame(classification_data))

if __name__ == "__main__":
    main()