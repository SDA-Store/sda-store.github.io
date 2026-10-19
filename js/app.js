/**
 * MASTER DESIGN SYSTEM SCRIPT
 * SDA Store - Application Logic & Interactive Micro-Physics
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
        obtainiumGuideCardBtn: document.getElementById('obtainiumGuideCardBtn'),
        obtainiumModal: document.getElementById('obtainiumModal'),
        obtainiumModalCloseBtn: document.getElementById('obtainiumModalCloseBtn'),
        obtainiumGotItBtn: document.getElementById('obtainiumGotItBtn')
    };

    /**
     * Initialize Application
     */
    async function init() {
        setupTheme();
        setupEventListeners();
        await loadAppsData();
    }

    /**
     * Theme Toggle System (Default: Light #fafafa Editorial Canvas)
     */
    function setupTheme() {
        const savedTheme = localStorage.getItem('sda_store_theme') || 'light';
        setTheme(savedTheme);

        if (DOM.themeToggleBtn) {
            DOM.themeToggleBtn.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme') || 'light';
                const next = current === 'dark' ? 'light' : 'dark';
                setTheme(next);
            });
        }
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('sda_store_theme', theme);

        if (DOM.themeIcon) {
            if (theme === 'dark') {
                DOM.themeIcon.className = 'fa-solid fa-sun';
            } else {
                DOM.themeIcon.className = 'fa-solid fa-moon';
            }
        }
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
            renderApps();
        } catch (err) {
            console.warn('Could not load data/apps.json via fetch:', err);
            if (DOM.appsGrid) {
                DOM.appsGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; background: var(--bg-card); border-radius: 24px; border: 1px solid var(--border-subtle);">
                        <i class="fa-solid fa-triangle-exclamation" style="font-size: 2rem; color: #f59e0b; margin-bottom: 1rem;"></i>
                        <h3 style="font-family: var(--font-sans); font-weight: 800; font-size: 1.25rem;">Data requires HTTP Server</h3>
                        <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.5rem;">To test locally, run <code>python -m http.server 8000</code> or access via GitHub Pages.</p>
                    </div>
                `;
            }
        }
    }

    /**
     * Render filtered and sorted apps grid with Master Cards
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
                : 'arm64';

            const displayPatches = (app.patches || []).slice(0, 3);
            const remainingPatches = Math.max(0, (app.patchCount || app.patches.length) - displayPatches.length);
            const obtainiumUrl = generateObtainiumUrl(app, targetAsset);

            // Flagship card accent (MovieBox gets emerald accent line)
            const isFlagship = app.id === 'moviebox';
            const topAccentClass = isFlagship ? 'card-top-accent-emerald' : 'card-top-accent';

            return `
                <article class="app-card" data-app-id="${escapeHtml(app.id)}">
                    <div class="${topAccentClass}"></div>
                    <div>
                        <div class="app-card-top">
                            <div class="app-icon-box">
                                <img class="app-icon-img" src="${escapeHtml(app.icon || '')}" alt="${escapeHtml(app.name)}" onerror="this.onerror=null;this.src='data:image/svg+xml,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 24 24\\' fill=\\'%230a0a0a\\'><circle cx=\\'12\\' cy=\\'12\\' r=\\'10\\'/></svg>';">
                            </div>
                            <div class="app-meta-box">
                                <span class="app-category-text">${escapeHtml(app.category || 'App')}</span>
                                <h3 class="app-name-title" title="${escapeHtml(app.name)}">${escapeHtml(app.name)}</h3>
                                <div class="app-badges-flex">
                                    <span class="chip-brand">${escapeHtml(app.brand || 'Morphe')}</span>
                                    <span class="chip-version">v${escapeHtml(app.version || 'latest')}</span>
                                    <span class="chip-arch">${escapeHtml(archLabel)}</span>
                                    ${isFlagship ? `<span class="chip-verified"><i class="fa-solid fa-check"></i> Verified</span>` : ''}
                                </div>
                            </div>
                        </div>

                        <p class="app-description-p">${escapeHtml(app.description || '')}</p>

                        <!-- Highlights Preview -->
                        <div class="patches-preview-wrap">
                            ${displayPatches.map(p => `<span class="patch-chip">${escapeHtml(p)}</span>`).join('')}
                            ${remainingPatches > 0 ? `<span class="patch-chip patch-chip-more" onclick="window.sdaStore.openPatchModal('${escapeHtml(app.id)}')">+${remainingPatches} more</span>` : ''}
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="app-action-grid">
                        <div class="action-row-buttons">
                            <a href="${escapeHtml(targetAsset?.downloadUrl || '#')}" 
                               class="btn btn-primary btn-apk-download" 
                               download="${escapeHtml(targetAsset?.name || 'app.apk')}"
                               target="_blank" rel="noopener">
                                <i class="fa-solid fa-download"></i>
                                <span>Download APK</span>
                            </a>
                            <a href="${escapeHtml(obtainiumUrl)}" 
                               class="btn-obtainium-ghost" 
                               title="Install or sync automated updates in Obtainium"
                               target="_blank" rel="noopener">
                                <i class="fa-solid fa-link"></i>
                                <span>Obtainium</span>
                            </a>
                        </div>
                        <div class="action-row-meta">
                            <button class="btn-text-patches" onclick="window.sdaStore.openPatchModal('${escapeHtml(app.id)}')">
                                <i class="fa-solid fa-list-check"></i>
                                <span>View all ${app.patchCount || app.patches.length} patches</span>
                            </button>
                            <span>${escapeHtml(fileSizeMB)}</span>
                        </div>
                    </div>
                </article>
            `;
        }).join('');
    }

    /**
     * Choose best APK asset
     */
    function pickBestAsset(app, requestedArch) {
        if (!app.assets || app.assets.length === 0) return null;

        if (requestedArch !== 'all') {
            const exactMatch = app.assets.find(a => a.arch === requestedArch);
            if (exactMatch) return exactMatch;
        }

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
            if (currentCategory !== 'all' && app.category !== currentCategory) {
                return false;
            }

            if (currentArch !== 'all') {
                const hasArch = (app.assets || []).some(a => a.arch === currentArch || a.arch === 'universal');
                if (!hasArch) return false;
            }

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
            DOM.modalPatchesList.innerHTML = `<li class="detailed-patch-item" style="color: var(--text-eyebrow); justify-content: center;">No patches matching "${escapeHtml(q)}"</li>`;
            return;
        }

        DOM.modalPatchesList.innerHTML = filtered.map(p => `
            <li class="detailed-patch-item">
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

        // Keyboard Shortcut: '/' focuses search input
        window.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== DOM.searchInput && document.activeElement.tagName !== 'INPUT') {
                e.preventDefault();
                DOM.searchInput.focus();
            }
            if (e.key === 'Escape') {
                closePatchModal();
                DOM.obtainiumModal.classList.add('hidden');
                document.body.style.overflow = '';
            }
        });

        // Category Pills
        DOM.categoryPills.addEventListener('click', (e) => {
            const pill = e.target.closest('.category-pill');
            if (!pill) return;

            DOM.categoryPills.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
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

            DOM.categoryPills.querySelectorAll('.category-pill').forEach(p => {
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

        // Obtainium Guide Modals
        const openObtainium = () => {
            DOM.obtainiumModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        };

        DOM.obtainiumGuideBtn.addEventListener('click', openObtainium);
        if (DOM.obtainiumGuideCardBtn) {
            DOM.obtainiumGuideCardBtn.addEventListener('click', openObtainium);
        }

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
    }

    /**
     * Show Toast Notification Pill
     */
    function showToast(message) {
        DOM.toastMsg.textContent = message;
        DOM.toast.classList.add('show');
        setTimeout(() => {
            DOM.toast.classList.remove('show');
        }, 2600);
    }

    /**
     * Helpers
     */
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Expose for inline handlers
    window.sdaStore = {
        openPatchModal
    };

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
