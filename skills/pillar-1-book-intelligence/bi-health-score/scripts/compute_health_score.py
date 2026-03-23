#!/usr/bin/env python3
"""
Health Score Engine -- Core Computation

Computes composite health scores for customer accounts.
This script handles the normalisation and weighting logic.
Data source integrations are handled upstream; this script
expects a structured input and produces a structured output.

Usage:
    python compute_health_score.py --input account_data.json --benchmarks benchmarks.json --output health_scores.json
    python compute_health_score.py --input account_data.json --benchmarks benchmarks.json --account ACCT-123
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import Optional


# Default component weights
DEFAULT_WEIGHTS = {
    "usage": 0.35,
    "engagement": 0.25,
    "support": 0.20,
    "sentiment": 0.10,
    "commercial": 0.10,
}

# Staleness thresholds in days
STALENESS_THRESHOLDS = {
    "usage": 7,
    "engagement": 7,
    "support": 3,
    "sentiment": 90,
    "commercial": 30,
}

# Health bands
HEALTH_BANDS = {
    "critical": (0, 40),
    "at_risk": (41, 65),
    "healthy": (66, 80),
    "strong": (81, 100),
}


def normalise_to_scale(value: float, p5: float, p25: float, p50: float, p75: float, p95: float) -> float:
    """
    Map a raw metric value to a 0-100 scale using segment benchmark percentiles.
    Uses linear interpolation between benchmark points.
    """
    if value <= p5:
        return 0.0
    elif value <= p25:
        return 25.0 * (value - p5) / max(p25 - p5, 0.001)
    elif value <= p50:
        return 25.0 + 25.0 * (value - p25) / max(p50 - p25, 0.001)
    elif value <= p75:
        return 50.0 + 25.0 * (value - p50) / max(p75 - p50, 0.001)
    elif value <= p95:
        return 75.0 + 25.0 * (value - p75) / max(p95 - p75, 0.001)
    else:
        return 100.0


def check_staleness(last_updated: str, threshold_days: int) -> bool:
    """Returns True if the data source is stale (older than threshold)."""
    if not last_updated:
        return True
    try:
        last_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
        now = datetime.now(last_dt.tzinfo)
        return (now - last_dt).days > threshold_days
    except (ValueError, TypeError):
        return True


def compute_component_score(metrics: list[dict], benchmarks: dict) -> tuple[float, list[str]]:
    """
    Compute a blended component score from multiple metrics.
    Returns (score, list_of_risk_flags).
    """
    if not metrics:
        return 0.0, ["No data available"]

    scores = []
    flags = []

    for metric in metrics:
        name = metric.get("name", "unknown")
        value = metric.get("value")
        bench = benchmarks.get(name, {})

        if value is None or not bench:
            continue

        score = normalise_to_scale(
            value,
            bench.get("p5", 0),
            bench.get("p25", 0),
            bench.get("p50", 0),
            bench.get("p75", 0),
            bench.get("p95", 0),
        )
        scores.append(score)

        # Flag if below 25th percentile
        if score < 25.0:
            flags.append(f"{name}: value {value} below segment 25th percentile ({bench.get('p25', 'N/A')})")

    if not scores:
        return 0.0, ["No scoreable metrics"]

    return sum(scores) / len(scores), flags


def compute_trend(current: float, history: list[float], window: int = 30) -> str:
    """
    Classify trend direction based on current value vs. rolling average.
    Returns: 'improving', 'stable', or 'declining'.
    """
    if not history or len(history) < 7:
        return "insufficient_data"

    recent = history[-min(window, len(history)):]
    avg = sum(recent) / len(recent)
    delta = current - avg

    if delta > 5:
        return "improving"
    elif delta < -5:
        return "declining"
    else:
        return "stable"


def detect_rapid_decline(current: float, history_7d: list[float]) -> bool:
    """Returns True if composite has dropped >10 points in 7 days."""
    if not history_7d:
        return False
    seven_days_ago = history_7d[0] if history_7d else current
    return (seven_days_ago - current) > 10


def classify_health_band(score: float) -> str:
    """Map composite score to health band."""
    for band, (low, high) in HEALTH_BANDS.items():
        if low <= score <= high:
            return band
    return "unknown"


def compute_health_score(account_data: dict, benchmarks: dict, weights: Optional[dict] = None) -> dict:
    """
    Main computation function.

    Args:
        account_data: Dict with account_id, segment, components (each with metrics and last_updated), history
        benchmarks: Dict of segment benchmarks keyed by segment identifier
        weights: Optional custom weights. Uses DEFAULT_WEIGHTS if not provided.

    Returns:
        Health record dict.
    """
    w = weights or DEFAULT_WEIGHTS.copy()
    account_id = account_data.get("account_id", "unknown")
    segment = account_data.get("segment", "default")
    segment_benchmarks = benchmarks.get(segment, benchmarks.get("default", {}))

    components = {}
    all_risk_drivers = []
    stale_sources = []
    active_weights = {}

    # Process each component
    for component_name in ["usage", "engagement", "support", "sentiment", "commercial"]:
        comp_data = account_data.get("components", {}).get(component_name, {})
        comp_benchmarks = segment_benchmarks.get(component_name, {})
        last_updated = comp_data.get("last_updated")

        # Check staleness
        is_stale = check_staleness(last_updated, STALENESS_THRESHOLDS[component_name])
        if is_stale:
            stale_sources.append(component_name)

        # Compute component score
        metrics = comp_data.get("metrics", [])
        score, flags = compute_component_score(metrics, comp_benchmarks)

        # Compute trend
        comp_history = account_data.get("history", {}).get(component_name, [])
        trend = compute_trend(score, comp_history)

        components[component_name] = {
            "score": round(score, 1),
            "trend": trend,
            "stale": is_stale,
        }

        if flags:
            for flag in flags:
                all_risk_drivers.append(f"{component_name.title()}: {flag}")

        if not is_stale and metrics:
            active_weights[component_name] = w[component_name]

    # Redistribute weights for stale/missing components
    if active_weights:
        total_active = sum(active_weights.values())
        normalised_weights = {k: v / total_active for k, v in active_weights.items()}
    else:
        normalised_weights = w

    # Compute composite
    composite = sum(
        components[comp]["score"] * normalised_weights.get(comp, 0)
        for comp in components
    )
    composite = round(min(max(composite, 0), 100), 1)

    # Composite trend
    composite_history = account_data.get("history", {}).get("composite", [])
    composite_trend = compute_trend(composite, composite_history)

    # Rapid decline detection
    history_7d = account_data.get("history", {}).get("composite_7d", [])
    rapid_decline = detect_rapid_decline(composite, history_7d)

    # Determine handoff triggers
    handoff_triggers = []
    if composite < 65:
        handoff_triggers.append({"type": "score_below_threshold", "urgency": "same_day"})
    if rapid_decline:
        handoff_triggers.append({"type": "rapid_decline", "urgency": "immediate"})
    for component_name, comp in components.items():
        if comp["score"] < 25 and not comp["stale"]:
            handoff_triggers.append({
                "type": "component_below_p25",
                "component": component_name,
                "urgency": "next_business_day",
            })

    return {
        "account_id": account_id,
        "composite_score": composite,
        "health_band": classify_health_band(composite),
        "trend": composite_trend,
        "rapid_decline": rapid_decline,
        "components": components,
        "risk_drivers": all_risk_drivers,
        "data_freshness": {
            "stale_sources": stale_sources,
            "last_computed": datetime.utcnow().isoformat() + "Z",
        },
        "handoff_triggers": handoff_triggers,
        "weights_applied": normalised_weights,
    }


def main():
    parser = argparse.ArgumentParser(description="Compute health scores for customer accounts")
    parser.add_argument("--input", required=True, help="Path to account data JSON file")
    parser.add_argument("--benchmarks", required=True, help="Path to segment benchmarks JSON file")
    parser.add_argument("--output", help="Path to write health scores JSON (default: stdout)")
    parser.add_argument("--account", help="Compute for a single account ID only")
    parser.add_argument("--weights", help="Path to custom weights JSON file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        accounts = json.load(f)

    with open(args.benchmarks, "r") as f:
        benchmarks = json.load(f)

    custom_weights = None
    if args.weights:
        with open(args.weights, "r") as f:
            custom_weights = json.load(f)

    if not isinstance(accounts, list):
        accounts = [accounts]

    if args.account:
        accounts = [a for a in accounts if a.get("account_id") == args.account]
        if not accounts:
            print(f"Account {args.account} not found in input data", file=sys.stderr)
            sys.exit(1)

    results = [compute_health_score(a, benchmarks, custom_weights) for a in accounts]

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Health scores written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
