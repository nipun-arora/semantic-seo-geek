#!/usr/bin/env python3
"""Validate and build the public Semantic SEO Geek plugin repository."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import sys
import tarfile
import tempfile
from typing import Iterable, Mapping, Sequence
from urllib.parse import unquote
import zlib


PACKAGE_NAME = "semantic-seo-geek"
PACKAGE_DIR = Path("plugins") / PACKAGE_NAME
PUBLISHER = "Nipun Arora"
PUBLISHER_URL = "https://nipunarora.me"
AUTHOR_EMAIL = "hi@nipunarora.me"
REPOSITORY = "https://github.com/nipun-arora/semantic-seo-geek"
VERSION = "1.0.0"
LICENSE_ID = "Apache-2.0"
DISPLAY_NAME = "Semantic SEO Geek"
CATEGORY = "Productivity"
GITATTRIBUTES_CONTENT = (
    "* text=auto eol=lf\n"
    "*.png binary\n"
    "*.sh text eol=lf\n"
)
EXPECTED_SKILLS = frozenset(
    {
        "aiseo-strategist",
        "algorithmic-writer",
        "content-auditor",
        "content-humanizer",
        "eav-optimizer",
        "page-production",
        "technical-seo",
        "title-heading-optimizer",
        "topical-map-architect",
        "using-semantic-seo-geek",
        "visual-semantics",
    }
)

CATALOG_PATHS = (
    Path(".agents/plugins/marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
)
MANIFEST_PATHS = (
    PACKAGE_DIR / ".codex-plugin/plugin.json",
    PACKAGE_DIR / ".claude-plugin/plugin.json",
)
GENERATED_FILES = frozenset({Path("FILES.json"), Path("SHA256SUMS")})

FORBIDDEN_SUFFIXES = frozenset(
    {".pdf", ".docx", ".pptx", ".zip", ".tar", ".gz"}
)
FORBIDDEN_FILENAMES = frozenset({"strings.txt"})
FORBIDDEN_DIRECTORIES = frozenset(
    {
        "notes",
        "research",
        "corpus",
        "knowledge" + "-base",
        "source" + "-material",
        "original" + "-package",
        ".planning",
    }
)

ROOT_PUBLIC_FILES = frozenset(
    {
        Path(".gitattributes"),
        Path(".gitignore"),
        Path("README.md"),
        Path("LICENSE"),
        Path("NOTICE.md"),
        Path("CHANGELOG.md"),
        Path("TRADEMARKS.md"),
        Path("ACKNOWLEDGEMENTS.md"),
        Path("CONTRIBUTING.md"),
        Path("CODE_OF_CONDUCT.md"),
        Path("SECURITY.md"),
        Path("SUPPORT.md"),
        Path("GOVERNANCE.md"),
        Path("VERSION"),
        Path(".github/CODEOWNERS"),
        Path(".github/ISSUE_TEMPLATE/bug.yml"),
        Path(".github/ISSUE_TEMPLATE/config.yml"),
        Path(".github/ISSUE_TEMPLATE/workflow-request.yml"),
        Path(".github/assets/social-preview.png"),
        Path(".github/workflows/validate.yml"),
        Path("docs/compatibility.md"),
        Path("docs/faq.md"),
        Path("docs/how-it-works.md"),
        Path("docs/installation.md"),
        Path("docs/license.md"),
        Path("docs/skills.md"),
        Path("docs/worked-example.md"),
        Path("scripts/validate.py"),
        Path("scripts/sync-public.sh"),
        Path("tests/test_validate.py"),
    }
)
ROOT_PUBLIC_FILES = ROOT_PUBLIC_FILES.union(CATALOG_PATHS)
PACKAGE_PUBLIC_FILES = frozenset(
    {
        PACKAGE_DIR / "LICENSE",
        PACKAGE_DIR / "NOTICE.md",
        PACKAGE_DIR / "CHANGELOG.md",
        PACKAGE_DIR / "SOURCES.md",
        PACKAGE_DIR / "TRADEMARKS.md",
        PACKAGE_DIR / "ACKNOWLEDGEMENTS.md",
        PACKAGE_DIR / "assets/icon.png",
        PACKAGE_DIR / "skills/content-humanizer/scripts/scan-copy-patterns.sh",
        PACKAGE_DIR / "skills/page-production/scripts/page-structure-audit.sh",
    }
).union(MANIFEST_PATHS)
SKILL_PUBLIC_FILES = frozenset(
    PACKAGE_DIR / "skills" / skill / relative_path
    for skill in EXPECTED_SKILLS
    for relative_path in (Path("SKILL.md"), Path("agents/openai.yaml"))
)
PUBLIC_FILES = (
    ROOT_PUBLIC_FILES
    | PACKAGE_PUBLIC_FILES
    | SKILL_PUBLIC_FILES
)
REQUIRED_PUBLIC_FILES = PUBLIC_FILES
PNG_REQUIREMENTS: Mapping[Path, tuple[int, int, int, int]] = {
    Path(".github/assets/social-preview.png"): (1280, 640, 8, 2),
    PACKAGE_DIR / "assets/icon.png": (512, 512, 8, 6),
}
PNG_SHA256: Mapping[Path, str] = {
    Path(".github/assets/social-preview.png"): (
        "b45dea4c608bdaffbe06908bb9fdf8d48fd4624e6fa30f0904debe67dbcb0755"
    ),
    PACKAGE_DIR / "assets/icon.png": (
        "33fdf74afe0e1fc8e0f0edc3c8cc29f404c50109ceee3026ffda2e793a25e65f"
    ),
}
BINARY_PUBLIC_FILES = frozenset(PNG_REQUIREMENTS)
MAX_PNG_SIZE = 2 * 1024 * 1024
FORBIDDEN_PNG_CHUNKS = frozenset({b"tEXt", b"zTXt", b"iTXt", b"eXIf"})
UNFINISHED_SCAN_SUFFIXES = frozenset(
    {"", ".cff", ".json", ".md", ".txt", ".yaml", ".yml"}
)


class ValidationError(ValueError):
    """Raised when repository validation fails."""


class _DuplicateKeyError(ValueError):
    pass


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _repository_entries(root: Path) -> Iterable[tuple[Path, Path, str]]:
    """Yield repository entries without following links or entering .git."""
    stack = [(root, Path())]
    while stack:
        directory, relative_directory = stack.pop()
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name, reverse=True)
        except OSError as error:
            raise ValidationError(f"cannot read {relative_directory or Path('.')}: {error}") from error

        child_directories: list[tuple[Path, Path]] = []
        for entry in entries:
            relative_path = relative_directory / entry.name
            if relative_path.parts and relative_path.parts[0] == ".git":
                continue
            path = Path(entry.path)
            if entry.is_symlink():
                yield relative_path, path, "symlink"
            elif entry.is_dir(follow_symlinks=False):
                yield relative_path, path, "directory"
                child_directories.append((path, relative_path))
            elif entry.is_file(follow_symlinks=False):
                yield relative_path, path, "file"
            else:
                yield relative_path, path, "special"
        stack.extend(child_directories)


def _validate_tree_structure(
    root: Path,
    *,
    strict_artifact: bool,
) -> tuple[Path, ...]:
    if root.is_symlink():
        raise ValidationError("repository root must not be a symlink")
    if not root.is_dir():
        raise ValidationError(f"repository root is not a directory: {root}")
    if strict_artifact and os.path.lexists(root / ".git"):
        raise ValidationError("public artifact contains .git outside the allowlist")

    allowed_artifact_directories = {
        parent
        for relative_path in PUBLIC_FILES.union(GENERATED_FILES)
        for parent in relative_path.parents
        if parent != Path(".")
    }

    files: list[Path] = []
    for relative_path, _path, kind in _repository_entries(root):
        display = relative_path.as_posix()
        if kind == "symlink":
            raise ValidationError(f"symlink is not allowed: {display}")
        if kind == "special":
            raise ValidationError(f"special filesystem entry is not allowed: {display}")
        if any(ord(character) < 32 or ord(character) == 127 for character in display):
            raise ValidationError(f"unsafe filename is not allowed: {display!r}")

        lower_parts = tuple(part.casefold() for part in relative_path.parts)
        is_private_planning_path = bool(lower_parts and lower_parts[0] == ".planning")
        is_allowed_private_planning_path = (
            is_private_planning_path and not strict_artifact
        )
        if (
            not is_allowed_private_planning_path
            and any(part in FORBIDDEN_DIRECTORIES for part in lower_parts)
        ):
            raise ValidationError(f"forbidden directory in path: {display}")
        if kind == "directory":
            if strict_artifact and relative_path not in allowed_artifact_directories:
                raise ValidationError(
                    f"public artifact contains directory outside the allowlist: {display}"
                )
            continue

        lower_name = relative_path.name.casefold()
        if (
            not is_allowed_private_planning_path
            and (
                lower_name in FORBIDDEN_FILENAMES
                or relative_path.suffix.casefold() in FORBIDDEN_SUFFIXES
            )
        ):
            raise ValidationError(f"forbidden file: {display}")
        files.append(relative_path)

    return tuple(sorted(files, key=lambda path: path.as_posix()))


def _is_public_file(relative_path: Path) -> bool:
    return relative_path in PUBLIC_FILES


def _is_private_control_path(relative_path: Path) -> bool:
    return (
        bool(relative_path.parts and relative_path.parts[0] == ".planning")
        or relative_path.name == "AGENTS.md"
    )


def _collect_public_files(files: Iterable[Path]) -> tuple[Path, ...]:
    return tuple(
        sorted(
            (path for path in files if _is_public_file(path)),
            key=lambda path: path.as_posix(),
        )
    )


def _required_paths() -> tuple[Path, ...]:
    return tuple(sorted(REQUIRED_PUBLIC_FILES, key=lambda path: path.as_posix()))


def _validate_required_files(root: Path) -> None:
    missing = [path.as_posix() for path in _required_paths() if not (root / path).is_file()]
    if missing:
        raise ValidationError("missing required files: " + ", ".join(missing))


def _read_utf8(path: Path, relative_path: Path) -> str:
    try:
        content = path.read_bytes()
        if content.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
            raise ValidationError(
                f"archive signature found at public text path: {relative_path.as_posix()}"
            )
        if b"\x00" in content:
            raise ValidationError(
                f"NUL byte found at public text path: {relative_path.as_posix()}"
            )
        return content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError(f"public text file is not valid UTF-8: {relative_path.as_posix()}") from error
    except OSError as error:
        raise ValidationError(f"cannot read {relative_path.as_posix()}: {error}") from error


def _frontmatter(path: Path, relative_path: Path) -> dict[str, str]:
    text = _read_utf8(path, relative_path)
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValidationError(f"invalid frontmatter opening delimiter: {relative_path.as_posix()}")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        raise ValidationError(f"invalid frontmatter closing delimiter: {relative_path.as_posix()}") from error

    values: dict[str, str] = {}
    current_block_key: str | None = None
    block_values: dict[str, list[str]] = {}
    for line in lines[1:closing_index]:
        if not line.strip():
            if current_block_key:
                block_values[current_block_key].append("")
            continue
        if line[0].isspace():
            if current_block_key is None:
                raise ValidationError(f"invalid frontmatter line in {relative_path.as_posix()}")
            block_values[current_block_key].append(line.strip())
            continue

        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)", line)
        if match is None:
            raise ValidationError(f"invalid frontmatter line in {relative_path.as_posix()}")
        key, value = match.groups()
        if key in values:
            raise ValidationError(f"duplicate frontmatter key {key!r}: {relative_path.as_posix()}")
        values[key] = value.strip()
        current_block_key = None
        if value.strip() in {">", "|", ">-", "|-", ">+", "|+"}:
            current_block_key = key
            block_values[key] = []

    for key, lines_for_key in block_values.items():
        values[key] = " ".join(part for part in lines_for_key if part).strip()
    for key, value in tuple(values.items()):
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            values[key] = value[1:-1].strip()
    return values


def _validate_skills(root: Path) -> None:
    skills_root = root / PACKAGE_DIR / "skills"
    if not skills_root.is_dir():
        raise ValidationError(f"missing skills directory: {(PACKAGE_DIR / 'skills').as_posix()}")
    actual_skills = {
        child.name
        for child in skills_root.iterdir()
        if child.is_dir()
        and not child.is_symlink()
    }
    missing_skill_files = {
        skill
        for skill in EXPECTED_SKILLS
        if not (skills_root / skill / "SKILL.md").is_file()
    }
    if actual_skills != EXPECTED_SKILLS:
        missing = sorted(EXPECTED_SKILLS - actual_skills)
        unexpected = sorted(actual_skills - EXPECTED_SKILLS)
        raise ValidationError(
            f"skill set must match expected 11 skills; missing={missing}, unexpected={unexpected}"
        )
    if missing_skill_files:
        raise ValidationError(
            "skill set must include a SKILL.md for every expected skill; missing="
            f"{sorted(missing_skill_files)}"
        )

    for skill in sorted(EXPECTED_SKILLS):
        relative_path = PACKAGE_DIR / "skills" / skill / "SKILL.md"
        values = _frontmatter(root / relative_path, relative_path)
        if set(values) != {"name", "description"}:
            raise ValidationError(
                f"frontmatter keys must be exactly name and description: {relative_path.as_posix()}"
            )
        if values["name"] != skill:
            raise ValidationError(
                f"frontmatter name must match folder name {skill!r}: {relative_path.as_posix()}"
            )
        if not values["description"]:
            raise ValidationError(f"frontmatter description must not be empty: {relative_path.as_posix()}")


def _reject_duplicate_keys(pairs: Sequence[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _load_json(root: Path, relative_path: Path) -> dict[str, object]:
    path = root / relative_path
    try:
        text = path.read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except _DuplicateKeyError as error:
        raise ValidationError(
            f"duplicate JSON key {error.args[0]!r}: {relative_path.as_posix()}"
        ) from error
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid JSON: {relative_path.as_posix()}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"JSON root must be an object: {relative_path.as_posix()}")
    return value


def _catalog_entry(
    root: Path,
    relative_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    catalog = _load_json(root, relative_path)
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        raise ValidationError(
            f"catalog must contain exactly one plugin object: {relative_path.as_posix()}"
        )
    entry = plugins[0]
    configured_source = entry.get("source")
    if relative_path == CATALOG_PATHS[0]:
        if not isinstance(configured_source, dict):
            raise ValidationError(
                f"Codex catalog source must be a local source object: {relative_path.as_posix()}"
            )
        if configured_source.get("source") != "local":
            raise ValidationError(
                f"catalog source object must declare source='local': {relative_path.as_posix()}"
            )
        configured_path = configured_source.get("path")
        if not isinstance(configured_path, str):
            raise ValidationError(
                f"catalog source object must include a string path: {relative_path.as_posix()}"
            )
    else:
        if not isinstance(configured_source, str):
            raise ValidationError(
                f"Claude catalog source must be a relative string: {relative_path.as_posix()}"
            )
        configured_path = configured_source
    if configured_path != "./" + PACKAGE_DIR.as_posix():
        raise ValidationError(
            f"catalog path must be exactly ./{PACKAGE_DIR.as_posix()}: "
            f"{relative_path.as_posix()}"
        )

    resolved_path = (root / unquote(configured_path)).resolve()
    expected_path = (root / PACKAGE_DIR).resolve()
    if (
        not _is_within(resolved_path, root)
        or resolved_path != expected_path
        or not resolved_path.is_dir()
    ):
        raise ValidationError(
            f"catalog path must resolve to {PACKAGE_DIR.as_posix()} inside the repository: "
            f"{relative_path.as_posix()}"
        )
    return catalog, entry


def _nested_value(record: object, keys: Sequence[str]) -> object:
    value = record
    for key in keys:
        if not isinstance(value, Mapping) or key not in value:
            return None
        value = value[key]
    return value


def _require_exact(
    record: Mapping[str, object],
    keys: Sequence[str],
    expected: object,
    *,
    source: Path,
    label: str,
) -> None:
    actual = _nested_value(record, keys)
    if actual != expected:
        raise ValidationError(
            f"{label} must be {expected!r} in {source.as_posix()}; got {actual!r}"
        )


def _validate_json_metadata(root: Path) -> None:
    catalog_records: list[
        tuple[Path, Mapping[str, object], Mapping[str, object]]
    ] = []
    for catalog_path in CATALOG_PATHS:
        catalog, entry = _catalog_entry(root, catalog_path)
        catalog_records.append((catalog_path, catalog, entry))
    manifest_records = [
        (manifest_path, _load_json(root, manifest_path))
        for manifest_path in MANIFEST_PATHS
    ]

    codex_path, codex_catalog, codex_entry = catalog_records[0]
    claude_path, claude_catalog, claude_entry = catalog_records[1]
    for path, catalog, entry in catalog_records:
        _require_exact(catalog, ("name",), PACKAGE_NAME, source=path, label="name")
        _require_exact(entry, ("name",), PACKAGE_NAME, source=path, label="name")
        _require_exact(entry, ("category",), CATEGORY, source=path, label="category")

    _require_exact(
        codex_catalog,
        ("interface", "displayName"),
        DISPLAY_NAME,
        source=codex_path,
        label="interface displayName",
    )
    _require_exact(
        codex_entry,
        ("policy", "installation"),
        "AVAILABLE",
        source=codex_path,
        label="policy installation",
    )
    _require_exact(
        codex_entry,
        ("policy", "authentication"),
        "ON_INSTALL",
        source=codex_path,
        label="policy authentication",
    )
    _require_exact(
        claude_catalog,
        ("owner", "name"),
        PUBLISHER,
        source=claude_path,
        label="owner name",
    )
    _require_exact(
        claude_catalog,
        ("owner", "url"),
        PUBLISHER_URL,
        source=claude_path,
        label="owner url",
    )
    _require_exact(
        claude_catalog,
        ("owner", "email"),
        AUTHOR_EMAIL,
        source=claude_path,
        label="owner email",
    )

    for manifest_path, manifest in manifest_records:
        for keys, expected, label in (
            (("name",), PACKAGE_NAME, "name"),
            (("version",), VERSION, "version"),
            (("author", "name"), PUBLISHER, "publisher author name"),
            (("author", "email"), AUTHOR_EMAIL, "author email"),
            (("author", "url"), PUBLISHER_URL, "author url"),
            (("homepage",), REPOSITORY, "homepage"),
            (("repository",), REPOSITORY, "repository"),
            (("license",), LICENSE_ID, "license"),
        ):
            _require_exact(
                manifest,
                keys,
                expected,
                source=manifest_path,
                label=label,
            )

    codex_manifest = manifest_records[0][1]
    for keys, expected, label in (
        (("skills",), "./skills/", "skills"),
        (("interface", "displayName"), DISPLAY_NAME, "interface displayName"),
        (("interface", "developerName"), PUBLISHER, "interface developerName"),
        (("interface", "category"), CATEGORY, "interface category"),
        (("interface", "websiteURL"), REPOSITORY, "interface websiteURL"),
        (("interface", "composerIcon"), "./assets/icon.png", "composerIcon"),
        (("interface", "logo"), "./assets/icon.png", "logo"),
    ):
        _require_exact(
            codex_manifest,
            keys,
            expected,
            source=MANIFEST_PATHS[0],
            label=label,
        )
    _require_exact(
        manifest_records[1][1],
        ("displayName",),
        DISPLAY_NAME,
        source=MANIFEST_PATHS[1],
        label="displayName",
    )


def _validate_release_invariants(root: Path) -> None:
    attributes_path = Path(".gitattributes")
    if _read_utf8(root / attributes_path, attributes_path) != GITATTRIBUTES_CONTENT:
        raise ValidationError(
            ".gitattributes must contain exactly the canonical three release rules"
        )

    version_path = Path("VERSION")
    if _read_utf8(root / version_path, version_path).rstrip("\r\n") != VERSION:
        raise ValidationError(f"VERSION must contain exactly {VERSION}")

    release_heading = re.compile(
        rf"^## \[{re.escape(VERSION)}\](?: - \d{{4}}-\d{{2}}-\d{{2}})?$",
        re.MULTILINE,
    )
    for relative_path in (Path("CHANGELOG.md"), PACKAGE_DIR / "CHANGELOG.md"):
        text = _read_utf8(root / relative_path, relative_path)
        if len(release_heading.findall(text)) != 1:
            raise ValidationError(
                f"changelog must contain exactly one {VERSION} release heading: "
                f"{relative_path.as_posix()}"
            )

    for filename in (
        "ACKNOWLEDGEMENTS.md",
        "LICENSE",
        "TRADEMARKS.md",
    ):
        root_path = root / filename
        package_path = root / PACKAGE_DIR / filename
        try:
            root_content = root_path.read_bytes()
            package_content = package_path.read_bytes()
        except OSError as error:
            raise ValidationError(f"cannot compare legal file {filename}: {error}") from error
        if root_content != package_content:
            raise ValidationError(
                f"root and package {filename} must be byte-identical"
            )


def _png_chunks(content: bytes, relative_path: Path) -> list[tuple[bytes, bytes]]:
    display = relative_path.as_posix()
    if len(content) > MAX_PNG_SIZE:
        raise ValidationError(f"PNG exceeds 2 MiB limit: {display}")
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValidationError(f"invalid PNG signature: {display}")

    chunks: list[tuple[bytes, bytes]] = []
    offset = 8
    saw_iend = False
    while offset < len(content):
        if len(content) - offset < 12:
            raise ValidationError(f"truncated PNG chunk header: {display}")
        length = struct.unpack(">I", content[offset : offset + 4])[0]
        chunk_type = content[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(content):
            raise ValidationError(f"truncated PNG chunk data: {display}")
        chunk_data = content[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack(">I", content[offset + 8 + length : chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if expected_crc != actual_crc:
            raise ValidationError(f"PNG chunk CRC mismatch: {display}")
        if chunk_type in FORBIDDEN_PNG_CHUNKS:
            raise ValidationError(
                f"forbidden PNG chunk {chunk_type.decode('ascii')}: {display}"
            )
        chunks.append((chunk_type, chunk_data))
        offset = chunk_end
        if chunk_type == b"IEND":
            saw_iend = True
            if offset != len(content):
                raise ValidationError(f"PNG has trailing bytes after IEND: {display}")
            break

    if not saw_iend:
        raise ValidationError(f"truncated PNG without final IEND: {display}")
    if not chunks or chunks[0][0] != b"IHDR":
        raise ValidationError(f"IHDR must be the first PNG chunk: {display}")
    if chunks[-1][0] != b"IEND":
        raise ValidationError(f"IEND must be the final PNG chunk: {display}")
    if sum(chunk_type == b"IHDR" for chunk_type, _data in chunks) != 1:
        raise ValidationError(f"PNG must contain exactly one IHDR chunk: {display}")
    if sum(chunk_type == b"IEND" for chunk_type, _data in chunks) != 1:
        raise ValidationError(f"PNG must contain exactly one IEND chunk: {display}")
    if chunks[-1][1]:
        raise ValidationError(f"IEND chunk must be empty: {display}")
    return chunks


def _decompress_png_rows(
    idat_data: bytes,
    expected_length: int,
    relative_path: Path,
) -> bytes:
    display = relative_path.as_posix()
    decompressor = zlib.decompressobj()
    try:
        decoded = decompressor.decompress(idat_data, expected_length + 1)
        if decompressor.unconsumed_tail or len(decoded) > expected_length:
            raise ValidationError(f"PNG decompressed length is too large: {display}")
        decoded += decompressor.flush(expected_length + 1 - len(decoded))
    except zlib.error as error:
        raise ValidationError(f"invalid PNG compressed image data: {display}") from error
    if decompressor.unconsumed_tail:
        raise ValidationError(f"PNG has unconsumed compressed image data: {display}")
    if not decompressor.eof:
        raise ValidationError(f"truncated PNG compressed image data: {display}")
    if decompressor.unused_data:
        raise ValidationError(f"PNG has unused compressed image data: {display}")
    if len(decoded) != expected_length:
        raise ValidationError(
            f"PNG decompressed length mismatch: {display}; "
            f"expected {expected_length}, got {len(decoded)}"
        )
    return decoded


def _validate_png(root: Path, relative_path: Path) -> None:
    display = relative_path.as_posix()
    try:
        content = (root / relative_path).read_bytes()
    except OSError as error:
        raise ValidationError(f"cannot read PNG {display}: {error}") from error
    chunks = _png_chunks(content, relative_path)
    ihdr = chunks[0][1]
    if len(ihdr) != 13:
        raise ValidationError(f"IHDR chunk must contain 13 bytes: {display}")
    width, height, bit_depth, color_type, compression, filtering, interlace = (
        struct.unpack(">IIBBBBB", ihdr)
    )
    expected_width, expected_height, expected_depth, expected_color = PNG_REQUIREMENTS[
        relative_path
    ]
    if (width, height) != (expected_width, expected_height):
        raise ValidationError(
            f"PNG dimensions must be {expected_width}x{expected_height}: {display}"
        )
    if bit_depth != expected_depth:
        raise ValidationError(f"PNG bit depth must be {expected_depth}: {display}")
    if color_type != expected_color:
        raise ValidationError(f"PNG color type must be {expected_color}: {display}")
    if (compression, filtering, interlace) != (0, 0, 0):
        raise ValidationError(
            f"PNG must use standard compression/filtering and no interlace: {display}"
        )

    idat_parts = [data for chunk_type, data in chunks if chunk_type == b"IDAT"]
    if not idat_parts:
        raise ValidationError(f"PNG must contain image data: {display}")
    channels = {2: 3, 6: 4}[color_type]
    row_length = 1 + width * channels
    decoded = _decompress_png_rows(
        b"".join(idat_parts),
        height * row_length,
        relative_path,
    )
    for row_index in range(height):
        filter_byte = decoded[row_index * row_length]
        if filter_byte > 4:
            raise ValidationError(
                f"PNG row filter byte must be between 0 and 4: "
                f"{display}, row {row_index + 1}"
            )

    digest = hashlib.sha256(content).hexdigest()
    if digest != PNG_SHA256[relative_path]:
        raise ValidationError(
            f"PNG SHA-256 does not match the canonical release asset: {display}"
        )


def _validate_png_files(root: Path) -> None:
    for relative_path in sorted(PNG_REQUIREMENTS, key=lambda path: path.as_posix()):
        _validate_png(root, relative_path)


def _unfinished_patterns() -> tuple[re.Pattern[str], ...]:
    words = (
        "TO" + "DO",
        "TK" + "TK",
        "lorem" + " ipsum",
        "coming" + " soon",
        "replace" + " me",
    )
    patterns = [
        re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
        for word in words
    ]
    patterns.append(
        re.compile(r"\b" + re.escape("PLACE" + "HOLDER") + r"\b(?!\s*:)", re.IGNORECASE)
    )
    return tuple(patterns)


def _private_patterns(configured_markers: Iterable[str]) -> tuple[re.Pattern[str], ...]:
    patterns = [
        re.compile(r"/" + r"Users/[A-Za-z0-9._-]+(?:(?:/|\\)|\b)"),
        re.compile(r"/" + r"home/[A-Za-z0-9._-]+(?:(?:/|\\)|\b)"),
        re.compile(
            r"[A-Za-z]:\\" + r"Users\\[A-Za-z0-9._-]+(?:\\|\b)",
            re.IGNORECASE,
        ),
        re.compile(re.escape("CL" + "00ENA"), re.IGNORECASE),
        re.compile(r"\bcourse[\s_-]+notes\b", re.IGNORECASE),
        re.compile(r"\bknowledge[\s_-]+base\b", re.IGNORECASE),
        re.compile(r"\bsource[\s_-]+material\b", re.IGNORECASE),
        re.compile(r"\boriginal[\s_-]+package\b", re.IGNORECASE),
        re.compile(
            r"\b[A-Z0-9._%+-]+@(?:gmail|yahoo|hotmail|outlook|icloud|protonmail)\."
            r"(?:com|net|org|me)\b",
            re.IGNORECASE,
        ),
    ]
    for marker in configured_markers:
        if not isinstance(marker, str) or not marker.strip():
            raise ValidationError("configured private markers must be non-empty strings")
        patterns.append(re.compile(re.escape(marker.strip()), re.IGNORECASE))
    return tuple(patterns)


def _secret_patterns() -> tuple[re.Pattern[str], ...]:
    return (
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(
            r"\b(?:api[_-]?key|secret|access[_-]?token|password)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}",
            re.IGNORECASE,
        ),
    )


def _scan_repository_content(
    root: Path,
    files: Iterable[Path],
    public_files: Iterable[Path],
    configured_markers: Iterable[str],
    *,
    ignore_private_control_paths: bool,
) -> None:
    private_patterns = _private_patterns(configured_markers)
    unfinished_patterns = _unfinished_patterns()
    secret_patterns = _secret_patterns()
    public_file_set = set(public_files)

    for relative_path, _path, _kind in _repository_entries(root):
        if ignore_private_control_paths and _is_private_control_path(relative_path):
            continue
        display = relative_path.as_posix()
        if any(pattern.search(display) for pattern in private_patterns):
            raise ValidationError(f"private marker found in filename: {display}")

    for relative_path in files:
        if ignore_private_control_paths and _is_private_control_path(relative_path):
            continue
        display = relative_path.as_posix()
        if relative_path in BINARY_PUBLIC_FILES:
            continue

        if relative_path in public_file_set or relative_path in GENERATED_FILES:
            text = _read_utf8(root / relative_path, relative_path)
        else:
            try:
                content = (root / relative_path).read_bytes()
                if b"\x00" in content:
                    continue
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                continue
            except OSError as error:
                raise ValidationError(f"cannot read {display}: {error}") from error
        if (
            relative_path in public_file_set
            and relative_path.suffix.casefold() in UNFINISHED_SCAN_SUFFIXES
            and any(pattern.search(text) for pattern in unfinished_patterns)
        ):
            raise ValidationError(f"unfinished content marker found: {display}")
        if any(pattern.search(text) for pattern in private_patterns):
            raise ValidationError(f"private marker found in UTF-8 text: {display}")
        if any(pattern.search(text) for pattern in secret_patterns):
            raise ValidationError(f"secret pattern found: {display}")


def _markdown_without_code_fences(text: str) -> str:
    visible_lines: list[str] = []
    fence_character: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if fence_character is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence_character = stripped[0]
            continue
        if fence_character is not None:
            if stripped.startswith(fence_character * 3):
                fence_character = None
            continue
        visible_lines.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(visible_lines)


def _markdown_targets(text: str) -> Iterable[str]:
    visible_text = _markdown_without_code_fences(text)
    inline_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
    reference_pattern = re.compile(r"^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(\S+)", re.MULTILINE)
    for match in inline_pattern.finditer(visible_text):
        raw_target = match.group(1).strip()
        if raw_target.startswith("<") and ">" in raw_target:
            yield raw_target[1 : raw_target.index(">")]
        else:
            yield raw_target.split(maxsplit=1)[0]
    for match in reference_pattern.finditer(visible_text):
        yield match.group(1).strip("<>")


def _github_heading_slug(heading: str) -> str:
    without_images = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    without_links = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", without_images)
    without_tags = re.sub(r"<[^>]*>", "", without_links)
    without_markup = re.sub(r"[`*_~]", "", without_tags).strip().casefold()
    without_punctuation = "".join(
        character
        for character in without_markup
        if character.isalnum() or character in {" ", "-", "_"}
    )
    return re.sub(r"\s", "-", without_punctuation)


def _markdown_anchors(text: str) -> frozenset[str]:
    anchors: set[str] = set()
    slug_counts: dict[str, int] = {}
    heading_pattern = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
    for line in _markdown_without_code_fences(text).splitlines():
        heading_match = heading_pattern.match(line)
        if heading_match:
            base_slug = _github_heading_slug(heading_match.group(1))
            if base_slug:
                occurrence = slug_counts.get(base_slug, 0)
                slug_counts[base_slug] = occurrence + 1
                anchors.add(base_slug if occurrence == 0 else f"{base_slug}-{occurrence}")
        for explicit_anchor in re.findall(
            r"<(?:a\s+[^>]*(?:name|id)|[A-Za-z][^>]*\sid)\s*=\s*['\"]([^'\"]+)['\"][^>]*>",
            line,
            flags=re.IGNORECASE,
        ):
            anchors.add(unquote(explicit_anchor).casefold())
    return frozenset(anchors)


def _normalize_link_path(source_parent: Path, path_part: str) -> Path | None:
    parts = list(source_parent.parts)
    for part in PurePosixPath(path_part).parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)
    return Path(*parts)


def _has_exact_path_component_case(root: Path, relative_path: Path) -> bool:
    current = root
    for component in relative_path.parts:
        try:
            with os.scandir(current) as entries:
                names = {entry.name for entry in entries}
        except OSError:
            return False
        if component not in names:
            return False
        current /= component
    return True


def _validate_markdown_links(root: Path, public_files: Iterable[Path]) -> None:
    uri_scheme = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
    for relative_path in public_files:
        if (
            relative_path.suffix.casefold() != ".md"
            and relative_path.name != "LICENSE"
        ):
            continue
        text = _read_utf8(root / relative_path, relative_path)
        for raw_target in _markdown_targets(text):
            target = unquote(raw_target).replace("\\ ", " ")
            if not target or target.startswith("/"):
                continue
            if uri_scheme.match(target):
                continue
            target_without_fragment, separator, fragment = target.partition("#")
            path_part = target_without_fragment.split("?", 1)[0]
            target_relative = (
                relative_path
                if not path_part
                else _normalize_link_path(relative_path.parent, path_part)
            )
            if target_relative is None:
                raise ValidationError(
                    f"Markdown link escapes the repository: "
                    f"{relative_path.as_posix()} -> {raw_target}"
                )
            if not _has_exact_path_component_case(root, target_relative):
                raise ValidationError(
                    f"Markdown link must use exact path-component case: "
                    f"{relative_path.as_posix()} -> {raw_target}"
                )
            resolved_target = (root / target_relative).resolve()
            if not _is_within(resolved_target, root) or not resolved_target.exists():
                raise ValidationError(
                    f"Markdown link does not resolve inside the repository: "
                    f"{relative_path.as_posix()} -> {raw_target}"
                )
            if separator and fragment:
                if not resolved_target.is_file():
                    raise ValidationError(
                        f"Markdown fragment target is not a file: "
                        f"{relative_path.as_posix()} -> {raw_target}"
                    )
                try:
                    resolved_relative = resolved_target.relative_to(root)
                except ValueError as error:
                    raise ValidationError(
                        f"Markdown fragment escapes the repository: "
                        f"{relative_path.as_posix()} -> {raw_target}"
                    ) from error
                target_text = _read_utf8(resolved_target, resolved_relative)
                if fragment.casefold() not in _markdown_anchors(target_text):
                    raise ValidationError(
                        f"Markdown fragment does not resolve: "
                        f"{relative_path.as_posix()} -> {raw_target}"
                    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _validate_generated_metadata(
    root: Path,
    public_files: tuple[Path, ...],
    *,
    required: bool,
) -> None:
    files_path = root / "FILES.json"
    checksums_path = root / "SHA256SUMS"
    if not files_path.exists() and not checksums_path.exists():
        if required:
            raise ValidationError(
                "strict artifact validation requires FILES.json and SHA256SUMS"
            )
        return
    if not files_path.is_file() or not checksums_path.is_file():
        raise ValidationError("FILES.json and SHA256SUMS must both be present")

    metadata = _load_json(root, Path("FILES.json"))
    entries = metadata.get("files")
    if metadata.get("format") != 1 or not isinstance(entries, list):
        raise ValidationError("FILES.json has an invalid schema")

    expected_entries = [
        {
            "path": path.as_posix(),
            "sha256": _sha256(root / path),
            "size": (root / path).stat().st_size,
        }
        for path in public_files
    ]
    if entries != expected_entries:
        raise ValidationError("FILES.json does not match the public artifact")

    checksum_records = [
        (entry["path"], entry["sha256"])
        for entry in expected_entries
    ]
    checksum_records.append(("FILES.json", _sha256(files_path)))
    expected_checksums = "".join(
        f"{digest}  {path}\n" for path, digest in sorted(checksum_records)
    )
    try:
        actual_checksums = checksums_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValidationError("SHA256SUMS must be valid UTF-8 text") from error
    if actual_checksums != expected_checksums:
        raise ValidationError("SHA256SUMS does not match the public artifact")


def validate_repository(
    root: str | Path,
    *,
    private_markers: Iterable[str] = (),
    require_all_files_public: bool = False,
) -> tuple[Path, ...]:
    """Validate a source repository and return its allowlisted public files."""
    input_root = Path(root).expanduser()
    if input_root.is_symlink():
        raise ValidationError("repository root must not be a symlink")
    resolved_root = input_root.resolve()
    files = _validate_tree_structure(
        resolved_root,
        strict_artifact=require_all_files_public,
    )
    _validate_skills(resolved_root)
    _validate_required_files(resolved_root)
    _validate_json_metadata(resolved_root)
    _validate_release_invariants(resolved_root)
    _validate_png_files(resolved_root)
    public_files = _collect_public_files(files)
    if any(_is_private_control_path(path) for path in public_files):
        raise ValidationError("private control paths must never enter the public export")
    _scan_repository_content(
        resolved_root,
        files,
        public_files,
        private_markers,
        ignore_private_control_paths=not require_all_files_public,
    )
    _validate_markdown_links(resolved_root, public_files)

    has_generated_metadata = any(path in files for path in GENERATED_FILES)
    if require_all_files_public or has_generated_metadata:
        allowed_artifact_files = set(public_files).union(GENERATED_FILES)
        unexpected_files = sorted(
            (path.as_posix() for path in files if path not in allowed_artifact_files)
        )
        if unexpected_files:
            raise ValidationError(
                "public artifact contains files outside the allowlist: "
                + ", ".join(unexpected_files)
            )
    _validate_generated_metadata(
        resolved_root,
        public_files,
        required=require_all_files_public,
    )
    return public_files


def _write_bytes(path: Path, content: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(content)
    path.chmod(mode)
    os.utime(path, (0, 0))


def _normalize_directories(root: Path) -> None:
    directories = [path for path in root.rglob("*") if path.is_dir()]
    for directory in sorted(directories, key=lambda path: len(path.parts), reverse=True):
        directory.chmod(0o755)
        os.utime(directory, (0, 0))
    root.chmod(0o755)
    os.utime(root, (0, 0))


def _stage_public_directory(
    source_root: Path,
    staging_root: Path,
    public_files: tuple[Path, ...],
) -> None:
    staging_root.mkdir()
    for relative_path in public_files:
        mode = 0o755 if relative_path.suffix == ".sh" else 0o644
        _write_bytes(staging_root / relative_path, (source_root / relative_path).read_bytes(), mode)

    entries = [
        {
            "path": relative_path.as_posix(),
            "sha256": _sha256(staging_root / relative_path),
            "size": (staging_root / relative_path).stat().st_size,
        }
        for relative_path in public_files
    ]
    files_json = (json.dumps({"files": entries, "format": 1}, indent=2, sort_keys=True) + "\n").encode()
    _write_bytes(staging_root / "FILES.json", files_json)

    checksum_records = [(entry["path"], entry["sha256"]) for entry in entries]
    checksum_records.append(("FILES.json", _sha256(staging_root / "FILES.json")))
    checksums = "".join(
        f"{digest}  {path}\n" for path, digest in sorted(checksum_records)
    ).encode()
    _write_bytes(staging_root / "SHA256SUMS", checksums)
    _normalize_directories(staging_root)


def _staged_files(staging_root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            (path.relative_to(staging_root) for path in staging_root.rglob("*") if path.is_file()),
            key=lambda path: path.as_posix(),
        )
    )


def _write_deterministic_tar_gzip(staging_root: Path, archive_path: Path) -> None:
    with archive_path.open("xb") as raw_stream:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=9,
            fileobj=raw_stream,
            mtime=0,
        ) as compressed_stream:
            with tarfile.open(
                mode="w",
                fileobj=compressed_stream,
                format=tarfile.GNU_FORMAT,
            ) as archive:
                for relative_path in _staged_files(staging_root):
                    content = (staging_root / relative_path).read_bytes()
                    information = tarfile.TarInfo(relative_path.as_posix())
                    information.size = len(content)
                    information.mode = 0o755 if relative_path.suffix == ".sh" else 0o644
                    information.mtime = 0
                    information.uid = 0
                    information.gid = 0
                    information.uname = ""
                    information.gname = ""
                    archive.addfile(information, io.BytesIO(content))


def _scan_tar_gzip(archive_path: Path, private_markers: Iterable[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="ssg-archive-scan-") as temporary_directory:
        extracted_root = Path(temporary_directory) / "artifact"
        extracted_root.mkdir()
        with tarfile.open(archive_path, mode="r:gz") as archive:
            members = archive.getmembers()
            names = [member.name for member in members]
            if names != sorted(names) or len(names) != len(set(names)):
                raise ValidationError("archive members must be unique and sorted")
            for member in members:
                pure_path = PurePosixPath(member.name)
                if (
                    not member.isfile()
                    or pure_path.is_absolute()
                    or not pure_path.parts
                    or any(part in {"", ".", ".."} for part in pure_path.parts)
                ):
                    raise ValidationError(f"unsafe archive member: {member.name}")
                source = archive.extractfile(member)
                if source is None:
                    raise ValidationError(f"cannot read archive member: {member.name}")
                _write_bytes(extracted_root.joinpath(*pure_path.parts), source.read(), member.mode)
        _normalize_directories(extracted_root)
        validate_repository(
            extracted_root,
            private_markers=private_markers,
            require_all_files_public=True,
        )


def build_public_artifact(
    root: str | Path,
    destination: str | Path,
    *,
    output_format: str,
    private_markers: Iterable[str] = (),
) -> Path:
    """Build a deterministic allowlisted directory or tar.gz artifact."""
    if output_format not in {"dir", "tar.gz"}:
        raise ValidationError("output format must be 'dir' or 'tar.gz'")

    source_input = Path(root).expanduser()
    if source_input.is_symlink():
        raise ValidationError("source repository root must not be a symlink")
    source_root = source_input.resolve()
    output_path = Path(destination).expanduser()
    if os.path.lexists(output_path):
        raise ValidationError(f"destination already exists: {output_path}")
    resolved_output = output_path.resolve()
    if _is_within(resolved_output, source_root):
        raise ValidationError("destination must be outside the source repository")

    markers = tuple(private_markers)
    public_files = validate_repository(source_root, private_markers=markers)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".ssg-public-build-",
        dir=resolved_output.parent,
    ) as temporary_directory:
        staging_root = Path(temporary_directory) / "artifact"
        _stage_public_directory(source_root, staging_root, public_files)
        validate_repository(
            staging_root,
            private_markers=markers,
            require_all_files_public=True,
        )

        if output_format == "dir":
            os.replace(staging_root, resolved_output)
        else:
            temporary_archive = Path(temporary_directory) / "artifact.tar.gz"
            _write_deterministic_tar_gzip(staging_root, temporary_archive)
            _scan_tar_gzip(temporary_archive, markers)
            os.replace(temporary_archive, resolved_output)
    return resolved_output


def _markers_from_environment() -> tuple[str, ...]:
    configured = os.environ.get("SSG_PRIVATE_MARKERS", "")
    return tuple(
        marker.strip()
        for line in configured.splitlines()
        for marker in line.split(",")
        if marker.strip()
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and build the public Semantic SEO Geek plugin repository."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command, help_text in (
        ("check", "validate a repository"),
        ("validate", "alias for check"),
    ):
        check_parser = subparsers.add_parser(command, help=help_text)
        check_parser.add_argument("root", nargs="?", default=".")
        check_parser.add_argument(
            "--private-marker",
            action="append",
            default=[],
            help="additional case-insensitive private marker; may be repeated",
        )
        check_parser.add_argument(
            "--strict",
            action="store_true",
            help="require a complete built artifact with generated integrity metadata",
        )

    build_parser = subparsers.add_parser("build", help="build a public artifact")
    build_parser.add_argument("root", nargs="?", default=".")
    build_parser.add_argument("--output", required=True)
    build_parser.add_argument("--format", choices=("dir", "tar.gz"), default="dir")
    build_parser.add_argument(
        "--private-marker",
        action="append",
        default=[],
        help="additional case-insensitive private marker; may be repeated",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    options = _parser().parse_args(arguments)
    markers = _markers_from_environment() + tuple(options.private_marker)
    try:
        if options.command in {"check", "validate"}:
            public_files = validate_repository(
                options.root,
                private_markers=markers,
                require_all_files_public=options.strict,
            )
            print(f"validated {len(public_files)} public files")
        else:
            output = build_public_artifact(
                options.root,
                options.output,
                output_format=options.format,
                private_markers=markers,
            )
            print(f"built {output}")
    except ValidationError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
