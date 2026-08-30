def test_knowledge_search_returns_relevant_results(api_client):
    response = api_client.post("/knowledge/search", json={"query": "What are the API rate limits?"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "What are the API rate limits?"
    assert body["results"]
    assert "60 requests per minute" in body["results"][0]["content"]
    assert body["results"][0]["retrieval_method"] == "hybrid_rrf"


def test_knowledge_search_respects_top_k(api_client):
    response = api_client.post(
        "/knowledge/search", json={"query": "billing plans pricing", "top_k": 1}
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) <= 1


def test_knowledge_search_rejects_empty_query(api_client):
    response = api_client.post("/knowledge/search", json={"query": ""})
    assert response.status_code == 422
