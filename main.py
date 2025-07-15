from fastapi import FastAPI, Request
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']

def get_google_creds():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def create_google_doc(content, title="Executive Meeting Brief"):
    creds = get_google_creds()
    docs_service = build('docs', 'v1', credentials=creds)

    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId")

    requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    print("Doc created:", f"https://docs.google.com/document/d/{doc_id}/edit")
    return f"https://docs.google.com/document/d/{doc_id}/edit"

class BriefRequest(BaseModel):
    customer: str
    meeting_date: str
    location: str
    executive_summary: str
    company_overview: str
    attendees: str
    internal_team: str
    deal_insights: str
    purpose: str
    talking_points: str

# @app.post("/generate-brief")
# async def generate_brief(req: BriefRequest):
#     content = f"""
# Executive Meeting Brief

# Customer: {req.customer}
# Meeting Date/Time: {req.meeting_date}
# Location/Format: {req.location}

# Executive Summary:
# {req.executive_summary}

# Company Overview:
# {req.company_overview}

# Customer Attendees:
# {req.attendees}

# Internal Team Participants:
# {req.internal_team}

# Deal Insights:
# {req.deal_insights}

# Meeting Purpose:
# {req.purpose}

# Key Talking Points:
# {req.talking_points}
# """
#     doc_link = create_google_doc(content)
#     return {"status": "success", "link": doc_link}

@app.post("/generate-brief")
async def generate_brief(req: BriefRequest):
    return {
        "status": "success",
        "link": "https://docs.google.com/document/d/1Zf1234567890EXAMPLE/edit"
    }


