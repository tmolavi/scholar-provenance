"""Schema validation tools for ScholarProvenance."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import yaml
import jsonschema


SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a schema JSON file by name."""
    schema_path = SCHEMAS_DIR / schema_name
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_json_data(data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
    """Validate JSON-compatible dictionary against a schema.

    Returns:
        (is_valid, error_messages)
    """
    schema = load_schema(schema_name)
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
        loc = ".".join(str(p) for p in err.path) if err.path else "root"
        errors.append(f"[{loc}] {err.message}")
    return (len(errors) == 0, errors)


def validate_file(file_path: str | Path, schema_name: str) -> Tuple[bool, List[str]]:
    """Validate a YAML or JSON file against a schema."""
    p = Path(file_path)
    if not p.exists():
        return (False, [f"File not found: {p}"])

    try:
        content = p.read_text(encoding="utf-8")
        if p.suffix.lower() in [".yaml", ".yml"]:
            data = yaml.safe_load(content)
        else:
            data = json.loads(content)
    except Exception as e:
        return (False, [f"Failed to parse {p.name}: {e}"])

    if not isinstance(data, dict):
        return (False, [f"Root of {p.name} must be a dictionary/object, found {type(data).__name__}"])

    return validate_json_data(data, schema_name)
