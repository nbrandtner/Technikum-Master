"""Interactive presentation of real experiments and explicit architectural judgment."""
from __future__ import annotations

from html import escape

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from earlybird.analysis import consensus
from earlybird.data import DATA, ROOT, load_clauses, load_sources, read_json
from earlybird.pipeline import load_bundle

BACKGROUND = "#10161d"
SURFACE = "#1a232e"
TEXT = "#e7edf3"
MUTED = "#b4c0cd"
BORDER = "#334354"
COLORS = ["#f0ab70", "#64c7b4", "#b8a0ec", "#ee91a7", "#adca74", "#79b9e6", "#e1c36b", "#d3a0c2", "#83c5d0", "#cbb49d"]


def dark_plot(fig):
    """Keep labels, tooltips, and grid lines readable on the dark app surface."""
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font_color=TEXT,
                      hoverlabel=dict(bgcolor=SURFACE, font_color=TEXT, bordercolor=BORDER))
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def style():
    st.markdown("""<style>
    .block-container {max-width:1400px; padding-top:2rem; padding-bottom:3rem;}
    h1,h2,h3 {font-family:Georgia,'Times New Roman',serif; letter-spacing:-.035em;}
    h1 {font-size:3rem !important; font-weight:500 !important;}
    h2 {font-size:2rem !important;}
    [data-testid=stSidebar] {border-right:1px solid #334354;}
    [data-testid=stMetric] {background:#1a232e; padding:.7rem 1rem; border-radius:12px;}
    .eyebrow {font-size:.74rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:#f0ab70;}
    .intro {font-size:1.12rem; color:#b4c0cd; max-width:780px; line-height:1.6;}
    .source-card {padding:1rem 1.25rem; color:#e7edf3; border-left:3px solid #f0ab70; background:#1a232e; border-radius:0 10px 10px 0;}
    .small-note {font-size:.83rem; color:#b4c0cd;}
    .component {padding:1rem 1.2rem; color:#e7edf3; border-radius:12px; background:#1a232e; border:1px solid #334354; margin-bottom:1rem;}
    .component h3 {margin-top:.2rem; margin-bottom:.5rem;}
    [data-testid=stAlertContentInfo] [data-testid=stMarkdownContainer] {color:#c4ddff;}
    [data-testid=stSliderThumbValue] [data-testid=stMarkdownContainer] {color:#f0ab70;}
    div.stButton>button {border-radius:8px;}
    </style>""", unsafe_allow_html=True)


def source_inspector(item_id, records, data=None, run=None, live_db=False):
    record = next(r for r in records if r["id"] == item_id)
    source = next(r for r in load_sources()["requirements"] if r["id"] == record["source"])
    st.markdown(f"### {item_id}")
    st.write(record["text"])
    if run:
        i = run["ids"].index(item_id)
        st.caption(f"Cluster {run['labels'][i]} · Euclidean silhouette {run['point_silhouettes'][i]:.3f}")
    with st.expander(f"Original {source['id']} · PDF page {source['page']}", expanded=True):
        st.markdown(f'<div class="source-card">{escape(source["text"])}</div>', unsafe_allow_html=True)
        if "review_note" in record:
            st.caption(record["review_note"])
    if data:
        st.markdown("**Nearest clauses · cosine similarity**")
        neighbors = data["neighbors"][item_id]
        if live_db:
            try:
                from earlybird.database import Database
                db = Database()
                try:
                    neighbors = db.nearest(data["fingerprint"], item_id)
                finally:
                    db.close()
                st.caption("Read from the live database on this interaction.")
            except Exception as error:
                st.warning(f"Live query unavailable; showing saved evidence. {type(error).__name__}")
        table = [{"Clause": n["id"], "Cosine": round(n["cosine"], 3),
                  "Text": next(r["text"] for r in records if r["id"] == n["id"])} for n in neighbors]
        st.dataframe(pd.DataFrame(table), hide_index=True, width="stretch")


def discover(bundle, live_db):
    st.markdown("## Follow the evidence")
    st.write("Explore the full-dimensional clustering. The map is a fixed PCA projection for display.")
    input_col, k_col, seed_col = st.columns([1.8, 1, 1])
    with input_col:
        name = st.selectbox("Input", ["reviewed", "source"], format_func=lambda x: {
            "reviewed": "Reviewed future-system clauses", "source": "Original source baseline"}[x])
    data = bundle["datasets"][name]
    review_path = DATA / "architecture.json"
    review = read_json(review_path) if review_path.exists() else None
    candidate = next((r for r in data["runs"] if review and r["id"] == review["basis"]["candidate_run"]), None)
    if name == "source":
        st.info("This baseline retains original wording, including retired phone interactions. It differs in scope and granularity from the reviewed clauses.")
    with k_col:
        ks = sorted({r["k"] for r in data["runs"]})
        default_k = candidate["k"] if candidate else data["suggested_k"]
        k = st.selectbox("Components to explore", ks, index=ks.index(default_k), key=f"k-{name}")
    choices = [r for r in data["runs"] if r["k"] == k]
    with seed_col:
        seed = st.selectbox("Seed", [r["seed"] for r in choices], key=f"seed-{name}")
    run = next(r for r in choices if r["seed"] == seed)
    summary = next(r for r in data["summary"] if r["k"] == k)
    if candidate:
        st.caption(f"Inspection candidate: k={candidate['k']}, seed={candidate['seed']}. Geometric reference: k={data['suggested_k']}. Neither is an architectural verdict.")
    else:
        st.caption(f"Geometric reference: k={data['suggested_k']}. Choose another k to inspect its tradeoffs.")
    a, b, c, d = st.columns(4)
    a.metric("Clauses", len(data["records"]))
    b.metric("Silhouette", f"{run['silhouette']:.3f}")
    c.metric("Seed agreement", f"{summary['seed_agreement']:.3f}")
    d.metric("Singletons", run["singletons"])
    st.caption("Silhouette = Euclidean separation; seed agreement = mean pairwise ARI at this k. Neither measures architectural correctness.")
    left, right = st.columns([1.25, 1], gap="large")
    frame = pd.DataFrame({"id": run["ids"], "PCA 1": [c[0] for c in data["coordinates"]],
                          "PCA 2": [c[1] for c in data["coordinates"]],
                          "Cluster": [f"Cluster {i}" for i in run["labels"]],
                          "Requirement": [r["text"] for r in data["records"]]})
    palette = {f"Cluster {i}": COLORS[i % len(COLORS)] for i in sorted(set(run["labels"]))}
    with left:
        show_labels = st.toggle("Show clause labels", value=False)
        fig = px.scatter(frame, x="PCA 1", y="PCA 2", color="Cluster", text="id" if show_labels else None,
                         custom_data=["id"], hover_name="id", hover_data={"Requirement": True},
                         color_discrete_map=palette)
        fig.update_traces(marker={"size": 13, "line": {"width": 1, "color": BACKGROUND}},
                          textposition="top center", textfont={"size": 10})
        fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          margin={"l": 10, "r": 10, "t": 15, "b": 10}, legend={"orientation": "h"},
                          font={"color": TEXT}, uirevision=name)
        selected = st.plotly_chart(dark_plot(fig), key=f"map-{name}", on_select="rerun", selection_mode="points",
                                 width="stretch", alt="Requirement clusters on a fixed PCA projection. Select a clause to inspect its source.")
        st.caption(f"PCA retains {sum(data['pca_variance']):.1%} of variance in two dimensions. Clustering uses all embedding dimensions. Cluster numbers and colors are local to a run.")
    with right:
        ids = run["ids"]
        points = selected.selection.points if selected else []
        if points:
            suggested = points[-1]["customdata"][0]
            # A retained chart selection must not overwrite a later dropdown choice.
            if st.session_state.get(f"last-map-selection-{name}") != suggested:
                st.session_state[f"inspect-{name}"] = suggested
                st.session_state[f"last-map-selection-{name}"] = suggested
        else:
            st.session_state[f"last-map-selection-{name}"] = None
        item_id = st.selectbox("Inspect a clause", ids, key=f"inspect-{name}")
        source_inspector(item_id, data["records"], data, run, live_db)
    with st.expander("Component membership · inspect names and source clauses", expanded=False):
        for card in run["cards"]:
            named = bool(candidate and run["id"] == candidate["id"])
            title = review["candidate_names"][str(card["cluster"])] if named else card["name"]
            st.markdown(f"**Cluster {card['cluster']} · {title}**")
            st.write(card["responsibility"])
            st.caption(", ".join(card["ids"]))
        st.caption("Human-reviewed names for the inspection candidate; TF-IDF keyword suggestions for other runs.")
    with st.expander("Experiment details"):
        st.code(bundle["cluster_query"], language="cypher")
        st.json({"run": run["id"], "dataset_hash": data["fingerprint"], "model": bundle["model"],
                 "database": bundle["database"], "parameters": bundle["parameters"]})


def stability(bundle):
    st.markdown("## Which boundaries hold?")
    st.write("Inspect agreement across repeated runs, then change one requirement's wording while preserving its meaning.")
    data = bundle["datasets"]["reviewed"]
    summary = pd.DataFrame(data["summary"])
    left, right = st.columns(2)
    with left:
        fig = px.line(summary, x="k", y="mean_silhouette", markers=True,
                      labels={"k": "Number of clusters", "mean_silhouette": "Mean Euclidean silhouette"})
        fig.update_traces(line_color=COLORS[0])
        st.plotly_chart(dark_plot(fig), width="stretch")
    with right:
        fig = px.line(summary, x="k", y="seed_agreement", markers=True,
                      labels={"k": "Number of clusters", "seed_agreement": "Mean seed agreement · ARI"})
        fig.update_traces(line_color=COLORS[1])
        st.plotly_chart(dark_plot(fig), width="stretch")
    k = st.select_slider("Inspect consensus at k", options=summary["k"].tolist(), value=data["suggested_k"])
    runs = [r for r in data["runs"] if r["k"] == k]
    matrix = consensus(runs)
    order = np.argsort(runs[0]["labels"], kind="stable")
    ids = [runs[0]["ids"][i] for i in order]
    fig = go.Figure(go.Heatmap(z=matrix[np.ix_(order, order)], x=ids, y=ids, zmin=0, zmax=1,
                              colorscale=[[0, "#17212b"], [1, "#64c7b4"]],
                              colorbar={"title": "Together"},
                              hovertemplate="%{x} + %{y}<br>Together in %{z:.0%} of seeds<extra></extra>"))
    fig.update_layout(height=620, margin={"t": 10, "b": 50})
    st.plotly_chart(dark_plot(fig), width="stretch")
    st.caption(f"Observed co-assignment across {len(runs)} runs at the same k. This is stability evidence, not a confidence probability.")
    st.markdown("### One clause, different words")
    if not bundle["paraphrases"]:
        st.info("Paraphrase probes were not included in this experiment. Run the full pipeline to add them.")
    for variant in bundle["paraphrases"]:
        with st.expander(f"{variant['clause']} · {variant['id']}"):
            original = next(r["text"] for r in data["records"] if r["id"] == variant["clause"])
            st.write("**Original:** " + original)
            st.write("**Paraphrase:** " + variant["text"])
            st.caption(variant["review"])
            rows = [{"k": r["k"], "seed": r["seed"], "ARI to same seed": r["ari_to_same_seed"]} for r in variant["runs"]]
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption("A stable paraphrase preserves meaning. A changed business rule requires a separate impact review. Same-seed changes can also alter K-Means initialization geometry.")


def architecture_graph(architecture, active=None):
    active = set(active or [])
    rows = ['digraph { rankdir=TB; bgcolor="transparent"; nodesep=0.6; ranksep=0.6; node [shape=box, style="rounded,filled", fontname="Arial", fontsize=13, margin="0.2,0.15"]; edge [color="#91a3b5", fontcolor="#b4c0cd", fontname="Arial", fontsize=11];']
    for i, component in enumerate(architecture["components"]):
        key = component["id"]
        highlighted = not active or key in active
        color = COLORS[i % len(COLORS)] if highlighted else BORDER
        fill = SURFACE if highlighted else BACKGROUND
        text = TEXT if highlighted else MUTED
        rows.append(f'"{key}" [label="{component["name"]}", fillcolor="{fill}", color="{color}", penwidth=2, fontcolor="{text}"];')
    for dep in architecture["dependencies"]:
        rows.append(f'"{dep["from"]}" -> "{dep["to"]}" [label="{dep["label"]}"];')
    rows.append('}')
    st.graphviz_chart("\n".join(rows), width="stretch")


def inspect_architecture(bundle):
    st.markdown("## From similarity to responsibility")
    path = DATA / "architecture.json"
    if not path.exists():
        st.info("The architectural review will be added after inspecting the first genuine database runs.")
        return
    architecture = read_json(path)
    st.caption("Human-reviewed proposal · ownership and dependency direction are architectural decisions.")
    st.write(architecture["rationale"])
    candidate = next((r for r in bundle["datasets"]["reviewed"]["runs"]
                      if r["id"] == architecture["basis"]["candidate_run"]), None)
    if candidate is None:
        st.warning("This review refers to an earlier experiment. Rerun the documented full configuration or update the review before treating it as a review of the current results.")
    else:
        with st.expander("The database proposal that was reviewed"):
            st.caption(architecture["basis"]["selection"])
            for card in candidate["cards"]:
                st.write(f"**C{card['cluster']} · {architecture['candidate_names'][str(card['cluster'])]}**")
                st.caption(", ".join(card["ids"]))
    architecture_graph(architecture)
    st.caption("Arrows show allowed use / producer-contract dependencies. They are not vector similarity links or a deployment diagram.")
    cols = st.columns(2, gap="large")
    for i, component in enumerate(architecture["components"]):
        with cols[i % 2]:
            st.markdown(f'<div class="component" style="border-top:4px solid {COLORS[i % len(COLORS)]}"><span class="eyebrow">{escape(component["scope"])}</span><h3>{escape(component["name"])}</h3>{escape(component["responsibility"])}</div>', unsafe_allow_html=True)
            with st.expander("Ownership, operations, and source clauses"):
                st.write("**Owns:** " + component["owns"])
                st.write("**Offers:** " + "; ".join(component["operations"]))
                st.caption(", ".join(component["clauses"]))
    st.markdown("### What changed during review?")
    for decision in architecture["decisions"]:
        with st.expander(decision["title"]):
            st.write(decision["reason"])
            st.caption("Evidence: " + ", ".join(decision["clauses"]))
    if candidate:
        owner = {clause: c["name"] for c in architecture["components"] for clause in c["clauses"]}
        with st.expander("Full ownership trail · every reviewed clause"):
            st.dataframe(pd.DataFrame([{"Clause": item, "Database cluster": f"C{label}",
                "Reviewed primary owner": owner[item]} for item, label in zip(candidate["ids"], candidate["labels"])]),
                hide_index=True, width="stretch")
    st.download_button("Download architecture proposal", path.read_text(encoding="utf-8"), "earlybird-architecture.json", "application/json")


def challenge(bundle):
    st.markdown("## Put the architecture under pressure")
    scenarios = read_json(DATA / "scenarios.json")
    chosen = st.selectbox("Walkthrough", scenarios, format_func=lambda s: s["title"])
    st.markdown(f"### {chosen['title']}")
    st.write(chosen["subtitle"])
    st.info(chosen["question"])
    sources = {r["id"]: r for r in load_sources()["requirements"]}
    with st.expander("Source evidence"):
        for source_id in chosen["sources"]:
            st.write(f"**{source_id}:** {sources[source_id]['text']}")
    data = bundle["datasets"]["reviewed"]
    architecture_path = DATA / "architecture.json"
    architecture = read_json(architecture_path) if architecture_path.exists() else None
    selected_id = architecture["basis"]["candidate_run"] if architecture else data["reference_run"]
    reference = next((r for r in data["runs"] if r["id"] == selected_id),
                     next(r for r in data["runs"] if r["id"] == data["reference_run"]))
    mapping = dict(zip(reference["ids"], reference["labels"]))
    st.caption(f"Database candidate k={reference['k']}, seed={reference['seed']}: " + " · ".join(f"{c} → C{mapping[c]}" for c in chosen["clauses"]))
    step = st.slider("Walk through the scenario", 1, len(chosen["steps"]), 1, key="step-"+chosen["id"])
    current = chosen["steps"][step-1]
    st.markdown(f"#### {step:02d} / {current['title']}")
    st.write(current["body"])
    architecture_path = DATA / "architecture.json"
    if architecture_path.exists():
        architecture_graph(read_json(architecture_path), current["components"])
    a, b = st.columns(2)
    with a:
        st.success("**Proposed decision**\n\n" + chosen["decision"])
    with b:
        st.warning("**Failure to prevent**\n\n" + chosen["failure"])
    st.caption(chosen["limit"])


def sources_view():
    st.markdown("## Every statement accounted for")
    source = load_sources()
    search = st.text_input("Find a statement", placeholder="Try cancellation, itinerary, or R43")
    dispositions = st.multiselect("Disposition", sorted({r["disposition"] for r in source["requirements"]}))
    clauses = load_clauses()
    for r in source["requirements"]:
        if search.lower() not in (r["id"] + " " + r["text"]).lower():
            continue
        if dispositions and r["disposition"] not in dispositions:
            continue
        with st.expander(f"{r['id']} · {r['disposition']} · page {r['page']}"):
            st.write(r["text"])
            st.caption(r["rationale"])
            for clause in [c for c in clauses if c["source"] == r["id"]]:
                st.write(f"**{clause['id']}** — {clause['text']}")
                st.caption(clause["review_note"])
    st.markdown("### Open questions, preserved")
    for assumption in read_json(DATA / "assumptions.json"):
        with st.expander(f"{assumption['id']} · {assumption['question']}"):
            st.write(assumption["handling"])
            st.caption(", ".join(assumption["sources"]))
    st.download_button("Download the reviewed clauses", (DATA / "clauses.json").read_text(encoding="utf-8"), "earlybird-clauses.json", "application/json")
    st.caption(f"Source PDF SHA-256: {source['sha256']}. {source['extraction']}.")


def main():
    st.set_page_config(page_title="EarlyBird · Boundary Lab", page_icon="◒", layout="wide")
    style()
    st.markdown('<div class="eyebrow">EarlyBird / An architecture investigation</div>', unsafe_allow_html=True)
    st.title("Good boundaries need evidence.")
    st.markdown('<p class="intro">Discover what requirements have in common. Inspect where the clusters hesitate. Challenge the architecture with the rules that matter.</p>', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## Boundary Lab")
        view = st.radio("Explore", ["Discover", "Stability", "Inspect", "Challenge", "Sources"], label_visibility="collapsed")
        st.divider()
        st.caption("LOCAL / FREE / REPRODUCIBLE")
        st.write("44 source statements. Every transformation has a trace.")
        live_db = st.toggle("Query live neighbors", value=False)
        if st.button("Check database"):
            try:
                from earlybird.database import Database
                db = Database()
                try:
                    st.success(str(db.status()))
                finally:
                    db.close()
            except Exception as error:
                st.warning(f"Database unavailable: {type(error).__name__}. Saved results remain usable.")
    bundle = load_bundle()
    if bundle:
        st.caption(f"SAVED EXPERIMENT REPLAY · {bundle['engine']} · {bundle['verification']['base_runs'] + bundle['verification']['paraphrase_runs']} genuine runs · {bundle['model']['model'].split('/')[-1]}")
    if view == "Sources":
        sources_view()
    elif not bundle:
        st.info("The source inventory is ready. Run `earlybird run` to generate the first genuine database experiment. No sample results are fabricated.")
        sources_view()
    elif view == "Discover":
        discover(bundle, live_db)
    elif view == "Stability":
        stability(bundle)
    elif view == "Inspect":
        inspect_architecture(bundle)
    else:
        challenge(bundle)
    st.divider()
    st.caption("Similarity proposes. Business rules constrain. Architectural judgment stays visible.")


if __name__ == "__main__":
    main()
