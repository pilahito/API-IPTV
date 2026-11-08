#!/usr/bin/env python3
"""Validate the repository's channels.json without third-party packages."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_FIELDS = ("canal", "pais", "m3u8", "enlace", "ruta", "codigo")


def validate(path: Path) -> int:
    try:
        # utf-8-sig also accepts the byte-order mark present in the current catalog.
        with path.open(encoding="utf-8-sig") as catalog_file:
            catalog = json.load(catalog_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: no se pudo leer {path}: {error}", file=sys.stderr)
        return 1

    errors = []
    if not isinstance(catalog, dict):
        print("ERROR: el catálogo debe ser un objeto JSON agrupado por país.", file=sys.stderr)
        return 1

    channel_count = 0
    for country, channels in catalog.items():
        if not isinstance(country, str) or not country.strip():
            errors.append("Hay una clave de país vacía o inválida.")
            continue
        if not isinstance(channels, list):
            errors.append(f"{country}: el valor debe ser una lista de canales.")
            continue

        for index, channel in enumerate(channels, start=1):
            location = f"{country}, canal #{index}"
            channel_count += 1
            if not isinstance(channel, dict):
                errors.append(f"{location}: cada canal debe ser un objeto JSON.")
                continue

            for field in REQUIRED_FIELDS:
                if not isinstance(channel.get(field), str) or not channel[field].strip():
                    errors.append(f"{location}: falta el campo de texto '{field}'.")

            if any(not isinstance(channel.get(field), str) or not channel[field].strip()
                   for field in REQUIRED_FIELDS):
                continue

            if channel["pais"] != country:
                errors.append(f"{location}: el campo 'pais' no coincide con la clave '{country}'.")

            stream_url = urlparse(channel["m3u8"])
            if stream_url.scheme not in ("http", "https") or not stream_url.netloc:
                errors.append(f"{location}: 'm3u8' debe ser una URL HTTP o HTTPS válida.")

            expected_link = f"player.html?=tv-{channel['codigo']}-{channel['ruta']}"
            if channel["enlace"] != expected_link:
                errors.append(
                    f"{location}: 'enlace' debería ser '{expected_link}'."
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validación fallida: {len(errors)} problema(s) en {channel_count} canal(es).", file=sys.stderr)
        return 1

    print(f"Catálogo válido: {len(catalog)} país(es), {channel_count} canal(es).")
    return 0


def main() -> int:
    default_catalog = Path(__file__).resolve().parent.parent / "channels.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "catalog",
        nargs="?",
        type=Path,
        default=default_catalog,
        help=f"archivo JSON a comprobar (por defecto: {default_catalog})",
    )
    args = parser.parse_args()
    return validate(args.catalog)


if __name__ == "__main__":
    raise SystemExit(main())
