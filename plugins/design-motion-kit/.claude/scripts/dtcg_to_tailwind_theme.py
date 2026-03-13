from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALIAS_RE = re.compile(r"^\{([A-Za-z0-9_.-]+)\}$")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: object) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def iter_tokens(node: object, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], dict]]:
    items: list[tuple[tuple[str, ...], dict]] = []
    if isinstance(node, dict):
        if "$value" in node:
            items.append((path, node))
        else:
            for key, value in node.items():
                if str(key).startswith("$"):
                    continue
                items.extend(iter_tokens(value, path + (str(key),)))
    return items


def normalize_name(path: tuple[str, ...]) -> str:
    return "-".join(part.replace("_", "-").lower() for part in path)


def to_css_value(value: object, token_type: str | None) -> str:
    if isinstance(value, str):
        alias = ALIAS_RE.match(value)
        if alias:
            return f"var(--{normalize_name(tuple(alias.group(1).split('.')))})"
        return value
    if isinstance(value, (int, float)):
        if token_type in {"duration", "time"}:
            return f"{value}ms"
        if token_type in {"dimension", "spacing", "borderRadius", "fontSize", "lineHeight", "letterSpacing"}:
            return f"{value}px"
        return str(value)
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        if {"x", "y", "blur", "spread", "color"}.issubset(value):
            return f"{value['x']} {value['y']} {value['blur']} {value['spread']} {value['color']}"
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def expand_token(path: tuple[str, ...], token: dict) -> list[tuple[str, str, str]]:
    token_type = token.get("$type")
    value = token.get("$value")
    logical_name = ".".join(path)
    flat_name = normalize_name(path)

    if token_type == "typography" and isinstance(value, dict):
        mapping = {
            "fontFamily": f"font-{flat_name}",
            "fontSize": f"text-{flat_name}",
            "fontWeight": f"font-weight-{flat_name}",
            "lineHeight": f"leading-{flat_name}",
            "letterSpacing": f"tracking-{flat_name}",
        }
        expanded: list[tuple[str, str, str]] = []
        for key, var_name in mapping.items():
            if key in value:
                expanded.append((var_name, to_css_value(value[key], key), f"{logical_name}.{key}"))
        return expanded

    if token_type in {"shadow", "boxShadow"} and isinstance(value, list):
        shadow_value = ", ".join(to_css_value(item, token_type) for item in value)
        return [(flat_name, shadow_value, logical_name)]

    if token_type == "cubicBezier" and isinstance(value, list) and len(value) == 4:
        return [(flat_name, f"cubic-bezier({', '.join(str(item) for item in value)})", logical_name)]

    return [(flat_name, to_css_value(value, token_type), logical_name)]


def build_theme_bundle(token_payload: object) -> tuple[dict[str, str], dict[str, str]]:
    variables: dict[str, str] = {}
    aliases: dict[str, str] = {}
    for path, token in iter_tokens(token_payload):
        for var_name, css_value, logical_name in expand_token(path, token):
            variables[var_name] = css_value
            aliases[logical_name] = f"var(--{var_name})"
    return variables, aliases


def write_theme_css(path: Path, variables: dict[str, str]) -> None:
    lines = ["@theme {"]
    for name in sorted(variables):
        lines.append(f"  --{name}: {variables[name]};")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-css", required=True)
    parser.add_argument("--out-aliases", required=True)
    args = parser.parse_args()

    token_payload = load_json(Path(args.input))
    variables, aliases = build_theme_bundle(token_payload)
    write_theme_css(Path(args.out_css), variables)
    write_json(Path(args.out_aliases), aliases)
    print(f"generated {len(variables)} theme variables")


if __name__ == "__main__":
    main()
