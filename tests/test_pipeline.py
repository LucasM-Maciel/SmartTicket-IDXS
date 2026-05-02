from app.services.pipeline import run_pipeline


def test_run_pipeline_returns_string():
    text = "Hello World"
    result = run_pipeline(text)
    assert isinstance(result, str)


def test_run_pipeline_empty_input():
    text = ""
    result = run_pipeline(text)
    assert result == ""


def test_run_pipeline_cleans_and_normalizes():
    text = "I WANT TO CANCEL!!!"
    result = run_pipeline(text)
    assert "i" not in result.split()
    assert "to" not in result.split()
    assert "want" in result.split()
    assert "cancel" in result.split()


def test_run_pipeline_non_string_input():
    result = run_pipeline(None)
    assert result == ""
