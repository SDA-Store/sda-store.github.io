/**
 * SDA Store - Application Logic
 * Fast, reactive catalog for patched Android APKs
 */

(() => {
    'use strict';

    // State
    let appsData = [];
    let currentCategory = 'all';
    let currentArch = 'all';
    let currentSort = 'name';
    let searchQuery = '';
    let activeModalApp = null;

    // DOM Elements
    const DOM = {
        appsGrid: document.getElementById('appsGrid'),
        noResults: document.getElementById('noResults'),
        searchInput: document.getElementById('searchInput'),
        searchClearBtn: document.getElementById('searchClearBtn'),
        categoryPills: document.getElementById('categoryPills'),
        archFilter: document.getElementById('archFilter'),
        sortFilter: document.getElementById('sortFilter'),
        resetFiltersBtn: document.getElementById('resetFiltersBtn'),
        totalAppsCount: document.getElementById('totalAppsCount'),
        totalPatchesCount: document.getElementById('totalPatchesCount'),
        themeToggleBtn: document.getElementById('themeToggleBtn'),
        themeIcon: document.getElementById('themeIcon'),
        toast: document.getElementById('toast'),
        toastMsg: document.getElementById('toastMsg'),

        // Patch Modal
        patchModal: document.getElementById('patchModal'),
        modalAppIcon: document.getElementById('modalAppIcon'),
        modalAppName: document.getElementById('modalAppName'),
        modalAppVersion: document.getElementById('modalAppVersion'),
        modalAppBrand: document.getElementById('modalAppBrand'),
        modalPatchCount: document.getElementById('modalPatchCount'),
        modalPatchesList: document.getElementById('modalPatchesList'),
        patchSearchInput: document.getElementById('patchSearchInput'),
        modalCloseBtn: document.getElementById('modalCloseBtn'),
        modalDirectDownloadBtn: document.getElementById('modalDirectDownloadBtn'),
        copyPatchesBtn: document.getElementById('copyPatchesBtn'),

        // Obtainium Guide Modal
        obtainiumGuideBtn: document.getElementById('obtainiumGuideBtn'),
        obtainiumModal: document.getElementById('obtainiumModal'),
        obtainiumModalCloseBtn: document.getElementById('obtainiumModalCloseBtn'),
        obtainiumGotItBtn: document.getElementById('obtainiumGotItBtn')
    };

    /**
     * Initialize Store Application
     */
    async function init() {
        setupTheme();
        setupEventListeners();
        await loadAppsData();
    }

    /**
     * Load Apps Data from local data/apps.json
     */
    async function loadAppsData() {
        try {
            const response = await fetch('data/apps.json');
            if (!response.ok) throw new Error('Network error');
            const data = await response.json();
            appsData = data.apps || [];
            updateStats();
            renderApps();
        } catch (err) {
            console.warn('Could not load data/apps.json via fetch, trying fallback:', err);
            // If running via direct file:// without server, fallback to default state
            DOM.appsGrid.innerHTML = `
                <div class="no-results" style="grid-column: 1 / -1;">
                    <i class="fa-solid fa-triangle-exclamation" style="font-size: 2.5rem; color: #f59e0b; margin-bottom: 1rem;"></i>
                    <h3>Data file requires HTTP server</h3>
                    <p>To view apps when running locally, start a local server like <code>python -m http.server 8000</code> or deploy to GitHub Pages.</p>
                </div>
            `;
        }
    }

    /**
     * Compute and render global stats
     */
    function updateStats() {
        if (!appsData.length) return;
        const totalApps = appsData.length;
        const totalPatches = appsData.reduce((acc, app) => acc + (app.patchCount || 0), 0);

        animateNumber(DOM.totalAppsCount, totalApps);
        animateNumber(DOM.totalPatchesCount, totalPatches);
    }

    function animateNumber(element, target) {
        if (!element) return;
        let start = 0;
        const duration = 1200;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(easeOut * target);
            element.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = target.toLocaleString();
            }
        }
        requestAnimationFrame(update);
    }

    /**
     * Render filtered and sorted apps grid
     */
    function renderApps() {
        const filtered = getFilteredApps();

        if (filtered.length === 0) {
            DOM.appsGrid.innerHTML = '';
            DOM.noResults.classList.remove('hidden');
            return;
        }

        DOM.noResults.classList.add('hidden');

        DOM.appsGrid.innerHTML = filtered.map(app => {
            const targetAsset = pickBestAsset(app, currentArch);
            const fileSizeMB = targetAsset && targetAsset.size 
                ? (targetAsset.size / (1024 * 1024)).toFixed(1) + ' MB' 
                : 'Direct APK';
            const archLabel = targetAsset && targetAsset.arch 
                ? (targetAsset.arch === 'arm64' ? 'arm64-v8a' : (targetAsset.arch === 'arm' ? 'arm-v7a' : targetAsset.arch)) 
                : 'APK';

            const displayPatches = (app.patches || []).slice(0, 3);
            const remainingPatches = Math.max(0, (app.patchCount || app.patches.length) - displayPatches.length);

            // Obtainium link config
            const obtainiumUrl = generateObtainiumUrl(app, targetAsset);

            return `
                <article class="app-card" data-app-id="${escapeHtml(app.id)}">
                    <div>
                        <div class="app-card-header">
                            <img class="app-icon" src="${escapeHtml(app.icon || '')}" alt="${escapeHtml(app.name)}" onerror="this.onerror=null;this.src='data:image/svg+xml,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 24 24\\' fill=\\'%236366f1\\'><circle cx=\\'12\\' cy=\\'12\\' r=\\'10\\'/></svg>';">
                            <div class="app-meta">
                                <div class="app-title-row">
                                    <h3 class="app-name" title="${escapeHtml(app.name)}">${escapeHtml(app.name)}</h3>
                                </div>
                                <span class="app-category">${escapeHtml(app.category || 'App')}</span>
                                <div class="app-badges-row">
                                    <span class="badge badge-brand">${escapeHtml(app.brand || 'Morphe')}</span>
                                    <span class="badge badge-subtle">v${escapeHtml(app.version || 'latest')}</span>
                                    <span class="badge badge-arch">${escapeHtml(archLabel)}</span>
                                </div>
                            </div>
                        </div>

                        <p class="app-desc">${escapeHtml(app.description || '')}</p>

                        <!-- Highlights -->
                        <div class="app-patches-preview">
                            ${displayPatches.map(p => `<span class="patch-tag">${escapeHtml(p)}</span>`).join('')}
                            ${remainingPatches > 0 ? `<span class="patch-tag more-tag" onclick="window.sdaStore.openPatchModal('${escapeHtml(app.id)}')">+${remainingPatches} more</span>` : ''}
                        </div>
                    </div>

                    <div class="app-card-actions">
                        <div class="action-row-primary">
                            <a href="${escapeHtml(targetAsset?.downloadUrl || '#')}" 
                               class="btn btn-primary btn-download" 
                               download="${escapeHtml(targetAsset?.name || 'app.apk')}"
                               target="_blank" rel="noopener">
                                <i class="fa-solid fa-download"></i>
                                <span>Download APK</span>
                            </a>
                            <a href="${escapeHtml(obtainiumUrl)}" 
                               class="btn btn-obtainium" 
                               title="Install or track automated updates in Obtainium"
                               target="_blank" rel="noopener">
                                <i class="fa-solid fa-link"></i>
                                <span>Obtainium</span>
                            </a>
                        </div>
                        <div class="action-row-secondary">
                            <button class="view-patches-btn" onclick="window.sdaStore.openPatchModal('${escapeHtml(app.id)}')">
                                <i class="fa-solid fa-list-check"></i>
                                <span>View all ${app.patchCount || app.patches.length} patches</span>
                            </button>
                            <span class="file-size-text">${escapeHtml(fileSizeMB)}</span>
                        </div>
                    </div>
                </article>
            `;
        }).join('');
    }

    /**
     * Choose the best APK asset based on requested architecture
     */
    function pickBestAsset(app, requestedArch) {
        if (!app.assets || app.assets.length === 0) return null;

        if (requestedArch !== 'all') {
            const exactMatch = app.assets.find(a => a.arch === requestedArch);
            if (exactMatch) return exactMatch;
        }

        // Default preference: arm64 -> universal -> arm -> first available
        return app.assets.find(a => a.arch === 'arm64') ||
               app.assets.find(a => a.arch === 'universal') ||
               app.assets.find(a => a.arch === 'arm') ||
               app.assets[0];
    }

    /**
     * Filter & Sort logic
     */
    function getFilteredApps() {
        return appsData.filter(app => {
            // Category filter
            if (currentCategory !== 'all' && app.category !== currentCategory) {
                return false;
            }

            // Architecture filter
            if (currentArch !== 'all') {
                const hasArch = (app.assets || []).some(a => a.arch === currentArch || a.arch === 'universal');
                if (!hasArch) return false;
            }

            // Search query filter
            if (searchQuery.trim() !== '') {
                const q = searchQuery.toLowerCase();
                const matchName = (app.name || '').toLowerCase().includes(q);
                const matchBrand = (app.brand || '').toLowerCase().includes(q);
                const matchCategory = (app.category || '').toLowerCase().includes(q);
                const matchDesc = (app.description || '').toLowerCase().includes(q);
                const matchPatch = (app.patches || []).some(p => p.toLowerCase().includes(q));

                if (!matchName && !matchBrand && !matchCategory && !matchDesc && !matchPatch) {
                    return false;
                }
            }

            return true;
        }).sort((a, b) => {
            if (currentSort === 'name') {
                return a.name.localeCompare(b.name);
            }
            if (currentSort === 'patches') {
                return (b.patchCount || 0) - (a.patchCount || 0);
            }
            if (currentSort === 'updated') {
                return new Date(b.publishedAt || 0) - new Date(a.publishedAt || 0);
            }
            return 0;
        });
    }

    /**
     * Generate an Obtainium 1-Click Redirect URL
     */
    function generateObtainiumUrl(app, targetAsset) {
        const releaseUrl = app.releaseUrl || 'https://github.com/sudarsanSDA/SDA-Store';
        // Match regex for this specific APK filename
        const filterRegex = targetAsset ? `^${escapeRegex(targetAsset.name)}$` : `^${escapeRegex(app.id)}.*\\.apk$`;
        
        const obtainiumConfig = {
            id: app.id,
            name: `${app.name} (${app.brand || 'Morphe'})`,
            url: releaseUrl,
            author: 'sudarsanSDA',
            additionalSettings: JSON.stringify({
                apkFilterRegEx: filterRegex
            })
        };

        const uriScheme = `obtainium://app/${JSON.stringify(obtainiumConfig)}`;
        return `https://apps.obtainium.imranr.dev/redirect?r=${encodeURIComponent(uriScheme)}`;
    }

    /**
     * Open Patch Details Modal
     */
    function openPatchModal(appId) {
        const app = appsData.find(a => a.id === appId);
        if (!app) return;

        activeModalApp = app;
        const targetAsset = pickBestAsset(app, currentArch);

        DOM.modalAppIcon.src = app.icon || '';
        DOM.modalAppName.textContent = app.name;
        DOM.modalAppVersion.textContent = `v${app.version || 'latest'}`;
        DOM.modalAppBrand.textContent = app.brand || 'Morphe';
        DOM.modalPatchCount.textContent = `${app.patchCount || (app.patches || []).length} Patches Applied`;
        DOM.modalDirectDownloadBtn.href = targetAsset ? targetAsset.downloadUrl : '#';
        DOM.modalDirectDownloadBtn.setAttribute('download', targetAsset ? targetAsset.name : 'app.apk');

        DOM.patchSearchInput.value = '';
        renderModalPatchList(app.patches || []);

        DOM.patchModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closePatchModal() {
        DOM.patchModal.classList.add('hidden');
        document.body.style.overflow = '';
        activeModalApp = null;
    }

    function renderModalPatchList(patches) {
        const q = DOM.patchSearchInput.value.toLowerCase().trim();
        const filtered = q ? patches.filter(p => p.toLowerCase().includes(q)) : patches;

        if (filtered.length === 0) {
            DOM.modalPatchesList.innerHTML = `<li class="patch-item" style="color: var(--text-muted); justify-content: center;">No patches matching "${escapeHtml(q)}"</li>`;
            return;
        }

        DOM.modalPatchesList.innerHTML = filtered.map(p => `
            <li class="patch-item">
                <i class="fa-solid fa-check"></i>
                <span>${escapeHtml(p)}</span>
            </li>
        `).join('');
    }

    /**
     * Copy Patches List to Clipboard
     */
    function copyPatchesToClipboard() {
        if (!activeModalApp || !activeModalApp.patches) return;
        const text = `${activeModalApp.name} (v${activeModalApp.version}) - Applied Patches:\n\n` + 
            activeModalApp.patches.map(p => `- ${p}`).join('\n');

        navigator.clipboard.writeText(text).then(() => {
            showToast('Patch list copied to clipboard!');
        }).catch(() => {
            showToast('Failed to copy');
        });
    }

    /**
     * Setup Event Listeners
     */
    function setupEventListeners() {
        // Search Input
        DOM.searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value;
            DOM.searchClearBtn.classList.toggle('hidden', searchQuery.trim() === '');
            renderApps();
        });

        DOM.searchClearBtn.addEventListener('click', () => {
            DOM.searchInput.value = '';
            searchQuery = '';
            DOM.searchClearBtn.classList.add('hidden');
            DOM.searchInput.focus();
            renderApps();
        });

        // Category Pills
        DOM.categoryPills.addEventListener('click', (e) => {
            const pill = e.target.closest('.pill');
            if (!pill) return;

            DOM.categoryPills.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            currentCategory = pill.dataset.category || 'all';
            renderApps();
        });

        // Architecture Filter
        DOM.archFilter.addEventListener('change', (e) => {
            currentArch = e.target.value;
            renderApps();
        });

        // Sort Filter
        DOM.sortFilter.addEventListener('change', (e) => {
            currentSort = e.target.value;
            renderApps();
        });

        // Reset Filters Button
        DOM.resetFiltersBtn.addEventListener('click', () => {
            DOM.searchInput.value = '';
            searchQuery = '';
            DOM.searchClearBtn.classList.add('hidden');
            currentCategory = 'all';
            currentArch = 'all';
            currentSort = 'name';

            DOM.categoryPills.querySelectorAll('.pill').forEach(p => {
                p.classList.toggle('active', p.dataset.category === 'all');
            });
            DOM.archFilter.value = 'all';
            DOM.sortFilter.value = 'name';

            renderApps();
        });

        // Modal Search
        DOM.patchSearchInput.addEventListener('input', () => {
            if (activeModalApp) {
                renderModalPatchList(activeModalApp.patches || []);
            }
        });

        // Modal Close Buttons
        DOM.modalCloseBtn.addEventListener('click', closePatchModal);
        DOM.patchModal.addEventListener('click', (e) => {
            if (e.target === DOM.patchModal) closePatchModal();
        });

        DOM.copyPatchesBtn.addEventListener('click', copyPatchesToClipboard);

        // Obtainium Guide Modal
        DOM.obtainiumGuideBtn.addEventListener('click', () => {
            DOM.obtainiumModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        });

        DOM.obtainiumModalCloseBtn.addEventListener('click', () => {
            DOM.obtainiumModal.classList.add('hidden');
            document.body.style.overflow = '';
        });

        DOM.obtainiumGotItBtn.addEventListener('click', () => {
            DOM.obtainiumModal.classList.add('hidden');
            document.body.style.overflow = '';
        });

        DOM.obtainiumModal.addEventListener('click', (e) => {
            if (e.target === DOM.obtainiumModal) {
                DOM.obtainiumModal.classList.add('hidden');
                document.body.style.overflow = '';
            }
        });

        // Keyboard Shortcuts
        document.addEventListener('keydown', (e) => {
            // Escape to close modals
            if (e.key === 'Escape') {
                closePatchModal();
                DOM.obtainiumModal.classList.add('hidden');
                document.body.style.overflow = '';
            }

            // '/' key to focus search if not in an input
            if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
                e.preventDefault();
                DOM.searchInput.focus();
            }
        });
    }

    /**
     * Theme Toggle (Dark / Light)
     */
    function setupTheme() {
        const savedTheme = localStorage.getItem('sda-store-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);

        DOM.themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('sda-store-theme', next);
            updateThemeIcon(next);
        });
    }

    function updateThemeIcon(theme) {
        if (!DOM.themeIcon) return;
        if (theme === 'dark') {
            DOM.themeIcon.className = 'fa-solid fa-moon';
        } else {
            DOM.themeIcon.className = 'fa-solid fa-sun';
        }
    }

    /**
     * Toast Notification Helper
     */
    let toastTimeout = null;
    function showToast(message) {
        if (!DOM.toast) return;
        DOM.toastMsg.textContent = message;
        DOM.toast.classList.remove('hidden');

        if (toastTimeout) clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            DOM.toast.classList.add('hidden');
        }, 2500);
    }

    /**
     * String utilities
     */
    function escapeHtml(str) {
        if (typeof str !== 'string') return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function escapeRegex(str) {
        return (str || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Expose global controller
    window.sdaStore = {
        openPatchModal
    };

    // Run
    document.addEventListener('DOMContentLoaded', init);
})();
