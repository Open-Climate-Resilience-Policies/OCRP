import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# CONFIG
POLICY_DIR = "policies"
REPORT_DIR = "data/reports"
IMAGE_DIR = "assets/images/reports"

# Ensure directories exist
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def load_policies():
    """Reads all index.md files from the policy directory."""
    documents = []
    filenames = []
    
    if not os.path.exists(POLICY_DIR):
        print(f"⚠️ Error: Directory '{POLICY_DIR}' not found.")
        return [], []

    print(f"📂 Scanning '{POLICY_DIR}' for policies...")
    
    for folder in sorted(os.listdir(POLICY_DIR)):
        # Skip hidden files or non-folders
        if folder.startswith('.'): continue
        
        file_path = os.path.join(POLICY_DIR, folder, "index.md")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append(f.read())
                filenames.append(folder)
                
    print(f"✅ Loaded {len(documents)} policies.")
    return documents, filenames

def analyze_redundancy():
    documents, filenames = load_policies()
    if not documents: return

    # 1. Load the "Brain" (Runs locally, downloads once ~80MB)
    print("🧠 Loading AI Model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Convert text to math (Vectors)
    print("🔢 Generating Semantic Embeddings...")
    embeddings = model.encode(documents)
    
    # 3. Calculate Similarity Matrix
    similarity_matrix = cosine_similarity(embeddings)
    
    # 4. Generate the Heatmap Image
    print("🎨 Generating Visualization...")
    df = pd.DataFrame(similarity_matrix, index=filenames, columns=filenames)
    plt.figure(figsize=(12, 10))
    sns.heatmap(df, annot=False, cmap="YlOrRd", vmin=0, vmax=1)
    plt.title("Policy Similarity Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "redundancy_heatmap.png"))
    plt.close()

    # 5. Generate the Markdown Report
    print("📝 Writing Audit Report...")
    report_path = os.path.join(REPORT_DIR, "redundancy_audit.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        # Frontmatter for Jekyll/GitHub Pages
        f.write("---\n")
        f.write("layout: page\n")
        f.write("title: Policy Redundancy Audit\n")
        f.write("permalink: /reports/redundancy/\n")
        f.write("---\n\n")
        
        f.write(f"# 🕵️ Policy Redundancy Audit\n")
        f.write(f"**Last Run:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("This report identifies policies that are semantically similar. High overlap (>80%) suggests a duplicate; Moderate overlap (>60%) suggests they should be linked.\n\n")
        
        f.write("## 🗺️ Similarity Cluster Map\n")
        f.write(f"![Heatmap](/assets/images/reports/redundancy_heatmap.png)\n\n")
        
        f.write("## 🚨 Potential Duplicates (Action Required)\n")
        f.write("| Policy A | Policy B | Similarity Score | Recommendation |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        count = 0
        # Iterate upper triangle of matrix only (avoid duplicates/self-matches)
        for i in range(len(filenames)):
            for j in range(i + 1, len(filenames)):
                score = similarity_matrix[i][j]
                if score > 0.60:
                    count += 1
                    policy_a = filenames[i]
                    policy_b = filenames[j]
                    percent = f"{int(score*100)}%"
                    
                    if score > 0.85:
                        rec = "**MERGE** (They are nearly identical)"
                    elif score > 0.70:
                        rec = "**LINK** (Add to 'Related Policies')"
                    else:
                        rec = "Review (Shared concepts)"
                        
                    f.write(f"| `{policy_a}` | `{policy_b}` | {percent} | {rec} |\n")
        
        if count == 0:
            f.write("\n*No significant redundancy detected. Great job!* 🎉\n")

    print(f"✅ Done! Report saved to {report_path}")

if __name__ == "__main__":
    analyze_redundancy()