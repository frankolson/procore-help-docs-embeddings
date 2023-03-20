import os
import openai
import pandas as pd
import time
from tqdm import tqdm

openai.api_key = os.environ["OPENAI_API_KEY"]
tqdm.pandas() # progress indicator for pandas

def get_embedding(text):
  model='text-embedding-ada-002'
  cleaned_text = text.replace("\n", " ")
  result = openai.Embedding.create(
    model=model,
    input=cleaned_text
  )
  # Add delay to avoid API rate limitting of 60 req/min
  time.sleep(1)

  return result["data"][0]["embedding"]

def set_embeddings(input_filename, output_filename):
  df = pd.read_csv(input_filename)
  df['embedding'] = df.content.progress_apply(get_embedding)

  df.to_csv(output_filename, index=False)
