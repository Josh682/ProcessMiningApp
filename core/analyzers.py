"""F03–F06: Core Analytics Engine for Chapter 11 Exercises (11.7 A–E, 11.15, 11.18, 11.22)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from core.models import (
    AnalysisResult,
    LoadedDataset,
    MissingOptionalAttributeError,
)


def _build_empty_matched_11_7() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            "case_id",
            "cycle_time_days",
            "event_count",
            "last_activity",
            "matching_event_count",
        ]
    )
    df["case_id"] = df["case_id"].astype("string")
    df["cycle_time_days"] = df["cycle_time_days"].astype("float64")
    df["event_count"] = df["event_count"].astype("int32")
    df["last_activity"] = df["last_activity"].astype("string")
    df["matching_event_count"] = df["matching_event_count"].astype("int32")
    return df


def _build_empty_matched_11_15() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            "case_id",
            "complete_count",
            "cycle_time_days",
            "event_count",
        ]
    )
    df["case_id"] = df["case_id"].astype("string")
    df["complete_count"] = df["complete_count"].astype("int32")
    df["cycle_time_days"] = df["cycle_time_days"].astype("float64")
    df["event_count"] = df["event_count"].astype("int32")
    return df


def _build_empty_matched_11_18() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            "case_id",
            "matching_resources",
            "max_resource_complete_count",
            "total_fraud_complete_count",
            "cycle_time_days",
            "event_count",
        ]
    )
    df["case_id"] = df["case_id"].astype("string")
    df["matching_resources"] = df["matching_resources"].astype("string")
    df["max_resource_complete_count"] = df["max_resource_complete_count"].astype("int32")
    df["total_fraud_complete_count"] = df["total_fraud_complete_count"].astype("int32")
    df["cycle_time_days"] = df["cycle_time_days"].astype("float64")
    df["event_count"] = df["event_count"].astype("int32")
    return df


def _build_empty_matched_11_22() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=[
            "case_id",
            "first_cancelled_idx",
            "first_cancelled_time",
            "following_accepted_idx",
            "following_accepted_time",
            "cycle_time_days",
            "event_count",
        ]
    )
    df["case_id"] = df["case_id"].astype("string")
    df["first_cancelled_idx"] = df["first_cancelled_idx"].astype("int64")
    df["first_cancelled_time"] = pd.to_datetime(
        df["first_cancelled_time"], utc=True
    ).dt.as_unit("ns")
    df["following_accepted_idx"] = df["following_accepted_idx"].astype("int64")
    df["following_accepted_time"] = pd.to_datetime(
        df["following_accepted_time"], utc=True
    ).dt.as_unit("ns")
    df["cycle_time_days"] = df["cycle_time_days"].astype("float64")
    df["event_count"] = df["event_count"].astype("int32")
    return df


def analyze_exercise_11_7(dataset: LoadedDataset) -> dict[str, AnalysisResult]:
    """Evaluate Exercise 11.7 (A–E) on case level using pre-computed whole-trace metrics."""
    total_cases = dataset.overview.total_cases
    case_summary = dataset.case_summary_df
    raw_df = dataset.raw_df

    results: dict[str, AnalysisResult] = {}

    # 11.7 A: Total Unique Cases
    matched_a = case_summary[
        ["case_id", "cycle_time_days", "event_count", "last_activity"]
    ].copy()
    matched_a["matching_event_count"] = np.int32(0)
    results["11.7 A"] = AnalysisResult(
        exercise_code="11.7 A",
        title="Total Unique Cases",
        filter_rule="Seluruh unique cases di dalam event log aktif (tanpa filter).",
        case_count=total_cases,
        total_cases=total_cases,
        mean_cycle_time_days=None,
        percentage=100.0 if total_cases > 0 else 0.0,
        matched_cases_df=matched_a[
            ["case_id", "cycle_time_days", "event_count", "last_activity", "matching_event_count"]
        ],
        evidence_event_indices={},
    )

    # 11.7 B: Mean Cycle Time (All Cases)
    matched_b = matched_a.copy()
    results["11.7 B"] = AnalysisResult(
        exercise_code="11.7 B",
        title="Mean Cycle Time (All Cases)",
        filter_rule=(
            "Rata-rata cycle time (hari) dari seluruh unique cases, "
            "dihitung dari selisih timestamp akhir dan awal pada trace utuh."
        ),
        case_count=total_cases,
        total_cases=total_cases,
        mean_cycle_time_days=dataset.overview.mean_cycle_time_days,
        percentage=100.0 if total_cases > 0 else 0.0,
        matched_cases_df=matched_b[
            ["case_id", "cycle_time_days", "event_count", "last_activity", "matching_event_count"]
        ],
        evidence_event_indices={},
    )

    # 11.7 C: Successful Cases (contains O_Accepted)
    c_events = raw_df[raw_df["concept:name"] == "O_Accepted"]
    if c_events.empty:
        results["11.7 C"] = AnalysisResult(
            exercise_code="11.7 C",
            title="Successful Cases (Contains O_Accepted)",
            filter_rule=(
                "Case memiliki minimal 1 event dengan concept:name == 'O_Accepted' "
                "(level case, non-eksklusif; cycle time dari trace utuh)."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_7(),
            evidence_event_indices={},
        )
    else:
        c_agg = (
            c_events.groupby("case:concept:name", observed=True)
            .agg(
                matching_event_count=("_orig_idx", "size"),
                orig_indices=("_orig_idx", list),
            )
            .reset_index()
        )
        c_evidence: dict[str, list[int]] = dict(
            zip(c_agg["case:concept:name"], c_agg["orig_indices"], strict=False)
        )
        matched_c = case_summary.merge(
            c_agg[["case:concept:name", "matching_event_count"]],
            left_on="case_id",
            right_on="case:concept:name",
            how="inner",
        )
        matched_c["matching_event_count"] = matched_c["matching_event_count"].astype("int32")
        matched_c = matched_c[
            ["case_id", "cycle_time_days", "event_count", "last_activity", "matching_event_count"]
        ]
        count_c = len(matched_c)
        mean_ct_c = float(matched_c["cycle_time_days"].mean()) if count_c > 0 else 0.0
        pct_c = (count_c / total_cases * 100.0) if total_cases > 0 else 0.0

        results["11.7 C"] = AnalysisResult(
            exercise_code="11.7 C",
            title="Successful Cases (Contains O_Accepted)",
            filter_rule=(
                "Case memiliki minimal 1 event dengan concept:name == 'O_Accepted' "
                "(level case, non-eksklusif; cycle time dari trace utuh)."
            ),
            case_count=count_c,
            total_cases=total_cases,
            mean_cycle_time_days=mean_ct_c,
            percentage=pct_c,
            matched_cases_df=matched_c,
            evidence_event_indices=c_evidence,
        )

    # 11.7 D: Unsuccessful Cases (contains O_Refused)
    d_events = raw_df[raw_df["concept:name"] == "O_Refused"]
    if d_events.empty:
        results["11.7 D"] = AnalysisResult(
            exercise_code="11.7 D",
            title="Unsuccessful Cases (Contains O_Refused)",
            filter_rule=(
                "Case memiliki minimal 1 event dengan concept:name == 'O_Refused' "
                "(level case, non-eksklusif terhadap 11.7 C; cycle time dari trace utuh)."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_7(),
            evidence_event_indices={},
        )
    else:
        d_agg = (
            d_events.groupby("case:concept:name", observed=True)
            .agg(
                matching_event_count=("_orig_idx", "size"),
                orig_indices=("_orig_idx", list),
            )
            .reset_index()
        )
        d_evidence: dict[str, list[int]] = dict(
            zip(d_agg["case:concept:name"], d_agg["orig_indices"], strict=False)
        )
        matched_d = case_summary.merge(
            d_agg[["case:concept:name", "matching_event_count"]],
            left_on="case_id",
            right_on="case:concept:name",
            how="inner",
        )
        matched_d["matching_event_count"] = matched_d["matching_event_count"].astype("int32")
        matched_d = matched_d[
            ["case_id", "cycle_time_days", "event_count", "last_activity", "matching_event_count"]
        ]
        count_d = len(matched_d)
        mean_ct_d = float(matched_d["cycle_time_days"].mean()) if count_d > 0 else 0.0
        pct_d = (count_d / total_cases * 100.0) if total_cases > 0 else 0.0

        results["11.7 D"] = AnalysisResult(
            exercise_code="11.7 D",
            title="Unsuccessful Cases (Contains O_Refused)",
            filter_rule=(
                "Case memiliki minimal 1 event dengan concept:name == 'O_Refused' "
                "(level case, non-eksklusif terhadap 11.7 C; cycle time dari trace utuh)."
            ),
            case_count=count_d,
            total_cases=total_cases,
            mean_cycle_time_days=mean_ct_d,
            percentage=pct_d,
            matched_cases_df=matched_d,
            evidence_event_indices=d_evidence,
        )

    # 11.7 E: Canceled Cases (last_activity == "O_Cancelled")
    e_cases = case_summary[case_summary["last_activity"] == "O_Cancelled"].copy()
    if e_cases.empty:
        results["11.7 E"] = AnalysisResult(
            exercise_code="11.7 E",
            title="Canceled Cases (Endpoint O_Cancelled)",
            filter_rule=(
                "Event paling akhir pada trace utuh (berdasarkan urutan time:timestamp "
                "dan _orig_idx) adalah 'O_Cancelled'."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_7(),
            evidence_event_indices={},
        )
    else:
        e_cases["matching_event_count"] = np.int32(1)
        matched_e = e_cases[
            ["case_id", "cycle_time_days", "event_count", "last_activity", "matching_event_count"]
        ]
        last_indices = raw_df.groupby("case:concept:name", observed=True)["_orig_idx"].last()
        e_evidence = {cid: [int(last_indices[cid])] for cid in matched_e["case_id"]}
        count_e = len(matched_e)
        mean_ct_e = float(matched_e["cycle_time_days"].mean()) if count_e > 0 else 0.0
        pct_e = (count_e / total_cases * 100.0) if total_cases > 0 else 0.0

        results["11.7 E"] = AnalysisResult(
            exercise_code="11.7 E",
            title="Canceled Cases (Endpoint O_Cancelled)",
            filter_rule=(
                "Event paling akhir pada trace utuh (berdasarkan urutan time:timestamp "
                "dan _orig_idx) adalah 'O_Cancelled'."
            ),
            case_count=count_e,
            total_cases=total_cases,
            mean_cycle_time_days=mean_ct_e,
            percentage=pct_e,
            matched_cases_df=matched_e,
            evidence_event_indices=e_evidence,
        )

    return results


def analyze_exercise_11_15(dataset: LoadedDataset) -> AnalysisResult:
    """Evaluate Exercise 11.15: W_Assess Potential Fraud with complete occurrence >= 2."""
    if not dataset.overview.has_lifecycle:
        raise MissingOptionalAttributeError("lifecycle:transition", "11.15")

    total_cases = dataset.overview.total_cases
    raw_df = dataset.raw_df
    case_summary = dataset.case_summary_df

    act_mask = (
        raw_df["concept:name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        == "w_assess potential fraud"
    )
    life_mask = (
        raw_df["lifecycle:transition"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        == "complete"
    )
    fraud_events = raw_df[act_mask & life_mask]

    if fraud_events.empty:
        return AnalysisResult(
            exercise_code="11.15",
            title="Repeated Activity (W_Assess Potential Fraud Complete >= 2)",
            filter_rule=(
                "Case memiliki >= 2 event dengan concept:name == 'W_Assess Potential Fraud' "
                "DAN lifecycle:transition (normalized lower/strip) == 'complete'."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_15(),
            evidence_event_indices={},
        )

    agg_15 = (
        fraud_events.groupby("case:concept:name", observed=True)
        .agg(
            complete_count=("_orig_idx", "size"),
            orig_indices=("_orig_idx", list),
        )
        .reset_index()
    )
    qualifying = agg_15[agg_15["complete_count"] >= 2]
    if qualifying.empty:
        return AnalysisResult(
            exercise_code="11.15",
            title="Repeated Activity (W_Assess Potential Fraud Complete >= 2)",
            filter_rule=(
                "Case memiliki >= 2 event dengan concept:name == 'W_Assess Potential Fraud' "
                "DAN lifecycle:transition (normalized lower/strip) == 'complete'."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_15(),
            evidence_event_indices={},
        )

    evidence_15: dict[str, list[int]] = dict(
        zip(qualifying["case:concept:name"], qualifying["orig_indices"], strict=False)
    )
    matched_15 = case_summary.merge(
        qualifying[["case:concept:name", "complete_count"]],
        left_on="case_id",
        right_on="case:concept:name",
        how="inner",
    )
    matched_15["complete_count"] = matched_15["complete_count"].astype("int32")
    matched_15 = matched_15[["case_id", "complete_count", "cycle_time_days", "event_count"]]

    count_15 = len(matched_15)
    mean_ct_15 = float(matched_15["cycle_time_days"].mean()) if count_15 > 0 else 0.0
    pct_15 = (count_15 / total_cases * 100.0) if total_cases > 0 else 0.0

    return AnalysisResult(
        exercise_code="11.15",
        title="Repeated Activity (W_Assess Potential Fraud Complete >= 2)",
        filter_rule=(
            "Case memiliki >= 2 event dengan concept:name == 'W_Assess Potential Fraud' "
            "DAN lifecycle:transition (normalized lower/strip) == 'complete'."
        ),
        case_count=count_15,
        total_cases=total_cases,
        mean_cycle_time_days=mean_ct_15,
        percentage=pct_15,
        matched_cases_df=matched_15,
        evidence_event_indices=evidence_15,
    )


def analyze_exercise_11_18(dataset: LoadedDataset) -> AnalysisResult:
    """Evaluate Exercise 11.18: Fraud assessment complete >= 2 by same resource."""
    if not dataset.overview.has_lifecycle:
        raise MissingOptionalAttributeError("lifecycle:transition", "11.18")
    if not dataset.overview.has_resource:
        raise MissingOptionalAttributeError("org:resource", "11.18")

    total_cases = dataset.overview.total_cases
    raw_df = dataset.raw_df
    case_summary = dataset.case_summary_df

    act_mask = (
        raw_df["concept:name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        == "w_assess potential fraud"
    )
    life_mask = (
        raw_df["lifecycle:transition"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        == "complete"
    )

    all_fraud_complete = raw_df[act_mask & life_mask]
    if all_fraud_complete.empty:
        return AnalysisResult(
            exercise_code="11.18",
            title="Repeated Activity by Same Resource (W_Assess Potential Fraud Complete >= 2)",
            filter_rule=(
                "Case memiliki >= 2 event 'W_Assess Potential Fraud' berstatus 'complete' "
                "yang dikerjakan oleh org:resource valid (tidak kosong/NaN) yang SAMA."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_18(),
            evidence_event_indices={},
        )

    # Compute total fraud complete count per case
    total_fraud_counts = all_fraud_complete.groupby(
        "case:concept:name", observed=True
    ).size().to_dict()

    # Filter for valid non-empty resources
    res_series = all_fraud_complete["org:resource"]
    res_str = res_series.fillna("").astype(str).str.strip()
    valid_res_mask = res_series.notna() & (res_str != "") & (~res_str.str.lower().isin(
        {"nan", "none", "null", "<na>"}
    ))

    fraud_valid = all_fraud_complete[valid_res_mask]
    if fraud_valid.empty:
        return AnalysisResult(
            exercise_code="11.18",
            title="Repeated Activity by Same Resource (W_Assess Potential Fraud Complete >= 2)",
            filter_rule=(
                "Case memiliki >= 2 event 'W_Assess Potential Fraud' berstatus 'complete' "
                "yang dikerjakan oleh org:resource valid (tidak kosong/NaN) yang SAMA."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_18(),
            evidence_event_indices={},
        )

    res_counts = (
        fraud_valid.groupby(["case:concept:name", "org:resource"], observed=True)
        .agg(
            res_occ=("_orig_idx", "size"),
            orig_indices=("_orig_idx", list),
        )
        .reset_index()
    )

    qualifying_res = res_counts[res_counts["res_occ"] >= 2]
    if qualifying_res.empty:
        return AnalysisResult(
            exercise_code="11.18",
            title="Repeated Activity by Same Resource (W_Assess Potential Fraud Complete >= 2)",
            filter_rule=(
                "Case memiliki >= 2 event 'W_Assess Potential Fraud' berstatus 'complete' "
                "yang dikerjakan oleh org:resource valid (tidak kosong/NaN) yang SAMA."
            ),
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_18(),
            evidence_event_indices={},
        )

    # Aggregate by case:concept:name
    records_18: list[dict[str, Any]] = []
    evidence_18: dict[str, list[int]] = {}

    for case_id, group in qualifying_res.groupby("case:concept:name", observed=True):
        sorted_group = group.sort_values(by="org:resource", ascending=True)
        resources_list = [str(r) for r in sorted_group["org:resource"]]
        matching_resources_str = ", ".join(resources_list)
        max_res_count = int(sorted_group["res_occ"].max())
        total_complete = int(total_fraud_counts.get(case_id, 0))

        case_evidence_indices: list[int] = []
        for idx_list in sorted_group["orig_indices"]:
            case_evidence_indices.extend(idx_list)

        evidence_18[str(case_id)] = case_evidence_indices

        records_18.append(
            {
                "case_id": str(case_id),
                "matching_resources": matching_resources_str,
                "max_resource_complete_count": max_res_count,
                "total_fraud_complete_count": total_complete,
            }
        )

    summary_part = pd.DataFrame(records_18)
    matched_18 = case_summary.merge(
        summary_part,
        on="case_id",
        how="inner",
    )

    matched_18["matching_resources"] = matched_18["matching_resources"].astype("string")
    matched_18["max_resource_complete_count"] = (
        matched_18["max_resource_complete_count"].astype("int32")
    )
    matched_18["total_fraud_complete_count"] = (
        matched_18["total_fraud_complete_count"].astype("int32")
    )
    matched_18 = matched_18[
        [
            "case_id",
            "matching_resources",
            "max_resource_complete_count",
            "total_fraud_complete_count",
            "cycle_time_days",
            "event_count",
        ]
    ]

    count_18 = len(matched_18)
    mean_ct_18 = float(matched_18["cycle_time_days"].mean()) if count_18 > 0 else 0.0
    pct_18 = (count_18 / total_cases * 100.0) if total_cases > 0 else 0.0

    return AnalysisResult(
        exercise_code="11.18",
        title="Repeated Activity by Same Resource (W_Assess Potential Fraud Complete >= 2)",
        filter_rule=(
            "Case memiliki >= 2 event 'W_Assess Potential Fraud' berstatus 'complete' "
            "yang dikerjakan oleh org:resource valid (tidak kosong/NaN) yang SAMA."
        ),
        case_count=count_18,
        total_cases=total_cases,
        mean_cycle_time_days=mean_ct_18,
        percentage=pct_18,
        matched_cases_df=matched_18,
        evidence_event_indices=evidence_18,
    )


def analyze_exercise_11_22(dataset: LoadedDataset) -> AnalysisResult:
    """Evaluate Exercise 11.22: O_Cancelled eventually followed by O_Accepted on case level."""
    total_cases = dataset.overview.total_cases
    raw_df = dataset.raw_df
    case_summary = dataset.case_summary_df

    target_events = raw_df[raw_df["concept:name"].isin({"O_Cancelled", "O_Accepted"})]

    filter_rule_22 = (
        "Case memiliki event 'O_Cancelled' pada posisi i yang diikuti oleh 'O_Accepted' "
        "pada posisi j > i (Eventually Follows level case "
        "berdasarkan time:timestamp dan _orig_idx)."
    )

    if target_events.empty:
        return AnalysisResult(
            exercise_code="11.22",
            title="Sequence Pattern (O_Cancelled Followed by O_Accepted)",
            filter_rule=filter_rule_22,
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_22(),
            evidence_event_indices={},
        )

    records_22: list[dict[str, Any]] = []
    evidence_22: dict[str, list[int]] = {}

    for case_id, group in target_events.groupby("case:concept:name", sort=False, observed=True):
        activities = group["concept:name"].to_numpy()
        orig_indices = group["_orig_idx"].to_numpy()
        timestamps = group["time:timestamp"].to_numpy()

        first_c_pos = -1
        for idx, act in enumerate(activities):
            if act == "O_Cancelled":
                first_c_pos = idx
                break

        if first_c_pos == -1:
            continue

        following_a_pos = -1
        for idx in range(first_c_pos + 1, len(activities)):
            if activities[idx] == "O_Accepted":
                following_a_pos = idx
                break

        if following_a_pos != -1:
            c_idx = int(orig_indices[first_c_pos])
            a_idx = int(orig_indices[following_a_pos])
            c_time = timestamps[first_c_pos]
            a_time = timestamps[following_a_pos]

            evidence_22[str(case_id)] = [c_idx, a_idx]
            records_22.append(
                {
                    "case_id": str(case_id),
                    "first_cancelled_idx": c_idx,
                    "first_cancelled_time": c_time,
                    "following_accepted_idx": a_idx,
                    "following_accepted_time": a_time,
                }
            )

    if not records_22:
        return AnalysisResult(
            exercise_code="11.22",
            title="Sequence Pattern (O_Cancelled Followed by O_Accepted)",
            filter_rule=filter_rule_22,
            case_count=0,
            total_cases=total_cases,
            mean_cycle_time_days=0.0,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_22(),
            evidence_event_indices={},
        )

    matched_22 = case_summary.merge(
        pd.DataFrame(records_22),
        on="case_id",
        how="inner",
    )

    matched_22["first_cancelled_idx"] = matched_22["first_cancelled_idx"].astype("int64")
    matched_22["first_cancelled_time"] = pd.to_datetime(
        matched_22["first_cancelled_time"], utc=True
    ).dt.as_unit("ns")
    matched_22["following_accepted_idx"] = matched_22["following_accepted_idx"].astype("int64")
    matched_22["following_accepted_time"] = pd.to_datetime(
        matched_22["following_accepted_time"], utc=True
    ).dt.as_unit("ns")

    matched_22 = matched_22[
        [
            "case_id",
            "first_cancelled_idx",
            "first_cancelled_time",
            "following_accepted_idx",
            "following_accepted_time",
            "cycle_time_days",
            "event_count",
        ]
    ]

    count_22 = len(matched_22)
    mean_ct_22 = float(matched_22["cycle_time_days"].mean()) if count_22 > 0 else 0.0
    pct_22 = (count_22 / total_cases * 100.0) if total_cases > 0 else 0.0

    return AnalysisResult(
        exercise_code="11.22",
        title="Sequence Pattern (O_Cancelled Followed by O_Accepted)",
        filter_rule=filter_rule_22,
        case_count=count_22,
        total_cases=total_cases,
        mean_cycle_time_days=mean_ct_22,
        percentage=pct_22,
        matched_cases_df=matched_22,
        evidence_event_indices=evidence_22,
    )


def run_all_required_analyses(dataset: LoadedDataset) -> dict[str, AnalysisResult]:
    """Execute all 8 Chapter 11 exercises, handling missing optional attributes gracefully."""
    results: dict[str, AnalysisResult] = {}

    results.update(analyze_exercise_11_7(dataset))

    try:
        results["11.15"] = analyze_exercise_11_15(dataset)
    except MissingOptionalAttributeError as err:
        results["11.15"] = AnalysisResult(
            exercise_code="11.15",
            title="Repeated Activity (W_Assess Potential Fraud Complete >= 2) [UNAVAILABLE]",
            filter_rule=f"[TIDAK TERSEDIA] {err.user_message}",
            case_count=0,
            total_cases=dataset.overview.total_cases,
            mean_cycle_time_days=None,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_15(),
            evidence_event_indices={},
        )

    try:
        results["11.18"] = analyze_exercise_11_18(dataset)
    except MissingOptionalAttributeError as err:
        results["11.18"] = AnalysisResult(
            exercise_code="11.18",
            title="Repeated Activity by Same Resource [UNAVAILABLE]",
            filter_rule=f"[TIDAK TERSEDIA] {err.user_message}",
            case_count=0,
            total_cases=dataset.overview.total_cases,
            mean_cycle_time_days=None,
            percentage=0.0,
            matched_cases_df=_build_empty_matched_11_18(),
            evidence_event_indices={},
        )

    results["11.22"] = analyze_exercise_11_22(dataset)

    return results


def extract_case_trace(
    dataset: LoadedDataset,
    case_id: str,
    highlight_indices: set[int] | None = None,
) -> pd.DataFrame:
    """Extract complete chronological trace for a case with evidence highlight badges."""
    cid_clean = str(case_id).strip()
    raw_df = dataset.raw_df

    trace = raw_df[raw_df["case:concept:name"] == cid_clean]
    if trace.empty:
        empty_df = pd.DataFrame(
            columns=[
                "step_no",
                "_orig_idx",
                "time:timestamp",
                "concept:name",
                "lifecycle:transition",
                "org:resource",
                "is_evidence",
                "evidence_badge",
            ]
        )
        empty_df["step_no"] = empty_df["step_no"].astype("int32")
        empty_df["_orig_idx"] = empty_df["_orig_idx"].astype("int64")
        empty_df["is_evidence"] = empty_df["is_evidence"].astype("bool")
        return empty_df

    sorted_trace = trace.sort_values(
        by=["time:timestamp", "_orig_idx"],
        ascending=[True, True],
        kind="mergesort",
    ).reset_index(drop=True)

    k = len(sorted_trace)
    step_nos = np.arange(1, k + 1, dtype=np.int32)
    time_strs = (
        sorted_trace["time:timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3] + " UTC"
    )

    life_strs = sorted_trace["lifecycle:transition"].fillna("-").astype(str)
    res_strs = sorted_trace["org:resource"].fillna("-").astype(str)

    hl = highlight_indices or set()
    is_ev = sorted_trace["_orig_idx"].isin(hl)
    badges = np.where(is_ev, "[EVIDENCE]", "")

    out_df = pd.DataFrame(
        {
            "step_no": step_nos,
            "_orig_idx": sorted_trace["_orig_idx"].astype("int64"),
            "time:timestamp": time_strs.astype("string"),
            "concept:name": sorted_trace["concept:name"].astype("string"),
            "lifecycle:transition": life_strs.astype("string"),
            "org:resource": res_strs.astype("string"),
            "is_evidence": is_ev.astype("bool"),
            "evidence_badge": pd.Series(badges, dtype="string"),
        }
    )

    return out_df
