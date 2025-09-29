__version__ = "1.0.0"

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import base64 
from io import BytesIO

GLOSSARY_DATA = "data/glossary.csv"
VIVA_DATA = "data/viva.csv"
LOGO_IMG = "images/logo.png"


st.set_page_config(page_title="Viva Q&A Review", layout="wide")

def load_qa_data(file_data):
    """
    Load Q&A data from CSV file or file object
    Returns DataFrame or None if loading fails
    """
    try:
        # Handle both file paths and file objects
        df = pd.read_csv(file_data, encoding='cp1252')
        
        # Handle the 4-column structure: Section, Question Number, Question, Answer
        if 'Question Number' in df.columns:
            df = df.rename(columns={'Question Number': 'question_num'})
        elif len(df.columns) == 4:
            df.columns = ['Section', 'question_num', 'Question', 'Answer']
        elif len(df.columns) == 3:
            df.columns = ['question_num', 'Question', 'Answer']
            
        return df
    except Exception as e:
        return None

def load_glossary_data(file_data):
    """
    Load Glossary data from CSV file
    Returns DataFrame or None if loading fails
    """
    try:
        df = pd.read_csv(file_data, encoding='utf-8')
        return df
    except Exception as e:
        return None

def show_header():
    """
    Display the common header for both tabs    
    """
    col_title, col_logo = st.columns(2, border=False, vertical_alignment="center")
    with col_title:
        st.title(":blue[PhD Viva Q&A]")    
        
    with col_logo:
        try:
            # Load the image that works
            image = Image.open(LOGO_IMG)

            # Convert to base64 for the HTML
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Use in markdown with link
            st.markdown(
                f'''<a href="https://thinkingml.com" style="
                    font-family: inherit;
                    font-weight: 500;
                    text-decoration: none;
                    font-size: 1.25rem;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: #5f6f8c !important;
                ">
                <img src="data:image/png;base64,{img_str}" width="40" />  thinkingML</a>''', 
                unsafe_allow_html=True)
            
        except Exception:
        # Fallback to styled text if image loading fails
            st.markdown(
                '''
                <a href="https://thinkingml.com" style="
                    font-family: inherit;
                    font-weight: 500;
                    text-decoration: none;
                    font-size: 1.25rem;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: #5f6f8c !important;
                ">thinkingML</a>
                ''',
                unsafe_allow_html=True
            )


def viva_tab():
    """
    Content for the Viva Q&A tab
    Includes section filtering, navigation, and progress bar        
    """
    show_header()
   
    df = load_qa_data(VIVA_DATA)
    
    if df is not None and not df.empty:
        total_sections = len(df['Section'].unique())            
        
        # Initialize session state
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
                
        # Section filtering - moved up before any navigation
        st.markdown("""
            <style>
                [data-testid="stMultiSelect"] span {
                    background: slategrey !important;
                    font-weight: 500 !important;
                }
            </style>
            """, unsafe_allow_html=True)
        
        # Get current selection from session state
        current_sections = st.session_state.get('selected_sections', df['Section'].unique().tolist())            
        filter_text = "🔍 Filter Sections"

        with st.expander(filter_text):
            all_sections = df['Section'].unique().tolist()
            selected_sections = st.multiselect(
                "Select sections to include:",
                options=all_sections,
                default=current_sections,
                label_visibility="collapsed",
                key="section_filter"
            )            
            # Update session state
            st.session_state.selected_sections = selected_sections
            
            # Create filtered and ordered dataframe
            if selected_sections:
                # Filter the dataframe
                filtered_df = df[df['Section'].isin(selected_sections)].copy()
                # Reorder based on selection order
                filtered_df['section_order'] = pd.Categorical(
                    filtered_df['Section'], 
                    categories=selected_sections, 
                    ordered=True
                )
                filtered_df = filtered_df.sort_values(['section_order', 'question_num']).drop('section_order', axis=1).reset_index(drop=True)
            else:
                filtered_df = pd.DataFrame()  # Empty dataframe when nothing selected
            
        # Show status info
        st.info(f"Showing {len(filtered_df)} of {len(df)} questions ({len(selected_sections)}/{total_sections})")
        
        # Handle empty filtered results
        if len(filtered_df) == 0:
            st.warning("No questions to display. Please select at least one section.")
            # Show disabled navigation buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.button("⏮ First", disabled=True)
            with col2:
                st.button("⏪ Previous", disabled=True)
            with col3:
                st.button("⏩ Next", disabled=True)
            with col4:
                st.button("⏭ Last", disabled=True)
            with col5:
                st.button("🔀 Random", disabled=True)
            return
        
        # Adjust current_index if it's beyond filtered results
        if st.session_state.current_index >= len(filtered_df):
            st.session_state.current_index = len(filtered_df) - 1
        
        # Progress indicator (using filtered dataframe)
        progress = (st.session_state.current_index + 1) / len(filtered_df)
        st.progress(progress, text=f"Question {st.session_state.current_index + 1} of {len(filtered_df)}")
        
        # Navigation buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⏮ First"):
                st.session_state.current_index = 0                
                st.rerun()
        
        with col2:
            if st.button("⏪ Previous"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1                    
                    st.rerun()
        
        with col3:
            if st.button("⏩ Next"):
                if st.session_state.current_index < len(filtered_df) - 1:
                    st.session_state.current_index += 1                    
                    st.rerun()
        
        with col4:
            if st.button("⏭ Last"):
                st.session_state.current_index = len(filtered_df) - 1                
                st.rerun()
        
        with col5:
            if st.button("🔀 Random"):
                import random
                st.session_state.current_index = random.randint(0, len(filtered_df) - 1)                
                st.rerun()
        
        # Current question (from filtered dataframe)
        current_row = filtered_df.iloc[st.session_state.current_index]
        
        st.markdown(f"### {current_row.get('Section', st.session_state.current_index + 1)}  Q{current_row.get('question_num', st.session_state.current_index + 1)}")
        st.markdown(f"**:blue[{current_row['Question']}]**")

        st.markdown("### Answer:")
        st.markdown(f"*{current_row['Answer']}*")
        
        st.markdown("---")
        
    else:
        st.error("⚠️ Could not load viva data")

def glossary_tab():
    """
    Content for the Glossary tab
    Custom html table - mainly to accommodate word-wrap due to some lengthy
    definitions.
    """
    
    show_header()    
    df = load_glossary_data(GLOSSARY_DATA)
    
    if df is not None and not df.empty:
        st.info(f"Glossary contains {len(df)} terms")
        
        # custom-table - simple and effective
        table_html = """
            <style>
                .glossary-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: Arial, sans-serif;
                }
                .glossary-table th {
                    background-color: #f0f2f6;
                    font-weight: bold;
                    padding: 8px;
                    text-align: left;
                    border-bottom: 2px solid #e6e6e6;
                }
                .glossary-table td {
                    padding: 8px;
                    border-bottom: 1px solid #e6e6e6;
                    word-wrap: break-word;
                }
                .glossary-table tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                .term-column {
                    color: darkslategrey;
                    
                }
                .definition-column {
                    color: slategrey;
                }
            </style>

            <table class='glossary-table'>
                <tr>
                    <th>Term</th>
                    <th>Definition</th>
                </tr>
            """

        for _, row in df.iterrows():
            table_html += f"""
                <tr>
                    <td class='term-column'>{row['Term']}</td>
                    <td class='definition-column'>{row['Definition']}</td>
                </tr>
            """

        table_html += "</table>"
        components.html(table_html, height=500, scrolling=True)

    else:
        st.error("⚠️ Could not load glossary data")

def main():
    """Main application function"""           
    tab_viva, tab_glossary = st.tabs(["🎓:blue[Viva Q&A]", "📖:blue[Glossary]"])
    
    with tab_viva:
        viva_tab()
    
    with tab_glossary:
        glossary_tab()

if __name__ == "__main__":
    main()