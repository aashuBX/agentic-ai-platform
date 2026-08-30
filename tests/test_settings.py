from app.config.settings import get_settings


def test_defaults_are_mock_and_local(monkeypatch):
    monkeypatch.delenv("LLM__PROVIDER", raising=False)
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.llm.provider == "mock"
    assert settings.app_env == "local"
    assert settings.neo4j.enabled is False
    assert settings.redis.enabled is False
    assert settings.rabbitmq.enabled is False


def test_nested_double_underscore_env_vars_override_sub_settings(monkeypatch):
    monkeypatch.setenv("LLM__PROVIDER", "openai")
    monkeypatch.setenv("LLM__MODEL", "gpt-4o-mini")
    monkeypatch.setenv("NEO4J__ENABLED", "true")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.llm.provider == "openai"
    assert settings.llm.model == "gpt-4o-mini"
    assert settings.neo4j.enabled is True
