"""External API for creating self-contained figures for topics."""
from typing import Any, Iterable, List, Optional

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

import topicwizard.plots.topics as plots
import topicwizard.prepare.topics as prepare
from topicwizard.prepare.data import prepare_topic_data


def topic_map(
    corpus: Iterable[str],
    pipeline: Optional[Pipeline] = None,
    contextual_model: Optional[TransformerMixin] = None,
    topic_names: Optional[List[str]] = None,
) -> go.Figure:
    """Plots topics on a scatter plot based on the UMAP projections
    of their parameters into 2D space.

    Parameters
    ----------
    corpus: iterable of str
        List of all works in the corpus you intend to visualize.
    pipeline: Pipeline, default None
        Sklearn compatible pipeline, that has two components:
        a vectorizer and a topic model.
    contextual_model: TransformerMixin, default None
        Contextual topic model.
    topic_names: list of str, default None
        List of topic names in the corpus, if not provided
        topic names will be inferred.

    Returns
    -------
    go.Figure
        Bubble chart of topics.
    """
    topic_data = prepare_topic_data(
        corpus=corpus,
        pipeline=pipeline,
        contextual_model=contextual_model,
        topic_names=topic_names,
    )
    x, y = prepare.topic_positions(topic_data["topic_term_matrix"])
    (
        topic_importances,
        _,
        _,
    ) = prepare.topic_importances(
        topic_data["topic_term_matrix"],
        topic_data["document_term_matrix"],
        topic_data["document_topic_matrix"],
    )
    fig = plots.intertopic_map(
        x=x,
        y=y,
        topic_importances=topic_importances,
        topic_names=topic_data["topic_names"],
    )
    return fig


def topic_barcharts(
    corpus: Iterable[str],
    pipeline: Optional[Pipeline] = None,
    contextual_model: Optional[TransformerMixin] = None,
    topic_names: Optional[List[str]] = None,
    top_n: int = 30,
    alpha: float = 1.0,
    n_columns: int = 4,
) -> go.Figure:
    """Plots most relevant words as bar charts for every topic.

    Parameters
    ----------
    corpus: iterable of str
        List of all works in the corpus you intend to visualize.
    pipeline: Pipeline, default None
        Sklearn compatible pipeline, that has two components:
        a vectorizer and a topic model.
    contextual_model: TransformerMixin, default None
        Contextual topic model.
    topic_names: list of str, default None
        List of topic names in the corpus, if not provided
        topic names will be inferred.
    top_n: int, default 5
        Specifies the number of words to show for each topic.
    alpha: float, default 1.0
        Specifies relevance metric for obtaining the most relevant
        words. Has to be in range (0.0, 1.0).
        Numbers closer to zero will yield words that are more
        exclusive to the given topic.
    n_columns: int, default 4
        Number of columns in the subplot grid.

    Returns
    -------
    go.Figure
        Bar chart of topics.
    """
    topic_data = prepare_topic_data(
        corpus=corpus,
        pipeline=pipeline,
        contextual_model=contextual_model,
        topic_names=topic_names,
    )
    (
        topic_importances,
        term_importances,
        topic_term_importances,
    ) = prepare.topic_importances(
        topic_data["topic_term_matrix"],
        topic_data["document_term_matrix"],
        topic_data["document_topic_matrix"],
    )
    n_topics = topic_data["topic_term_matrix"].shape[0]
    n_rows = (n_topics // n_columns) + 1
    fig = make_subplots(
        rows=n_rows,
        cols=n_columns,
        subplot_titles=topic_data["topic_names"],
        vertical_spacing=0.05,
        horizontal_spacing=0.01,
    )
    for topic_id in range(n_topics):
        top_words = prepare.calculate_top_words(
            topic_id,
            top_n,
            alpha,
            term_importances,
            topic_term_importances,
            topic_data["vocab"],
        )
        max_importance = top_words.overall_importance.max()
        subfig = plots.topic_plot(top_words)
        row, column = (topic_id // n_columns) + 1, (topic_id % n_columns) + 1
        for trace in subfig.data:
            # hiding legend if it isn't the first trace.
            if topic_id:
                trace.showlegend = False
            fig.add_trace(trace, row=row, col=column)
            fig.update_xaxes(range=[0, max_importance * 1.5], row=row, col=column)
    fig.update_layout(
        barmode="overlay",
        plot_bgcolor="white",
        hovermode=False,
        uniformtext=dict(
            minsize=10,
            mode="show",
        ),
        legend=dict(
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.6)",
        ),
        margin=dict(l=0, r=0, b=18, pad=2),
    )
    fig.update_xaxes(
        showticklabels=False,
    )
    fig.update_yaxes(ticks="", showticklabels=False)
    fig.update_xaxes(
        gridcolor="#e5e7eb",
    )
    fig.update_yaxes(
        gridcolor="#e5e7eb",
    )
    return fig


def topic_wordclouds(
    corpus: Iterable[str],
    pipeline: Optional[Pipeline] = None,
    contextual_model: Optional[TransformerMixin] = None,
    topic_names: Optional[List[str]] = None,
    top_n: int = 30,
    alpha: float = 1.0,
    n_columns: int = 4,
) -> go.Figure:
    """Plots most relevant words as word clouds for every topic.

    Parameters
    ----------
    corpus: iterable of str
        List of all works in the corpus you intend to visualize.
    pipeline: Pipeline, default None
        Sklearn compatible pipeline, that has two components:
        a vectorizer and a topic model.
    contextual_model: TransformerMixin, default None
        Contextual topic model.
    topic_names: list of str, default None
        List of topic names in the corpus, if not provided
        topic names will be inferred.
    top_n: int, default 30
        Specifies the number of words to show for each topic.
    alpha: float, default 1.0
        Specifies relevance metric for obtaining the most relevant
        words. Has to be in range (0.0, 1.0).
        Numbers closer to zero will yield words that are more
        exclusive to the given topic.
    n_columns: int, default 4
        Number of columns in the subplot grid.

    Returns
    -------
    go.Figure
        Word clouds of topics.
    """
    topic_data = prepare_topic_data(
        corpus=corpus,
        pipeline=pipeline,
        contextual_model=contextual_model,
        topic_names=topic_names,
    )
    n_topics = topic_data["topic_term_matrix"].shape[0]
    (
        topic_importances,
        term_importances,
        topic_term_importances,
    ) = prepare.topic_importances(
        topic_data["topic_term_matrix"],
        topic_data["document_term_matrix"],
        topic_data["document_topic_matrix"],
    )
    n_rows = (n_topics // n_columns) + 1
    fig = make_subplots(
        rows=n_rows,
        cols=n_columns,
        subplot_titles=topic_data["topic_names"],
        vertical_spacing=0.05,
        horizontal_spacing=0.01,
    )
    for topic_id in range(n_topics):
        top_words = prepare.calculate_top_words(
            topic_id,
            top_n,
            alpha,
            term_importances,
            topic_term_importances,
            topic_data["vocab"],
        )
        subfig = plots.wordcloud(top_words)
        row, column = (topic_id // n_columns) + 1, (topic_id % n_columns) + 1
        fig.add_trace(subfig.data[0], row=row, col=column)
    fig.update_layout(
        plot_bgcolor="white",
    )
    fig.update_yaxes(
        showticklabels=False,
        gridcolor="white",
        linecolor="white",
        zerolinecolor="white",
    )
    fig.update_xaxes(
        showticklabels=False,
        gridcolor="white",
        linecolor="white",
        zerolinecolor="white",
    )
    fig.update_traces(hovertemplate="", hoverinfo="none")
    return fig
