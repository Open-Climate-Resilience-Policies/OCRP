(() => {
  let isOnline = navigator.onLine;
  let checkInterval = null;

  function updateStatus(online) {
    const indicator = document.getElementById('status-indicator');
    if (!indicator) return;

    if (online) {
      // Hide when online
      indicator.hidden = true;
    } else {
      // Show red dot when offline
      indicator.hidden = false;
    }
  }

  function checkConnectivity() {
    // Try to fetch a small resource to verify actual connectivity
    // Use HEAD request to minimize bandwidth
    fetch(window.location.origin + '/', { method: 'HEAD', cache: 'no-cache' })
      .then(() => {
        if (!isOnline) {
          isOnline = true;
          updateStatus(true);
        }
      })
      .catch(() => {
        if (isOnline) {
          isOnline = false;
          updateStatus(false);
        }
      });
  }

  function initConnectivity() {
    // Initial state
    updateStatus(navigator.onLine);

    // Listen for browser online/offline events
    window.addEventListener('online', () => {
      isOnline = true;
      updateStatus(true);
    });

    window.addEventListener('offline', () => {
      isOnline = false;
      updateStatus(false);
    });

    // Periodically check connectivity (every 10 seconds)
    // This catches cases where browser thinks we're online but server is unreachable
    checkInterval = setInterval(checkConnectivity, 10000);

    // Check immediately
    checkConnectivity();
  }

  // Clean up interval on page unload
  window.addEventListener('beforeunload', () => {
    if (checkInterval) {
      clearInterval(checkInterval);
    }
  });

  document.addEventListener('DOMContentLoaded', initConnectivity);
})();
