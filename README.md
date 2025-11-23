# 🔍 Resume Keyword Matcher

A beginner-friendly Python app that compares your resume with a job description and shows keyword matches, missing skills, and a match percentage. Built with Streamlit for easy web access.

## 🚀 Live Demo

[My Streamlit Cloud Link should Appear Here After Deployment]

## 🧠 Computational Thinking Approach

### Decomposition
- **Input Collection**: File upload for resume and job description (.txt files)
- **Text Processing**: Clean text and extract keywords using frequency analysis
- **Comparison Logic**: Check resume for job keywords using exact matching
- **Results Display**: Show match percentage, found/missing keywords with visual charts

### Pattern Recognition
- Identifies frequently used technical terms and skills in job descriptions
- Matches exact word patterns between documents
- Recognizes common industry terminology through frequency analysis

### Abstraction
- **Shows User**: Match percentage, specific keywords found/missing, visual charts
- **Hides Complexity**: File parsing, text cleaning, stop word removal, frequency counting

### Algorithm Design
1. User uploads resume.txt and job_description.txt
2. App extracts and cleans text from both files
3. App identifies top 25 keywords from job description using frequency analysis
4. App scans resume for these keywords using exact matching
5. App calculates match percentage and displays visual results
6. User sees which keywords to add to improve resume


## 🛠️ Installation & Local Development

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps to Run Locally

1. **Clone or download this project**
   ```bash
   # If using git
   git clone https://github.com/yourusername/resume-keyword-matcher.git
   cd resume-keyword-matcher

## 🔧 Future Enhancements

✅ **Implemented in Current Version:**
- [x] Add support for .docx and .pdf files
- [x] Implement synonym matching for better accuracy  
- [x] Add skill categorization (technical vs soft skills)
- [x] Include resume scoring and improvement suggestions

🔄 **Planned for Next Version:**
- [ ] Add support for multiple resume formats comparison
- [ ] Include industry-specific keyword libraries
- [ ] Add ATS (Applicant Tracking System) compatibility scoring
- [ ] Implement machine learning for better keyword matching
- [ ] Add resume template suggestions