document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  
  if (!themeToggle) return;

  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
  const savedTheme = localStorage.getItem('theme');
  
  let currentTheme;
  let userHasOverride = false;
  
  if (savedTheme) {
    // User has explicitly set a preference
    currentTheme = savedTheme;
    userHasOverride = true;
  } else {
    // No user override - inherit from browser/OS default
    currentTheme = prefersDarkScheme.matches ? 'dark' : 'light';
  }
  
  function applyTheme(theme) {
    // Set data-theme on root document element
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update button label to reflect the action
    if (theme === 'dark') {
      themeToggle.setAttribute('aria-label', 'Switch to light mode');
    } else {
      themeToggle.setAttribute('aria-label', 'Switch to dark mode');
    }
  }
  
  themeToggle.addEventListener('click', () => {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    currentTheme = newTheme;
    userHasOverride = true;
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  });
  
  // Listen for system theme preference changes (only when no user override exists)
  prefersDarkScheme.addEventListener('change', (e) => {
    if (!userHasOverride) {
      currentTheme = e.matches ? 'dark' : 'light';
      applyTheme(currentTheme);
    }
  });

  // Apply theme on load
  applyTheme(currentTheme);
});
