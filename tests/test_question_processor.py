import json
import time

from question_processor import QuestionProcessor


def test_inactive_response():
    process = QuestionProcessor()
    assert process.response() == json.dumps(
        {"question": None, "facts": None, "status": "Inactive"}
    )


def tests_processing_response(monkeypatch):
    process = QuestionProcessor()

    def mock_process_question(self, question, documents):
        time.sleep(0.5)
        return ["facts", "facts", "more facts"]

    monkeypatch.setattr(QuestionProcessor, "process_question", mock_process_question)
    process.submit_question(
        question="What are our product design decisions?", documents="log.txt"
    )

    assert process.response() == json.dumps(
        {"question": process.question, "facts": None, "status": "processing"}
    )
    time.sleep(1)
    assert process.response() == json.dumps(
        {
            "question": process.question,
            "facts": ["facts", "facts", "more facts"],
            "status": "done",
        }
    )


def test_graceful_exit_on_document_load_error():
    process = QuestionProcessor()
    process.submit_question(
        question="What are our product design decisions?", documents="foo"
    )
    time.sleep(1)
    assert process.response() == json.dumps(
        {
            "question": process.question,
            "facts": "UserError: Could not process the url(s) provided",
            "status": "done",
        }
    )
