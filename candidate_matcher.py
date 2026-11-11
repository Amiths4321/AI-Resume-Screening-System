
def normalize_skill(skill):
    return " ".join(str(skill).lower().strip().split())


def match_candidate(candidate_data, job_data):

    candidate_skills = {
        normalize_skill(skill)
        for skill in candidate_data.get("skills", [])
    }

    required_skills = job_data.get(
        "required_skills", []
    )

    preferred_skills = job_data.get(
        "preferred_skills", []
    )

    required_results = []
    preferred_results = []

    # Compare mandatory skills
    for skill in required_skills:

        normalized = normalize_skill(skill)

        found = normalized in candidate_skills

        required_results.append({
            "skill": skill,
            "status": "Found" if found else "Not found"
        })

    # Compare preferred skills
    for skill in preferred_skills:

        normalized = normalize_skill(skill)

        found = normalized in candidate_skills

        preferred_results.append({
            "skill": skill,
            "status": "Found" if found else "Not found"
        })

    return {
        "required_skills": required_results,
        "preferred_skills": preferred_results
    }
