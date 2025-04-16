import pandas as pd
import json
import os
from datetime import datetime
from app.inference import call_model
from app.prompting import QUESTION_MAPPING

def update_progress(total, done):
    with open("progress.json", "w") as f:
        json.dump({"total": total, "done": done}, f)

def process_csv(file_path, model):
    df = pd.read_csv(file_path)
    df['question_text'] = df['QUESTION_ID'].map(QUESTION_MAPPING)

    # Reorder columns
    cols = df.columns.tolist()
    if 'question_text' in cols and 'Anonymized Narrative' in cols:
        cols.remove('question_text')
        idx = cols.index('Anonymized Narrative')
        cols.insert(idx, 'question_text')
        df = df[cols]

    total = len(df)
    done = 0
    update_progress(total, done)

    def process_row(row):
        nonlocal done
        if pd.isna(row['Anonymized Narrative']) or str(row['Anonymized Narrative']).strip() == "":
            done += 1
            update_progress(total, done)
            return ""
        result = call_model(row, model)
        done += 1
        update_progress(total, done)
        return result

    df['LLM_Response'] = df.apply(process_row, axis=1)

    output_path = os.path.join("output", f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(output_path, index=False)

    update_progress(total, total)  # 100% done
    return output_path