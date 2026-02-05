/**
 * AI Storage Saver - Frontend Logic
 */

// State
let currentMode = 'fast';
let selectedModel = '';
let scannedFiles = [];
let displayedFiles = [];
let selectedFile = null;
let currentSort = 'size-desc';
let isScanning = false;
let abortController = null;
let showSafeOnly = false;  // Safe to delete filter

// DOM Elements
const modelSelect = document.getElementById('modelSelect');
const toggleBtns = document.querySelectorAll('.toggle-btn');
const pathGroup = document.getElementById('pathGroup');
const pathInput = document.getElementById('pathInput');
const excludeSystem = document.getElementById('excludeSystem');
const scanBtn = document.getElementById('scanBtn');
const statsPanel = document.getElementById('statsPanel');
const fileCount = document.getElementById('fileCount');
const totalSize = document.getElementById('totalSize');
const statusText = document.getElementById('statusText');
const fileGrid = document.getElementById('fileGrid');
const emptyState = document.getElementById('emptyState');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const detailPanel = document.getElementById('detailPanel');
const closePanel = document.getElementById('closePanel');
const panelContent = document.getElementById('panelContent');
const sortControl = document.getElementById('sortControl');
const sortSelect = document.getElementById('sortSelect');
const filterControl = document.getElementById('filterControl');
const safeFilterBtn = document.getElementById('safeFilterBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadModels();
    setupEventListeners();
});

// Load available Ollama models
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();

        modelSelect.innerHTML = '';

        if (data.models && data.models.length > 0) {
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.name;
                option.textContent = model.name;
                modelSelect.appendChild(option);
            });
            selectedModel = data.models[0].name;
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No models available';
            modelSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Failed to load models:', error);
        modelSelect.innerHTML = '<option value="">Error loading models</option>';
    }
}

// Setup event listeners
function setupEventListeners() {
    // Model selection
    modelSelect.addEventListener('change', (e) => {
        selectedModel = e.target.value;
    });

    // Scan mode toggle
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;
            pathGroup.style.display = currentMode === 'advance' ? 'flex' : 'none';
        });
    });

    // Scan button
    scanBtn.addEventListener('click', startScan);

    // Sort selection
    sortSelect.addEventListener('change', (e) => {
        currentSort = e.target.value;
        sortAndRenderFiles();
    });

    // Safe filter toggle
    safeFilterBtn.addEventListener('click', () => {
        showSafeOnly = !showSafeOnly;
        safeFilterBtn.classList.toggle('active', showSafeOnly);
        sortAndRenderFiles();
    });

    // Close detail panel
    closePanel.addEventListener('click', () => {
        detailPanel.classList.remove('open');
        selectedFile = null;
    });
}

// Start file scan
async function startScan() {
    // Prevent multiple scans
    if (isScanning) {
        return;
    }

    isScanning = true;

    // Determine path text for loading message
    let pathText = 'Downloads, Desktop, Documents...';
    if (currentMode === 'advance' && pathInput.value) {
        pathText = pathInput.value;
    } else if (currentMode === 'advance') {
        pathText = 'User Home Directory';
    }

    showLoading(`Scanning: ${pathText}`);

    // Clear previous results immediately for better UX
    scannedFiles = [];
    displayedFiles = [];
    fileGrid.innerHTML = '';

    try {
        let url = `/api/scan?mode=${currentMode}`;
        if (currentMode === 'advance' && pathInput.value) {
            url += `&path=${encodeURIComponent(pathInput.value)}`;
        }
        if (excludeSystem.checked) {
            url += '&exclude_system=true';
        }

        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
            scannedFiles = data.files;
            updateStats(data.file_count, data.total_size);
            sortAndRenderFiles();
            statusText.textContent = `Found ${data.file_count} large files in ${data.path}`;
            sortControl.style.display = 'flex';
            filterControl.style.display = 'flex';
        } else {
            throw new Error(data.detail || 'Scan failed');
        }
    } catch (error) {
        console.error('Scan error:', error);
        statusText.textContent = `Error: ${error.message}`;
        renderEmptyState();
    } finally {
        isScanning = false;
        hideLoading();
    }
}

// Sort and render files
function sortAndRenderFiles() {
    if (scannedFiles.length === 0) {
        renderEmptyState();
        return;
    }

    // Clone array for sorting
    displayedFiles = [...scannedFiles];

    // Apply safe filter
    if (showSafeOnly) {
        displayedFiles = displayedFiles.filter(f => f.safe_to_delete);
    }

    // Sort based on current selection
    switch (currentSort) {
        case 'size-desc':
            displayedFiles.sort((a, b) => b.size_bytes - a.size_bytes);
            break;
        case 'size-asc':
            displayedFiles.sort((a, b) => a.size_bytes - b.size_bytes);
            break;
        case 'name-asc':
            displayedFiles.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'name-desc':
            displayedFiles.sort((a, b) => b.name.localeCompare(a.name));
            break;
        case 'date-desc':
            displayedFiles.sort((a, b) => new Date(b.modified) - new Date(a.modified));
            break;
        case 'date-asc':
            displayedFiles.sort((a, b) => new Date(a.modified) - new Date(b.modified));
            break;
    }

    renderFiles(displayedFiles);
}

// Render empty state
function renderEmptyState() {
    fileGrid.innerHTML = `
        <div class="empty-state">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                <polyline points="13 2 13 9 20 9"/>
            </svg>
            <h3>No files scanned yet</h3>
            <p>Start a scan to discover large files on your system</p>
        </div>
    `;
}

// Update stats display
function updateStats(count, size) {
    fileCount.textContent = count;
    totalSize.textContent = formatSize(size);
    statsPanel.style.display = 'grid';
}

// Format file size
function formatSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return `${size.toFixed(1)} ${units[unitIndex]}`;
}

// Get file icon type
function getFileIconType(extension) {
    const ext = (extension || '').toLowerCase();
    if (['.pdf'].includes(ext)) return 'pdf';
    if (['.doc', '.docx', '.txt', '.rtf'].includes(ext)) return 'doc';
    if (['.xls', '.xlsx', '.csv'].includes(ext)) return 'xls';
    if (['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'].includes(ext)) return 'img';
    if (['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'].includes(ext)) return 'video';
    if (['.zip', '.rar', '.7z', '.tar', '.gz'].includes(ext)) return 'archive';
    return 'other';
}

// Get file icon SVG
function getFileIconSVG(type) {
    const icons = {
        pdf: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        doc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        xls: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><rect x="8" y="12" width="8" height="6"/><line x1="12" y1="12" x2="12" y2="18"/><line x1="8" y1="15" x2="16" y2="15"/></svg>',
        img: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
        video: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>',
        archive: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 8v13H3V8"/><path d="M23 3H1v5h22V3z"/><path d="M10 12h4"/></svg>',
        other: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>'
    };
    return icons[type] || icons.other;
}

// Format date
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Render file cards with optimized DOM manipulation
function renderFiles(files) {
    if (files.length === 0) {
        renderEmptyState();
        return;
    }

    // Use DocumentFragment for better performance
    const fragment = document.createDocumentFragment();

    files.forEach(file => {
        const iconType = getFileIconType(file.extension);
        const iconSVG = getFileIconSVG(iconType);

        const card = document.createElement('div');
        card.className = 'file-card';
        card.dataset.path = file.path;

        card.innerHTML = `
            ${file.safe_to_delete
                ? '<span class="file-safety-badge safe">✓ Safe</span>'
                : '<span class="file-safety-badge review">⚠ Review</span>'
            }
            ${file.can_summarize ? '<span class="file-badge">AI</span>' : ''}
            <div class="file-card-header">
                <div class="file-icon ${iconType}">
                    ${iconSVG}
                </div>
                <div class="file-info">
                    <h3 class="file-name" title="${escapeHtml(file.name)}">${escapeHtml(file.name)}</h3>
                    <p class="file-path" title="${escapeHtml(file.path)}">${escapeHtml(file.path)}</p>
                </div>
            </div>
            <div class="file-card-meta">
                <span class="file-size">${file.size_readable}</span>
                <span class="file-date">Modified ${formatDate(file.modified)}</span>
            </div>
        `;

        // Add click handler directly
        card.addEventListener('click', () => openFileDetails(file));

        fragment.appendChild(card);
    });

    // Clear and append all at once
    fileGrid.innerHTML = '';
    fileGrid.appendChild(fragment);
}

// Open file details panel
function openFileDetails(file) {
    selectedFile = file;
    const iconType = getFileIconType(file.extension);
    const iconSVG = getFileIconSVG(iconType);

    panelContent.innerHTML = `
        <div class="panel-file-header">
            <div class="panel-file-icon file-icon ${iconType}">
                ${iconSVG}
            </div>
            <div class="panel-file-info">
                <h3>${escapeHtml(file.name)}</h3>
                <p>${escapeHtml(file.path)}</p>
            </div>
        </div>
        
        <div class="panel-meta-grid">
            <div class="meta-item">
                <label>Size</label>
                <span>${file.size_readable}</span>
            </div>
            <div class="meta-item">
                <label>Extension</label>
                <span>${file.extension || 'None'}</span>
            </div>
            <div class="meta-item">
                <label>Modified</label>
                <span>${formatDate(file.modified)}</span>
            </div>
            <div class="meta-item">
                <label>Accessed</label>
                <span>${formatDate(file.accessed)}</span>
            </div>
        </div>
        
        <div class="panel-actions">
            <button class="action-btn primary" onclick="openCurrentFile()">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                    <polyline points="15 3 21 3 21 9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
                Open File
            </button>
            <button class="action-btn secondary" onclick="openCurrentLocation()">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                Open Location
            </button>
            ${file.can_summarize ? `
            <button class="action-btn secondary" onclick="summarizeCurrentFile()">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                Analyze with AI
            </button>
            ` : ''}
            <button class="action-btn danger" onclick="deleteCurrentFile()">
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
                Delete File
            </button>
        </div>
        
        <div class="summary-section" id="summarySection" style="display: none;">
            <h4>
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                AI Analysis
            </h4>
            <div class="summary-content" id="summaryContent"></div>
        </div>
    `;

    detailPanel.classList.add('open');
}

// Open file with system default app
async function openCurrentFile() {
    if (!selectedFile) return;
    try {
        const response = await fetch(`/api/open?filepath=${encodeURIComponent(selectedFile.path)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to open file');
        }
    } catch (error) {
        console.error('Open file error:', error);
        alert(`Error: ${error.message}`);
    }
}

// Open file location in explorer
async function openCurrentLocation() {
    if (!selectedFile) return;
    try {
        const response = await fetch(`/api/open-location?filepath=${encodeURIComponent(selectedFile.path)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to open location');
        }
    } catch (error) {
        console.error('Open location error:', error);
        alert(`Error: ${error.message}`);
    }
}

// Summarize file with AI
async function summarizeCurrentFile() {
    if (!selectedFile) return;
    const filepath = selectedFile.path;

    const summarySection = document.getElementById('summarySection');
    const summaryContent = document.getElementById('summaryContent');

    summarySection.style.display = 'block';
    summaryContent.innerHTML = `
        <div class="summary-loading">
            <div class="spinner"></div>
            <span>Analyzing with ${selectedModel || 'AI'}...</span>
        </div>
    `;

    try {
        const response = await fetch('/api/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filepath: filepath,
                model: selectedModel || 'llama3.2'
            })
        });

        const data = await response.json();

        if (data.success) {
            summaryContent.textContent = data.summary;
        } else {
            summaryContent.textContent = data.error || 'Failed to analyze file.';
        }
    } catch (error) {
        console.error('Summarize error:', error);
        summaryContent.textContent = `Error: ${error.message}`;
    }
}

// Delete file
async function deleteCurrentFile() {
    if (!selectedFile) return;
    const filepath = selectedFile.path;

    if (!confirm('Are you sure you want to delete this file? It will be moved to the Recycle Bin.')) {
        return;
    }

    try {
        const response = await fetch(`/api/delete?filepath=${encodeURIComponent(filepath)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            // Remove from lists and close panel
            scannedFiles = scannedFiles.filter(f => f.path !== filepath);
            displayedFiles = displayedFiles.filter(f => f.path !== filepath);
            renderFiles(displayedFiles);
            detailPanel.classList.remove('open');
            selectedFile = null;

            // Update stats
            const newTotal = scannedFiles.reduce((sum, f) => sum + f.size_bytes, 0);
            updateStats(scannedFiles.length, newTotal);
        } else {
            throw new Error(data.detail || 'Failed to delete file');
        }
    } catch (error) {
        console.error('Delete error:', error);
        alert(`Error: ${error.message}`);
    }
}

// Show loading overlay
function showLoading(message) {
    loadingText.textContent = message;
    loadingOverlay.style.display = 'flex';
    scanBtn.disabled = true;
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.style.display = 'none';
    scanBtn.disabled = false;
}
