"""great-tables views for the Quake Radar dashboard."""
from __future__ import annotations

import pandas as pd
from great_tables import GT, loc, style, md

# Brand palette (editorial: navy ink + clay accent) — shared with the portfolio.
NAVY = "#1f3a5f"
INK = "#16202e"
CLAY = "#a8482b"
PAPER = "#faf7f1"


def _fmt_mag(v) -> str:
    if v is None or pd.isna(v):
        return "—"
    return f"M{v:.1f}"


def _view(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["mag_disp"] = out["mag"].map(_fmt_mag)
    out["depth_disp"] = out["depth"].map(
        lambda d: "—" if pd.isna(d) else f"{d:,.0f} km"
    )
    out["details"] = out["url"].map(lambda u: f"[USGS ↗]({u})" if u else "—")
    return out[
        ["mag_disp", "place", "depth_disp", "alert", "time_str", "details"]
    ]


def build_table(df: pd.DataFrame, title: str, subtitle: str) -> GT:
    """Styled great-tables view of earthquakes (matches the portfolio theme)."""
    view = _view(df)
    gt = (
        GT(view)
        .tab_header(title=title, subtitle=subtitle)
        .cols_label(
            mag_disp="Mag",
            place="Place",
            depth_disp="Depth",
            alert="PAGER",
            time_str="Time (UTC)",
            details="Source",
        )
        .cols_align("right", columns=["mag_disp", "depth_disp"])
        .cols_align("center", columns=["alert"])
        .fmt_markdown(columns=["details"])
        .tab_source_note(
            md(
                "PAGER = USGS impact estimate (green→red) · "
                "Data: [USGS Earthquake Hazards](https://earthquake.usgs.gov/earthquakes/)"
            )
        )
        .opt_table_font(font="IBM Plex Sans")
        .tab_options(
            table_background_color=PAPER,
            heading_title_font_size="20px",
            heading_title_font_weight="600",
            heading_subtitle_font_size="13px",
            column_labels_background_color=NAVY,
            column_labels_font_weight="600",
            table_font_size="13px",
            row_striping_include_table_body=True,
        )
    )
    gt = gt.tab_style(
        style=style.text(color=CLAY, weight="700"),
        locations=loc.body(columns=["mag_disp"]),
    )
    gt = gt.tab_style(
        style=style.text(color=NAVY, weight="600"),
        locations=loc.body(columns=["place"]),
    )
    return gt


def recent_table(df: pd.DataFrame, n: int = 15) -> GT:
    quakes = df[df["type"] == "earthquake"]
    return build_table(
        quakes.head(n),
        title="Most recent earthquakes",
        subtitle="Latest events worldwide, newest first (last 24h)",
    )


def strongest_table(df: pd.DataFrame, n: int = 15) -> GT:
    quakes = df[df["type"] == "earthquake"]
    return build_table(
        quakes.sort_values("mag", ascending=False).head(n),
        title="Strongest in the last 24h",
        subtitle="Same window, ranked by magnitude",
    )


def significant_table(df_sig: pd.DataFrame, n: int = 20) -> GT:
    return build_table(
        df_sig.head(n),
        title="Significant earthquakes (last 7 days)",
        subtitle="USGS 'significant' feed — the events that matter, with official links",
    )
