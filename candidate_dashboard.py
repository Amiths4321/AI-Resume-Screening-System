
import pandas as pd
import streamlit as st


def show_candidate_dashboard(candidates, job_data):

    st.title("Candidate Comparison Dashboard")

    if not candidates:
        st.info("No candidate data available.")
        return

    comparison_rows = []

    for filename, candidate_data in candidates.items():

        match_results = match_candidate(
            candidate_data,
            job_data
        )

        required = match_results["required_skills"]
        preferred = match_results["preferred_skills"]

        found_required = sum(
            item["status"] == "Found"
            for item in required
        )

        found_preferred = sum(
            item["status"] == "Found"
            for item in preferred
        )

        comparison_rows.append({
            "Resume": filename,
            "Candidate": candidate_data.get(
                "candidate_name"
            ) or "Not provided",
            "Required Skills Found": (
                f"{found_required}/{len(required)}"
            ),
            "Preferred Skills Found": (
                f"{found_preferred}/{len(preferred)}"
            ),
            "Documented Experience": (
                candidate_data.get(
                    "total_experience_years"
                )
            )
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.subheader("Candidate Comparison")

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Candidate Details")

    for filename, candidate_data in candidates.items():

        with st.expander(
            candidate_data.get("candidate_name")
            or filename
        ):

            st.write("**Skills**")

            st.write(
                ", ".join(
                    candidate_data.get("skills", [])
                )
            )

            st.write("**Work Experience**")

            st.json(
                candidate_data.get(
                    "work_experience", []
                )
            )

            st.write("**Education**")

            st.json(
                candidate_data.get(
                    "education", []
                )
            )

            st.write("**Certifications**")

            st.write(
                candidate_data.get(
                    "certifications", []
                )
            )
