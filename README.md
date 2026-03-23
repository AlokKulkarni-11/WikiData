The current version of the project is implemented in main.py, which serves as the central entry point for executing both processing streams.

Our Mini Project 1 focuses on building a system that identifies the most relevant categories for a user-provided word using two different approaches:

Stream 1: Offline Semantic Analysis using CUDA & HPC

In this approach, we utilize High Performance Computing (HPC) with CUDA acceleration to process a locally stored Wikipedia data dump. The system parses large chunks of Wikipedia data and performs semantic analysis to understand contextual relationships. Based on this analysis, it returns the top 3 most relevant categories for any input word.

Stream 2: Online Data Fetching & Semantic Processing

The second approach relies on real-time data retrieval using Wikipedia APIs. It:

Fetches the top 10 categories from the given word’s Wikipedia page
Expands context by exploring related linked pages
Applies semantic analysis while filtering out stop words and irrelevant content

After processing, it outputs the top 3 most meaningful categories for the input word.

Objective

The objective of this project is to determine the most relevant categories associated with any user-input word. For example, the term “entropy” is closely related to Physics, Chemistry, and Machine Learning, and the system aims to correctly identify such top 3 contextually relevant categories.
