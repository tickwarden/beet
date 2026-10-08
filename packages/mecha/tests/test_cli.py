# AI-assisted (Claude, Anthropic): see the commit message.
import json
import subprocess
import sys
from pathlib import Path


def run_mecha(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "mecha", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_json_output_without_stats_flag(tmp_path: Path):
    (tmp_path / "foo.mcfunction").write_text("say hello\n")

    result = run_mecha(tmp_path, "-j", "stats.json", "foo.mcfunction")

    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads((tmp_path / "stats.json").read_text())
    assert data["function_count"] == 1


def test_json_output_with_stats_flag(tmp_path: Path):
    (tmp_path / "foo.mcfunction").write_text("say hello\n")

    result = run_mecha(tmp_path, "-s", "-j", "stats.json", "foo.mcfunction")

    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / "stats.json").read_text())["function_count"] == 1


def test_no_json_file_without_json_flag(tmp_path: Path):
    (tmp_path / "foo.mcfunction").write_text("say hello\n")

    result = run_mecha(tmp_path, "foo.mcfunction")

    assert result.returncode == 0, result.stdout + result.stderr
    assert list(tmp_path.glob("*.json")) == []
