import pandas as pd
from sentence_transformers import SentenceTransformer
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

model = SentenceTransformer("all-MiniLM-L6-v2") # usung the same model

'''Create a function to check for drift'''

def run_drift():

    train = pd.read_csv("/data/train_ref.csv")
    prod = pd.read_sql("SELECT * FROM logs", "sqlite:///logs.db") 

    # embeddings
    train_emb = model.encode(train["text"].tolist())
    prod_emb = model.encode(prod["text"].tolist())

    df_train = pd.DataFrame(train_emb)
    df_prod = pd.DataFrame(prod_emb)

    report = Report(metrics=[DataDriftPreset()]) #create a report
    report.run(reference_data=df_train, current_data=df_prod)

    report.save_html("/reports/drift_report.html") #Save the result in an HTML page

    result = report.as_dict()

    drift = result["metrics"][0]["result"]["dataset_drift"]

    return drift #return the result
