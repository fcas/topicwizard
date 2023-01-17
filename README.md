![Logo with text](assets/logo_text.svg)

# topicwizard: Pretty and opinionated topic model visualization

[![PyPI version](https://badge.fury.io/py/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)
[![pip downloads](https://img.shields.io/pypi/dm/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)
[![python version](https://img.shields.io/badge/Python-%3E=3.8-blue)](https://github.com/centre-for-humanities-computing/tweetopic)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
<br>

## Features

-   Pretty :art:
-   Intuitive :cow:
-   Clean API :candy:
-   Sklearn compatible :nut_and_bolt:
-   Easy deployment :earth_africa:

## Installation

Install from PyPI:

```bash
pip install topic-wizard
```

## Usage

### Step 1:

Train a scikit-learn compatible topic model.

```python
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

topic_pipeline = Pipeline(
    [
        ("bow", CountVectorizer()),
        ("nmf", NMF(n_components=10)),
    ]
)
topic_pipeline.fit(texts)
```

### Step 2:

Visualize with topicwizard.

```python
import topicwizard

topicwizard.visualize(pipeline=topic_pipeline, corpus=texts)
```

### Step 3:

Investigate :eyes: .

#### a) Topics

![topics screenshot](assets/screenshot_topics.png)

#### b) Words

![words screenshot](assets/screenshot_words.png)
![words screenshot](assets/screenshot_words_zoomed.png)

#### c) Documents

![documents screenshot](assets/screenshot_documents.png)
