import streamlit as st
from candidate_report import generate_candidate_report
from candidate_report import generate_candidate_report

from resume_ai import extract_candidate_data
from resume_extractor import extract_pdf_text, extract_resume_image
from job_analyzer import analyze_job_description
from candidate_matcher import match_candidate
from candidate_dashboard import show_candidate_dashboard

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Screening and Candidate Matching")
st.write("Upload candidate resumes and analyze job descriptions for AI-powered screening.")

# ---------------------------------------------------------
# SECTION 1: JOB DESCRIPTION ANALYSIS (Global)
# ---------------------------------------------------------
st.header("1. Job Description Analysis")
job_description = st.text_area(
    "Paste the Job Description",
    height=200,
    placeholder="Paste the complete job description here..."
)

if st.button("Analyze Job Description"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Analyzing job requirements..."):
            try:
                job_data = analyze_job_description(job_description)
                st.session_state["job_data"] = job_data
                st.session_state["job_description"] = job_description
                st.success("Job description analyzed successfully!")
            except Exception as error:
                st.error(f"Analysis failed: {error}")

if "job_data" in st.session_state:
    with st.expander("View Extracted Job Requirements"):
        st.json(st.session_state["job_data"])

st.divider()

# ---------------------------------------------------------
# SECTION 2: RESUME UPLOAD & INDIVIDUAL EXTRACTION
# ---------------------------------------------------------
st.header("2. Candidate Resumes")
uploaded_files = st.file_uploader(
    "Upload candidate resumes",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

candidates = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📄 {uploaded_file.name}")

        # Step A: Extract Text Button
        if st.button("Extract Resume Text", key=f"extract_{uploaded_file.name}"):
            with st.spinner("Extracting resume text..."):
                try:
                    if uploaded_file.name.lower().endswith(".pdf"):
                        pages = extract_pdf_text(uploaded_file)
                        extracted_text = "\n\n".join(page["text"] for page in pages)
                    else:
                        extracted_text = extract_resume_image(uploaded_file)

                    st.session_state[f"resume_text_{uploaded_file.name}"] = extracted_text
                    st.success("Resume text extracted successfully!")
                except Exception as error:
                    st.error(f"Extraction failed: {error}")

        # Retrieve text from session state
        extracted_text = st.session_state.get(f"resume_text_{uploaded_file.name}")

        if extracted_text:
            st.text_area(
                "Extracted Resume Text",
                extracted_text,
                height=180,
                key=f"display_{uploaded_file.name}"
            )

            # Step B: AI Candidate Info Extraction Button
            if st.button("Extract Candidate Information", key=f"candidate_{uploaded_file.name}"):
                with st.spinner("AI is analyzing the resume..."):
                    try:
                        candidate_data = extract_candidate_data(extracted_text)
                        st.session_state[f"candidate_data_{uploaded_file.name}"] = candidate_data
                        st.success("Candidate information extracted!")
                    except Exception as error:
                        st.error(f"AI extraction failed: {error}")

        # Collect candidate data if present in session state
        candidate_data = st.session_state.get(f"candidate_data_{uploaded_file.name}")
        if candidate_data:
            candidates[uploaded_file.name] = candidate_data
            with st.expander(f"View Extracted Profile: {uploaded_file.name}"):
                st.json(candidate_data)

# ---------------------------------------------------------
# SECTION 3: CANDIDATE MATCHING & DASHBOARD
# ---------------------------------------------------------
st.divider()
st.header("3. Candidate Matching & Dashboard")

if "job_data" in st.session_state and candidates:
    # Individual Candidate Skill Breakdowns
    for name, candidate_data in candidates.items():
        with st.expander(f"Skill Match Breakdown: {name}"):
            try:
                match_results = match_candidate(candidate_data, st.session_state["job_data"])
                
                st.write("**Required Skills**")
                st.dataframe(match_results["required_skills"], use_container_width=True, hide_index=True)
                
                st.write("**Preferred Skills**")
                st.dataframe(match_results["preferred_skills"], use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Matching failed for {name}: {e}")

    st.divider()
    st.subheader("Comparison Dashboard")
    try:
        show_candidate_dashboard(candidates, st.session_state["job_data"])
    except Exception as e:
        st.error(f"Dashboard failed to load: {e}")

elif not "job_data" in st.session_state:
    st.info("💡 Please analyze a job description in Section 1 before matching candidates.")
elif not candidates:
    st.info("💡 Please extract candidate information from at least one uploaded resume in Section 2.")

    # ---------------------------------------------------------
# SECTION 4: EXCEL REPORT EXPORT
# ---------------------------------------------------------

st.divider()
st.header("4. Export Candidate Evaluation Report")

if "job_data" in st.session_state and candidates:

    try:
        report = generate_candidate_report(
            candidates,
            st.session_state["job_data"]
        )

        st.download_button(
            label="Download Candidate Evaluation Report",
            data=report,
            file_name="candidate_evaluation_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as error:
        st.error(f"Report generation failed: {error}")

else:
    st.info(
        "Analyze a job description and extract at least one candidate "
        "profile before downloading the report."
    )