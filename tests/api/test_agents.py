def test_list_agents_includes_every_phase_1_agent(api_client):
    response = api_client.get("/agents")

    assert response.status_code == 200
    names = {agent["name"] for agent in response.json()}
    assert {"faq_agent", "rag_agent", "crm_agent", "handoff_agent", "intent_agent"}.issubset(names)


def test_run_single_agent_bypasses_routing(api_client):
    response = api_client.post(
        "/agents/run", json={"agent_name": "handoff_agent", "message": "help"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["agent"] == "handoff_agent"
    assert body["metadata"]["handoff_requested"] is True


def test_run_unknown_agent_returns_404_with_available_names(api_client):
    response = api_client.post(
        "/agents/run", json={"agent_name": "not-a-real-agent", "message": "help"}
    )

    assert response.status_code == 404
    assert "faq_agent" in response.json()["detail"]
