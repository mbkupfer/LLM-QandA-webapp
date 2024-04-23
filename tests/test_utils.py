from pathlib import Path
from urllib.request import urlopen

import pytest

import utils

log_fp = Path(__file__).parent / "test_logs"


@pytest.fixture
def mock_response(monkeypatch):
    def mock_urlopen(url):
        return open(log_fp / url, "rb")

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)


def test_extract_one_log(mock_response):
    assert (
        utils.extract_logs("log_1.txt")
        == "John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.\n"
        + "Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.\n"
        + "Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work."
    )


def test_extract_multiple_logs(mock_response):
    assert (
        utils.extract_logs("log_1.txt, log_2.txt")
        == "John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.\n"
        + "Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.\n"
        + "Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.\n"
        + "John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.\n"
        + "Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.\n"
        + "Mike: I'm on board with that."
    )
