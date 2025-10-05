import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Paths
# ---------------------------
input_path = r"BESALARY.csv"
standard_path = r"occupations_en.csv"
output_path = r"jobs_standardized.csv"

# ---------------------------
# Load datasets
# ---------------------------
df = pd.read_csv(input_path)
df["Job title"] = df["Job title"].astype(str)

# Load standard job titles
standard_df = pd.read_csv(standard_path)
standard_titles = standard_df["preferredLabel"].astype(str).tolist()

# ---------------------------
# Load JobBERT-v2
# ---------------------------
model = SentenceTransformer("TechWolf/JobBERT-v2")

# ---------------------------
# Generate embeddings
# ---------------------------
print("Embedding job titles...")
job_embeddings = model.encode(df["Job title"].tolist(), show_progress_bar=True)
standard_embeddings = model.encode(standard_titles, show_progress_bar=True)

# ---------------------------
# Compute cosine similarity
# ---------------------------
print("Computing similarity...")
similarities = cosine_similarity(job_embeddings, standard_embeddings)

# ---------------------------
# Assign standardized titles
# ---------------------------
top_indices = np.argmax(similarities, axis=1)
df["StandardizedTitle"] = [standard_titles[i] for i in top_indices]

# ---------------------------
# Save results
# ---------------------------
df.to_csv(output_path, index=False)
print(f"Standardized job titles saved to {output_path}")
