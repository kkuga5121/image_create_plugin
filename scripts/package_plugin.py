"""Build one validated portable plugin ZIP without replacing existing files."""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

from validate_plugin import validate_plugin


def build_archive(plugin_dir: Path, output_dir: Path) -> Path:
    errors = validate_plugin(plugin_dir)
    if errors:
        raise ValueError("\n".join(errors))
    root = plugin_dir.resolve()
    output = output_dir.resolve()
    if output.is_relative_to(root):
        raise ValueError("Archive output must be outside the plugin directory")
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    target = output / f'{manifest["name"]}-{manifest["version"]}.zip'
    if target.exists() or target.is_symlink():
        raise ValueError(f"Archive already exists; preserve or remove it explicitly: {target}")
    output.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output, suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(root.rglob("*")):
                if path.is_symlink():
                    raise ValueError(f"symlink forbidden: {path.relative_to(root)}")
                if path.is_file():
                    archive.write(path, (Path(root.name) / path.relative_to(root)).as_posix())
        # Same-directory hard link publishes atomically and fails if a target appeared.
        try:
            os.link(temporary, target)
        except FileExistsError:
            raise ValueError(f"Archive already exists: {target}") from None
        return target
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(build_archive(args.plugin_dir, args.output_dir))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
