(() => {
  const path = window.location.pathname || '';
  const isPolicyPage = path.startsWith('/policies/') && path !== '/policies/' && path !== '/policies' && path !== '/policies/index.html';
  if (!isPolicyPage) return;
  if (window.__policyAssistantLoaded) return;
  window.__policyAssistantLoaded = true;

  const STORAGE_KEY = 'user_civic_profile';
  const MAX_CONTEXT_LENGTH = 10000;

  const storage = (() => {
    try {
      return window.localStorage;
    } catch (err) {
      return null;
    }
  })();

  const state = {
    profile: null,
    role: 'activist',
  };

  function getGeolocation() {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        resolve(null);
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`, {
            headers: { 'Accept': 'application/json' }
          })
            .then((r) => r.json())
            .then((data) => {
              const addr = data.address || {};
              resolve({
                city: addr.city || addr.town || addr.village || '',
                region: addr.state || '',
                country: addr.country || ''
              });
            })
            .catch(() => resolve(null));
        },
        () => resolve(null),
        { timeout: 5000 }
      );
    });
  }

  function loadProfile() {
    if (!storage) return null;
    try {
      const raw = storage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (err) {
      return null;
    }
  }

  function saveProfile(profile) {
    if (!storage) return;
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(profile));
    } catch (err) {
      // ignore storage errors silently
    }
  }

  function cleanTitle() {
    const raw = (document.title || '').trim();
    if (!raw) return '';
    const parts = raw.split(' - ');
    return (parts[0] || raw).trim();
  }

  function scrapeContext() {
    const title = cleanTitle();
    const url = window.location.href;
    let root = document.querySelector('main');
    if (!root) root = document.body;
    let text = root ? root.textContent || '' : '';
    text = text.replace(/\s+/g, ' ').trim();
    if (text.length > MAX_CONTEXT_LENGTH) {
      text = text.slice(0, MAX_CONTEXT_LENGTH);
    }
    return { title, url, content: text };
  }

  function ensureStyle() {
    const style = document.createElement('style');
    style.setAttribute('data-policy-assistant-style', 'true');
    style.textContent = `
      #pa-widget { position: fixed; bottom: 16px; right: 16px; z-index: 9999; font-family: 'Helvetica Neue', Arial, sans-serif; display: flex; flex-direction: column; align-items: flex-end; gap: 12px; }
      #pa-widget * { box-sizing: border-box; }
      .pa-launch { background: #0f766e; color: #fff; border: none; border-radius: 999px; padding: 12px 16px; font-weight: 600; box-shadow: 0 8px 24px rgba(0,0,0,0.15); cursor: pointer; display: flex; align-items: center; gap: 8px; transition: transform 120ms ease, box-shadow 120ms ease; }
      .pa-launch:hover { transform: translateY(-1px); box-shadow: 0 10px 28px rgba(0,0,0,0.18); }
      .pa-launch:focus-visible { outline: 3px solid #99f6e4; outline-offset: 2px; }
      .pa-panel { width: 360px; max-width: calc(100vw - 32px); max-height: calc(80vh); background: #fff; border-radius: 16px; box-shadow: 0 16px 48px rgba(0,0,0,0.2); overflow: hidden; display: none; flex-direction: column; }
      .pa-panel.open { display: block; }
      .pa-header { padding: 16px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: flex-start; }
      .pa-title { font-size: 18px; font-weight: 700; color: #0f172a; }
      .pa-subtitle { font-size: 13px; color: #475569; margin-top: 4px; }
      .pa-close { background: none; border: none; font-size: 18px; cursor: pointer; color: #64748b; padding: 4px; border-radius: 8px; }
      .pa-close:hover, .pa-close:focus-visible { color: #0f172a; outline: 2px solid #99f6e4; }
      .pa-body { padding: 16px; display: flex; flex-direction: column; gap: 16px; overflow-y: auto; max-height: calc(80vh - 70px); }
      .pa-section-title { font-size: 15px; font-weight: 700; margin: 0 0 8px 0; color: #0f172a; }
      .pa-note { font-size: 12px; color: #475569; margin: 0 0 8px 0; }
      .pa-form { display: grid; gap: 10px; }
      .pa-form[hidden], .pa-summary[hidden] { display: none; }
      .pa-field { display: flex; flex-direction: column; gap: 4px; }
      .pa-field label { font-size: 13px; color: #0f172a; font-weight: 600; }
      .pa-field input, .pa-field textarea { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 14px; font-family: inherit; background: #f8fafc; }
      .pa-field textarea { min-height: 96px; resize: vertical; }
      .pa-field input:focus-visible, .pa-field textarea:focus-visible { outline: 2px solid #99f6e4; outline-offset: 1px; border-color: #0ea5e9; background: #fff; }
      .pa-actions { display: flex; gap: 8px; justify-content: flex-end; }
      .pa-btn { border: none; border-radius: 10px; padding: 10px 14px; font-weight: 700; cursor: pointer; transition: transform 120ms ease, box-shadow 120ms ease; }
      .pa-btn.primary { background: #0f766e; color: #fff; box-shadow: 0 8px 18px rgba(15,118,110,0.25); }
      .pa-btn.secondary { background: #e2e8f0; color: #0f172a; }
      .pa-btn:disabled { opacity: 0.65; cursor: not-allowed; box-shadow: none; }
      .pa-btn:hover:not(:disabled) { transform: translateY(-1px); }
      .pa-copy-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 10px; background: #e2e8f0; color: #0f172a; border: none; border-radius: 10px; cursor: pointer; font-weight: 700; }
      .pa-copy-btn[hidden] { display: none !important; }
      .pa-copy-btn:hover:not(:disabled) { transform: translateY(-1px); }
      .pa-role-options { display: grid; gap: 8px; }
      .pa-role { border: 1px solid #cbd5e1; border-radius: 12px; padding: 10px; display: flex; align-items: flex-start; gap: 10px; cursor: pointer; background: #f8fafc; }
      .pa-role input { margin-top: 4px; }
      .pa-role strong { display: block; color: #0f172a; }
      .pa-role small { color: #475569; }
      .pa-role.active { border-color: #0f766e; background: #ecfeff; }
      .pa-summary { padding: 12px; background: #f1f5f9; border-radius: 12px; font-size: 13px; color: #0f172a; display: flex; justify-content: space-between; gap: 8px; align-items: center; }
      .pa-context { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; font-size: 13px; color: #0f172a; }
      .pa-context div { margin-bottom: 4px; }
      .pa-output { width: 100%; min-height: 160px; max-height: 260px; overflow: auto; border: 1px solid #cbd5e1; border-radius: 12px; padding: 12px; font-size: 13px; background: #0b1120; color: #e2e8f0; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }
      .pa-output.copied { border-color: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.3); }
      .pa-status { min-height: 18px; font-size: 12px; color: #0f172a; background: #ecfdf3; border: 1px solid #bbf7d0; border-radius: 10px; padding: 8px 10px; margin-top: 6px; display: none; }
      .pa-status.pa-error { background: #fef2f2; border-color: #fecdd3; color: #b91c1c; }
      .pa-status.pa-success { background: #ecfdf3; border-color: #bbf7d0; color: #065f46; }
      .pa-status.show { display: block; }
      .pa-error { color: #b91c1c; }
      .pa-success { color: #065f46; }
      .pa-hint { background: #0f172a; color: #e2e8f0; padding: 10px 12px; border-radius: 12px; box-shadow: 0 10px 24px rgba(0,0,0,0.2); font-size: 13px; max-width: 260px; text-align: left; display: none; }
      .pa-hint.show { display: block; }
      .pa-hint strong { display: block; color: #99f6e4; margin-bottom: 2px; }
      @media (max-width: 480px) { #pa-widget { right: 8px; bottom: 8px; } .pa-panel { width: 320px; max-height: calc(85vh); } .pa-body { max-height: calc(85vh - 70px); } }
    `;
    document.head.appendChild(style);
  }

  function buildWidget(ideaHint) {
    ensureStyle();

    const container = document.createElement('div');
    container.id = 'pa-widget';

    const hint = document.createElement('div');
    hint.className = 'pa-hint';
    const hintTitle = ideaHint ? ideaHint : 'this policy';
    hint.innerHTML = `<strong>Ready-to-use prompt</strong> This will pull context from: ${hintTitle}`;

    const launch = document.createElement('button');
    launch.className = 'pa-launch';
    launch.type = 'button';
    launch.setAttribute('aria-expanded', 'false');
    const hintText = ideaHint ? `Want more ideas on how to implement ${ideaHint}?` : 'Want more ideas on how to implement this policy?';
    launch.innerHTML = '<span aria-hidden="true">\u2699</span><span>Policy Assistant</span>';
    launch.title = hintText;
    launch.setAttribute('aria-label', hintText);

    const panel = document.createElement('div');
    panel.className = 'pa-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');
    panel.setAttribute('aria-label', 'Policy Assistant');

    const subtitle = ideaHint
      ? `I can help you craft AI-ready prompts for "${ideaHint}" in your community.`
      : 'I can help you craft AI-ready prompts to advance ideas like this in your community.';

    panel.innerHTML = `
      <div class="pa-header">
        <div>
          <div class="pa-title">Policy Assistant</div>
          <div class="pa-subtitle">${subtitle}</div>
        </div>
        <button class="pa-close" type="button" aria-label="Close Policy Assistant">\u00d7</button>
      </div>
      <div class="pa-body">
        <div id="pa-role-section" class="pa-section">
          <h2 class="pa-section-title">What is your goal?</h2>
          <div class="pa-role-options" role="radiogroup" aria-label="Select your goal">
            <label class="pa-role active" id="pa-role-activist"><input type="radio" name="pa-role" value="activist" checked /> <div><strong>Activist (Citizen)</strong><small>Draft a persuasive letter and campaign ideas.</small></div></label>
            <label class="pa-role" id="pa-role-pro"><input type="radio" name="pa-role" value="professional" /> <div><strong>Policy Professional (Government)</strong><small>Draft an internal starter policy brief and clarifying questions.</small></div></label>
          </div>
        </div>

        <div id="pa-citizen-section" class="pa-section">
          <h2 class="pa-section-title">Your details</h2>
          <div class="pa-field"><label for="pa-name">Name</label><input id="pa-name" name="pa-name" autocomplete="name" placeholder="Your first and last name" /></div>
          <div class="pa-field"><label for="pa-activist-level">Who are you writing to?</label><input id="pa-activist-level" name="pa-activist-level" placeholder="Example: City council, parks board, school district." /></div>
          <div class="pa-field"><label for="pa-motivation">Personal motivation</label><textarea id="pa-motivation" name="pa-motivation" placeholder="Example: My basement flooded last spring."></textarea></div>
        </div>

        <div id="pa-professional-section" class="pa-section" hidden>
          <h2 class="pa-section-title">Government context</h2>
          <div class="pa-field"><label for="pa-level">What level of government?</label><input id="pa-level" name="pa-level" placeholder="Example: City council, regional district, provincial ministry." /></div>
          <div class="pa-field"><label for="pa-barrier">What is your main barrier?</label><textarea id="pa-barrier" name="pa-barrier" placeholder="Example: Budget cuts reduced maintenance capacity."></textarea></div>
          <div class="pa-field"><label for="pa-samples">Sample policies to emulate (optional)</label><textarea id="pa-samples" name="pa-samples" placeholder="Example: Boston building emissions bylaw sections 3-5; C40 retrofit procurement guide."></textarea></div>
        </div>

        <div id="pa-profile-summary" class="pa-summary" hidden>
          <div>
            <div><strong id="pa-summary-name"></strong></div>
            <div id="pa-summary-location"></div>
          </div>
          <button type="button" class="pa-btn secondary" id="pa-edit-profile">Edit profile</button>
        </div>
        <form id="pa-profile-form" class="pa-form" novalidate hidden>
          <h2 class="pa-section-title">Your location</h2>
          <p class="pa-note">Stored only in your browser.</p>
          <div class="pa-field"><label for="pa-city">City</label><input id="pa-city" name="pa-city" autocomplete="address-level2" /></div>
          <div class="pa-field"><label for="pa-region">Province / State</label><input id="pa-region" name="pa-region" autocomplete="address-level1" /></div>
          <div class="pa-field"><label for="pa-country">Country</label><input id="pa-country" name="pa-country" autocomplete="country-name" /></div>
          <div class="pa-actions">
            <button type="button" class="pa-btn secondary" id="pa-cancel-profile">Cancel</button>
            <button type="button" class="pa-btn primary" id="pa-save-profile">Save</button>
          </div>
        </form>

        <div class="pa-section">
          <h2 class="pa-section-title">Page context</h2>
          <div class="pa-context">
            <div><strong id="pa-context-title"></strong></div>
            <div id="pa-context-url"></div>
            <div id="pa-context-length"></div>
          </div>
        </div>

        <div class="pa-section">
          <h2 class="pa-section-title">Your prompt</h2>
          <div class="pa-actions" style="justify-content: flex-end; margin-bottom: 8px;">
            <button type="button" class="pa-btn primary" id="pa-generate">Generate</button>
            <button type="button" class="pa-copy-btn" id="pa-copy-output" aria-label="Copy generated prompt" hidden>📋 Copy</button>
          </div>
          <textarea id="pa-output" class="pa-output" readonly aria-label="Generated prompt"></textarea>
        </div>

        <div id="pa-status" class="pa-status" role="status" aria-live="polite"></div>
      </div>
    `;

    container.appendChild(panel);
    container.appendChild(hint);
    container.appendChild(launch);
    document.body.appendChild(container);

    return { container, launch, panel, hint };
  }

  function setRole(role, elements) {
    state.role = role;
    if (!state.profile) state.profile = {};
    state.profile.role = role;
    saveProfile(state.profile);
    const isActivist = role === 'activist';
    elements.citizenSection.hidden = !isActivist;
    elements.professionalSection.hidden = isActivist;
    elements.roleActivist.classList.toggle('active', isActivist);
    elements.rolePro.classList.toggle('active', !isActivist);
    const activistInput = elements.roleActivist.querySelector('input');
    const proInput = elements.rolePro.querySelector('input');
    if (activistInput) activistInput.checked = isActivist;
    if (proInput) proInput.checked = !isActivist;
    // Clear generated prompt when switching roles to avoid cross-template carryover
    clearOutput(elements);
  }

  function updateContextDisplay(context, elements) {
    elements.contextTitle.textContent = context.title || 'Untitled page';
    elements.contextUrl.textContent = context.url || '';
    elements.contextLength.textContent = `Context length: ${context.content.length.toLocaleString()} characters`;
  }

  function fillProfileForm(profile, elements) {
    if (!profile) return;
    elements.name.value = profile.name || '';
    elements.city.value = profile.city || '';
    elements.region.value = profile.region || '';
    elements.country.value = profile.country || '';
  }

  function hydrateProfessionalFields(profile, elements) {
    if (!profile) return;
    if (profile.level) elements.level.value = profile.level;
    if (profile.barrier) elements.barrier.value = profile.barrier;
  }

  function hydrateActivistFields(profile, elements) {
    if (!profile) return;
    if (profile.target_level) elements.activistLevel.value = profile.target_level;
  }

  function showProfileSummary(profile, elements) {
    if (!profile || (!profile.city && !profile.region && !profile.country)) {
      elements.profileSummary.hidden = true;
      elements.profileForm.hidden = false;
      return;
    }
    // Show name only if it exists
    if (profile.name) {
      elements.summaryName.textContent = profile.name;
      elements.summaryName.style.display = 'block';
    } else {
      elements.summaryName.style.display = 'none';
    }
    const parts = [profile.city, profile.region, profile.country].filter(Boolean).join(', ');
    elements.summaryLocation.textContent = parts || 'Location not set';
    elements.profileSummary.hidden = false;
    elements.profileForm.hidden = true;
  }

  function showStatus(message, type, elements) {
    elements.status.textContent = message;
    elements.status.classList.remove('pa-error', 'pa-success');
    if (type === 'error') elements.status.classList.add('pa-error');
    if (type === 'success') elements.status.classList.add('pa-success');
    if (message) {
      elements.status.classList.add('show');
    } else {
      elements.status.classList.remove('show');
    }
  }

  function copyToClipboard(text, elements) {
    if (!navigator.clipboard) {
      try {
        const temp = document.createElement('textarea');
        temp.value = text;
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
        showStatus('Prompt generated and ready to be pasted into your AI.', 'success', elements);
        highlightOutput(elements);
      } catch (err) {
        showStatus('Unable to copy automatically. Please copy manually.', 'error', elements);
      }
      return;
    }
    navigator.clipboard.writeText(text).then(() => {
      showStatus('Prompt generated and ready to be pasted into your AI.', 'success', elements);
      highlightOutput(elements);
    }).catch(() => {
      showStatus('Unable to copy automatically. Please copy manually.', 'error', elements);
    });
  }

  function highlightOutput(elements) {
    if (elements.output) {
      elements.output.classList.add('copied');
      setTimeout(() => {
        elements.output.classList.remove('copied');
      }, 2000);
    }
  }

  function updateCopyVisibility(elements) {
    const hasText = !!elements.output.value && elements.output.value.trim().length > 0;
    elements.copyOutput.hidden = !hasText;
  }

  function clearOutput(elements) {
    elements.output.value = '';
    elements.copyOutput.hidden = true;
    updateCopyVisibility(elements);
  }

  function init() {
    state.profile = loadProfile();
    if (state.profile && state.profile.role) {
      state.role = state.profile.role;
    }
    let context = scrapeContext();
    const { container, launch, panel } = buildWidget(context.title);

    const elements = {
      panel,
      launch,
      roleActivist: panel.querySelector('#pa-role-activist'),
      rolePro: panel.querySelector('#pa-role-pro'),
      citizenSection: panel.querySelector('#pa-citizen-section'),
      professionalSection: panel.querySelector('#pa-professional-section'),
      name: panel.querySelector('#pa-name'),
      motivation: panel.querySelector('#pa-motivation'),
      activistLevel: panel.querySelector('#pa-activist-level'),
      level: panel.querySelector('#pa-level'),
      barrier: panel.querySelector('#pa-barrier'),
      samples: panel.querySelector('#pa-samples'),
      profileForm: panel.querySelector('#pa-profile-form'),
      profileSummary: panel.querySelector('#pa-profile-summary'),
      summaryName: panel.querySelector('#pa-summary-name'),
      summaryLocation: panel.querySelector('#pa-summary-location'),
      editProfile: panel.querySelector('#pa-edit-profile'),
      cancelProfile: panel.querySelector('#pa-cancel-profile'),
      saveProfile: panel.querySelector('#pa-save-profile'),
      city: panel.querySelector('#pa-city'),
      region: panel.querySelector('#pa-region'),
      country: panel.querySelector('#pa-country'),
      contextTitle: panel.querySelector('#pa-context-title'),
      contextUrl: panel.querySelector('#pa-context-url'),
      contextLength: panel.querySelector('#pa-context-length'),
      generate: panel.querySelector('#pa-generate'),
      output: panel.querySelector('#pa-output'),
      copyOutput: panel.querySelector('#pa-copy-output'),
      status: panel.querySelector('#pa-status'),
      close: panel.querySelector('.pa-close'),
    };

    context = scrapeContext();
    updateContextDisplay(context, elements);
    setRole(state.role, elements);
    hydrateProfessionalFields(state.profile, elements);
    hydrateActivistFields(state.profile, elements);
    // Ensure a clean slate on load so stale text never keeps the copy button visible
    elements.output.value = '';
    elements.copyOutput.hidden = true;
    updateCopyVisibility(elements);
    
    // Display profile UI: show summary if profile exists, otherwise show form
    showProfileSummary(state.profile, elements);
    
    // Auto-detect location on load if no profile yet
    if (!state.profile || !state.profile.city) {
      getGeolocation().then((geo) => {
        if (geo && (!state.profile || !state.profile.city)) {
          if (!state.profile) state.profile = {};
          state.profile.city = geo.city;
          state.profile.region = geo.region;
          state.profile.country = geo.country;
          saveProfile(state.profile);
          showProfileSummary(state.profile, elements);
        }
      });
    }

    function openPanel() {
      panel.classList.add('open');
      launch.setAttribute('aria-expanded', 'true');
      const roleInput = panel.querySelector('input[name="pa-role"]:checked');
      if (roleInput) roleInput.focus();
    }

    function closePanel() {
      panel.classList.remove('open');
      launch.setAttribute('aria-expanded', 'false');
      launch.focus();
    }

    launch.addEventListener('click', () => {
      if (panel.classList.contains('open')) {
        closePanel();
      } else {
        updateCopyVisibility(elements);
        openPanel();
      }
    });

    launch.addEventListener('mouseenter', () => {
      const hint = container.querySelector('.pa-hint');
      if (hint) hint.classList.add('show');
    });

    launch.addEventListener('mouseleave', () => {
      const hint = container.querySelector('.pa-hint');
      if (hint) hint.classList.remove('show');
    });

    launch.addEventListener('focus', () => {
      const hint = container.querySelector('.pa-hint');
      if (hint) hint.classList.add('show');
    });

    launch.addEventListener('blur', () => {
      const hint = container.querySelector('.pa-hint');
      if (hint) hint.classList.remove('show');
    });

    elements.close.addEventListener('click', closePanel);

    elements.editProfile.addEventListener('click', () => {
      if (!state.profile) state.profile = {};
      elements.city.value = state.profile.city || '';
      elements.region.value = state.profile.region || '';
      elements.country.value = state.profile.country || '';
      elements.profileForm.hidden = false;
      elements.profileSummary.hidden = true;
      elements.city.focus();
      updateCopyVisibility(elements);
    });

    elements.cancelProfile.addEventListener('click', () => {
      elements.profileForm.hidden = true;
      if (state.profile && (state.profile.city || state.profile.region || state.profile.country)) {
        elements.profileSummary.hidden = false;
      }
      updateCopyVisibility(elements);
    });

    elements.saveProfile.addEventListener('click', () => {
      if (!state.profile) state.profile = {};
      state.profile.city = elements.city.value.trim();
      state.profile.region = elements.region.value.trim();
      state.profile.country = elements.country.value.trim();
      saveProfile(state.profile);
      elements.profileForm.hidden = true;
      showProfileSummary(state.profile, elements);
      showStatus('✓ Location saved.', 'success', elements);
      setTimeout(() => {
        showStatus('', null, elements);
      }, 3000);
    });

    panel.querySelectorAll('input[name="pa-role"]').forEach((input) => {
      input.addEventListener('change', (event) => {
        const role = event.target.value === 'professional' ? 'professional' : 'activist';
        setRole(role, elements);
      });
    });

    elements.generate.addEventListener('click', () => {
      const isActivist = state.role === 'activist';
      const motivation = elements.motivation.value.trim();
      const activistLevel = elements.activistLevel.value.trim();
      const level = elements.level.value.trim();
      const barrier = elements.barrier.value.trim();
      const samples = elements.samples.value.trim();
      const name = elements.name.value.trim();

      if (isActivist) {
        if (!motivation) {
          showStatus('Please add your personal motivation.', 'error', elements);
          elements.motivation.focus();
          return;
        }
        if (!activistLevel) {
          showStatus('Who are you writing to? Add the target level of government.', 'error', elements);
          elements.activistLevel.focus();
          return;
        }
      } else {
        if (!level) {
          showStatus('Please note the level of government.', 'error', elements);
          elements.level.focus();
          return;
        }
        if (!barrier) {
          showStatus('Please describe your implementation barriers.', 'error', elements);
          elements.barrier.focus();
          return;
        }
      }

      let prompt = '';
      const city = (state.profile && state.profile.city) || '';
      const region = (state.profile && state.profile.region) || '';
      const country = (state.profile && state.profile.country) || '';

      // Persist activist target level so it follows the user between policies
      if (!state.profile) state.profile = {};
      if (activistLevel) state.profile.target_level = activistLevel;
      saveProfile(state.profile);
      hydrateActivistFields(state.profile, elements);

      // Persist professional context so it follows the user between policies
      state.profile.level = level;
      state.profile.barrier = barrier;
      saveProfile(state.profile);
      hydrateProfessionalFields(state.profile, elements);

      if (isActivist) {
        const location = [city, region].filter(Boolean).join(', ') || 'my community';
        const targetLevel = activistLevel || 'local decision makers';
        const nameLine = name ? `My name is ${name}.` : 'I am a resident and constituent.';
        prompt = `Please review this new prompt for a fresh start with your AI assistant. Do not blend this with previous prompts.

---
      Act as a concerned citizen and expert lobbyist. You have written many letters that effectively shifted policy in your community and know how to write a convincing argument.

      Writer context:
      - ${nameLine}
      - Location: ${location}
      - Target audience: ${targetLevel}
      - Policy: ${context.title} (Source: ${context.url})
      - Personal motivation: ${motivation}
      - Reference text: ${context.content}

      Please draft:
      1) A concise, evidence-minded letter to ${targetLevel} urging action, tailored to ${location}.
      2) 3 practical follow-up actions (e.g., public comment, meeting ask, coalition outreach) with rationale.
      Keep the tone constructive and specific to ${location}.`;
      } else {
        const location = [city, country].filter(Boolean).join(', ') || 'my jurisdiction';
        const sampleText = samples || 'No sample policies provided. Suggest suitable analogs.';
        const bilingualCue = city && city.toLowerCase() === 'ottawa' ? 'Ask if bilingual (English/French) output is required for Ottawa.' : 'Ask if bilingual (English/French) output is required when the jurisdiction expects it.';
        const languageCue = country && country.toLowerCase() === 'canada' ? 'Use Canadian English by default.' : 'Match local terminology and spelling for the provided country.';
        prompt = `Please review this new prompt for a fresh start with your AI assistant. Do not blend this with previous prompts.

---

Act as a Policy Learning Partner for ${level} government in ${location}.

CONTEXT
-------
Audience: internal policy professionals developing a draft policy outline for internal circulation (not yet a finalized bill).
Language: ${languageCue}
Bilingual: ${bilingualCue}

POLICY IDEA
-----------
Title: ${context.title}
Source: ${context.url}
Reference text: ${context.content}

IMPLEMENTATION CHALLENGE
------------------------
Barrier: ${barrier}

REFERENCE POLICIES
------------------
Sample policies to study: ${sampleText}

TASK
----
STEP 1: Provide a brief **issue snapshot** for ${location} covering:
  • Why this issue matters locally (health, fiscal, environmental, or operational impact in this jurisdiction)
  • What related policies or programs already exist in ${location}
  • Key stakeholders or departments who will be affected
  • Realistic timelines and budget considerations for ${level}

STEP 2: Ask 5–7 tailored clarifying questions covering:
  • Statutory authority and enabling legislation in ${location}
  • Required legislative instrument format
  • Stakeholder consultation or approval gates
  • Bilingual publication needs
  • Fiscal note and cost-benefit expectations
  • Which sample clauses or approaches fit this jurisdiction best

STEP 3: Propose a starter outline with decision points and a next-step checklist.

IMPORTANT: Explicitly reference ${location} throughout your response and avoid generic outputs.`;
      }

      elements.output.value = prompt;
      // Copy the textarea content to ensure what's copied matches what's displayed
      const textToCopy = elements.output.value;
      copyToClipboard(textToCopy, elements);
      updateCopyVisibility(elements);
      // Keep the success message visible for 4 seconds
      setTimeout(() => {
        showStatus('', null, elements);
      }, 4000);
    });

    elements.copyOutput.addEventListener('click', () => {
      const prompt = elements.output.value;
      if (!prompt) {
        showStatus('No prompt to copy yet.', 'error', elements);
        updateCopyVisibility(elements);
        return;
      }
      copyToClipboard(prompt, elements);
      setTimeout(() => {
        showStatus('', null, elements);
      }, 4000);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && panel.classList.contains('open')) {
        closePanel();
      }
    });
  }

  init();
})();
