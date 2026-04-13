"""Optional service facade between HTTP layer and ML.

If routes should not import ``app.ml`` directly, implement a thin wrapper that
calls ``predict_category`` here. Otherwise leave unused and route imports
``predict_category`` — avoid duplicating classification logic.
"""
