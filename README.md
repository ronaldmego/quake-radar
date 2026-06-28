<p align="center">
  <img src="./images/logo.svg" alt="Quake Radar" width="92">
</p>

<h1 align="center">Quake Radar</h1>

<p align="center">
  <strong>A live world map of earthquakes</strong> — public USGS data, refreshed every 30 minutes. Open-source, zero-server.
</p>

<p align="center">
  <a href="https://ronaldmego.github.io/quake-radar"><img src="https://img.shields.io/badge/live-quake--radar-1f3a5f?style=for-the-badge" alt="Live"></a>
  <a href="https://github.com/ronaldmego/quake-radar/actions/workflows/publish.yml"><img src="https://github.com/ronaldmego/quake-radar/actions/workflows/publish.yml/badge.svg" alt="Publish"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT"></a>
</p>

<p align="center">
  <img src="./screenshots/dashboard.png" alt="Quake Radar dashboard" width="820">
</p>

## Why

When the ground shakes, the first question is "what was that, and where?" **Quake Radar** pulls every earthquake reported worldwide in the last 24 hours onto one live map — magnitude, depth, and a link to the official USGS event page — and keeps it current automatically.

> Informational only — not an official alert system. For emergencies and official guidance, refer to your national agency (e.g. **FUNVISIS** in Venezuela) and the USGS event pages linked in each table.

## What it shows

- **Live world map** — every quake in the last 24h as a dot (size = magnitude, color = depth), with hover details.
- **At-a-glance stats** — quakes in 24h, strongest, M4.5+ count, significant in the last 7 days, deepest.
- **Tables** — most recent · strongest (24h) · significant (7d), each linking to the official USGS event page · plus a searchable catalog.
- **About** — the open methodology behind it (so you can audit, fork, or reuse the pipeline).

## How it works

```
USGS GeoJSON API  →  Python (pandas + great-tables)  →  Quarto dashboard  →  GitHub Pages
        \____________ refreshed every 30 min by GitHub Actions (cron) ____________/
```

**Zero server, zero cost, no API key.** The USGS feeds are public, so a GitHub Actions cron re-fetches the data, re-renders the dashboard, and redeploys to GitHub Pages — no secrets, no backend. Every number traces back to the exact public endpoint shown in the *Source* footer on each page.

## Run locally

Requires [uv](https://docs.astral.sh/uv/) and [Quarto](https://quarto.org) 1.8+.

```bash
git clone https://github.com/ronaldmego/quake-radar.git
cd quake-radar
uv run quarto preview index.qmd
```

To check the data pipeline alone:

```bash
uv run python src/data_processor.py
```

## Data source

[USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/) — the public GeoJSON summary feeds (`all_day`, `significant_week`). Public domain. Quake Radar is an independent project and is not affiliated with the USGS.

## License

MIT — see [LICENSE](LICENSE).
