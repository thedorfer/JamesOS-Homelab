from jamesos import JamesOS, __version__
from jamesos.core.models import CheckResult, DoctorReport
from jamesos.interfaces.cli.main import main


def test_version_is_defined():
    assert __version__ == "0.2.0"


def test_core_registers_builtin_providers():
    app = JamesOS()
    assert "linux" in app.registry.provider_names()
    assert "docker" in app.registry.provider_names()
    assert "wordpress" in app.registry.provider_names()
    assert "nextcloud" in app.registry.provider_names()


def test_doctor_report_status_rollup():
    report = DoctorReport()
    assert report.status == "unknown"

    report.add(CheckResult(name="one", status="ok", message="ok"))
    assert report.status == "ok"

    report.add(CheckResult(name="two", status="warn", message="warn"))
    assert report.status == "warn"

    report.add(CheckResult(name="three", status="fail", message="fail"))
    assert report.status == "fail"


def test_cli_version_runs(capsys):
    result = main(["version"])
    captured = capsys.readouterr()
    assert result == 0
    assert "JamesOS" in captured.out
