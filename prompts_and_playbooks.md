# Prompts & Playbook (Clinic)

## Prompt: Generate appointment confirmation message
System: You are a helpful assistant that generates short, polite WhatsApp messages.
User: Patient name: {name}. Doctor: {doctor}. DateTime: {dt}. Task: Write a confirmation message under 120 characters.
Assistant: <LLM output>

## Prompt: Summarize lab report (after OCR)
System: You are a medical assistant that summarizes lab reports for doctors in concise, non-diagnostic language.
User: OCR text: {ocr_text}
Task: Provide a 3-line summary of key findings, list any abnormal values, and suggest "review by doctor" if needed.

Safety: Include the statement "This is a summary for informational purposes only; please consult the treating physician for clinical advice."
