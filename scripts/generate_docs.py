#!/usr/bin/env python3
"""
Rolex Price API - Static Documentation Generator

Fetches or generates the OpenAPI specification and produces a standalone,
production-ready Swagger UI static website under `docs-site/` ready for S3 deployment.
"""

import sys
import os
import argparse
import urllib.request
import json
from pathlib import Path

# Add project root to python path to import FastAPI app if running locally
sys.path.insert(0, str(Path(__file__).parent.parent))


def generate_openapi_spec(api_url: str = None) -> dict:
    """Retrieves OpenAPI schema from deployed API Gateway or local FastAPI instance."""
    if api_url:
        target_url = f"{api_url.rstrip('/')}/openapi.json"
        print(f"Fetching remote OpenAPI schema from {target_url}...")
        try:
            req = urllib.request.Request(target_url, headers={"User-Agent": "DocsGenerator/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    print("✅ Successfully fetched remote OpenAPI schema.")
                    return data
        except Exception as err:
            print(f"⚠️ Remote OpenAPI fetch failed ({err}). Falling back to local FastAPI schema.")

    print("Generating local OpenAPI schema from app.main:app...")
    from app.main import app
    return app.openapi()


def create_swagger_html() -> str:
    """Returns standalone Swagger UI HTML page template."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>👑 Rolex Price API - Technical Documentation & API Reference</title>
  <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/favicon-32x32.png" />
  <style>
    html { box-sizing: border-box; overflow-y: scroll; }
    *, *:before, *:after { box-sizing: inherit; }
    body { margin: 0; background: #fafafa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .topbar { background-color: #0d1117; padding: 12px 24px; color: #ffffff; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #30363d; }
    .topbar-title { font-size: 1.15rem; font-weight: 700; color: #f0f6fc; display: flex; align-items: center; gap: 8px; }
    .topbar-links { display: flex; gap: 16px; font-size: 0.9rem; }
    .topbar-links a { color: #58a6ff; text-decoration: none; font-weight: 600; transition: color 0.2s ease; }
    .topbar-links a:hover { color: #79c0ff; text-decoration: underline; }
    .swagger-ui .topbar { display: none; }
    .swagger-ui .wrapper { max-width: 1200px; padding: 20px; }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-title">
      👑 Rolex Price API SaaS — Interactive API Reference & Technical Docs
    </div>
    <div class="topbar-links">
      <a href="./index.html">API Reference</a>
      <a href="./openapi.json" target="_blank">OpenAPI Spec (JSON)</a>
    </div>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: "./openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout",
        displayRequestDuration: true,
        docExpansion: "list",
        filter: true
      });
    };
  </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Generate Rolex API Static Documentation Site")
    parser.add_argument("--api-url", help="Deployed API Gateway base URL")
    parser.add_argument("--out-dir", default="docs-site", help="Output directory for generated site")
    args = parser.parse_args()

    out_path = Path(args.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Generate OpenAPI Spec
    openapi_data = generate_openapi_spec(args.api_url)
    
    # Write openapi.json
    openapi_file = out_path / "openapi.json"
    with open(openapi_file, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, indent=2)
    print(f"✅ Created {openapi_file} ({openapi_file.stat().st_size} bytes)")

    # 2. Write index.html (Swagger UI)
    index_file = out_path / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(create_swagger_html())
    print(f"✅ Created {index_file} ({index_file.stat().st_size} bytes)")

    print(f"\n🎉 Static documentation site generated successfully in '{out_path}/'")


if __name__ == "__main__":
    main()
