def test_upload_text_document(api_client):
    content = b"NimbusDesk supports two-factor authentication via TOTP apps or SMS codes."
    response = api_client.post(
        "/documents/upload",
        files={"file": ("2fa-guide.txt", content, "text/plain")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["chunk_count"] > 0
    assert body["was_duplicate"] is False
    assert body["strategy"] == "recursive"


def test_uploading_the_same_content_twice_is_detected_as_duplicate(api_client):
    content = b"Duplicate detection test content, unique enough to not collide with seed data."
    files = {"file": ("dup.txt", content, "text/plain")}

    first = api_client.post("/documents/upload", files=files)
    second = api_client.post("/documents/upload", files=files)

    assert first.json()["was_duplicate"] is False
    assert second.json()["was_duplicate"] is True
    assert second.json()["document_id"] == first.json()["document_id"]


def test_upload_rejects_unsupported_file_type(api_client):
    response = api_client.post(
        "/documents/upload",
        files={"file": ("notes.docx", b"binary-ish content", "application/octet-stream")},
    )
    assert response.status_code == 422
