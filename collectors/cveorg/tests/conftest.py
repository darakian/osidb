import json
from pathlib import Path

import pytest
from django.utils import timezone

from collectors.cveorg.collectors import CVEorgCollector
from collectors.cveorg.models import Keyword


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def _enable_sync(enable_jira_task_sync, enable_bz_sync):
    pass


@pytest.fixture(autouse=True)
def auto_enable_sync(request):
    # only activate this autouse fixture for integration tests
    if request.node.get_closest_marker("integration"):
        request.getfixturevalue("_enable_sync")


@pytest.fixture()
def mock_keywords(monkeypatch) -> None:
    """
    Set testing keywords to mock the ones from the ps-constants repository.
    """
    Keyword(keyword="kernel", type=Keyword.Type.ALLOWLIST).save()
    Keyword(keyword=r"(?:\W|^)\.NET\b", type=Keyword.Type.ALLOWLIST_SPECIAL_CASE).save()
    Keyword(keyword=".*plugin.*for WordPress", type=Keyword.Type.BLOCKLIST).save()
    Keyword(keyword="Cisco", type=Keyword.Type.BLOCKLIST).save()
    Keyword(keyword="IBM Tivoli", type=Keyword.Type.BLOCKLIST).save()
    Keyword(keyword="iTunes", type=Keyword.Type.BLOCKLIST).save()
    Keyword(keyword="iOS", type=Keyword.Type.BLOCKLIST_SPECIAL_CASE).save()


@pytest.fixture
def repo_path():
    return f"{Path(__file__).resolve().parent}/cvelistV5"


@pytest.fixture()
def mock_repo(monkeypatch, repo_path) -> None:
    """
    Set testing data and variables to mock the cvelistV5 repository.
    """
    cve_path = r"CVE-(?:1999|2\d{3})-(?!0{4})(?:0\d{3}|[1-9]\d{3,}).json$"

    def clone_repo(self):
        return

    def update_repo(self):
        return

    def get_repo_changes(self):
        stdout = "CVE-2024-0181.json\nCVE-2024-0203.json\nCVE-2024-1087.json\nCVE-2024-4923.json\n"
        period_end = timezone.datetime(
            2024, 7, 1, tzinfo=timezone.get_current_timezone()
        )
        return stdout, period_end

    def get_cve_file_path(self, cve):
        return f"{repo_path}/CVE-2024-0181.json"

    monkeypatch.setattr(CVEorgCollector, "REPO_PATH", repo_path)
    monkeypatch.setattr(CVEorgCollector, "CVE_PATH", cve_path)
    monkeypatch.setattr(CVEorgCollector, "clone_repo", clone_repo)
    monkeypatch.setattr(CVEorgCollector, "update_repo", update_repo)
    monkeypatch.setattr(CVEorgCollector, "get_repo_changes", get_repo_changes)
    monkeypatch.setattr(CVEorgCollector, "get_cve_file_path", get_cve_file_path)


@pytest.fixture
def cna_cvss_content(repo_path):
    with open(f"{repo_path}/CVE-2024-0203.json", "r") as f:
        return json.load(f)


@pytest.fixture
def cisa_cvss_content(repo_path):
    with open(f"{repo_path}/CVE-2025-22871.json", "r") as f:
        return json.load(f)


@pytest.fixture
def no_descriptions_content(repo_path):
    with open(f"{repo_path}/CVE-2025-37902.json", "r") as f:
        return json.load(f)
