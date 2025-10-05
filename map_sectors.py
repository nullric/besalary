import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Paths
# ---------------------------
input_path = r"BESALARY.csv"
output_path = r"BESALARY_with_groups.csv"

# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv(input_path)
df["Sector/industry"] = df["Sector/industry"].astype(str)  # single column with sector or industry

# ---------------------------
# Hardcoded GICS sectors (11) and industry groups (25)
# ---------------------------
canonical_sectors = [
    "Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples",
    "Health Care", "Financials", "Information Technology", "Communication Services",
    "Utilities", "Real Estate"
]

canonical_industries = [
    "Energy Equipment & Services", "Oil, Gas & Consumable Fuels", "Chemicals", "Construction Materials",
    "Containers & Packaging", "Metals & Mining", "Paper & Forest Products", "Capital Goods",
    "Commercial & Professional Services", "Transportation", "Automobiles & Components",
    "Consumer Durables & Apparel", "Consumer Services", "Retailing", "Food & Staples Retailing",
    "Food, Beverage & Tobacco", "Household & Personal Products", "Health Care Equipment & Services",
    "Pharmaceuticals, Biotechnology & Life Sciences", "Banks", "Diversified Financials",
    "Insurance", "Software & Services", "Technology Hardware & Equipment", "Semiconductors & Semiconductor Equipment"
]

# ---------------------------
# Load embedding model
# ---------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Pre-encode canonical lists once for speed
canonical_sector_embeddings = model.encode(canonical_sectors)
canonical_industry_embeddings = model.encode(canonical_industries)

# ---------------------------
# Function to map closest group
# ---------------------------
def map_to_group(name):
    name_emb = model.encode([name])
    
    # Compare to sectors
    sector_sim = cosine_similarity(name_emb, canonical_sector_embeddings)[0]
    top_sector_idx = np.argmax(sector_sim)
    top_sector_score = sector_sim[top_sector_idx]
    
    # Compare to industries
    industry_sim = cosine_similarity(name_emb, canonical_industry_embeddings)[0]
    top_industry_idx = np.argmax(industry_sim)
    top_industry_score = industry_sim[top_industry_idx]
    
    # Pick higher similarity
    if top_sector_score >= top_industry_score:
        return canonical_sectors[top_sector_idx], "Sector", top_sector_score
    else:
        return canonical_industries[top_industry_idx], "Industry", top_industry_score

# ---------------------------
# Apply mapping
# ---------------------------
mapped_results = df["Sector/industry"].apply(lambda x: map_to_group(x))
df[["MappedGroup", "Type", "Similarity"]] = pd.DataFrame(mapped_results.tolist(), index=df.index)

# ---------------------------
# Save results
# ---------------------------
df.to_csv(output_path, index=False)
print(f"Mapped sector/industry groups saved to {output_path}")
