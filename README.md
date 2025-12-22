# Open Climate Resilience Policies (OCRP)

A collaborative repository of climate resilience policies, strategies, and best practices for municipalities and organizations worldwide. This site is built with Jekyll and hosted on GitHub Pages.

## 🚀 Project Structure

```
/
├── _layouts/            # Jekyll layouts
│   ├── default.html     # Main page layout
│   └── policy.html      # Policy page layout
├── _policies/           # Policy collection (markdown files)
│   ├── urban-heat-model.md
│   └── ...
├── assets/
│   ├── css/             # Stylesheets
│   └── img/             # Images and SVG files
├── policies/            # Policy listing page (paginated)
│   └── index.md
├── _config.yml          # Jekyll configuration
├── index.md             # Home page
├── about.md             # About page
└── contribute.md        # Contribution guide
```

## 🌐 Live Site

The site is available at: https://ocrap.net/

## 📝 Adding New Policies

We welcome contributions! You can add policies in two ways:

1.  **Via GitHub Issues**: Follow the instructions on our [Contribute page](https://ocrap.net/contribute/) to format your policy using AI and submit it as an issue.
2.  **Direct Pull Request**:
    *   Create a new markdown file in `_policies/`.
    *   Add the required frontmatter (title, summary, type, jurisdiction, date_enacted).
    *   Submit a Pull Request.

## 📄 License

Content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code is licensed under the AGPL-3.0 License. See LICENSE and <https://www.gnu.org/licenses/agpl-3.0.html>.
# OCRaP.ai (Open Climate Resilience Policies AI)

> **Stop reading policy. Start debugging it.**

**OCRaP.ai** is an open-source intelligence platform that verifies, archives, and democratizes climate legislation. We verify "Green" claims against hard science, economic reality, and legal precedent.

### ❓ What does OCRaP stand for?
It’s a **nacronym** (*noun*): A lexical construct that masquerades as an acronym but holds no allegiance to specific words. It started because looking at the state of legislative drafting made us say, *"Oh, crap."*

---

### 🏗️ The Architecture

We don't rely on "Trust." We rely on the **Integrity Engine**.

1.  **The Science Layer (The Physicist):**
    * **Task:** Cross-references policy claims against peer-reviewed studies (IPCC, WHO).
    * **Goal:** If the physics doesn't work, the policy doesn't pass.
2.  **The Business Layer (The CFO):**
    * **Task:** Stress-tests policies for supply chain reality, ROI, and investment risk.
    * **Goal:** Replace "Red Tape" with "Green Tape" (efficiency).
3.  **The Archival Layer (The Time Machine):**
    * **Task:** Automatically saves every cited URL to the Wayback Machine.
    * **Goal:** Prevent "Link Rot" and stealth edits by future administrations.

---

### 🚀 Getting Started

#### For Citizens (The "Lobbyist-in-a-Box")
Don't write a letter from scratch. Use our templates to demand verified, pre-audited policies for your city.
* [Download the "Right to Cool" Letter](#)
* [Download the "Balcony Solar" Request](#)

#### For Developers
We are an AGPL-3.0 project. We need Python devs, Data Scientists, and prompt engineers.

```bash
# Clone the repo
git clone [https://github.com/ocrap-ai/core.git](https://github.com/ocrap-ai/core.git)

# Setup Environment (Ollama or Gemini)
cp example.env .env
pip install -r requirements.txt