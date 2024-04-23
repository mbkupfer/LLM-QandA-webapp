import json
import threading
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

import utils

load_dotenv()

class QuestionProcessor:
    def __init__(self):
        self.question: str = None
        self.documents: List[str] = None
        self.facts: List[str] = None
        self.status: str = None
        self.processing_event = threading.Event()
        self.client = OpenAI()

    def submit_question(self, question: str, documents: List[str]):
        self.question = question
        self.documents = documents
        self.status = "processing"
        self.processing_event.clear()
        thread = threading.Thread(target=self.process_question_thread)
        thread.start()

    def process_question_thread(self):
        facts = self.process_question(self.question, self.documents)
        self.facts = facts
        self.status = "done"
        self.processing_event.set()

    def process_question(self, question: str, documents: List[str]):
        log_context = utils.extract_logs(documents)
        if not log_context:
            return 'UserError: Could not process the url(s) provided'
        prompt = f"""
 Given a chat log and a question, generate a concise and stricly literal 
 answer using only bullet points, ensuring that we discard any information that is overridden.

Chat Log: {log_context}

Question: {question}
"""

        response = self.client.chat.completions.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}])
        bullets = response.choices[0].message.content
        return bullets.replace('- ', '').split('\n')
        
    
    def response(self):
        if self.status is None:
            return json.dumps({"status": "Inactive"})

        response_data = {
            "question": self.question,
            "facts": None,
            "status": self.status,
        }

        if self.processing_event.is_set():
            response_data["facts"] = self.facts

        return json.dumps(response_data)
