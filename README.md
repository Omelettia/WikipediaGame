# WikipediaGame

The approach is based on this [report](https://cs229.stanford.edu/proj2015/309_report.pdf).

## Setup
1. Download the XML file of Simple English Wikipedia from this [link](https://dumps.wikimedia.org/simplewiki/20240220/).
2. Run the following files in order:
    1. `Create_graph.ipynb`
    2. `Create_randomized_articles.ipynb`
    3. `Create_Data.ipynb`
    4. `Training_classifier.ipynb`

## Features
There are three path searching algorithms you can use:
- **BFS** (Breadth-First Search)
- **IDDFS** (Iterative Deepening Depth-First Search)
- **A\*** (for this, the ending article is fixed as Minecraft)

You can run `Comparision.ipynb` to compare the three algorithms.
<img src="Results.png">
You can also run `Analysis.ipynb` to compare the performance of the three algorithms over 100 tries.

