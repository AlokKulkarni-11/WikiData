import xml.etree.ElementTree as ET
import sqlite3
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

# ============================
# Load Wikipedia XML Dump
# ============================
def load_wikipedia_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    documents = []
    titles = []
    
    # Extract article titles and text
    for page in root.findall(".//page"):
        title = page.find("title").text
        text = page.find("revision/text").text
        
        if text:
            documents.append(text)
            titles.append(title)
    
    return documents, titles

# ============================
# Load SQL Files (Page and Category Links)
# ============================
def load_sql(sql_file):
    # Connect to the SQLite database or SQL dump
    conn = sqlite3.connect(sql_file)
    return conn

# ============================
# Process Category Mappings
# ============================
def get_categories_for_articles(pages_df, categorylinks_df):
    # Merge the pages with category links using page_id
    merged_df = pd.merge(categorylinks_df, pages_df, on="page_id", how="inner")
    
    # Group by article title and aggregate category names
    category_map = merged_df.groupby('title')['category_id'].apply(list).to_dict()
    return category_map

# ============================
# TF-IDF + LSA Topic Modeling
# ============================
def perform_lsa(documents, vocab, k=80):
    vectorizer = TfidfVectorizer(
        vocabulary=vocab,
        lowercase=True,
        token_pattern=r"(?u)\b\w+\b"
    )
    dtm = vectorizer.fit_transform(documents)
    print("✅ DTM shape:", dtm.shape)

    svd = TruncatedSVD(n_components=k, random_state=42)
    lsa_matrix = svd.fit_transform(dtm)
    terms = vectorizer.get_feature_names_out()

    # Term embedding matrix (used for KD-Tree or further analysis)
    term_embeddings = svd.components_.T  # shape: (num_terms, k)
    np.save("term_vectors.npy", term_embeddings)
    print("✅ Term Vectors saved to: term_vectors.npy")
    
    return lsa_matrix, terms, term_embeddings

# ============================
# Save Results to CSV
# ============================
def save_results(lsa_matrix, term_embeddings, terms, titles, category_map, k=80):
    # Document-Topic strengths
    doc_topic_df = pd.DataFrame(lsa_matrix, columns=[f"Topic_{i+1}" for i in range(k)], index=titles)
    doc_topic_df.to_csv("document_topic_strengths.csv")
    print("✅ Document-Topic strengths saved.")

    # Document-Document similarity
    doc_sim_matrix = cosine_similarity(lsa_matrix)
    pd.DataFrame(doc_sim_matrix, index=titles, columns=titles).to_csv("document_document_similarity.csv")
    print("✅ Document-Document similarity saved.")

    # Term-Term similarity
    term_sim_matrix = cosine_similarity(term_embeddings)
    pd.DataFrame(term_sim_matrix, index=terms, columns=terms).to_csv("term_term_similarity.csv")
    print("✅ Term-Term similarity saved.")

    # Term-Document relationships
    term_doc_matrix = np.dot(term_embeddings, lsa_matrix.T)
    pd.DataFrame(term_doc_matrix, index=terms, columns=titles).to_csv("term_document_relationships.csv")
    print("✅ Term-Document relationships saved.")

    # Category mapping (articles to their categories)
    category_map_df = pd.DataFrame(list(category_map.items()), columns=["Article", "Categories"])
    category_map_df.to_csv("category_article_mapping.csv", index=False)
    print("✅ Category-Article mapping saved.")

# ============================
# Main Processing Function
# ============================
def main():
    # Define file paths
    xml_file_path = "C:/Users/Project/source/repos/WikiParseCuda/WikiParseCuda/data/enwiki-latest-pages-articles.xml"
    pages_sql_file = "C:/Users/Project/source/repos/WikiParseCuda/WikiParseCuda/data/enwiki-latest-page.sql"
    categorylinks_sql_file = "C:/Users/Project/source/repos/WikiParseCuda/WikiParseCuda/data/enwiki-latest-categorylinks.sql"
    
    # 1. Load Wikipedia XML data
    print("🔄 Loading Wikipedia XML data...")
    documents, titles = load_wikipedia_xml(xml_file_path)
    print(f"✅ Loaded {len(documents)} Wikipedia articles.")
    
    # 2. Load SQL data (pages and category links)
    print("🔄 Loading SQL data...")
    conn_pages = load_sql(pages_sql_file)
    pages_df = pd.read_sql_query("SELECT page_id, title FROM page", conn_pages)
    print(f"✅ Loaded {len(pages_df)} pages from the pages SQL file.")

    conn_categorylinks = load_sql(categorylinks_sql_file)
    categorylinks_df = pd.read_sql_query("SELECT page_id, category_id FROM categorylinks", conn_categorylinks)
    print(f"✅ Loaded {len(categorylinks_df)} category links from the categorylinks SQL file.")
    
    # 3. Map categories to articles
    print("🔄 Mapping categories to articles...")
    category_map = get_categories_for_articles(pages_df, categorylinks_df)
    print(f"✅ Mapped categories to {len(category_map)} articles.")
    
    # 4. Preprocess N-Grams (this could be customized as per your N-gram files)
    # For simplicity, let's assume we have the N-gram vocabulary available in a CSV
    ngram_files = ["new_1_grams.csv", "new_2_grams.csv", "new_3_grams.csv", "new_4_grams.csv"]
    vocab = []
    for ngram_file in ngram_files:
        df = pd.read_csv(ngram_file)
        vocab.extend(df['ngram'].dropna().astype(str).tolist())
    vocab = list(set(vocab))
    print(f"✅ Vocabulary size: {len(vocab)} terms.")
    
    # 5. Perform LSA (Topic Modeling)
    print("🔄 Performing LSA (Topic Modeling)...")
    lsa_matrix, terms, term_embeddings = perform_lsa(documents, vocab)
    
    # 6. Save results to CSV files
    print("🔄 Saving results...")
    save_results(lsa_matrix, term_embeddings, terms, titles, category_map)

    print("\n🚀 All embeddings and similarity files updated successfully!")

if __name__ == "__main__":
    main()
