Interview Follow-Up Question Generator API
------------------------------------------
A FastAPI service that uses OpenAI to generate concise follow-up interview questions based on a candidate’s response.

Tech used:
- FastAPI
- Pydantic
- OpenAI API
- Python-dotenv

How to run:
1. Install dependencies: pip install fastapi uvicorn openai python-dotenv
2. Add your OPENAI_API_KEY to a .env file
3. Start the server: uvicorn main:app --reload
4. Open http://localhost:8000/docs to test the API
