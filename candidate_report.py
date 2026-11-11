import io
import pandas as pd
from candidate_matcher import match_candidate

def generate_candidate_report(candidates: dict, job_data: dict) -> bytes:
    """
    Generates an Excel evaluation report comparing candidates against job requirements.
    """
    rows = []

    for candidate_name, candidate_info in candidates.items():
        # Calculate match scores/results
        match_results = match_candidate(candidate_info, job_data)

        # Extract skill counts or match data
        req_skills = match_results.get("required_skills", [])
        pref_skills = match_results.get("preferred_skills", [])

        rows.append({
            "Candidate Name": candidate_name,
            "Total Required Skills": len(req_skills),
            "Total Preferred Skills": len(pref_skills),
            "Candidate Data": str(candidate_info)
        })

    df = pd.DataFrame(rows)

    # Write to an in-memory BytesIO buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidate Summary")

    return output.getvalue()