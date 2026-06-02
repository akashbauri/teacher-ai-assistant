def generate_document_notes(topic, student_level="Class 5"):
    context = get_context(topic)

    prompt = f"""
You are an expert teacher.

Create detailed notes from the uploaded document.

Topic: {topic}

Student Level: {student_level}

Document Content:
{context}

Include:
1. Introduction
2. Important Concepts
3. Key Points
4. Summary

Explain in simple language.
"""

    client = get_client()

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=3000
    )

    return response.choices[0].message.content
