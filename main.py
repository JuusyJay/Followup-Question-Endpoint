from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Interview Follow-Up Question Generator",
    description="API to generate follow-up interview questions using OpenAI"
)

# Request schema
class InterviewRequest(BaseModel):
    question: str = Field(..., description="Original interview question")
    answer: str = Field(..., description="Candidate's answer")
    role: Optional[str] = Field(None, description="Target job role/title")
    interview_type: Optional[List[str]] = Field(None, description="Type(s) of interview")

# Response schema
class InterviewResponse(BaseModel):
    result: str
    message: str
    data: dict


@app.post("/interview/generate-followups", response_model=InterviewResponse)
async def generate_followups(payload: InterviewRequest):
    """
    Generate follow-up interview questions based on candidate's response.
    """
    try:
        # Build system prompt with safety rails
        system_prompt = (
            "You are an expert technical interviewer. "
            "Your task is to generate **1-3 very concise follow-up interview questions**. "
            "Do NOT number the questions or use bullet points — just write each question on a separate line, followed by a rationale on the same line. "
            "based strictly on the candidate’s response. "
            "The follow-ups should probe for depth, reflection, or clarification. "
            "Keep them professional, neutral, and relevant to the given role and interview type. "
            "Do not return long explanations — just return the question(s) and a very short rationale as if you're talking to the person you're interviewing."
        )

        # Construct user prompt
        user_prompt = f"""
            Original Question: {payload.question}
            Candidate's Answer: {payload.answer}
            Role Context: {payload.role or "Not specified"}
            Interview Type: {", ".join(payload.interview_type) if payload.interview_type else "Not specified"}

            Now generate appropriate follow-up interview question(s).
            """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=250,
            temperature=0.7
        )

        followup_output = response.choices[0].message.content.strip()

        return {
            "result": "success",
            "message": "Follow-up question generated.",
            "data": {
                "followup_question": followup_output
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating follow-up: {str(e)}")
