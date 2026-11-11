
import io
import fitz
from PIL import Image
import ollama


OLLAMA_HOST = "http://10.22.39.192:11434"
CHAT_MODEL = "qwen2.5vl:latest"

client = ollama.Client(host=OLLAMA_HOST)


def extract_image_text(image_bytes):

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": """
                Extract all readable text from this resume.

                Preserve:
                - Candidate name
                - Contact details
                - Professional summary
                - Skills
                - Work experience
                - Education
                - Certifications
                - Projects

                Do not invent missing information.
                Preserve dates, company names and job titles.
                """,
                "images": [image_bytes]
            }
        ]
    )

    return response.message.content


def extract_pdf_text(uploaded_file):

    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    extracted_pages = []

    for page_number, page in enumerate(pdf):

        text = page.get_text().strip()

        # OCR scanned pages when selectable text is absent
        if len(text) < 20:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image_bytes = pix.tobytes("png")

            text = extract_image_text(image_bytes)

        extracted_pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    pdf.close()

    return extracted_pages


def extract_resume_image(uploaded_file):

    image = Image.open(
        io.BytesIO(uploaded_file.getvalue())
    ).convert("RGB")

    image_buffer = io.BytesIO()

    image.save(image_buffer, format="PNG")

    return extract_image_text(
        image_buffer.getvalue()
    )
