# 🧹 Data Cleaning and Standardization — Reddit BEsalary

This repository documents the process used to clean and standardize salary data collected from **Reddit’s r/BEsalary** community.  
The goal was to make the dataset consistent, analyzable, and compatible with recognized international classification systems.

---

## 📊 1. Overview

The cleaning process focused on two main aspects:

1. **Job Title Standardization** — aligning job titles with the official **ESCO** (European Skills, Competences, and Occupations) taxonomy using **JobBERT-v2**.  
2. **Sector and Industry Mapping** — classifying the “Sector/industry” field into standard **GICS** (Global Industry Classification Standard) categories.

---

## 💼 2. Job Title Standardization

**Purpose:** Convert free-text job titles such as “frontend dev” or “data scientist intern” into consistent occupation names.

**Process Summary:**
- The Reddit salary dataset and ESCO occupation list were loaded.
- Each job title and each ESCO occupation name were transformed into vector representations using a language model trained for job-related text (**JobBERT-v2**).
- Each title was compared to all ESCO occupations using similarity scores.
- The most similar occupation was selected as the standardized title.
- The final dataset was saved with an added column named **`StandardizedTitle`**.

**Outcome:**  
Every job title in the dataset now matches one ESCO occupation, improving consistency for further analysis.

---

## 🏭 3. Sector and Industry Mapping

**Purpose:** Normalize all sector and industry names according to the official **MSCI GICS** structure.

**Process Summary:**
- The “Sector/industry” column was extracted from the Reddit dataset.
- A list of **11 GICS sectors** and **25 industry groups** was used as reference.
- Each entry was semantically compared to these categories using a general text embedding model (**all-MiniLM-L6-v2**).
- The category with the highest similarity score was assigned.
- Three new columns were added:
  - **MappedGroup** — standardized sector or industry name  
  - **Type** — whether it matched a Sector or Industry  
  - **Similarity** — confidence score of the match

**Outcome:**  
All records are now associated with consistent sector or industry classifications, allowing cross-comparison and aggregation.

---

## 🧠 4. Models Used

| Model | Purpose | Source |
|--------|----------|--------|
| **JobBERT-v2** | Understanding and comparing job titles | [Hugging Face](https://huggingface.co/TechWolf/JobBERT-v2) |
| **all-MiniLM-L6-v2** | General-purpose text similarity for sector mapping | [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |

---

## 💾 5. Output Files

| File | Description |
|------|--------------|
| `jobs_standardized.csv` | Dataset with standardized job titles |
| `BESALARY_with_groups.csv` | Dataset with standardized sector and industry categories |

---

## ⚙️ 6. Reproducibility

### Requirements
Python 3.8 or higher with the following libraries:
- pandas  
- numpy  
- scikit-learn  
- sentence-transformers

### Execution
Both scripts can be run independently to produce the standardized outputs.

---


