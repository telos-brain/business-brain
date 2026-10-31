#!/usr/bin/env python3
"""Generate BRA214 API tool YAML from the official Xero Accounting + Identity OpenAPI specs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ACCOUNTING_SPEC = Path("/tmp/xero_accounting.yaml")
IDENTITY_SPEC = Path("/tmp/xero_identity.yaml")
SPEC_DIR = Path("/tmp/xero-specs")
# region key, spec file, folder prefix, sentence prepended to each description.
PAYROLL_SPECS = (
    (
        "au",
        SPEC_DIR / "xero-payroll-au.yaml",
        "payroll-au",
        "Xero Payroll Australia (payroll.xro/1.0). Use only for an Australian organisation.",
    ),
    (
        "au_v2",
        SPEC_DIR / "xero-payroll-au-v2.yaml",
        "payroll-au-v2",
        "Xero Payroll Australia timesheets v2 (payroll.xro/2.0). Use for Australian timesheet lines, approve, and revert. Do not use for New Zealand or the United Kingdom.",
    ),
    (
        "nz",
        SPEC_DIR / "xero-payroll-nz.yaml",
        "payroll-nz",
        "Xero Payroll New Zealand (payroll.xro/2.0). Use only for a New Zealand organisation.",
    ),
    (
        "uk",
        SPEC_DIR / "xero-payroll-uk.yaml",
        "payroll-uk",
        "Xero Payroll United Kingdom (payroll.xro/2.0). Use only for a United Kingdom organisation.",
    ),
)
OUT_DIR = Path(__file__).resolve().parent
MANIFEST_HEADER = [
    "name: Xero",
    "description: >-",
    "  Tools for the Xero Accounting API (api.xro/2.0), Identity connections,",
    "  and Payroll APIs (Australia 1.0, Australia timesheets 2.0, New Zealand,",
    "  United Kingdom). Each tool maps one-to-one to a documented Xero endpoint.",
    "  Accept and xeroTenantId (header Xero-Tenant-Id) come from connectors/xero.yml",
    "  request-defaults.",
    "tools:",
]

SKIP_BODY_FIELDS = {
    "pagination",
    "Warnings",
    "ValidationErrors",
    "HasAttachments",
    "UpdatedDateUTC",
    "SystemAccount",
    "ReportingCodeName",
}
SKIP_HEADERS = {
    "xero-tenant-id",
    "Xero-Tenant-Id",
    "If-Modified-Since",
    "Idempotency-Key",
    "contentType",
    "Content-Type",
}
RESPONSE_ONLY = SKIP_BODY_FIELDS

BRITISH = (
    ("uncategorizes", "uncategorises"),
    ("uncategorize", "uncategorise"),
    ("categorized", "categorised"),
    ("categorizes", "categorises"),
    ("categorizing", "categorising"),
    ("categorize", "categorise"),
    ("organized", "organised"),
    ("organizing", "organising"),
    ("organize", "organise"),
    ("canceled", "cancelled"),
    ("canceling", "cancelling"),
    ("behavior", "behaviour"),
    ("favorite", "favourite"),
    ("authorized", "authorised"),
    ("authorizes", "authorises"),
    ("authorizing", "authorising"),
    ("organistaions", "organisations"),
    ("organistaion", "organisation"),
    ("organizations", "organisations"),
    ("organization", "organisation"),
)


def british(text: str) -> str:
    out = text
    for src, dst in BRITISH:
        out = re.sub(src, dst, out)
        out = re.sub(src[0].upper() + src[1:], dst[0].upper() + dst[1:], out)
    return out


def collapse(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def resolve(obj, spec, seen=None):
    if not isinstance(obj, dict):
        return obj
    ref = obj.get("$ref")
    if not ref:
        return obj
    seen = seen or set()
    if ref in seen:
        return {k: v for k, v in obj.items() if k != "$ref"}
    seen.add(ref)
    cur = spec
    for part in ref.lstrip("#/").split("/"):
        cur = cur[part]
    merged = {k: v for k, v in obj.items() if k != "$ref"}
    resolved = resolve(cur, spec, seen)
    if isinstance(resolved, dict):
        return {**resolved, **merged}
    return resolved


def deep_resolve(obj, spec, seen=None, depth=0):
    if depth > 6:
        return obj
    seen = set(seen) if seen else set()
    if isinstance(obj, dict) and "$ref" in obj:
        if obj["$ref"] in seen:
            return {"type": "object"}
        obj = resolve(obj, spec, seen)
    if isinstance(obj, dict):
        return {
            k: deep_resolve(v, spec, seen, depth + 1) if k != "example" else v
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [deep_resolve(v, spec, seen, depth + 1) for v in obj]
    return obj


def kebab(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    return value.strip("-").lower()


def snake_operation(operation_id: str, region: str = "") -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", operation_id)
    value = value.replace("-", "_").lower()
    if region:
        return f"xero_{region}_{value}"
    return "xero_" + value


def folder_for(path: str, tag: str) -> str:
    if tag == "identity":
        return "identity"
    first = path.strip("/").split("/")[0]
    return kebab(first) or "other"


def emit_folded(value: str, indent: int) -> list[str]:
    inner = " " * (indent + 2)
    return [f"{' ' * indent}>-", f"{inner}{value}"]


def map_type(schema: dict, name: str = "", description: str = "") -> str:
    t = (schema or {}).get("type")
    fmt = (schema or {}).get("format")
    blob = f"{name} {description} {fmt or ''}".lower()
    if t in {"object", "array"}:
        return "json"
    if t == "boolean":
        return "string"
    if t == "integer":
        return "int"
    if t == "number":
        return "decimal"
    if fmt == "date-time":
        return "datetime"
    if fmt == "date" or (name.lower().endswith("date") and "utc" not in name.lower()):
        return "date"
    if "yyyy-mm-dd" in blob or "e.g. 2021-02" in blob:
        return "date"
    return "string"


def field_bits(props: dict, limit: int = 18) -> str:
    bits = []
    for key, val in list(props.items())[:limit]:
        if key in RESPONSE_ONLY:
            continue
        bit = key
        if val.get("type"):
            bit += f" ({val['type']})"
        enum = val.get("enum")
        if enum:
            bit += " [" + ", ".join(str(v) for v in enum[:8]) + "]"
        elif val.get("description"):
            bit += f": {collapse(val['description']).rstrip('.')}"
        bits.append(bit)
    extra = f" and {len(props) - limit} more" if len(props) > limit else ""
    return "; ".join(bits) + extra


def describe_schema(schema: dict | None) -> str:
    schema = schema or {}
    t = schema.get("type")
    enum = schema.get("enum")
    desc = collapse(schema.get("description"))
    parts: list[str] = []
    if desc:
        parts.append(desc if desc.endswith(".") else desc + ".")
    if enum:
        shown = ", ".join(str(v) for v in enum[:20])
        more = "" if len(enum) <= 20 else f" ({len(enum)} values)"
        parts.append(f"One of: {shown}{more}.")
    if t == "array":
        if schema.get("_query_csv"):
            parts.append("Pass as a comma-separated list.")
        else:
            parts.append("Pass as a JSON array.")
            items = schema.get("items") or {}
            if isinstance(items, dict):
                item_props = items.get("properties") or {}
                if item_props:
                    parts.append("Each item may include: " + field_bits(item_props) + ".")
    elif t == "object":
        parts.append("Pass as a JSON object.")
        props = schema.get("properties") or {}
        if props:
            parts.append("Fields: " + field_bits(props) + ".")
    elif t == "boolean":
        parts.append("Use true or false.")
    return british(" ".join(parts)).strip()


def collect_parameters(item: dict, op: dict, spec: dict) -> list[dict]:
    raws = []
    for src in (item.get("parameters") or []), (op.get("parameters") or []):
        raws.extend(src)
    params = []
    seen = set()
    for raw in raws:
        raw = deep_resolve(raw, spec)
        name = raw.get("name")
        if not name or name in seen or name in SKIP_HEADERS:
            continue
        if raw.get("in") == "header":
            continue
        schema = deep_resolve(raw.get("schema") or {}, spec)
        if raw.get("in") == "query" and schema.get("type") == "array":
            schema = {**schema, "_query_csv": True, "type": "string"}
        desc = describe_schema({**schema, "description": raw.get("description") or schema.get("description")})
        if not desc:
            desc = f"{name} parameter."
        if name == "where":
            desc = (
                "Xero where filter, e.g. Status==\"AUTHORISED\" AND Type==\"ACCREC\". "
                "See https://developer.xero.com/documentation/guides/how-to-guides/filtering"
            )
        elif name == "order":
            desc = "Sort expression, e.g. Date DESC or InvoiceNumber."
        params.append(
            {
                "name": name,
                "description": british(desc),
                "type": map_type(schema, name, desc),
                "required": bool(raw.get("required")),
            }
        )
        seen.add(name)
    return params


def body_params(op: dict, spec: dict) -> list[dict]:
    rb = op.get("requestBody")
    if not rb:
        return []
    rb = deep_resolve(rb, spec)
    content = rb.get("content") or {}
    if "application/json" in content:
        schema = deep_resolve((content["application/json"] or {}).get("schema") or {}, spec)
        required = set(schema.get("required") or [])
        params = []
        props = schema.get("properties") or {}
        if props:
            for name, prop in props.items():
                if name in SKIP_BODY_FIELDS:
                    continue
                prop = deep_resolve(prop, spec)
                desc = describe_schema(prop) or f"{name} field."
                params.append(
                    {
                        "name": name,
                        "description": british(desc),
                        "type": map_type(prop, name, desc),
                        "required": name in required,
                    }
                )
            return params
        if schema.get("type") == "array":
            return [
                {
                    "name": "body",
                    "description": british(describe_schema(schema) or "JSON request body."),
                    "type": "json",
                    "required": True,
                }
            ]
        return []
    if "application/octet-stream" in content:
        return [
            {
                "name": "file",
                "description": (
                    "Raw file bytes. The Xero API expects application/octet-stream. "
                    "Include the file name in the path."
                ),
                "type": "string",
                "required": True,
            }
        ]
    return []


def emit_tool(tool: dict) -> str:
    lines = [f"name: {tool['name']}", "version: 1"]
    folded = emit_folded(tool["description"], 0)
    folded[0] = "description: >-"
    lines.extend(folded)
    lines.append("api:")
    lines.append(f"  method: {tool['method']}")
    lines.append(f"  path: {tool['path']}")
    lines.append("  connector: xero")
    params = tool["parameters"]
    if params:
        lines.append("parameters:")
        for p in params:
            lines.append(f"  - name: {p['name']}")
            folded = emit_folded(p["description"], 4)
            folded[0] = "    description: >-"
            lines.extend(folded)
            if p.get("header"):
                lines.append(f"    header: {p['header']}")
            if p.get("secret"):
                lines.append(f"    secret: {p['secret']}")
            if p.get("entity"):
                lines.append(f"    entity: {p['entity']}")
            if p.get("value") is not None:
                lines.append(f"    value: {p['value']}")
            if p.get("type"):
                lines.append(f"    type: {p['type']}")
            if p.get("required"):
                lines.append("    required: true")
    return "\n".join(lines) + "\n"


def iter_ops(spec: dict):
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            if not isinstance(op, dict):
                continue
            yield path, item, method, op


def build_from_spec(
    spec: dict,
    *,
    prefix: str,
    default_tag: str,
    region: str = "",
    folder_prefix: str = "",
    summary_prefix: str = "",
) -> list[dict]:
    tools = []
    for path, item, method, op in iter_ops(spec):
        operation_id = op.get("operationId") or f"{method}_{path.strip('/').replace('/', '_')}"
        name = snake_operation(operation_id, region)
        tag = (op.get("tags") or [default_tag])[0]
        folder = folder_for(path, tag if default_tag != "identity" else "identity")
        if folder_prefix:
            folder = f"{folder_prefix}/{folder}"
        summary = collapse(op.get("summary")) or collapse(operation_id)
        extra = collapse(op.get("description"))
        if summary and not summary.endswith("."):
            summary += "."
        parts = []
        if summary_prefix:
            parts.append(summary_prefix if summary_prefix.endswith(".") else summary_prefix + ".")
        parts.append(summary)
        if (
            extra
            and extra != summary
            and len(extra) < 400
            and "Override the base" not in extra
        ):
            parts.append(extra)
        full_path = prefix.rstrip("/") + path
        parts.append(f"Xero API {method.upper()} {full_path}.")
        description = british(" ".join(parts))

        # Accept and xeroTenantId live on connectors/xero.yml request-defaults.
        params = []
        params.extend(collect_parameters(item, op, spec))
        existing = {p["name"] for p in params}
        for p in body_params(op, spec):
            if p["name"] not in existing:
                params.append(p)
                existing.add(p["name"])

        short = name[5:] if name.startswith("xero_") else name
        if region and short.startswith(region + "_"):
            short = short[len(region) + 1 :]
        filename = kebab(short) + ".yml"
        tools.append(
            {
                "name": name,
                "method": method.upper(),
                "path": full_path,
                "description": description,
                "parameters": params,
                "rel": f"{folder}/{filename}",
                "folder": folder,
            }
        )
    return tools


def assert_unique(tools: list[dict]) -> None:
    names = [t["name"] for t in tools]
    if len(names) != len(set(names)):
        dupes = sorted({n for n in names if names.count(n) > 1})
        raise SystemExit(f"Duplicate names: {dupes}")
    rels = [t["rel"] for t in tools]
    if len(rels) != len(set(rels)):
        dupes = sorted({n for n in rels if rels.count(n) > 1})
        raise SystemExit(f"Duplicate files: {dupes}")
    for t in tools:
        tokens = set(re.findall(r"\{([^{}]+)\}", t["path"]))
        param_names = {p["name"] for p in t["parameters"]}
        missing = tokens - param_names
        if missing:
            raise SystemExit(f"{t['name']} path tokens missing parameters: {sorted(missing)}")


def write_tools(tools: list[dict]) -> None:
    for t in tools:
        dest = OUT_DIR / t["rel"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(emit_tool(t))


def write_manifest(rels: list[str]) -> None:
    lines = list(MANIFEST_HEADER)
    for rel in rels:
        lines.append(f"  - {rel}")
    (OUT_DIR / "tools.yml").write_text("\n".join(lines) + "\n")


def load_payroll_tools() -> list[dict]:
    missing = [str(path) for _, path, _, _ in PAYROLL_SPECS if not path.exists()]
    if missing:
        raise SystemExit("Missing payroll specs:\n  " + "\n  ".join(missing))
    tools = []
    for region, path, folder_prefix, summary_prefix in PAYROLL_SPECS:
        spec = yaml.safe_load(path.read_text())
        server = spec["servers"][0]["url"]
        prefix = server.removeprefix("https://api.xero.com")
        tools.extend(
            build_from_spec(
                spec,
                prefix=prefix,
                default_tag="Payroll",
                region=region,
                folder_prefix=folder_prefix,
                summary_prefix=summary_prefix,
            )
        )
    assert_unique(tools)
    return tools


def payroll_only() -> None:
    tools = load_payroll_tools()
    for yml in OUT_DIR.rglob("*.yml"):
        rel = yml.relative_to(OUT_DIR).as_posix()
        if rel.startswith("payroll-"):
            yml.unlink()
    write_tools(tools)
    existing = []
    manifest = (OUT_DIR / "tools.yml").read_text().splitlines()
    for line in manifest:
        if line.startswith("  - ") and not line[4:].startswith("payroll-"):
            existing.append(line[4:])
    write_manifest(existing + [t["rel"] for t in tools])
    print(f"wrote {len(tools)} payroll tools")
    by_folder = {}
    for t in tools:
        by_folder[t["folder"].split("/")[0]] = by_folder.get(t["folder"].split("/")[0], 0) + 1
    for folder, count in sorted(by_folder.items()):
        print(f"  {count:3} {folder}")


def main() -> None:
    accounting = yaml.safe_load(ACCOUNTING_SPEC.read_text())
    identity = yaml.safe_load(IDENTITY_SPEC.read_text())
    tools = build_from_spec(
        accounting, prefix="/api.xro/2.0", default_tag="Accounting"
    )
    tools.extend(
        build_from_spec(identity, prefix="", default_tag="identity")
    )
    tools.extend(load_payroll_tools())
    assert_unique(tools)

    for yml in OUT_DIR.rglob("*.yml"):
        yml.unlink()

    write_tools(tools)
    write_manifest([t["rel"] for t in tools])

    print(f"wrote {len(tools)} tools + tools.yml")
    by_folder = {}
    for t in tools:
        by_folder[t["folder"]] = by_folder.get(t["folder"], 0) + 1
    for folder, count in sorted(by_folder.items()):
        print(f"  {count:3} {folder}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "payroll":
        payroll_only()
    else:
        main()
