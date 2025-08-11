from spacy import load
import pandas as pd

nlp = load("en_core_web_trf")

def filter_entities(doc, entity_type: str) -> list[str]:
    a = [process_text(ent.text) for ent in doc.ents if ent.label_ in entity_type]
    return list(set(a))

def resolve_entities(text: str, prefix: str) -> dict:
    doc = nlp(text)
    return {
        f"{prefix}_geo": filter_entities(doc, ["GPE", "LOC"]),
        f"{prefix}_org": filter_entities(doc, "ORG"),
        f"{prefix}_ppl": filter_entities(doc, "PERSON"),
    }

def resolve_entities_multi(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        df = pd.concat(
            [
                df, 
                test.get(col).apply(resolve_entities, prefix=col).apply(pd.Series)
            ], 
            axis=1
            )
    return df
    

test = pd.read_csv("output.csv", keep_default_na=False)

results = resolve_entities_multi(test, cols=["title", "abstract"])