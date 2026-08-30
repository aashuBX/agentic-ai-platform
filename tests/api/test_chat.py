def test_chat_faq_returns_full_contract(api_client):
    response = api_client.post(
        "/chat",
        json={"session_id": "api-1", "message": "What are your business hours?", "channel": "web"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["agent"] == "faq_agent"
    assert body["intent"] == "FAQ"
    assert body["trace_id"]
    assert body["guardrail_passed"] is True
    assert "9am-6pm" in body["response"]


def test_chat_rejects_empty_message_at_the_schema_level(api_client):
    response = api_client.post("/chat", json={"session_id": "api-2", "message": ""})

    assert response.status_code == 422


def test_chat_requires_session_id(api_client):
    response = api_client.post("/chat", json={"message": "hi"})

    assert response.status_code == 422


def test_chat_defaults_channel_to_web(api_client):
    response = api_client.post("/chat", json={"session_id": "api-3", "message": "hello"})

    assert response.status_code == 200
