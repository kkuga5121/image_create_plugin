"""Validate this repository's portable skills-only plugin authoring format."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?\Z")
SEMVER = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z"
)
FORBIDDEN_DIRS = {".git", ".superpowers", "node_modules", "vendor", "dist",
                  "__pycache__", "wallpaper-output"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".svg"}


def _nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_name(value):
    return isinstance(value, str) and bool(NAME.fullmatch(value)) and "--" not in value and ".." not in value


def _object(path, errors):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("expected a JSON object")
        return value
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{path.name}: {exc}")
        return {}


def parse_skill_frontmatter(text: str) -> dict[str, str]:
    """Parse the documented flat, JSON-quoted YAML subset, not general YAML."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("frontmatter must start with ---")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("frontmatter needs a closing ---") from None
    result = {}
    for line in lines[1:end]:
        key, separator, raw = line.partition(":")
        if not separator or key not in {"name", "description"} or key in result:
            raise ValueError("frontmatter requires unique name and description fields")
        try:
            value = json.loads(raw.strip())
        except ValueError:
            raise ValueError(f"{key}: use a single-line JSON-quoted YAML string") from None
        if not _nonblank(value):
            raise ValueError(f"{key}: expected a nonblank string")
        result[key] = value
    if set(result) != {"name", "description"}:
        raise ValueError("frontmatter requires name and description")
    if not _valid_name(result["name"]):
        raise ValueError("invalid skill name")
    if not "\n".join(lines[end + 1:]).strip():
        raise ValueError("skill body is empty")
    return result


def _reference(value, source, root, errors):
    if not isinstance(value, str):
        errors.append(f"{source.name}: reference must be a string")
        return
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    try:
        url = urlsplit(value)
        if url.scheme or url.netloc:
            if url.scheme != "https" or not url.netloc or url.username or url.password:
                errors.append(f"{source.name}: invalid external reference {value}")
            return
        if not url.path:
            return  # Same-document fragment.
        path = Path(unquote(url.path))
        target = (source.parent / path).resolve()
        if path.is_absolute() or not target.is_relative_to(root):
            errors.append(f"{source.name}: reference escapes plugin: {value}")
        elif not target.is_file():
            errors.append(f"{source.name}: reference missing: {value}")
    except (ValueError, OSError) as exc:
        errors.append(f"{source.name}: invalid reference {value}: {exc}")


def _metadata(path, errors):
    data = _object(path, errors)
    interface = data.get("interface", {})
    if not isinstance(interface, dict):
        errors.append(f"{path.name}: interface must be an object")
    elif "interface" in data:
        for key in ("display_name", "short_description"):
            if not _nonblank(interface.get(key)):
                errors.append(f"{path.name}: interface.{key} must be nonblank")
        if "default_prompt" in interface and not _nonblank(interface["default_prompt"]):
            errors.append(f"{path.name}: invalid default_prompt")
    policy = data.get("policy", {})
    if not isinstance(policy, dict):
        errors.append(f"{path.name}: policy must be an object")
        return
    if set(policy) - {"products", "allow_implicit_invocation"}:
        errors.append(f"{path.name}: unsupported policy field")
    products = policy.get("products")
    if products is not None and (not isinstance(products, list) or
                                 any(p not in ("CODEX", "CHAT") for p in products)):
        errors.append(f"{path.name}: products must be a list of CODEX/CHAT")
    implicit = policy.get("allow_implicit_invocation")
    if implicit is not None and not isinstance(implicit, bool):
        errors.append(f"{path.name}: allow_implicit_invocation must be boolean")


def _marketplace(path, root, name, errors):
    data = _object(path, errors)
    entries = data.get("plugins")
    if not _nonblank(data.get("name")) or not isinstance(entries, list):
        errors.append("marketplace: name and plugins array required")
        return
    matches = [e for e in entries if isinstance(e, dict) and e.get("name") == name]
    if len(matches) != 1:
        errors.append("marketplace: expected one matching plugin entry")
        return
    entry = matches[0]
    source = entry.get("source", {})
    raw = source.get("path") if isinstance(source, dict) else None
    # This tool consumes the repository catalog at .agents/plugins/marketplace.json.
    repo = path.resolve().parents[2]
    if (not isinstance(source, dict) or source.get("source") != "local" or
            not isinstance(raw, str) or not raw.startswith("./")):
        errors.append("marketplace: expected local ./-prefixed source path")
    else:
        target = (repo / raw).resolve()
        if not target.is_relative_to(repo) or target != root:
            errors.append("marketplace: source does not resolve to this plugin")
    if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        errors.append("marketplace: expected AVAILABLE/ON_INSTALL policy")
    if entry.get("category") != "Productivity":
        errors.append("marketplace: expected Productivity category")


def validate_plugin(plugin_dir: Path, marketplace: Path | None = None) -> list[str]:
    errors = []
    if plugin_dir.is_symlink() or not plugin_dir.is_dir():
        return [f"Plugin directory missing or symlink: {plugin_dir}"]
    root = plugin_dir.resolve()
    try:
        paths = sorted(root.rglob("*"))
        for path in paths:
            relative = path.relative_to(root)
            if path.is_symlink():
                errors.append(f"symlink forbidden: {relative}")
            if (FORBIDDEN_DIRS.intersection(relative.parts) or path.name.startswith(".env") or
                    path.name == ".DS_Store" or
                    path.name.lower().endswith((".zip", ".tar", ".tar.gz", ".tgz", ".pyc"))):
                errors.append(f"forbidden package content: {relative}")
        if any("symlink" in error for error in errors):
            return errors  # Never read a symlink target, including its descendants.
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                errors.append(f"{path.relative_to(root)}: unreadable UTF-8 text")
                continue
            if re.search(r"chatgpt\.com/library|libfile_", text, re.I):
                errors.append(f"{path.relative_to(root)}: private library reference")
            if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}", text):
                errors.append(f"{path.relative_to(root)}: credential material forbidden")
            if path.suffix.lower() == ".md":
                for link in re.findall(r"\]\(([^)\n]+)\)", text):
                    _reference(link, path, root, errors)
        manifest_path = root / "plugin.json"
        data = _object(manifest_path, errors)
        name = data.get("name")
        if data.get("$schema") != SCHEMA:
            errors.append("plugin.json: incorrect or missing Agent Plugins schema")
        if not _valid_name(name) or name != root.name:
            errors.append("plugin.json: name must be valid and match its directory")
        version = data.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append("plugin.json: version must be strict SemVer")
        if set(data).intersection({"skills", "mcpServers", "apps", "interface"}):
            errors.append("plugin.json: portable components are not top-level manifest fields")
        extensions = data.get("extensions", {})
        openai = extensions.get("com.openai", {}) if isinstance(extensions, dict) else None
        interface = openai.get("interface", {}) if isinstance(openai, dict) else None
        if not isinstance(interface, dict):
            errors.append("plugin.json: extensions.com.openai.interface must be an object")
        else:
            for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
                if key in interface and not _nonblank(interface[key]):
                    errors.append(f"plugin.json: {key} must be nonblank")
            subtitle = interface.get("shortDescription", "")
            if isinstance(subtitle, str) and len(subtitle) > 30:
                errors.append("plugin.json: shortDescription exceeds 30 characters")
            if "category" in interface and interface["category"] != "Productivity":
                errors.append("plugin.json: expected Productivity category")
            caps = interface.get("capabilities", [])
            if not isinstance(caps, list) or any(not _nonblank(c) for c in caps):
                errors.append("plugin.json: capabilities must be an array of strings")
            for key in ("logo", "logoDark", "composerIcon", "composerIconDark"):
                if key in interface:
                    _reference(interface[key], manifest_path, root, errors)
        skills = sorted((root / "skills").glob("*/SKILL.md"))
        if not skills:
            errors.append("skills: at least one usable skill required")
        names = set()
        for skill in skills:
            if skill.parent.name.startswith("."):
                errors.append("skills: hidden skill directory is not discoverable")
            try:
                if skill.stat().st_size > 1024 * 1024:
                    raise ValueError("skill exceeds 1 MiB")
                fields = parse_skill_frontmatter(skill.read_text(encoding="utf-8"))
                if fields["name"] != skill.parent.name or fields["name"] in names:
                    raise ValueError("skill name must be unique and match its directory")
                names.add(fields["name"])
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append(f"{skill.relative_to(root)}: {exc}")
            meta = skill.parent / "agents" / "openai.yaml"
            if meta.exists():
                _metadata(meta, errors)
        if marketplace is not None:
            _marketplace(marketplace, root, name, errors)
    except (OSError, ValueError) as exc:
        errors.append(f"Package validation failed: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-dir", type=Path, required=True)
    parser.add_argument("--marketplace", type=Path)
    args = parser.parse_args()
    errors = validate_plugin(args.plugin_dir, args.marketplace)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Plugin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
