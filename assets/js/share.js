(() => {
  function getHashtags() {
    const btn = document.getElementById('share-btn');
    if (!btn) return '';
    const raw = btn.dataset.hashtags || '';
    return raw.trim();
  }

  function getShareText() {
    const title = document.title || 'This page';
    const hashtags = getHashtags();
    const base = `Check this out: ${title}`;
    return hashtags ? `${base}\n\n${hashtags}` : base;
  }

  function shareNative() {
    const text = getShareText();
    const url = window.location.href;
    if (navigator.share) {
      navigator.share({ title: document.title, text, url }).catch(() => {
        // If native share fails, fall back to options
        showFallback();
      });
      return true;
    }
    return false;
  }

  function buildFinalString() {
    const text = getShareText();
    const url = window.location.href;
    return `${text}\n\n${url}`;
  }

  function shareToBluesky() {
    const finalString = buildFinalString();
    const bskyLink = `https://bsky.app/intent/compose?text=${encodeURIComponent(finalString)}`;
    window.open(bskyLink, '_blank', 'noopener');
  }

  function shareToMastodon() {
    const text = buildFinalString();
    const domain = prompt('Enter your Mastodon instance (e.g., mastodon.social):', 'mastodon.social');
    if (domain) {
      const url = `https://${domain.trim()}/share?text=${encodeURIComponent(text)}`;
      window.open(url, '_blank', 'noopener');
    }
  }

  function showFallback() {
    const fallback = document.getElementById('share-fallback');
    const btn = document.getElementById('share-btn');
    if (fallback && btn) {
      fallback.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
    }
  }

  function hideFallback() {
    const fallback = document.getElementById('share-fallback');
    const btn = document.getElementById('share-btn');
    if (fallback && btn) {
      fallback.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }
  }

  function initShare() {
    const btn = document.getElementById('share-btn');
    const bsky = document.getElementById('share-bsky');
    const masto = document.getElementById('share-masto');
    const fallback = document.getElementById('share-fallback');

    if (!btn) return;

    btn.addEventListener('click', () => {
      const usedNative = shareNative();
      if (!usedNative) {
        // Toggle fallback visibility
        if (fallback.hidden) {
          showFallback();
        } else {
          hideFallback();
        }
      }
    });

    if (bsky) {
      bsky.addEventListener('click', () => {
        shareToBluesky();
        hideFallback();
      });
    }

    if (masto) {
      masto.addEventListener('click', () => {
        shareToMastodon();
        hideFallback();
      });
    }

    // Close fallback when clicking outside
    document.addEventListener('click', (e) => {
      const container = document.querySelector('.share-controls');
      if (!container) return;
      if (!container.contains(e.target)) hideFallback();
    });
  }

  document.addEventListener('DOMContentLoaded', initShare);
})();
