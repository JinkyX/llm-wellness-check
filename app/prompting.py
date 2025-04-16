# from app.utils import QUESTION_MAPPING

QUESTION_MAPPING = {
    50668: "Did you see the client in the last week?",
    50669: "Did the client report that they have been taking their medication as prescribed this week?",
    50670: "Did the client report they have engaged with their treatment team in the last week?",
    50671: "Did you observe any significant changes in the client's mental health status since last week?",
    50672: "Did you observe any significant changes in the client's physical health / well-being since last week?",
    50673: "Did you observe any significant changes in the client's physical space since last week?",
    50674: "Any additional observations/concerns/notes?",
    50675: "Did you engage with the client's treatment team in the last week?",
    50676: "Did the person entering complete, if not select from a dropdown of users to select who completed"
}

def build_prompt(row):
    question_text = QUESTION_MAPPING.get(row['QUESTION_ID'], "[Unknown Question]")
    return f"""You are a wellness assistant helping to assess potential safety concerns based on narrative notes from mental health visits.

Below is a question and the corresponding observation note from the caseworker:

Question: {question_text}
Narrative Note: {row['Anonymized Narrative']}

Task:
Based ONLY on the narrative note above, determine if there is any indication of a concern that may require further attention. This could include:
- Safety concerns (e.g., self-harm, harm to others, neglect)
- Clinical concerns (e.g., deteriorating mental state, disengagement from care)
- Social concerns (e.g., isolation, lack of support)
- Resource concerns (e.g.,financial struggles, lack of transportation, inadequate support)
- Functional concerns (e.g.,difficulty with daily activities, self-care decline)
- Physical health concerns (e.g.,untreated medical conditions, physical symptoms)
- Legal concerns (e.g.,legal issues affecting wellbeing or care)
- Any other potential concern that may warrant attention or follow-up

Format your response exactly as follows:
Answer: [Yes or No]
Explanation: [Provide one sentence, clear and logically reasoned to explain why you chose Yes or No]

CONSTRAINTS:
1. First line must be \"Answer: \" followed by ONLY the word \"Yes\" or \"No\"
2. Second line must be \"Explanation: \" followed by exactly one sentence
3. Do not include any other text, greetings, or additional information
4. Do not repeat the question or narrative
5. Do not add any disclaimer or additional thoughts
6. Do not use bullet points or numbering
7. Keep your explanation to a single sentence"""

def format_inference(prompt: str) -> dict:
    return {
        "prompt": f"<s>[INST] {prompt.strip()} [/INST]",
        "max_tokens": 150,
        "temperature": 0.8,
        "top_p": 0.95,
    }
