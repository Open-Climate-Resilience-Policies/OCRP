# OCRP TODOs

_Generated 2025-12-21 · Converted to Markdown 2025-12-28_

1. **Remove vendored gems** — **completed**
   - `vendor/bundle` removed from Git index; `.gitignore` updated and committed.

2. **Push current branch** — **completed**
   - `main` pushed to `origin` (b7c21b0..92cdaef); branch now tracks `origin/main`.

3. **Inspect policies folder** — **in-progress**
   - List files in `_policies/` and locate duplicate/backup files that surface as empty listings on the site.

4. **Open offending files** — **not-started**
   - Targets: `_policies/urban-heat-model.md.bak`, `_policies/virtual-power-plant/` (dir), `_policies/virtual-power-plant.md`, `_policies/virtual-power-plant.md.bak`, `_policies/virtual-power-plant.md.bak.overview`, etc.

5. **Fix or remove backups** — **not-started**
   - Either add `published: false` to backup files' frontmatter or delete/rename them so Jekyll ignores them.

6. **Commit and push fix** — **not-started**
   - `git add ...`, `git commit -m "Fix policy backups/published flags"`, `git push`.

7. **Verify GitHub Pages build/logs** — **not-started**
   - After pushing, confirm Pages/Actions builds finish without errors.

8. **Run Docker Jekyll build (optional)** — **not-started**
   - Build site via `make build-docker` to validate `_site` without native Ruby toolchain.

9. **Update taxonomy data for Jekyll** — **not-started**
   - Move `src/data/taxonomy_index.json` to `_data/taxonomy_index.json` or update scripts accordingly.

10. **Add optional policy media include** — **not-started**
    - Add a `media` array to policy frontmatter plus a shared include that renders optional images/diagrams (with required alt text) so visual asides can be dropped into policies without layout churn.

11. **Standardize metadata vocabulary** — **not-started**
   - Align `policy_category`, `hazard_type`, and related tags with the hyphenated taxonomy used elsewhere; ensure each policy carries consistent `equity`/`cost` notes where prior reviews flagged gaps.

12. **Embed equity & cost sections** — **not-started**
   - When policies reference affordability impacts (e.g., 15-minute city, balcony solar), add explicit equity/cost subsections or tags to maintain comparability across the library.

13. **Implement Quality GitHub Actions workflow** — **not-started**
   - Build `.github/workflows/quality.yml` with the planned Jekyll build, HTML validation, accessibility (axe), and JavaScript lint jobs so manual checks become automated.

14. **Automate link checker runs** — **not-started**
   - Wire `scripts/find_broken_links.py` into CI or a scheduled job to catch dead/redirected citations regularly, using the redirect-rewrite flag we recently added.

_Next focus: finish the backup-policy cleanup flow (items 3–7), then tackle the optional media include to unlock richer policy documentation._