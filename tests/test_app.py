import json
import time

import pytest
from app import app


from question_processor import QuestionProcessor


@pytest.fixture()
def my_app():
    return app


@pytest.fixture()
def client(my_app):
    return my_app.test_client()


@pytest.fixture
def mock_ai_agent(monkeypatch):
    def mock_process_question(self, question, documents):
        time.sleep(0.5)
        return ["fact_a", "fact_b", "fact_c"]

    monkeypatch.setattr(QuestionProcessor, "process_question", mock_process_question)


def test_post_response(client, mock_ai_agent):
    data = {
        "question": "What are our product design decisions?",
        "documents": [
            "http://localhost:5000/static/log_1.txt",
        ],
    }
    client.post("/submit_question_and_documents", data=data)
    resp = client.get("/get_question_and_facts")
    assert json.loads(resp.data.decode("utf-8"))["status"] == "processing"
    time.sleep(1)
    resp = client.get("/get_question_and_facts")
    assert json.loads(resp.data.decode("utf-8"))["facts"] == [
        "fact_a",
        "fact_b",
        "fact_c",
    ]


@pytest.mark.timeout(1)
def test_ui_submission(client, mock_ai_agent):
    data = {
        "question": "What are our product design decisions?",
        "documents": "http://localhost:5000/static/log_1.txt",
    }
    resp = client.post("/output", data=data)
    assert (
        """<li class="list-group-item">fact_a</li>\n            \n            <li class="list-group-item">fact_b</li>\n            \n            <li class="list-group-item">fact_c</li>"""
        in resp.data.decode("utf-8")
    )


@pytest.mark.timeout(1)
def test_bad_links(client):
    data = {
        "question": "What are our product design decisions?",
        "documents": "bad_url",
    }
    resp = client.post("/output", data=data)
    assert "<title>Error</title>" in resp.data.decode("utf-8")
