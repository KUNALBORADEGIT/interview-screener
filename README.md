# Interview Screener

A FastAPI + Twilio-based automated interview platform that asks questions to candidates via voice, records their answers, converts them to text, scores them using an LLM, and stores results in a database.

---

## Features

- Automated phone interviews via Twilio
- Speech-to-Text (STT) conversion for candidate responses
- LLM-based scoring for each answer
- Tracks candidate progress and scores in the database
- Recommendation system based on total score (`hire` or `reject`)

---

## Tech Stack

- **Backend:** FastAPI, Python 3.12
- **Database:** PostgreSQL (via SQLAlchemy)
- **Voice/Telephony:** Twilio
- **LLM:** Custom LLMClient wrapper
- **STT:** STTService (converts audio recordings to text)

---



