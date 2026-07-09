"""Transform raw USGS earthquake features into a clean DataFrame for the dashboard."""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd


# Canonical columns of the tidy DataFrame — kept even when a feed is empty so
# downstream views never KeyError (e.g. 'significant_week' has zero events for a
# calm week, which is normal and must render as an empty table, not crash CI).
QUAKE_COLUMNS = [
    "mag", "mag_type", "place", "lon", "lat", "depth", "time", "time_str",
    "age_h", "url", "felt", "tsunami", "alert", "sig", "type",
]


def _alert_label(alert: str | None) -> str:
    # USGS PAGER alert level (impact estimate): green < yellow < orange < red.
    return (alert or "").lower() or "—"


def process_quakes(features: list[dict], now: datetime | None = None) -> pd.DataFrame:
    """Return a tidy DataFrame, one row per earthquake (most recent first)."""
    now = now or datetime.now(timezone.utc)
    rows = []
    for f in features:
        p = f.get("properties") or {}
        geom = (f.get("geometry") or {}).get("coordinates") or [None, None, None]
        lon, lat, depth = (geom + [None, None, None])[:3]
        t_ms = p.get("time")
        t_dt = (
            datetime.fromtimestamp(t_ms / 1000, tz=timezone.utc) if t_ms else None
        )
        mag = p.get("mag")
        rows.append(
            {
                "mag": float(mag) if mag is not None else None,
                "mag_type": p.get("magType") or "—",
                "place": p.get("place") or p.get("title") or "—",
                "lon": float(lon) if lon is not None else None,
                "lat": float(lat) if lat is not None else None,
                "depth": round(float(depth), 1) if depth is not None else None,
                "time": t_dt,
                "time_str": t_dt.strftime("%Y-%m-%d %H:%M") if t_dt else "—",
                "age_h": round((now - t_dt).total_seconds() / 3600, 1) if t_dt else None,
                "url": p.get("url") or "",
                "felt": int(p["felt"]) if p.get("felt") else 0,
                "tsunami": bool(p.get("tsunami")),
                "alert": _alert_label(p.get("alert")),
                "sig": int(p.get("sig") or 0),
                "type": p.get("type") or "earthquake",
            }
        )
    df = pd.DataFrame(rows, columns=QUAKE_COLUMNS)
    if not df.empty:
        df = df.sort_values("time", ascending=False).reset_index(drop=True)
    return df


def summary_stats(df_day: pd.DataFrame, df_sig: pd.DataFrame) -> dict:
    """High-level numbers for the hero value boxes."""
    quakes = df_day[df_day["type"] == "earthquake"]
    strongest = quakes.nlargest(1, "mag") if len(quakes) else quakes
    return {
        "count_24h": int(len(quakes)),
        "max_mag": f'{strongest["mag"].iloc[0]:.1f}' if len(strongest) else "—",
        "max_mag_place": strongest["place"].iloc[0] if len(strongest) else "—",
        "m45_24h": int((quakes["mag"] >= 4.5).sum()) if len(quakes) else 0,
        "significant_7d": int(len(df_sig)),
        "max_depth": int(quakes["depth"].max()) if len(quakes) and quakes["depth"].notna().any() else 0,
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


if __name__ == "__main__":  # smoke test
    from api_client import USGSClient

    c = USGSClient()
    df = process_quakes(c.get_feed("all_day"))
    sig = process_quakes(c.get_feed("significant_week"))
    print(df[["time_str", "mag", "place", "depth", "alert"]].head(8).to_string())
    print()
    for k, v in summary_stats(df, sig).items():
        print(f"{k}: {v}")
