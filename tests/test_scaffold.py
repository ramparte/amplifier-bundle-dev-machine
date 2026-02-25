"""Tests for Task 1: Bundle scaffold structure.

Validates:
- bundle.md exists with valid YAML frontmatter
- behaviors/dev-machine.yaml exists with correct config
- README.md exists with required sections
- All required directories exist
- All YAML files parse without errors
"""

import os
import yaml
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_file(rel_path):
    """Read a file relative to repo root."""
    full_path = os.path.join(REPO_ROOT, rel_path)
    with open(full_path) as f:
        return f.read()


def _parse_frontmatter(content):
    """Extract and parse YAML frontmatter from markdown file."""
    parts = content.split("---")
    assert len(parts) >= 3, "File must have YAML frontmatter delimited by ---"
    return yaml.safe_load(parts[1])


# ---------------------------------------------------------------------------
# bundle.md tests
# ---------------------------------------------------------------------------

class TestBundleMd:
    def test_bundle_md_exists(self):
        assert os.path.isfile(os.path.join(REPO_ROOT, "bundle.md"))

    def test_bundle_name(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        assert fm["bundle"]["name"] == "dev-machine"

    def test_bundle_version(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        assert fm["bundle"]["version"] == "0.1.0"

    def test_agents_include_lists_three_agents(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        agents = fm["agents"]["include"]
        assert len(agents) == 3
        assert "admissions-advisor" in agents
        assert "machine-designer" in agents
        assert "machine-generator" in agents

    def test_context_include_lists_two_files(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        ctx = fm["context"]["include"]
        assert len(ctx) == 2
        assert any("pattern.md" in c for c in ctx)
        assert any("gate-criteria.md" in c for c in ctx)

    def test_includes_behavior(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        includes = fm["includes"]
        assert any("behaviors/dev-machine.yaml" in str(i) for i in includes)

    def test_bundle_has_description(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        assert "description" in fm["bundle"]
        assert len(fm["bundle"]["description"]) > 10

    def test_bundle_body_mentions_three_modes(self):
        content = _read_file("bundle.md")
        body = content.split("---", 2)[2]
        assert "/admissions" in body or "admissions" in body.lower()
        assert "/machine-design" in body or "machine-design" in body.lower()
        assert "/generate-machine" in body or "generate-machine" in body.lower()

    def test_bundle_body_mentions_pattern(self):
        content = _read_file("bundle.md")
        body = content.split("---", 2)[2]
        assert "pattern" in body.lower()


# ---------------------------------------------------------------------------
# behaviors/dev-machine.yaml tests
# ---------------------------------------------------------------------------

class TestBehaviorYaml:
    def test_behavior_file_exists(self):
        assert os.path.isfile(os.path.join(REPO_ROOT, "behaviors", "dev-machine.yaml"))

    def test_behavior_yaml_parses(self):
        content = _read_file("behaviors/dev-machine.yaml")
        data = yaml.safe_load(content)
        assert data is not None

    def test_hooks_mode_configured(self):
        data = yaml.safe_load(_read_file("behaviors/dev-machine.yaml"))
        hooks = data.get("hooks", [])
        hook_modules = [h["module"] for h in hooks]
        assert "hooks-mode" in hook_modules

    def test_hooks_mode_search_paths(self):
        data = yaml.safe_load(_read_file("behaviors/dev-machine.yaml"))
        hooks = data.get("hooks", [])
        hooks_mode = [h for h in hooks if h["module"] == "hooks-mode"][0]
        search_paths = hooks_mode["config"]["search_paths"]
        assert any("@dev-machine:modes" in p for p in search_paths)

    def test_three_tool_modules_configured(self):
        data = yaml.safe_load(_read_file("behaviors/dev-machine.yaml"))
        tools = data.get("tools", [])
        tool_modules = [t["module"] for t in tools]
        assert "tool-mode" in tool_modules
        assert "tool-filesystem" in tool_modules
        assert "tool-search" in tool_modules
        assert "tool-bash" in tool_modules

    def test_tool_mode_gate_policy_warn(self):
        data = yaml.safe_load(_read_file("behaviors/dev-machine.yaml"))
        tools = data.get("tools", [])
        tool_mode = [t for t in tools if t["module"] == "tool-mode"][0]
        assert tool_mode["config"]["gate_policy"] == "warn"


# ---------------------------------------------------------------------------
# README.md tests
# ---------------------------------------------------------------------------

class TestReadme:
    def test_readme_exists(self):
        assert os.path.isfile(os.path.join(REPO_ROOT, "README.md"))

    def test_readme_has_quick_start(self):
        content = _read_file("README.md")
        assert "## Quick Start" in content

    def test_readme_has_what_it_does(self):
        content = _read_file("README.md")
        assert "## What It Does" in content

    def test_readme_has_generated_output(self):
        content = _read_file("README.md")
        assert "## Generated Output" in content

    def test_readme_has_the_pattern(self):
        content = _read_file("README.md")
        assert "## The Pattern" in content

    def test_readme_has_license(self):
        content = _read_file("README.md")
        assert "## License" in content

    def test_readme_mentions_three_phases(self):
        content = _read_file("README.md")
        assert "Admissions" in content
        assert "Machine Design" in content or "machine-design" in content
        assert "Generate" in content


# ---------------------------------------------------------------------------
# Directory structure tests
# ---------------------------------------------------------------------------

class TestDirectories:
    @pytest.mark.parametrize("dirname", [
        "agents",
        "modes",
        "context",
        "templates",
        os.path.join("templates", "recipes"),
        "behaviors",
        os.path.join("docs", "plans"),
    ])
    def test_directory_exists(self, dirname):
        full_path = os.path.join(REPO_ROOT, dirname)
        assert os.path.isdir(full_path), f"Directory {dirname} does not exist"


# ---------------------------------------------------------------------------
# YAML parsing tests
# ---------------------------------------------------------------------------

class TestYamlValidity:
    def test_behavior_yaml_valid(self):
        content = _read_file("behaviors/dev-machine.yaml")
        data = yaml.safe_load(content)
        assert isinstance(data, dict)

    def test_bundle_frontmatter_valid(self):
        fm = _parse_frontmatter(_read_file("bundle.md"))
        assert isinstance(fm, dict)
        assert "bundle" in fm
