
import ollama
import json

OLLAMA_HOST = "http://10.22.39.192:11434"
CHAT_MODEL = "qwen2.5vl:latest"

client = ollama.Client(host=OLLAMA_HOST)


def extract_candidate_data(resume_text):

    prompt = f"""
    You are a resume information extraction assistant.

    Extract factual information from the resume below.

    Return ONLY valid JSON using this structure:

    {{
        "candidate_name": null,
        "email": null,
        "phone": null,
        "professional_summary": null,
        "skills": [],
        "total_experience_years": null,
        "work_experience": [
            {{
                "company": null,
                "job_title": null,
                "start_date": null,
                "end_date": null,
                "responsibilities": []
            }}
        ],
        "education": [
            {{
                "degree": null,
                "institution": null,
                "graduation_year": null
            }}
        ],
        "certifications": [],
        "projects": [
            {{
                "project_name": null,
                "description": null
            }}
        ]
    }}

    Extraction rules:

    1. Extract only information explicitly supported by the resume.
    2. Never invent candidate information.
    3. Use null when information is unavailable.
    4. Use empty arrays when no records are available.
    5. Preserve company names and job titles.
    6. Preserve skills as written in the resume.
    7. Do not infer age, gender, religion or other sensitive traits.
    8. Do not estimate missing experience.
    9. Return valid JSON only.

    Resume text:

    {resume_text}
    """

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    candidate_data = json.loads(
        response.message.content
    )

    return candidate_data
