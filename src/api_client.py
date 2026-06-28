"""USGS Earthquake API client.

The USGS GeoJSON summary feeds are fully public (no auth, ~1-minute freshness),
so the dashboard refreshes itself from a GitHub Actions cron with no secret.
Feeds: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
"""
from __future__ import annotations

import requests

USGS_FEED_URL = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{feed}.geojson"
)


class USGSClient:
    """Minimal client for the public USGS earthquake GeoJSON feeds."""

    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout

    def get_feed(self, feed: str) -> list[dict]:
        """Return the raw GeoJSON `features` list for a named summary feed.

        Common feeds: ``all_hour``, ``all_day``, ``all_week``,
        ``significant_week``, ``significant_month``, ``4.5_day``.
        Each feature has ``properties`` (mag, place, time, url, depth via
        geometry, felt, tsunami, alert, sig, magType, type, title) and
        ``geometry.coordinates`` = [lon, lat, depth_km].
        """
        resp = requests.get(
            USGS_FEED_URL.format(feed=feed),
            headers={"Accept": "application/json", "User-Agent": "quake-radar"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        features = data.get("features", [])
        if not isinstance(features, list):
            raise ValueError(f"USGS feed '{feed}' returned no features")
        return features


if __name__ == "__main__":  # smoke test
    c = USGSClient()
    day = c.get_feed("all_day")
    sig = c.get_feed("significant_week")
    print(f"all_day: {len(day)} quakes · significant_week: {len(sig)}")
    if day:
        p = day[0]["properties"]
        print("sample keys:", sorted(p.keys()))
        print("sample:", p.get("mag"), "—", p.get("place"), "|", p.get("url"))
