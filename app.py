# Resume Keyword Matcher - Enhanced Streamlit App
# Now with .docx/.pdf support, synonym matching, and skill categorization

import streamlit as st
import re
from collections import Counter
import nltk
import io
from docx import Document
import PyPDF2

# Set up the page
st.set_page_config(
    page_title="Resume Keyword Matcher Pro",
    page_icon="🔍",
    layout="centered"
)

# Title and description
st.title("🔍 Resume Keyword Matcher Pro")
st.markdown("Upload your resume and job description to analyze keyword matches, missing skills, and get improvement suggestions!")
st.markdown("---")

# Initialize NLTK data with error handling
@st.cache_resource
def setup_nltk():
    """
    Download required NLTK data with progress indication
    """
    try:
        nltk.data.find('corpora/wordnet')
        return True
    except LookupError:
        with st.spinner("📥 Downloading language data (first time only)..."):
            try:
                nltk.download('wordnet', quiet=True)
                return True
            except Exception as e:
                st.error(f"Failed to download required data: {e}")
                return False

# Setup NLTK
nltk_ready = setup_nltk()

if nltk_ready:
    from nltk.corpus import wordnet
else:
    # Fallback: create a dummy wordnet module
    class DummyWordnet:
        def synsets(self, word):
            return []
    wordnet = DummyWordnet()

def extract_text_from_file(uploaded_file):
    """
    Enhanced function to read text from .txt, .docx, and .pdf files
    """
    if uploaded_file is not None:
        try:
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'txt':
                # Read text file
                text = uploaded_file.getvalue().decode("utf-8")
                return text
                
            elif file_type == 'docx':
                # Read Word document
                doc = Document(io.BytesIO(uploaded_file.getvalue()))
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return text
                
            elif file_type == 'pdf':
                # Read PDF file
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
                return text
                
            else:
                st.error(f"Unsupported file type: {file_type}")
                return ""
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            return ""
    return ""

def clean_text(text):
    """
    Clean and prepare text for analysis
    """
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def get_synonyms(word):
    """
    Get synonyms for a word using WordNet with fallback
    """
    synonyms = set()
    try:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym != word and len(synonym.split()) == 1:
                    synonyms.add(synonym)
        return list(synonyms)[:3]  # Return top 3 synonyms
    except:
        # Fallback if wordnet is not available
        return []

def categorize_keyword(keyword):
    """
    Categorize keywords into technical skills, soft skills, or tools
    """
    # Technical skills patterns
    technical_patterns = [
        r'.*programming.*', r'.*development.*', r'.*engineering.*', r'.*coding.*',
        r'.*algorithm.*', r'.*data.*structure.*', r'.*database.*', r'.*sql.*',
        r'.*python.*', r'.*java.*', r'.*javascript.*', r'.*react.*', r'.*node.*',
        r'.*machine.learning.*', r'.*ai.*', r'.*cloud.*', r'.*aws.*', r'.*azure.*',
        r'.*docker.*', r'.*kubernetes.*', r'.*devops.*', r'.*api.*', r'.*web.*',
        r'.*mobile.*', r'.*software.*', r'.*system.*', r'.*network.*', r'.*security.*'
    ]
    
    # Tools and technologies
    tools_patterns = [
        r'^[a-z]+\+?$', r'.*tool.*', r'.*framework.*', r'.*library.*', r'.*platform.*',
        r'.*git.*', r'.*jenkins.*', r'.*jira.*', r'.*excel.*', r'.*tableau.*',
        r'.*photoshop.*', r'.*figma.*', r'.*word.*', r'.*powerpoint.*'
    ]
    
    # Soft skills patterns
    soft_patterns = [
        r'.*communication.*', r'.*teamwork.*', r'.*leadership.*', r'.*problem.solving.*',
        r'.*critical.thinking.*', r'.*adaptability.*', r'.*creativity.*', r'.*time.management.*',
        r'.*collaboration.*', r'.*negotiation.*', r'.*presentation.*', r'.*analytical.*',
        r'.*strategic.*', r'.*innovative.*', r'.*proactive.*', r'.*organized.*'
    ]
    
    for pattern in technical_patterns:
        if re.match(pattern, keyword, re.IGNORECASE):
            return "Technical Skills"
    
    for pattern in tools_patterns:
        if re.match(pattern, keyword, re.IGNORECASE):
            return "Tools & Technologies"
    
    for pattern in soft_patterns:
        if re.match(pattern, keyword, re.IGNORECASE):
            return "Soft Skills"
    
    return "Other Skills"

def extract_keywords(text):
    """
    Enhanced keyword extraction with categorization and synonym detection
    """
    # Clean the text first
    text = clean_text(text)
    
    # Find all words (alphanumeric characters, 3+ letters)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    
    # Enhanced stop words list
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'your', 'has', 'had', 
        'her', 'his', 'how', 'out', 'see', 'now', 'one', 'may', 'get', 'its', 'who', 'than', 
        'been', 'any', 'our', 'from', 'with', 'this', 'that', 'have', 'will', 'would', 'should', 
        'could', 'what', 'when', 'where', 'which', 'there', 'their', 'they', 'them', 'these', 
        'those', 'then', 'than', 'such', 'some', 'also', 'more', 'most', 'just', 'like', 'only', 
        'other', 'about', 'into', 'over', 'under', 'after', 'before', 'between', 'through', 
        'during', 'without', 'being', 'both', 'each', 'while', 'until', 'upon', 'within', 'using',
        'based', 'including', 'according', 'following', 'various', 'including', 'provide', 'provided'
    }
    
    # Filter out stop words and count frequency
    filtered_words = [word for word in words if word not in stop_words]
    
    # Get the 30 most common words as keywords
    word_counter = Counter(filtered_words)
    top_keywords = [word for word, count in word_counter.most_common(30)]
    
    # Categorize keywords
    categorized_keywords = []
    for keyword in top_keywords:
        category = categorize_keyword(keyword)
        synonyms = get_synonyms(keyword)
        categorized_keywords.append({
            'keyword': keyword,
            'category': category,
            'synonyms': synonyms,
            'count': word_counter[keyword]
        })
    
    return categorized_keywords

def calculate_match(resume_text, job_keywords):
    """
    Enhanced matching with synonym support and categorization
    """
    resume_clean = clean_text(resume_text)
    
    found_keywords = []
    missing_keywords = []
    exact_matches = 0
    synonym_matches = 0
    
    for kw_info in job_keywords:
        keyword = kw_info['keyword']
        synonyms = kw_info['synonyms']
        category = kw_info['category']
        
        # Check for exact match
        if keyword in resume_clean:
            found_keywords.append({
                'keyword': keyword,
                'category': category,
                'match_type': 'exact',
                'synonyms': synonyms
            })
            exact_matches += 1
        # Check for synonym matches
        elif any(synonym in resume_clean for synonym in synonyms):
            matching_synonym = next(synonym for synonym in synonyms if synonym in resume_clean)
            found_keywords.append({
                'keyword': keyword,
                'category': category,
                'match_type': 'synonym',
                'matched_synonym': matching_synonym,
                'synonyms': synonyms
            })
            synonym_matches += 1
        else:
            missing_keywords.append({
                'keyword': keyword,
                'category': category,
                'synonyms': synonyms
            })
    
    # Calculate enhanced match score (exact matches count more)
    total_keywords = len(job_keywords)
    if total_keywords > 0:
        # Weight exact matches higher
        weighted_score = (exact_matches * 1.0 + synonym_matches * 0.7) / total_keywords * 100
        match_percentage = weighted_score
    else:
        match_percentage = 0
    
    return {
        'match_percentage': match_percentage,
        'found_keywords': found_keywords,
        'missing_keywords': missing_keywords,
        'total_keywords': total_keywords,
        'exact_matches': exact_matches,
        'synonym_matches': synonym_matches
    }

def generate_improvement_suggestions(missing_keywords, found_keywords):
    """
    Generate actionable improvement suggestions
    """
    suggestions = []
    
    # Categorize missing keywords
    missing_by_category = {}
    for kw in missing_keywords:
        category = kw['category']
        if category not in missing_by_category:
            missing_by_category[category] = []
        missing_by_category[category].append(kw)
    
    # Generate category-specific suggestions
    for category, keywords in missing_by_category.items():
        if category == "Technical Skills":
            tech_keywords = [kw['keyword'] for kw in keywords[:3]]  # Top 3
            if tech_keywords:
                suggestions.append(f"**Add technical skills**: Consider including {', '.join(tech_keywords)} in your skills section")
        
        elif category == "Tools & Technologies":
            tools = [kw['keyword'] for kw in keywords[:3]]
            if tools:
                suggestions.append(f"**Learn tools**: Gain experience with {', '.join(tools)} through online courses or projects")
        
        elif category == "Soft Skills":
            soft_skills = [kw['keyword'] for kw in keywords[:2]]
            if soft_skills:
                suggestions.append(f"**Highlight soft skills**: Add examples demonstrating {', '.join(soft_skills)} in your experience section")
    
    # General suggestions based on match score
    if len(missing_keywords) > 10:
        suggestions.append("**Major revision needed**: Consider significantly restructuring your resume to better match the job requirements")
    elif len(missing_keywords) > 5:
        suggestions.append("**Moderate improvements**: Focus on adding the top missing keywords to your resume")
    else:
        suggestions.append("**Good match**: Minor tweaks suggested for optimal alignment")
    
    return suggestions

def main():
    """
    Main function to run the enhanced Streamlit app
    """
    
    # Show NLTK status
    if not nltk_ready:
        st.warning("⚠️ Advanced synonym features are disabled. The app will still work with basic keyword matching.")
    
    # File upload section with enhanced support
    st.subheader("📁 Upload Your Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Your Resume")
        st.markdown("**Supported formats:** .txt, .docx, .pdf")
        resume_file = st.file_uploader(
            "Choose resume file", 
            type=['txt', 'docx', 'pdf'],
            key="resume_uploader",
            help="Upload your resume in any supported format"
        )
    
    with col2:
        st.markdown("#### 📋 Job Description")
        st.markdown("**Supported formats:** .txt, .docx, .pdf")  
        job_file = st.file_uploader(
            "Choose job description file",
            type=['txt', 'docx', 'pdf'],
            key="job_uploader",
            help="Upload the job description in any supported format"
        )
    
    st.markdown("---")
    
    # Analysis button
    if st.button("🚀 Analyze Match & Get Suggestions", type="primary", use_container_width=True):
        if resume_file and job_file:
            with st.spinner("🔍 Analyzing documents... This may take a few seconds."):
                
                # Extract text from files
                resume_text = extract_text_from_file(resume_file)
                job_text = extract_text_from_file(job_file)
                
                # Check if files have content
                if not resume_text.strip():
                    st.error("❌ Resume file is empty. Please upload a valid file.")
                    return
                
                if not job_text.strip():
                    st.error("❌ Job description file is empty. Please upload a valid file.")
                    return
                
                # Extract keywords from job description
                job_keywords = extract_keywords(job_text)
                
                if not job_keywords:
                    st.warning("⚠️ No significant keywords found in the job description.")
                    return
                
                # Calculate match
                results = calculate_match(resume_text, job_keywords)
                suggestions = generate_improvement_suggestions(results['missing_keywords'], results['found_keywords'])
                
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Enhanced match score with detailed breakdown
            match_score = results['match_percentage']
            
            # Score interpretation
            if match_score >= 80:
                score_emoji = "🎉"
                score_message = "Excellent match!"
                score_color = "green"
            elif match_score >= 60:
                score_emoji = "👍"
                score_message = "Good match"
                score_color = "orange"
            elif match_score >= 40:
                score_emoji = "💡"
                score_message = "Needs improvement"
                score_color = "orange"
            else:
                score_emoji = "🚨"
                score_message = "Major improvements needed"
                score_color = "red"
            
            # Main metric
            col_metric, col_breakdown = st.columns([1, 2])
            
            with col_metric:
                st.metric(
                    label=f"**Overall Match Score** {score_emoji}", 
                    value=f"{match_score:.1f}%",
                    help=score_message
                )
            
            with col_breakdown:
                st.markdown(f"**Breakdown:**")
                st.markdown(f"- **Exact matches:** {results['exact_matches']} keywords")
                st.markdown(f"- **Synonym matches:** {results['synonym_matches']} keywords")
                st.markdown(f"- **Missing:** {len(results['missing_keywords'])} keywords")
            
            st.markdown("---")
            
            # Enhanced results display with categorization
            st.markdown("### 📊 Detailed Analysis")
            
            # Found keywords by category
            if results['found_keywords']:
                st.markdown("#### ✅ Keywords Found")
                
                # Group found keywords by category
                found_by_category = {}
                for kw in results['found_keywords']:
                    category = kw['category']
                    if category not in found_by_category:
                        found_by_category[category] = []
                    found_by_category[category].append(kw)
                
                # Display by category
                for category, keywords in found_by_category.items():
                    with st.expander(f"**{category}** ({len(keywords)} found)"):
                        for kw in keywords:
                            if kw['match_type'] == 'exact':
                                st.markdown(f"• **{kw['keyword']}** ✓")
                            else:
                                st.markdown(f"• **{kw['keyword']}** (via synonym: *{kw['matched_synonym']}*)")
            else:
                st.info("No keywords matched.")
            
            # Missing keywords by category
            if results['missing_keywords']:
                st.markdown("#### ❌ Keywords Missing")
                
                # Group missing keywords by category
                missing_by_category = {}
                for kw in results['missing_keywords']:
                    category = kw['category']
                    if category not in missing_by_category:
                        missing_by_category[category] = []
                    missing_by_category[category].append(kw)
                
                # Display by category
                for category, keywords in missing_by_category.items():
                    with st.expander(f"**{category}** ({len(keywords)} missing)"):
                        for kw in keywords:
                            st.markdown(f"• **{kw['keyword']}**")
                            if kw['synonyms']:
                                st.caption(f"  *Similar terms: {', '.join(kw['synonyms'])}*")
            else:
                st.success("🎉 All keywords found! Your resume is well-matched.")
            
            # Improvement suggestions
            st.markdown("---")
            st.markdown("### 💡 Improvement Suggestions")
            
            for suggestion in suggestions:
                st.markdown(f"• {suggestion}")
            
            # Visual chart
            st.markdown("---")
            st.markdown("### 📈 Match Overview")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Category distribution of missing keywords
                if results['missing_keywords']:
                    category_counts = {}
                    for kw in results['missing_keywords']:
                        category = kw['category']
                        category_counts[category] = category_counts.get(category, 0) + 1
                    
                    if category_counts:
                        st.markdown("**Missing Keywords by Category**")
                        st.bar_chart(category_counts)
            
            with chart_col2:
                # Match type distribution
                match_types = {
                    'Exact Matches': results['exact_matches'],
                    'Synonym Matches': results['synonym_matches'],
                    'Missing Keywords': len(results['missing_keywords'])
                }
                st.markdown("**Match Type Distribution**")
                st.bar_chart(match_types)
                
        else:
            st.warning("⚠️ Please upload both files to analyze.")
    
    # Enhanced instructions section
    with st.expander("📖 How to Use This Enhanced Tool"):
        st.markdown("""
        ### New Features:
        
        **📁 Multiple File Formats**
        - Now supports .txt, .docx, and .pdf files
        - No need to convert your documents
        
        **🔤 Smart Synonym Matching**
        - Finds related terms (e.g., "programming" matches "coding")
        - Uses natural language processing
        
        **📊 Skill Categorization**
        - Automatically categorizes skills as:
          - **Technical Skills**: Programming, development, engineering
          - **Tools & Technologies**: Software, frameworks, platforms
          - **Soft Skills**: Communication, leadership, teamwork
        
        **💡 Actionable Suggestions**
        - Get specific improvement recommendations
        - Categorized by importance and type
        
        ### How to Get Best Results:
        1. **Use original files** - no need to convert formats
        2. **Review categorized results** - understand what types of skills are missing
        3. **Check synonym matches** - see how your existing skills relate
        4. **Follow suggestions** - implement the improvement recommendations
        """)
    
    # Tips for better resumes
    with st.expander("🎯 Pro Tips for Resume Optimization"):
        st.markdown("""
        **Technical Resume Tips:**
        - Include specific programming languages and frameworks
        - Mention tools and platforms you've used
        - Quantify achievements with numbers and metrics
        
        **Soft Skills Strategy:**
        - Don't just list soft skills - provide examples
        - Show how you used these skills to achieve results
        - Use action verbs (led, developed, implemented, optimized)
        
        **Keyword Optimization:**
        - Mirror the language used in the job description
        - Include both exact keywords and related terms
        - Spread keywords throughout your resume (not just skills section)
        
        **Formatting Tips:**
        - Use standard, readable fonts
        - Include clear section headings
        - Save as PDF to preserve formatting
        """)

# Run the app
if __name__ == "__main__":
    main()