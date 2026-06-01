import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional


ROOT_DIR = Path(__file__).resolve().parents[1]
LOGS_DIR = ROOT_DIR / "logs"
RESULTS_DIR = ROOT_DIR / "evaluation" / "results"


def load_json_lines(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def load_log_events(log_dir: Path) -> List[Dict[str, Any]]:
    if not log_dir.exists():
        return []

    events = []
    for path in sorted(log_dir.glob("*.log")):
        for event in load_json_lines(path):
            event["_source_file"] = str(path.relative_to(ROOT_DIR))
            events.append(event)
    return events


def load_result_files(results_dir: Path, pattern: str) -> List[Dict[str, Any]]:
    if not results_dir.exists():
        return []

    rows = []
    for path in sorted(results_dir.glob(pattern)):
        if path.suffix != ".json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        if isinstance(payload, list):
            for item in payload:
                item["_source_file"] = str(path.relative_to(ROOT_DIR))
                rows.append(item)
    return rows


def average(values: List[Optional[float]]) -> Optional[float]:
    clean_values = [value for value in values if value is not None]
    if not clean_values:
        return None
    return round(mean(clean_values), 2)


def count_events(events: List[Dict[str, Any]]) -> Counter:
    return Counter(event.get("event", "UNKNOWN") for event in events)


def summarize_results(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_runs = len(rows)
    completed_runs = sum(1 for row in rows if row.get("status") == "completed")
    passed_runs = sum(1 for row in rows if row.get("correctness", {}).get("passed") is True)

    metrics = [row.get("metrics", {}) for row in rows]
    latency_values = [metric.get("latency_ms") for metric in metrics]
    token_values = [metric.get("total_tokens") for metric in metrics]
    step_values = [metric.get("steps") for metric in metrics]

    parser_errors = sum(metric.get("parser_errors") or 0 for metric in metrics)
    unknown_tool_errors = sum(metric.get("hallucinated_tool_errors") or 0 for metric in metrics)
    timeouts = sum(metric.get("timeouts") or 0 for metric in metrics)
    tool_errors = sum(metric.get("tool_errors") or 0 for metric in metrics)

    by_target = defaultdict(list)
    for row in rows:
        by_target[row.get("target", "unknown")].append(row)

    target_summary = {}
    for target, target_rows in by_target.items():
        target_metrics = [row.get("metrics", {}) for row in target_rows]
        target_passed = sum(
            1 for row in target_rows if row.get("correctness", {}).get("passed") is True
        )
        target_summary[target] = {
            "runs": len(target_rows),
            "success_rate": round(target_passed / len(target_rows), 4) if target_rows else 0,
            "average_latency_ms": average(
                [metric.get("latency_ms") for metric in target_metrics]
            ),
            "average_total_tokens": average(
                [metric.get("total_tokens") for metric in target_metrics]
            ),
            "average_loop_count": average([metric.get("steps") for metric in target_metrics]),
        }

    return {
        "total_runs": total_runs,
        "completed_runs": completed_runs,
        "passed_runs": passed_runs,
        "success_rate": round(passed_runs / total_runs, 4) if total_runs else 0,
        "average_latency_ms": average(latency_values),
        "average_total_tokens": average(token_values),
        "average_loop_count": average(step_values),
        "parser_errors": parser_errors,
        "unknown_tool_errors": unknown_tool_errors,
        "timeouts": timeouts,
        "tool_errors": tool_errors,
        "by_target": target_summary,
    }


def summarize_logs(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    event_counts = count_events(events)
    llm_metric_events = [event for event in events if event.get("event") == "LLM_METRIC"]
    agent_end_events = [event for event in events if event.get("event") == "AGENT_END"]

    return {
        "total_events": len(events),
        "event_counts": dict(sorted(event_counts.items())),
        "average_llm_latency_ms": average(
            [event.get("data", {}).get("latency_ms") for event in llm_metric_events]
        ),
        "average_llm_tokens": average(
            [event.get("data", {}).get("total_tokens") for event in llm_metric_events]
        ),
        "average_agent_steps": average(
            [event.get("data", {}).get("steps") for event in agent_end_events]
        ),
        "parser_errors": event_counts.get("AGENT_PARSE_ERROR", 0),
        "unknown_tool_errors": event_counts.get("AGENT_UNKNOWN_TOOL", 0)
        + event_counts.get("UNKNOWN_TOOL", 0),
        "timeouts": event_counts.get("AGENT_TIMEOUT", 0),
        "tool_errors": event_counts.get("TOOL_ERROR", 0),
    }


def build_report(summary: Dict[str, Any]) -> str:
    result_summary = summary["evaluation_results"]
    log_summary = summary["telemetry_logs"]

    lines = [
        "# Evaluation Log Analysis",
        "",
        "## Evaluation Results",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total runs | {result_summary['total_runs']} |",
        f"| Completed runs | {result_summary['completed_runs']} |",
        f"| Passed runs | {result_summary['passed_runs']} |",
        f"| Success rate | {result_summary['success_rate']:.2%} |",
        f"| Average latency ms | {result_summary['average_latency_ms'] or ''} |",
        f"| Average total tokens | {result_summary['average_total_tokens'] or ''} |",
        f"| Average loop count | {result_summary['average_loop_count'] or ''} |",
        f"| Parser errors | {result_summary['parser_errors']} |",
        f"| Unknown tool errors | {result_summary['unknown_tool_errors']} |",
        f"| Timeouts | {result_summary['timeouts']} |",
        f"| Tool errors | {result_summary['tool_errors']} |",
        "",
        "## By Target",
        "",
        "| Target | Runs | Success rate | Avg latency ms | Avg tokens | Avg loops |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for target, target_summary in result_summary["by_target"].items():
        lines.append(
            "| {target} | {runs} | {success_rate:.2%} | {latency} | {tokens} | {loops} |".format(
                target=target,
                runs=target_summary["runs"],
                success_rate=target_summary["success_rate"],
                latency=target_summary["average_latency_ms"] or "",
                tokens=target_summary["average_total_tokens"] or "",
                loops=target_summary["average_loop_count"] or "",
            )
        )

    lines.extend(
        [
            "",
            "## Telemetry Logs",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Total events | {log_summary['total_events']} |",
            f"| Average LLM latency ms | {log_summary['average_llm_latency_ms'] or ''} |",
            f"| Average LLM tokens | {log_summary['average_llm_tokens'] or ''} |",
            f"| Average agent steps | {log_summary['average_agent_steps'] or ''} |",
            f"| Parser errors | {log_summary['parser_errors']} |",
            f"| Unknown tool errors | {log_summary['unknown_tool_errors']} |",
            f"| Timeouts | {log_summary['timeouts']} |",
            f"| Tool errors | {log_summary['tool_errors']} |",
            "",
            "## Event Counts",
            "",
            "| Event | Count |",
            "|---|---:|",
        ]
    )

    for event_name, count in log_summary["event_counts"].items():
        lines.append(f"| {event_name} | {count} |")

    return "\n".join(lines) + "\n"


def write_outputs(summary: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "analysis_summary.json"
    markdown_path = output_dir / "analysis_summary.md"

    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(build_report(summary), encoding="utf-8")

    print(f"Saved JSON analysis to {json_path}")
    print(f"Saved Markdown analysis to {markdown_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze evaluation results and telemetry logs.")
    parser.add_argument("--results-pattern", default="*.json")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    events = load_log_events(LOGS_DIR)
    result_rows = load_result_files(RESULTS_DIR, args.results_pattern)

    summary = {
        "sources": {
            "logs_dir": str(LOGS_DIR),
            "results_dir": str(RESULTS_DIR),
            "results_pattern": args.results_pattern,
        },
        "evaluation_results": summarize_results(result_rows),
        "telemetry_logs": summarize_logs(events),
    }

    print(build_report(summary))

    if not args.no_write:
        write_outputs(summary, RESULTS_DIR)


if __name__ == "__main__":
    sys.exit(main())
