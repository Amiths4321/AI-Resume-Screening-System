
import ollama
import json

OLLAMA_HOST = "http://10.22.39.192:11434"
CHAT_MODEL = "qwen2.5vl:latest"

client = ollama.Client(host=OLLAMA_HOST)


def analyze_job_description(job_description):

    prompt = f"""
    You are an expert job description analysis assistant.

    Analyze the job description and extract job requirements.

    Return ONLY valid JSON using this structure:

    {{
        "job_title": null,
        "required_skills": [],
        "preferred_skills": [],
        "minimum_experience_years": null,
        "education_requirements": [],
        "responsibilities": []
    }}

    Rules:

    1. Extract only requirements stated in the job description.
    2. Separate mandatory skills from preferred skills.
    3. Do not invent requirements.
    4. Use null when experience requirements are not specified.
    5. Preserve the original meaning.
    6. Return JSON only.

    Job Description:

    {job_description}
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

    return json.loads(response.message.content)
