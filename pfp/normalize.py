from re import sub, IGNORECASE
from deep_translator import GoogleTranslator

def process_text(text:str) -> str:
    text = sub(r"^(the|an) ", "", text, flags=IGNORECASE)
    text = sub(r"^-|-$", "", text, flags=IGNORECASE)
    text = sub(r"[’']s$", "", text, flags=IGNORECASE)
    text = sub(r"\.", "", text, flags=IGNORECASE)
    return text

def preprocess_text(text):
    """Clean and preprocess text"""
    if not isinstance(text, str):
        return ""

    # Convert to lowercase and remove special characters
    text = sub(r'\\W+', ' ', text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english')).union({
        'reparation', 'reparations', 'study', 'research', 'paper',
        'article', 'analysis', 'discussion', 'abstract', 'examines',
        'describes', 'investigates', 'explores'
    })

    words = word_tokenize(text)
    words = [w for w in words if w not in stop_words]

    return ' '.join(words)

def translate_text(text):
    """Translate non-English text to English"""
    try:
        translator = GoogleTranslator(source='auto', target='en')
        return translator.translate(text)
    except:
        return text