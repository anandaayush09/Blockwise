"""Dependency-injection providers: settings, DB session, Redis, store, LLM client, tool registry.

Owns: one function per dependency so tests can override them (FastAPI dependency_overrides),
e.g. swapping the LLM client for a FakeLLMClient and the DB for a test database.
Must NOT: create clients at import time.
"""

from __future__ import annotations


def get_settings_dep(): ...


def get_db_session(): ...


def get_redis(): ...


def get_llm_client(): ...
