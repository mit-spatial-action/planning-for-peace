import pandas as pd
import re
from collections import Counter
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords
nltk.download('stopwords')

# Load the Excel file
FILE_PATH = "data/2015.xlsx"

# Initialize translator (using `deep_translator` instead of `googletrans`)
def translate_text(text):
    try:
        # Translate text to English
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text  # Return original text if translation fails


df = pd.read_excel(FILE_PATH)

# Define a comprehensive set of stopwords
STOPWORDS = set(stopwords.words('english')).union({
    "reparation", "reparations", "study", "research", "paper", "article", "analysis", "discussion"
})

# Clean the text by removing special characters and converting to lowercase
def clean_text(text):
    if not isinstance(text, str):  # Handle non-string inputs
        return ""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    return text

# Apply cleaning and translation to the 'Summary' column (previously 'Description')
df['Summary'] = df['Summary'].dropna().apply(clean_text).apply(translate_text)

# Ensure 'Summary' values are strings
df['Summary'] = df['Summary'].astype(str)

# Define a list of geographical regions and case studies related to reparations

# ----------------------------------------------------------------------------------------------------------------
kws = pd.read_csv("data/kws.csv", usecols=["kw"])

# Count the frequency of geographical regions/case studies
kws = Counter()
for text in df['Summary']:  # Changed from 'Description' to 'Summary'
    if not isinstance(text, str):  # Skip non-string entries to prevent errors
        continue
    for keyword in kws:
        if keyword in text:
            geographical_counts[keyword] += 1

# Show the frequency of geographical regions/case studies
print("Frequency of geographical regions/case studies related to reparations:")
for region, count in geographical_counts.most_common():  # This will print ALL terms, sorted by frequency
    print(f"{region}: {count}")