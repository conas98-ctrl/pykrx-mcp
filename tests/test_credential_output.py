"""Credential-safe dependency output tests."""

from pykrx_mcp.utils.credential_output import safe_dependency_output


def test_redacts_credentials_from_stdout_and_stderr(monkeypatch, capsys):
    dummy_id = "dummy-krx-user"
    dummy_password = "dummy-krx-password"
    monkeypatch.setenv("KRX_ID", dummy_id)
    monkeypatch.setenv("KRX_PW", dummy_password)

    with safe_dependency_output():
        print(f"normal stdout; login={dummy_id}")
        import sys

        print(f"normal stderr; password={dummy_password}", file=sys.stderr)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert dummy_id not in captured.err
    assert dummy_password not in captured.out
    assert dummy_password not in captured.err
    assert "normal stdout; login=[REDACTED]" in captured.err
    assert "normal stderr; password=[REDACTED]" in captured.err


def test_preserves_output_when_credentials_are_absent(monkeypatch, capsys):
    monkeypatch.delenv("KRX_ID", raising=False)
    monkeypatch.delenv("KRX_PW", raising=False)

    with safe_dependency_output():
        print("ordinary dependency diagnostic")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "ordinary dependency diagnostic\n"
