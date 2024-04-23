import json
import threading
from typing import List


class QuestionProcessor:
    def __init__(self):
        self.question: str = None
        self.documents: List[str] = None
        self.facts: List[str] = None
        self.status: str = None
        self.processing_event = threading.Event()

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

    def process_question(self, question, documents):
        raise NotImplementedError

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
