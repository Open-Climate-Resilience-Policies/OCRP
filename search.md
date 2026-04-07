---
layout: default
title: Search Policy Library
permalink: /search/
---

# Search

<noscript>
  <div style="padding: 1rem; border: 2px solid #856404; background-color: #fff3cd; color: #856404; margin-bottom: 1rem; border-radius: 4px;" role="alert">
    <strong>JavaScript is disabled.</strong> The search feature operates locally in your browser and requires JavaScript. You can still navigate all policies sequentially in the <a href="{{ '/policies/' | relative_url }}">Policy Library</a>.
  </div>
</noscript>

<div id="search" class="search-container"></div>

<script src="/pagefind/pagefind-ui.js"></script>
<script>
  window.addEventListener('DOMContentLoaded', (event) => {
    try {
      if (typeof PagefindUI !== 'undefined') {
        new PagefindUI({ 
          element: "#search", 
          showSubResults: true,
          showImages: false
        });
      } else {
        throw new Error("PagefindUI script did not load.");
      }
    } catch (e) {
      console.error("Pagefind initialization failed", e);
      document.getElementById("search").innerHTML = 
        `<div style="padding: 1rem; border: 2px solid #721c24; background-color: #f8d7da; color: #721c24; margin-bottom: 1rem; border-radius: 4px;" role="alert">
           Search failed to load. Please verify your network connection and try again later.
         </div>`;
    }
  });
</script>

<!-- Pre-fetch CSS to prevent FOUC, Pagefind styles default -->
<link rel="stylesheet" href="/pagefind/pagefind-ui.css">

<style>
/* Base overrides for Pagefind UI to match AGENTS.md accessibility rules */
.search-container {
    margin-top: 2rem;
    margin-bottom: 4rem;
}
.pagefind-ui__search-input {
    border: 2px solid var(--border-color, #ccc);
    border-radius: 4px;
}
.pagefind-ui__search-input:focus {
    outline: 3px solid var(--focus-color, #0b6e4f);
    outline-offset: 2px;
}
</style>
