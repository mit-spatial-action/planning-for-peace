import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
import re
from deep_translator import GoogleTranslator
import spacy

FILE_PATH = 'path/to/exported.results'

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def analyze_topics(df, n_topics=10):
    """Perform topic modeling using LDA"""
    # Combine all relevant columns for better context
    df['combined_text'] = (
        df['Title'].fillna('') + ' ' +
        df['Summary'].fillna('') + ' ' +
        df['Contents'].fillna('') + ' ' +
        df['Subjects'].fillna('')
    )

    # Preprocess and translate texts
    print("Preprocessing texts...")
    processed_texts = df['combined_text'].apply(translate_text).apply(preprocess_text)

    # Create TF-IDF matrix
    print("Creating TF-IDF matrix...")
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(processed_texts)

    # Perform LDA
    print("Performing topic modeling...")
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(tfidf_matrix)

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Extract top words for each topic
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10:-1]]
        topics.append(top_words)

    return topics

def main():
    # Load the Excel file with the correct path

    print(f"Loading data from {FILE_PATH}...")
    try:
        df = pd.read_excel(FILE_PATH)
        print(f"Successfully loaded {len(df)} rows of data")

        # Print available columns for verification
        print("\\nAvailable columns in the dataset:")
        print(df.columns.tolist())

    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Extract topics using LDA
    topics = analyze_topics(df)

    # Extract locations and specific topics from all relevant columns
    print("\\nExtracting locations and topics...")
    all_entities = []

    # Process each column separately for better tracking
    for column in ['Title', 'Summary', 'Contents', 'Subjects']:
        print(f"\\nProcessing {column} column...")
        column_entities = []
        for text in df[column].fillna(''):
            translated_text = translate_text(text)
            entities = extract_locations_and_topics(translated_text)
            column_entities.extend(entities)

        # Print top entities for this column
        column_counts = Counter(column_entities)
        print(f"\\nTop 10 entities in {column}:")
        for entity, count in column_counts.most_common(10):
            print(f"{entity}: {count}")

        all_entities.extend(column_entities)

    # Overall counts
    entity_counts = Counter(all_entities)

    print("\\nOverall Top 20 Most Frequent Locations/Organizations:")
    for entity, count in entity_counts.most_common(20):
        print(f"{entity}: {count}")

    print("\\nDiscovered Topics:")
    for idx, topic_words in enumerate(topics):
        print(f"\\nTopic {idx + 1}: {', '.join(topic_words)}")

if __name__ == "__main__":
    main()