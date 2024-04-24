from flask import Flask, render_template, request, jsonify, redirect, url_for
from question_processor import QuestionProcessor

app = Flask(__name__)
ai_agent = QuestionProcessor()


@app.route("/")
def index():
    """UI Interface for Q&A"""

    return render_template("index.html")


@app.route("/output", methods=["GET", "POST"])
def summary():
    """UI Redirect for Q&A output"""
    if request.method == "GET":
        return redirect(url_for("index"))
    
    question = request.form["question"]
    urls = request.form["documents"].split(",")
    ai_agent.submit_question(question, urls)
    ai_agent.processing_event.wait()
    facts = ai_agent.facts
    if isinstance(facts, list):
        return render_template("output.html", question=question, urls=urls, facts=facts)
    else:
        return render_template("error.html")

@app.route("/submit_question_and_documents", methods=["POST"])
def submit_question_and_documents():
    """REST API entrypoint for Q&A"""

    if request.headers.get('Content-Type') == 'application/json':
        data = request.json
        question = data.get("question")
        documents = data.get("documents")
    else:
        question = request.form.get("question")
        documents = request.form.getlist("documents")
    ai_agent.submit_question(question, documents=documents)
    return jsonify(
        {
            "message": "Question has been submitted. Check /get_question_and_facts endpoint for response"
        }
    )


@app.route("/get_question_and_facts")
def get_question_and_facts():
    """REST API entrypoint for Q&A output"""

    return ai_agent.response()


if __name__ == "__main__":
    app.run(debug=True)
