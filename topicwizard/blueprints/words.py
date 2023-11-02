from typing import Any, List

import dash_mantine_components as dmc
import numpy as np
from dash_extensions.enrich import DashBlueprint, dcc, html
from plotly import colors

import topicwizard.prepare.words as prepare
from topicwizard.components.color_legend import make_color_legend
from topicwizard.components.words.association_slider import create_association_slider
from topicwizard.components.words.word_barplot import create_word_barplot
from topicwizard.components.words.word_map import create_word_map
from topicwizard.components.words.word_selector import create_word_selector


def create_blueprint(
    vocab: np.ndarray,
    document_term_matrix: np.ndarray,
    topic_term_matrix: np.ndarray,
    topic_names: List[str],
    **kwargs,
) -> DashBlueprint:
    # --------[ Preparing data ]--------
    word_positions = prepare.word_positions(topic_term_matrix=topic_term_matrix)
    word_frequencies = prepare.word_importances(document_term_matrix)
    dominant_topic = prepare.dominant_topic(topic_term_matrix)
    n_topics = len(topic_names)
    # Creating unified color scheme
    tempo = colors.get_colorscale("Rainbow")
    topic_colors = colors.sample_colorscale(tempo, np.arange(n_topics) / n_topics)
    topic_colors = np.array(topic_colors)

    # --------[ Collecting blueprints ]--------
    word_map = create_word_map(
        word_positions=word_positions,
        word_frequencies=word_frequencies,
        vocab=vocab,
        dominant_topic=dominant_topic,
        topic_colors=topic_colors,
    )
    word_selector = create_word_selector(vocab=vocab)
    association_slider = create_association_slider(
        topic_term_matrix=topic_term_matrix,
    )
    word_barplot = create_word_barplot(
        topic_term_matrix=topic_term_matrix, topic_colors=topic_colors
    )
    blueprints = [word_map, word_selector, word_barplot, association_slider]

    # --------[ Creating app blueprint ]--------
    app_blueprint = DashBlueprint()
    app_blueprint.layout = html.Div(
        [
            dcc.Store("selected_words", data=[]),
            dcc.Store("associated_words", data=[]),
            dcc.Store("vocab", data=vocab.tolist()),
            dmc.Grid(
                [
                    dmc.Col(
                        word_selector.layout,
                        span=5,
                    ),
                    dmc.Col(association_slider.layout, span=4),
                ],
                columns=10,
                align="center",
                gutter="md",
                justify="space-between",
                mr=5,
            ),
            dmc.Group(
                [
                    word_map.layout,
                    word_barplot.layout,
                ],
                position="apart",
                grow=1,
                align="stretch",
                className="flex-1 p-3",
            ),
            html.Div(
                make_color_legend(topic_names, topic_colors),
                className="""
                bg-white rounded-md px-4 py-2 fixed bottom-5 left-5
                opacity-80 hover:opacity-100 shadow-md
                h-1/4
                scroll-smooth overflow-y-scroll max-h-full
                """,
            ),
        ],
        className="""
        hidden
        """,
        id="words_container",
    )

    # --------[ Registering callbacks ]--------
    for blueprint in blueprints:
        blueprint.register_callbacks(app_blueprint)
    return app_blueprint
