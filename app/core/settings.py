"""Application settings (environment / deployment).

Use for: ``DATABASE_URL``, API keys, feature flags, etc. Prefer
``pydantic-settings`` or similar.

Note: ``app/core/config.py`` holds **ML paths and dataset columns** for training
and ``predict_category`` — do not merge those concerns here unless you refactor
explicitly.
"""
