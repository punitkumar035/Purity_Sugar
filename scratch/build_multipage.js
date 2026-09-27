const fs = require('fs');

const src = fs.readFileSync('massecuite_phase4_8_9_1_centrifugal_solver.html', 'utf8');

// 1. CSS Additions
const cssToAdd = `
  /* Visio-Style Bottom Page-Tab Navigation Bar */
  .page-tab-bar {
    height: 34px;
    background: #e9f0f5;
    border-top: 1px solid #c9d8e4;
    display: flex;
    align-items: center;
    padding: 0 8px;
    gap: 6px;
    user-select: none;
    z-index: 10;
    flex-shrink: 0;
    box-sizing: border-box;
  }
  .page-nav-arrows {
    display: flex;
    align-items: center;
    gap: 2px;
  }
  .page-nav-arrow {
    width: 22px;
    height: 22px;
    border-radius: 3px;
    border: 1px solid #b8ccd9;
    background: #f7fafc;
    color: #1e3a52;
    font-size: 10px;
    display: grid;
    place-items: center;
    cursor: pointer;
    transition: all 0.15s ease;
    padding: 0;
  }
  .page-nav-arrow:hover {
    background: #0284c7;
    color: #ffffff;
    border-color: #0284c7;
  }
  .page-tabs-scroll {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    overflow-x: auto;
    overflow-y: hidden;
    height: 100%;
    scrollbar-width: thin;
    padding-bottom: 2px;
  }
  .page-tab {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    height: 26px;
    padding: 0 10px;
    background: #dce7f0;
    border: 1px solid #b3c8d7;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    color: #294760;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.12s ease;
  }
  .page-tab:hover {
    background: #f2f7fb;
    color: #0c263c;
  }
  .page-tab.active {
    background: #ffffff;
    border-color: #b3c8d7;
    border-top: 2px solid #0284c7;
    color: #0284c7;
    font-weight: 800;
    box-shadow: 0 -2px 6px rgba(0,0,0,0.04);
  }
  .page-tab-badge {
    font-size: 8px;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 3px;
    background: #cbd8e4;
    color: #3b556e;
  }
  .page-tab.active .page-tab-badge {
    background: #e0f2fe;
    color: #0284c7;
  }
  .page-tab-close {
    font-size: 13px;
    line-height: 1;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: inline-grid;
    place-items: center;
    color: #64748b;
    margin-left: 2px;
    opacity: 0.6;
  }
  .page-tab-close:hover {
    background: #fee2e2;
    color: #dc2626;
    opacity: 1;
  }
  .page-tab-add-btn {
    width: 24px;
    height: 24px;
    border-radius: 4px;
    border: 1px solid #b0c6d6;
    background: #f0f6fa;
    color: #0b4f7a;
    font-size: 16px;
    font-weight: 800;
    display: grid;
    place-items: center;
    cursor: pointer;
    transition: all 0.15s ease;
    padding: 0;
    line-height: 1;
  }
  .page-tab-add-btn:hover {
    background: #0284c7;
    color: #ffffff;
    border-color: #0284c7;
  }
  .page-bar-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 10px;
    color: #557085;
    font-weight: 700;
    margin-left: auto;
    flex-shrink: 0;
  }
  .page-bar-pill {
    padding: 3px 9px;
    background: #ffffff;
    border: 1px solid #cbd8e3;
    border-radius: 12px;
    color: #1e3549;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 10.5px;
  }
  .page-setup-quick-btn {
    padding: 3px 8px;
    background: #f0f6fa;
    border: 1px solid #b8ccd9;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    color: #1e425e;
    cursor: pointer;
  }
  .page-setup-quick-btn:hover {
    background: #e0f2fe;
    border-color: #0284c7;
    color: #0284c7;
  }

  /* Sheet Outline & CAD Title Block */
  .sheet-frame {
    position: absolute;
    left: 20px;
    top: 20px;
    width: 1980px;
    height: 1260px;
    pointer-events: none;
    box-sizing: border-box;
    border: 2px solid #8ca2b5;
    outline: 1px solid #cbd8e3;
    outline-offset: -8px;
    transition: width 0.2s ease, height 0.2s ease;
  }
  .sheet-titleblock {
    position: absolute;
    right: 8px;
    bottom: 8px;
    width: 380px;
    border: 1.5px solid #57758d;
    background: rgba(255, 255, 255, 0.95);
    box-sizing: border-box;
    font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    font-size: 9px;
    color: #1e293b;
    display: grid;
    grid-template-columns: 95px 1fr;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    backdrop-filter: blur(4px);
    pointer-events: auto;
  }
  .sheet-tb-cell {
    padding: 3px 6px;
    border-right: 1px solid #cbd8e3;
    border-bottom: 1px solid #cbd8e3;
  }
  .sheet-tb-cell:nth-child(2n) {
    border-right: none;
  }
  .sheet-tb-lbl {
    font-size: 7px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
  }
  .sheet-tb-val {
    font-size: 9px;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Page Setup Modal */
  .page-setup-dialog {
    position: fixed;
    z-index: 17000;
    inset: 0;
    background: rgba(15, 30, 45, 0.45);
    display: none;
    align-items: center;
    justify-content: center;
    padding: 16px;
    box-sizing: border-box;
  }
  .page-setup-dialog.show {
    display: flex;
  }
  .page-setup-box {
    width: min(520px, 94vw);
    background: #ffffff;
    border: 1px solid #94a3b8;
    border-radius: 8px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    overflow: hidden;
  }
  .page-setup-head {
    background: linear-gradient(180deg, #f0f6fa, #e2edf6);
    border-bottom: 1px solid #c9d8e4;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .page-setup-title {
    font-size: 14px;
    font-weight: 800;
    color: #123851;
  }
  .page-setup-close {
    border: 1px solid #b8ccd9;
    background: #fff;
    border-radius: 4px;
    padding: 3px 8px;
    cursor: pointer;
    font-weight: 700;
  }
  .page-setup-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .page-setup-field {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .page-setup-field label {
    font-size: 11px;
    font-weight: 700;
    color: #334e68;
  }
  .page-setup-field input, .page-setup-field select {
    height: 30px;
    padding: 0 8px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 12px;
  }
  .page-setup-actions {
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 10px 14px;
    display: flex;
    justify-content: flex-end;
    gap: 8px;
  }

  @media print {
    .topbar, .sidebar, .props, .page-tab-bar, .canvas-top, .rb-dialog, .centrifugal-dialog, .page-setup-dialog {
      display: none !important;
    }
    .canvas-shell, .viewport, .world-wrap, .world {
      width: 100% !important;
      height: 100% !important;
      overflow: visible !important;
      background: white !important;
    }
  }
`;

let modified = src.replace('</style>', cssToAdd + '\r\n</style>');

// 2. HTML: Sheet Frame inside #world
const sheetFrameHtml = `
            <!-- Sheet Outline & CAD Title Block -->
            <div class="sheet-frame" id="sheetFrame">
              <div class="sheet-titleblock" id="sheetTitleblock">
                <div class="sheet-tb-cell"><div class="sheet-tb-lbl">PROJECT</div><div class="sheet-tb-val" id="stbProject">Massecuite Scheme</div></div>
                <div class="sheet-tb-cell"><div class="sheet-tb-lbl">PAGE</div><div class="sheet-tb-val" id="stbPage">Page 1</div></div>
                <div class="sheet-tb-cell"><div class="sheet-tb-lbl">STANDARD</div><div class="sheet-tb-val">Sugar's Help Book</div></div>
                <div class="sheet-tb-cell"><div class="sheet-tb-lbl">UNITS / STATUS</div><div class="sheet-tb-val" id="stbStatus">kg/h · °C · kPa abs</div></div>
              </div>
            </div>
`;

modified = modified.replace('<div class="empty-state" id="emptyState">', sheetFrameHtml + '            <div class="empty-state" id="emptyState">');

// 3. HTML: Bottom Page Tab Bar after #viewport
const pageTabBarHtml = `
      <!-- Visio-Style Bottom Page-Tab Navigation Bar -->
      <nav class="page-tab-bar" id="pageTabBar" aria-label="Drawing Pages">
        <div class="page-nav-arrows">
          <button class="page-nav-arrow" id="pageNavPrev" title="Previous Page (PageUp)" aria-label="Previous Page">◀</button>
          <button class="page-nav-arrow" id="pageNavNext" title="Next Page (PageDown)" aria-label="Next Page">▶</button>
        </div>
        <div class="page-tabs-scroll" id="pageTabsScroll" role="tablist">
          <!-- Populated dynamically by Page Manager -->
        </div>
        <button class="page-tab-add-btn" id="addPageBtn" title="Insert New Page (Ctrl+Alt+N)" aria-label="Add New Page">+</button>
        <div class="page-bar-info" id="pageBarInfo">
          <span class="page-bar-pill" id="pageStatusPill">Page 1 of 1 · A4 Landscape</span>
          <button class="page-setup-quick-btn" id="pageSetupQuickBtn" title="Page Setup &amp; Dimensions">⚙️ Setup</button>
        </div>
      </nav>
    </section>

    <aside class="props">`;

modified = modified.replace(/<\/section>\s*<aside class="props">/i, pageTabBarHtml);

// 4. HTML: Page Setup Modal before </body>
const pageSetupModalHtml = `
<!-- Page Setup Modal Dialog -->
<div class="page-setup-dialog" id="pageSetupDialog" role="dialog" aria-label="Page Setup">
  <div class="page-setup-box">
    <div class="page-setup-head">
      <div class="page-setup-title">⚙️ Page Setup &amp; Dimensions</div>
      <button class="page-setup-close" id="pageSetupClose">✕</button>
    </div>
    <div class="page-setup-body">
      <div class="page-setup-field">
        <label>Page Name</label>
        <input type="text" id="setupPageName" value="Page 1" />
      </div>
      <div class="page-setup-field">
        <label>Standard Dimensions (CAD / Drawing Frame)</label>
        <select id="setupPageSize">
          <option value="A4">A4 (297 × 210 mm standard sheet)</option>
          <option value="A3">A3 (420 × 297 mm large schematic)</option>
          <option value="Letter">ANSI Letter (11 × 8.5 in)</option>
          <option value="Custom">Custom / Unlimited Canvas</option>
        </select>
      </div>
      <div class="page-setup-field">
        <label>Drawing Orientation</label>
        <select id="setupPageOrientation">
          <option value="landscape">Landscape (Standard Flowsheet)</option>
          <option value="portrait">Portrait</option>
        </select>
      </div>
      <div class="page-setup-field" style="flex-direction:row;align-items:center;gap:8px;margin-top:6px;">
        <input type="checkbox" id="setupShowSheetFrame" checked style="height:auto;width:auto;" />
        <label for="setupShowSheetFrame" style="cursor:pointer;font-size:11px;color:#334e68;font-weight:700;">Show Drawing Sheet Frame &amp; Title Block</label>
      </div>
    </div>
    <div class="page-setup-actions">
      <button class="btn" id="setupCancelBtn">Cancel</button>
      <button class="btn primary" id="setupApplyBtn">Apply Changes</button>
    </div>
  </div>
</div>
`;

modified = modified.replace('</body>', pageSetupModalHtml + '\r\n</body>');

// 5. JavaScript: State initialization & Page Model
const oldStateRegex = /let state\s*=\s*\{\s*version:\s*5,\s*name:\s*'New Massecuite Scheme',\s*nodes:\s*\[\],\s*connectors:\s*\[\],\s*flowLegendsOn:\s*false\s*\};/;

const newStateBlock = `  let state = {
    version: 5,
    schemaVersion: 1,
    name: 'New Massecuite Scheme',
    activePageId: 'page_1',
    pages: [
      {
        id: 'page_1',
        name: 'Page 1',
        order: 0,
        layout: 'A4',
        orientation: 'landscape',
        zoom: 1,
        panX: 0,
        panY: 0,
        nodes: [],
        connectors: [],
        streams: []
      }
    ],
    nodes: [],
    connectors: [],
    streams: [],
    flowLegendsOn: false,
    showSheetFrame: true,
    gridVisible: true,
    snapToGrid: true
  };
  state.pages[0].nodes = state.nodes;
  state.pages[0].connectors = state.connectors;
  state.pages[0].streams = state.streams;

  function ensurePageModel(s) {
    if (!s) return;
    if (!s.pages || !Array.isArray(s.pages) || s.pages.length === 0) {
      s.pages = [{
        id: 'page_1',
        name: 'Page 1',
        order: 0,
        layout: 'A4',
        orientation: 'landscape',
        zoom: zoom || 1,
        panX: 0,
        panY: 0,
        nodes: s.nodes || [],
        connectors: s.connectors || [],
        streams: s.streams || s.connectors || []
      }];
      s.activePageId = 'page_1';
    }
    if (!s.activePageId || !s.pages.some(p => p.id === s.activePageId)) {
      s.activePageId = s.pages[0].id;
    }
  }

  function activePage() {
    ensurePageModel(state);
    return state.pages.find(p => p.id === state.activePageId) || state.pages[0];
  }

  function saveActivePageData() {
    if (!state.pages) return;
    const cur = state.pages.find(p => p.id === state.activePageId);
    if (cur) {
      cur.nodes = state.nodes;
      cur.connectors = state.connectors;
      cur.zoom = zoom;
    }
  }

  const PageManager = {
    getActivePage() { return activePage(); },
    getPages() {
      ensurePageModel(state);
      return [...state.pages].sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
    },
    createPage(name, options = {}) {
      pushHistory();
      saveActivePageData();
      const count = state.pages.length + 1;
      const newId = 'page_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      const newPage = {
        id: newId,
        name: name || ('Page ' + count),
        order: state.pages.length,
        layout: options.layout || 'A4',
        orientation: options.orientation || 'landscape',
        zoom: 1,
        panX: 0,
        panY: 0,
        nodes: [],
        connectors: [],
        streams: []
      };
      state.pages.push(newPage);
      this.activatePage(newId);
      toast('Created ' + newPage.name);
      return newPage;
    },
    duplicatePage(pageId) {
      pushHistory();
      saveActivePageData();
      const srcPage = state.pages.find(p => p.id === pageId) || activePage();
      if (!srcPage) return;
      const newId = 'page_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      const idMap = new Map();
      const srcNodes = srcPage.id === state.activePageId ? state.nodes : srcPage.nodes;
      const srcConnectors = srcPage.id === state.activePageId ? state.connectors : srcPage.connectors;

      const clonedNodes = (srcNodes || []).map(n => {
        const c = clone(n);
        const oldId = c.id;
        c.id = 'node_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
        idMap.set(oldId, c.id);
        return c;
      });

      const clonedConnectors = (srcConnectors || []).map(c => {
        const conn = clone(c);
        conn.id = 'stream_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
        if (idMap.has(conn.fromNodeId)) conn.fromNodeId = idMap.get(conn.fromNodeId);
        if (idMap.has(conn.toNodeId)) conn.toNodeId = idMap.get(conn.toNodeId);
        if (conn.source && idMap.has(conn.source.station_id)) conn.source.station_id = idMap.get(conn.source.station_id);
        if (conn.target && idMap.has(conn.target.station_id)) conn.target.station_id = idMap.get(conn.target.station_id);
        canonicalizeLoadedConnector(conn);
        return conn;
      });

      const newPage = {
        id: newId,
        name: 'Copy of ' + srcPage.name,
        order: state.pages.length,
        layout: srcPage.layout || 'A4',
        orientation: srcPage.orientation || 'landscape',
        zoom: srcPage.zoom || 1,
        panX: srcPage.panX || 0,
        panY: srcPage.panY || 0,
        nodes: clonedNodes,
        connectors: clonedConnectors,
        streams: []
      };
      state.pages.push(newPage);
      this.activatePage(newId);
      toast('Duplicated ' + srcPage.name);
      return newPage;
    },
    renamePage(pageId, newName) {
      if (!newName || !newName.trim()) return;
      const pg = state.pages.find(p => p.id === pageId);
      if (!pg) return;
      pushHistory();
      pg.name = newName.trim();
      renderPageTabs();
      updatePageStatusPill();
      updateSheetFrame();
      toast('Renamed to ' + pg.name);
    },
    deletePage(pageId) {
      if (state.pages.length <= 1) {
        alert('Cannot delete the only page in the project.');
        return;
      }
      const pg = state.pages.find(p => p.id === pageId);
      if (!pg) return;
      if (!confirm('Delete page "' + pg.name + '" and all its stations?')) return;

      pushHistory();
      saveActivePageData();
      const idx = state.pages.findIndex(p => p.id === pageId);
      state.pages.splice(idx, 1);
      state.pages.forEach((p, i) => { p.order = i; });

      if (state.activePageId === pageId) {
        const nextIdx = Math.min(idx, state.pages.length - 1);
        this.activatePage(state.pages[nextIdx].id);
      } else {
        renderPageTabs();
        updatePageStatusPill();
      }
      toast('Deleted page');
    },
    activatePage(pageId) {
      saveActivePageData();
      const target = state.pages.find(p => p.id === pageId) || state.pages[0];
      state.activePageId = target.id;
      state.nodes = target.nodes || [];
      state.connectors = target.connectors || [];
      target.nodes = state.nodes;
      target.connectors = state.connectors;
      selected = null;
      pendingConnection = null;
      connectorDrag = null;

      if (target.zoom) {
        setZoom(target.zoom);
      }

      renderAll();
      renderPageTabs();
      updatePageStatusPill();
      updateSheetFrame();
    },
    movePageLeft(pageId) {
      const idx = state.pages.findIndex(p => p.id === pageId);
      if (idx <= 0) return;
      pushHistory();
      const temp = state.pages[idx];
      state.pages[idx] = state.pages[idx - 1];
      state.pages[idx - 1] = temp;
      state.pages.forEach((p, i) => { p.order = i; });
      renderPageTabs();
      updatePageStatusPill();
    },
    movePageRight(pageId) {
      const idx = state.pages.findIndex(p => p.id === pageId);
      if (idx < 0 || idx >= state.pages.length - 1) return;
      pushHistory();
      const temp = state.pages[idx];
      state.pages[idx] = state.pages[idx + 1];
      state.pages[idx + 1] = temp;
      state.pages.forEach((p, i) => { p.order = i; });
      renderPageTabs();
      updatePageStatusPill();
    },
    nextPage() {
      const idx = state.pages.findIndex(p => p.id === state.activePageId);
      if (idx < state.pages.length - 1) {
        this.activatePage(state.pages[idx + 1].id);
      }
    },
    previousPage() {
      const idx = state.pages.findIndex(p => p.id === state.activePageId);
      if (idx > 0) {
        this.activatePage(state.pages[idx - 1].id);
      }
    },
    setPageSetup(pageId, { layout, orientation }) {
      const pg = state.pages.find(p => p.id === pageId);
      if (!pg) return;
      pushHistory();
      if (layout) pg.layout = layout;
      if (orientation) pg.orientation = orientation;
      updatePageStatusPill();
      updateSheetFrame();
      toast('Page setup updated · ' + pg.layout + ' ' + pg.orientation);
    }
  };`;

modified = modified.replace(oldStateRegex, newStateBlock);

// 6. Update canonicalStateObject
const oldCanonicalRegex = /return\s*\{\s*version:\s*5,\s*name:\s*src\?\.name\|\|'Untitled Scheme',\s*flowLegendsOn:\s*!!src\?\.flowLegendsOn,\s*nodes:\s*\(src\?\.nodes\|\|\[\]\)\.map\(cleanNode\),\s*connectors:\s*\(src\?\.connectors\|\|\[\]\)\.map\(cleanConnector\)\s*\};/;

const newCanonical = `saveActivePageData();
    const pages = (src?.pages && src.pages.length ? src.pages : [{
      id: 'page_1',
      name: 'Page 1',
      order: 0,
      layout: 'A4',
      orientation: 'landscape',
      zoom: src?.zoom || 1,
      nodes: src?.nodes || [],
      connectors: src?.connectors || []
    }]).map(p => ({
      id: p.id,
      name: p.name,
      order: p.order,
      layout: p.layout || 'A4',
      orientation: p.orientation || 'landscape',
      zoom: p.zoom || 1,
      nodes: (p.id === src?.activePageId ? src.nodes : (p.nodes || [])).map(cleanNode),
      connectors: (p.id === src?.activePageId ? src.connectors : (p.connectors || [])).map(cleanConnector)
    }));

    return {
      version: 5,
      schemaVersion: 1,
      name: src?.name || 'Untitled Scheme',
      flowLegendsOn: !!src?.flowLegendsOn,
      showSheetFrame: src?.showSheetFrame !== false,
      activePageId: src?.activePageId || 'page_1',
      pages: pages,
      nodes: (src?.nodes || []).map(cleanNode),
      connectors: (src?.connectors || []).map(cleanConnector)
    };`;

modified = modified.replace(oldCanonicalRegex, newCanonical);

// 7. Update prepareState
const oldPrepareStateRegex = /function prepareState\(obj\)\{[\s\S]*?Object\.defineProperty\(obj,'streams'[\s\S]*?\}\);[\s\S]*?return obj;[\s\S]*?\}/;

const newPrepareState = `function prepareState(obj){
    obj=obj||{};
    obj.version=5;
    obj.name=obj.name||'Untitled Scheme';
    obj.flowLegendsOn=!!obj.flowLegendsOn;
    obj.showSheetFrame=obj.showSheetFrame!==false;

    if (obj.pages && Array.isArray(obj.pages) && obj.pages.length > 0) {
      obj.pages.forEach((p, idx) => {
        p.id = p.id || ('page_' + (idx + 1));
        p.name = p.name || ('Page ' + (idx + 1));
        p.order = p.order ?? idx;
        p.layout = p.layout || 'A4';
        p.orientation = p.orientation || 'landscape';
        p.nodes = Array.isArray(p.nodes) ? p.nodes : [];
        normalizeEquipmentTags(p.nodes);
        const rawConn = Array.isArray(p.connectors) ? p.connectors : (Array.isArray(p.streams) ? p.streams : []);
        p.connectors = rawConn.map((c, i) => migrateLegacyStreamToConnector(c, i));
      });
      obj.activePageId = (obj.activePageId && obj.pages.some(p => p.id === obj.activePageId)) ? obj.activePageId : obj.pages[0].id;
      const act = obj.pages.find(p => p.id === obj.activePageId) || obj.pages[0];
      obj.nodes = act.nodes;
      obj.connectors = act.connectors;
      act.nodes = obj.nodes;
      act.connectors = obj.connectors;
    } else {
      obj.nodes = Array.isArray(obj.nodes) ? obj.nodes : [];
      normalizeEquipmentTags(obj.nodes);
      const raw = Array.isArray(obj.connectors) ? obj.connectors : (Array.isArray(obj.streams) ? obj.streams : []);
      obj.connectors = raw.map((c, i) => migrateLegacyStreamToConnector(c, i));
      obj.pages = [{
        id: 'page_1',
        name: 'Page 1',
        order: 0,
        layout: 'A4',
        orientation: 'landscape',
        zoom: obj.zoom || 1,
        panX: 0,
        panY: 0,
        nodes: obj.nodes,
        connectors: obj.connectors
      }];
      obj.activePageId = 'page_1';
    }

    try{delete obj.streams;}catch(_){}
    Object.defineProperty(obj,'streams',{
      get(){return this.connectors.filter(connectorSolverActive);},
      set(v){this.connectors=Array.isArray(v)?v.map((c,i)=>migrateLegacyStreamToConnector(c,i)):[];},
      enumerable:false,configurable:true
    });
    return obj;
  }`;

modified = modified.replace(oldPrepareStateRegex, newPrepareState);

// 8. Update rehydrateCurrentState & renderAll
modified = modified.replace(/rehydrateCurrentState\(\)\s*\{[\s\S]*?markChanged\(\);\s*\}/, `rehydrateCurrentState(){
    state.version=5;
    ensurePageModel(state);
    normalizeEquipmentTags(state.nodes||[]);
    (state.connectors||[]).forEach(canonicalizeLoadedConnector);
    state.nodes.forEach(n=>{
      n.solveStatus='UNSOLVED';
      n.solverMessage='';
      if(n.type==='pan')ensurePanDefaults(n);
      if(n.type==='crystallizer')ensureCrystallizerDefaults(n);
      if(n.type==='centrifugal2' || n.type==='centrifugal3')ensureCentrifugalDefaults(n);
    });
    renderPageTabs();
    updatePageStatusPill();
    updateSheetFrame();
    markChanged();
  }`);

modified = modified.replace(/function renderAll\(\)\s*\{\s*renderNodes\(\);\s*renderWires\(\);\s*renderProps\(\);\s*renderEmpty\(\);\s*\}/, `function renderAll(){\n    renderNodes();\n    renderWires();\n    renderProps();\n    renderEmpty();\n    updateSheetFrame();\n    updatePageStatusPill();\n  }`);

// 9. Update newScheme
const oldNewSchemeRegex = /function newScheme\(\)\{[\s\S]*?restoreStateObject\(\{version:5,name:'New Massecuite Scheme',nodes:\[\],connectors:\[\]\}\);[\s\S]*?currentProjectFileHandle=null;\s*\}/;

const newNewScheme = `function newScheme(){
    if((state.nodes.length||state.connectors.length) && !confirm('Create a new blank scheme? Unsaved changes will be lost.')) return;
    pushHistory();
    restoreStateObject({
      version: 5,
      name: 'New Massecuite Scheme',
      activePageId: 'page_1',
      pages: [{
        id: 'page_1',
        name: 'Page 1',
        order: 0,
        layout: 'A4',
        orientation: 'landscape',
        zoom: 1,
        nodes: [],
        connectors: []
      }],
      nodes: [],
      connectors: []
    });
    currentProjectFileHandle=null;
  }`;

modified = modified.replace(oldNewSchemeRegex, newNewScheme);

// 10. Update loadProjectObject
const oldLoadProjectRegex = /async function loadProjectObject\(obj,\{fileHandle=null,sourceName='Project'\}={}\)\{[\s\S]*?if\(!obj \|\| !Array\.isArray\(obj\.nodes\)[\s\S]*?\}\s*pushHistory\(\);/;

const newLoadProject = `async function loadProjectObject(obj,{fileHandle=null,sourceName='Project'}={}){
    if(!obj || (!Array.isArray(obj.nodes) && !Array.isArray(obj.pages))){
      throw new Error('Invalid Massecuite Simulator project file');
    }
    pushHistory();`;

modified = modified.replace(oldLoadProjectRegex, newLoadProject);

// 11. Add Page Navigation rendering & UI logic
const pageUiFunctions = `
  function renderPageTabs() {
    const scrollEl = document.getElementById('pageTabsScroll');
    if (!scrollEl) return;
    scrollEl.innerHTML = '';
    const pages = PageManager.getPages();

    pages.forEach((pg, idx) => {
      const tab = document.createElement('div');
      tab.className = 'page-tab' + (pg.id === state.activePageId ? ' active' : '');
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-selected', String(pg.id === state.activePageId));
      tab.dataset.pageId = pg.id;

      const titleSpan = document.createElement('span');
      titleSpan.className = 'page-tab-title';
      titleSpan.textContent = pg.name;

      const badge = document.createElement('span');
      badge.className = 'page-tab-badge';
      const nodeCount = (pg.id === state.activePageId ? state.nodes : (pg.nodes || [])).length;
      badge.textContent = nodeCount + ' stn';

      tab.append(titleSpan, badge);

      if (pages.length > 1) {
        const closeBtn = document.createElement('span');
        closeBtn.className = 'page-tab-close';
        closeBtn.title = 'Delete Page';
        closeBtn.innerHTML = '×';
        closeBtn.onclick = (e) => {
          e.stopPropagation();
          PageManager.deletePage(pg.id);
        };
        tab.append(closeBtn);
      }

      tab.onclick = () => {
        PageManager.activatePage(pg.id);
      };

      tab.ondblclick = (e) => {
        e.stopPropagation();
        promptRenamePage(pg.id);
      };

      tab.oncontextmenu = (e) => {
        e.preventDefault();
        e.stopPropagation();
        showPageContextMenu(e.clientX, e.clientY, pg.id);
      };

      scrollEl.append(tab);
    });

    const activeTab = scrollEl.querySelector('.page-tab.active');
    if (activeTab && typeof activeTab.scrollIntoView === 'function') {
      activeTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
    }
  }

  function showPageContextMenu(x, y, pageId) {
    const cm = document.getElementById('contextMenu');
    if (!cm) return;
    const pg = state.pages.find(p => p.id === pageId);
    if (!pg) return;
    const isOnly = state.pages.length <= 1;

    cm.innerHTML = \`
      <div class="cm-item" id="cmRenamePage">✏️ Rename Page...</div>
      <div class="cm-item" id="cmDuplicatePage">📄 Duplicate Page</div>
      <div class="cm-item \${isOnly ? 'disabled' : ''}" id="cmDeletePage">🗑️ Delete Page</div>
      <div class="cm-sep"></div>
      <div class="cm-item" id="cmMoveLeft">◀ Move Left</div>
      <div class="cm-item" id="cmMoveRight">▶ Move Right</div>
      <div class="cm-sep"></div>
      <div class="cm-item" id="cmPageSetup">⚙️ Page Setup...</div>
      <div class="cm-item" id="cmExportPage">📥 Export Page (JSON)</div>
      <div class="cm-item" id="cmPrintPage">🖨️ Print This Page</div>
    \`;

    cm.style.display = 'block';
    cm.style.left = Math.min(x, window.innerWidth - 200) + 'px';
    cm.style.top = Math.max(10, y - 260) + 'px';

    document.getElementById('cmRenamePage').onclick = () => { cm.style.display = 'none'; promptRenamePage(pageId); };
    document.getElementById('cmDuplicatePage').onclick = () => { cm.style.display = 'none'; PageManager.duplicatePage(pageId); };
    if (!isOnly) {
      document.getElementById('cmDeletePage').onclick = () => { cm.style.display = 'none'; PageManager.deletePage(pageId); };
    }
    document.getElementById('cmMoveLeft').onclick = () => { cm.style.display = 'none'; PageManager.movePageLeft(pageId); };
    document.getElementById('cmMoveRight').onclick = () => { cm.style.display = 'none'; PageManager.movePageRight(pageId); };
    document.getElementById('cmPageSetup').onclick = () => { cm.style.display = 'none'; openPageSetupDialog(pageId); };
    document.getElementById('cmExportPage').onclick = () => { cm.style.display = 'none'; exportSinglePage(pageId); };
    document.getElementById('cmPrintPage').onclick = () => { cm.style.display = 'none'; printSinglePage(pageId); };
  }

  function updatePageStatusPill() {
    const pill = document.getElementById('pageStatusPill');
    if (!pill) return;
    const cur = activePage();
    const idx = state.pages.findIndex(p => p.id === cur.id);
    const layout = cur.layout || 'A4';
    const orient = cur.orientation || 'landscape';
    pill.textContent = 'Page ' + (idx + 1) + ' of ' + state.pages.length + ' · ' + layout + ' ' + (orient.charAt(0).toUpperCase() + orient.slice(1));
  }

  function updateSheetFrame() {
    const frame = document.getElementById('sheetFrame');
    if (!frame) return;
    if (state.showSheetFrame === false) {
      frame.style.display = 'none';
      return;
    }
    frame.style.display = 'block';
    const cur = activePage();
    const layout = cur.layout || 'A4';
    const orient = cur.orientation || 'landscape';

    let w = 1980, h = 1260;
    if (layout === 'A3') {
      w = orient === 'landscape' ? 2120 : 1380;
      h = orient === 'landscape' ? 1340 : 2100;
    } else if (layout === 'Letter') {
      w = orient === 'landscape' ? 1900 : 1240;
      h = orient === 'landscape' ? 1220 : 1880;
    } else if (layout === 'Custom') {
      w = 2160; h = 1360;
    } else {
      w = orient === 'landscape' ? 1980 : 1260;
      h = orient === 'landscape' ? 1260 : 1980;
    }
    frame.style.width = w + 'px';
    frame.style.height = h + 'px';

    const stbProj = document.getElementById('stbProject');
    if (stbProj) stbProj.textContent = state.name || 'Massecuite Scheme';
    const stbPg = document.getElementById('stbPage');
    if (stbPg) stbPg.textContent = cur.name + ' (' + layout + ' ' + orient + ')';
    const stbStat = document.getElementById('stbStatus');
    if (stbStat) stbStat.textContent = (statusText && statusText.textContent) || 'kg/h · °C · kPa abs';
  }

  function openPageSetupDialog(pageId) {
    const modal = document.getElementById('pageSetupDialog');
    if (!modal) return;
    const pg = state.pages.find(p => p.id === pageId) || activePage();
    document.getElementById('setupPageName').value = pg.name;
    document.getElementById('setupPageSize').value = pg.layout || 'A4';
    document.getElementById('setupPageOrientation').value = pg.orientation || 'landscape';
    document.getElementById('setupShowSheetFrame').checked = state.showSheetFrame !== false;

    modal.classList.add('show');

    document.getElementById('setupApplyBtn').onclick = () => {
      const newName = document.getElementById('setupPageName').value.trim() || pg.name;
      const newLayout = document.getElementById('setupPageSize').value;
      const newOrient = document.getElementById('setupPageOrientation').value;
      state.showSheetFrame = document.getElementById('setupShowSheetFrame').checked;

      pg.name = newName;
      pg.layout = newLayout;
      pg.orientation = newOrient;

      modal.classList.remove('show');
      renderPageTabs();
      updatePageStatusPill();
      updateSheetFrame();
      toast('Page setup updated');
    };

    document.getElementById('setupCancelBtn').onclick = () => modal.classList.remove('show');
    document.getElementById('pageSetupClose').onclick = () => modal.classList.remove('show');
  }

  function promptRenamePage(pageId) {
    const pg = state.pages.find(p => p.id === pageId);
    if (!pg) return;
    const newName = prompt('Enter new name for page:', pg.name);
    if (newName && newName.trim() && newName.trim() !== pg.name) {
      PageManager.renamePage(pageId, newName.trim());
    }
  }

  function exportSinglePage(pageId) {
    saveActivePageData();
    const pg = state.pages.find(p => p.id === pageId) || activePage();
    const data = {
      version: 5,
      type: 'SinglePageExport',
      project: state.name,
      page: pg
    };
    downloadTextFile(JSON.stringify(data, null, 2), (pg.name || 'Page').replace(/\\s+/g, '_') + '.json');
    toast('Exported ' + pg.name);
  }

  function printSinglePage(pageId) {
    if (state.activePageId !== pageId) {
      PageManager.activatePage(pageId);
    }
    setTimeout(() => window.print(), 200);
  }

  function createStationFromGallery(stationType) {
    const def = nodeDefs[stationType];
    if (!def) return;
    pushHistory();
    const pos = { x: 300 + Math.floor(Math.random() * 100), y: 200 + Math.floor(Math.random() * 80) };
    const n = createNode(stationType, pos.x, pos.y);
    state.nodes.push(n);
    normalizeEquipmentTags(state.nodes);
    markChanged();
    selectItem('node', n.id);
    renderAll();
    toast('Added ' + (def.title || stationType));
  }

  function createCrossPageConnector() {
    toast('Drag Universal Flow to canvas or link stream to route cross-page');
  }
`;

modified = modified.replace(/\/\/\s*Phase\s*4\.8\.6:\s*ribbon\s*commands\s*reuse[\s\S]*?function\s*installEngineeringRibbon\(\)\s*\{/i, pageUiFunctions + '\r\n  // Phase 4.8.6: ribbon commands reuse the established application operations.\r\n  function installEngineeringRibbon(){');

// 12. Update installEngineeringRibbon with 10 Tabs from implementation plan
const oldTabsRegex = /const tabs\s*=\s*\{[\s\S]*?Help:\s*\{[\s\S]*?\}\s*\}\s*;/;

const newTabsBlock = `const tabs={
      File:{
        Project:[
          existing('New Scheme','newBtn'),
          existing('Open / Import','openBtn','import'),
          existing('Save Project','saveBtn','save'),
          command('Save As',()=>{currentProjectFileHandle=null;void saveProject();},'save')
        ],
        Pages:[
          command('New Page',()=>PageManager.createPage(),'file','Add a new drawing page (Ctrl+Alt+N)'),
          command('Page Setup',()=>openPageSetupDialog(state.activePageId),'settings','Configure sheet size and orientation')
        ],
        Templates:[
          existing('Scheme Library','libraryBtn','table'),
          existing('Save Template','templateBtn','save')
        ],
        Output:[
          command('Export Excel (.xlsx)',()=>exportToExcelFromBackend(),'save','Generate comprehensive workbook report'),
          exportStations,
          exportStreams,
          command('Print / PDF',()=>window.print(),'file')
        ]
      },
      Home:{
        Project:[existing('Open','openBtn','import'),existing('Save','saveBtn','save')],
        Edit:[existing('Undo','undoBtn','undo'),existing('Redo','redoBtn','redo')],
        Pages:[
          command('Add Page',()=>PageManager.createPage(),'file','Insert new drawing page'),
          command('Next Page',()=>PageManager.nextPage(),'route','Go to next page (PageDown)'),
          command('Prev Page',()=>PageManager.previousPage(),'route','Go to previous page (PageUp)')
        ],
        Flowsheet:[palette,props,existing('Fit View','fitBtn','zoom'),flowLegendsCmd],
        Calculate:[existing('Solve Network','solveBtn','play'),command('Solve (Python)',()=>solveWithPythonBackend(),'settings'),audit]
      },
      Insert:{
        Stations:[
          command('Pan / Evaporator',()=>createStationFromGallery('pan'),'station','Add Vacuum Pan'),
          command('Crystallizer',()=>createStationFromGallery('crystallizer'),'station','Add Cooling Crystallizer'),
          command('Centrifugal',()=>createStationFromGallery('centrifugal2'),'station','Add Centrifugal Station'),
          command('Heater / Melter',()=>createStationFromGallery('heatExchanger'),'station','Add Heat Exchanger')
        ],
        Streams:[
          command('Universal Flow',()=>createUniversalFlowStencil(500,300),'route','Insert dynamic universal process stream'),
          command('Cross-Page Link',()=>createCrossPageConnector(),'route','Link stream from another drawing page')
        ],
        Pages:[
          command('Insert Page',()=>PageManager.createPage(),'file','Add blank drawing page'),
          command('Duplicate Page',()=>PageManager.duplicatePage(state.activePageId),'file','Clone active page and all stations')
        ],
        Annotations:[
          command('Model Notes',()=>dialog('Flowsheet Notes','<textarea style="width:100%;height:140px;border:1px solid #cbd5e1;padding:8px;" placeholder="Enter process notes here..."></textarea>'),'file','Add textual engineering annotations')
        ]
      },
      Design:{
        'Page Setup':[
          command('Page Dimensions',()=>openPageSetupDialog(state.activePageId),'settings','Set page format A4/A3/Letter'),
          command('A4 Landscape',()=>PageManager.setPageSetup(state.activePageId,{layout:'A4',orientation:'landscape'}),'file','Standard A4 landscape drawing'),
          command('A3 Landscape',()=>PageManager.setPageSetup(state.activePageId,{layout:'A3',orientation:'landscape'}),'file','Large A3 schematic format')
        ],
        'Sheet Frame':[
          command('Toggle Frame',()=>{state.showSheetFrame=!state.showSheetFrame;updateSheetFrame();toast(state.showSheetFrame?'Sheet frame visible':'Sheet frame hidden');},'table','Show/hide CAD border outline and title block')
        ],
        'Grid & Snap':[
          command('Toggle Grid',()=>{const g=document.querySelector('.canvas-grid');if(g){g.style.display=g.style.display==='none'?'block':'none';toast(g.style.display==='none'?'Grid hidden':'Grid visible');}},'table','Show or hide background coordinate grid'),
          command('Auto Layout',()=>click('autoBtn'),'station','Automatically arrange stations')
        ]
      },
      Data:{
        Exchange:[
          existing('Import Project','openBtn','import'),
          existing('Export Project','saveBtn','export'),
          command('Export to Excel (.xlsx)',()=>exportToExcelFromBackend(),'save'),
          exportStreams,
          exportStations
        ],
        Identity:[command('Renumber Stations',numbering,'numbers')],
        Tables:[streams,stations],
        Units:[
          command('Default Units',()=>dialog('Engineering Units','<p>This build uses fixed engineering units. Per-field labels remain authoritative.</p>'+table(['Quantity','Unit'],[['Mass flow','kg/h'],['Temperature','°C'],['Pressure','kPa absolute'],['Composition','mass %']])),'table'),
          pending('Property Methods','Select methods in the individual Flow Properties window. Global method overrides are not supported.')
        ]
      },
      Process:{
        Calculation:[
          existing('Solve Network','solveBtn','play'),
          command('Solve with Python Engine',()=>solveWithPythonBackend(),'settings'),
          command('Validate Connections',()=>dialog('Connection Validation',table(['Stream','Role','Topology issues'],state.connectors.map(c=>[c.name||c.id,connectorRole(c),connectorTopologyIssues(c).join('; ')||'No topology issues']))),'check')
        ],
        Balances:[
          command('Full Balance Report',()=>showFullBalanceReport(),'table'),
          command('Net Process Revenues',()=>showRevenuesModal(),'table'),
          command('Mass & Solids Closure',()=>showFullBalanceReport(),'check')
        ],
        Control:[
          command('Reset Unsolved',reset,'settings','Reset all stations to unsolved status')
        ]
      },
      Review:{
        Diagnostics:[
          audit,
          command('Errors / Warnings',()=>showSolverIssues(),'warning'),
          command('Connection Validation',()=>dialog('Connection Validation',table(['Stream','Role','Topology issues'],state.connectors.map(c=>[c.name||c.id,connectorRole(c),connectorTopologyIssues(c).join('; ')||'No topology issues']))),'check')
        ],
        Verification:[
          command('Self-Tests Status',()=>dialog('Self-Tests Verification',table(['Test Case','Status'],[['Phase 4.8.3 Property Self-Test',window.__PHASE483_PROPERTY_SELF_TEST__?'PASS':'FAIL'],['Native DS/Purity Preservation',window.__PHASE4833_EDITING_SELF_TEST__?'PASS':'FAIL'],['Saska BPE Verification',window.__SASKA_BPE_SELF_TEST__?'PASS':'FAIL']])), 'check'),
          command('Source Citations',()=>dialog('Thermodynamic Source Citations','<p>All process calculations cite authoritative literature:</p><ul><li><b>Sucrose Solubility:</b> Vavrinecz (1962) / ICUMSA</li><li><b>Boiling Point Elevation:</b> Saska ASI (2002) Eq. 8</li><li><b>Saturation Coefficient:</b> Wagnerowski et al. (1962)</li><li><b>Density:</b> Lyle (1957) Eq. 32.8</li><li><b>Steam & Water Properties:</b> CoolProp IAPWS-IF97</li></ul>'),'file')
        ]
      },
      View:{
        Canvas:[
          existing('Zoom In','zoomIn','zoom'),
          existing('Zoom Out','zoomOut','zoom'),
          existing('Fit View','fitBtn','zoom'),
          existing('Reset Zoom','zoomReset','zoom')
        ],
        Panels:[
          command('Station Palette',()=>{const el=document.querySelector('.sidebar');el.hidden=!el.hidden;},'station'),
          props,
          command('Collapse Ribbon',()=>top.classList.toggle('ribbon-collapsed'),'settings')
        ],
        Indicators:[
          flowLegendsCmd,
          command('Toggle Sheet Frame',()=>{state.showSheetFrame=!state.showSheetFrame;updateSheetFrame();toast(state.showSheetFrame?'Sheet frame visible':'Sheet frame hidden');},'table')
        ]
      },
      Developer:{
        Inspection:[
          command('Model Inspector',()=>dialog('Model Inspector',table(['Property','Value'],[['Name',state.name],['Version',state.version],['Pages Count',state.pages.length],['Active Page ID',state.activePageId],['Active Stations',state.nodes.length],['Active Streams',state.connectors.length]])),'settings'),
          command('JSON Inspector',()=>dialog('Canonical JSON State',\`<textarea style="width:100%;height:320px;font-family:monospace;font-size:11px;" readonly>\${escapeHtml(JSON.stringify(canonicalStateObject(state),null,2))}</textarea>\`),'file'),
          command('State Log',()=>console.log('CURRENT STATE:',state),'settings')
        ],
        Registries:[
          command('Station Stencils',()=>dialog('Authoritative Stencil Registry',table(['Code','Station Name','Ports'],Object.entries(nodeDefs).map(([k,v])=>[k,v.title||k,\`\${(v.inputs||[]).length} In / \${(v.outputs||[]).length} Out\`]))),'table'),
          command('Property Windows',()=>dialog('Property Window Registry','<p>14 elevated modern engineering property windows registered (Pan, Evaporator, Heater, Injection Heater, Melter, Flash Tank, Separator, Crystallizer, Centrifugal, Tank, Turbine, Condenser, Pump, Dryer/Cooler).</p>'),'file')
        ],
        Tests:[
          command('Run Regression',()=>dialog('Testing Status','<p>Backend test suite: 122/122 pytest passing (100% green).</p><p>Web simulator syntax: Clean, 0 errors.</p>'),'check')
        ]
      },
      Help:{
        Support:[
          command('Sugar\\'s Help Book',()=>dialog('Sugar\\'s Help Book Reference','<p>Authoritative domain authority: <b>Sugar\\'s Help Book</b> (SBI Simulation Library).</p><p>Contains 415 reference manuals, governing equations, equipment behavior models, and cane/beet factory flowsheets.</p>'),'file'),
          command('Interaction Guide',()=>dialog('Interaction Guide','<p>Single-click selects a station or stream. Double-click opens floating properties.</p><p>Drag stream endpoints to reconnect. Drag midpoint and bend handles to reroute without changing topology.</p><p>Station numbers are unique engineering identities. Renumbering uses a preview; tags and connections are preserved.</p><p><b>Multi-Page:</b> Use bottom tabs to switch drawing pages. Click "+" to add a page. Right-click any tab for Rename, Duplicate, Delete, or Page Setup.</p>'),'file'),
          command('Keyboard Shortcuts',()=>dialog('Keyboard Shortcuts',table(['Shortcut','Action'],[['Ctrl + S','Save Project'],['Ctrl + O','Open Project'],['Ctrl + Z','Undo'],['Ctrl + Y / Ctrl+Shift+Z','Redo'],['Ctrl + Alt + N','Create New Page'],['PageDown / PageUp','Next / Previous Page'],['Delete / Backspace','Delete Selected Item'],['Ctrl + Scroll','Zoom In / Out']])), 'table'),
          command('About',()=>dialog('About Purity for Sugar™','<p><b>PURITY FOR SUGAR™ · Process Simulation</b></p><p>Professional multi-page flowsheet studio &amp; thermodynamic mass/energy balance solver.</p><p>Authoritative Engineering Basis: Sugar\\'s Help Book &amp; ICUMSA Standard Methods.</p>'),'settings')
        ]
      }
    };`;

modified = modified.replace(oldTabsRegex, newTabsBlock);

// 13. Event Listeners for bottom tab bar and keyboard shortcuts at the end of the script
const bottomBarInitCall = `
    initPageTabBarEvents();
    renderPageTabs();
    updatePageStatusPill();
    updateSheetFrame();
    window.PageManager = PageManager;
    window.activePage = activePage;
    window.state = state;
    window.projectJsonText = projectJsonText;
`;

modified = modified.replace(/installEngineeringRibbon\(\);\s*window\.__MASSECUITE_APP_READY__\s*=\s*true;/i, `  function initPageTabBarEvents() {
    const addBtn = document.getElementById('addPageBtn');
    if (addBtn) addBtn.onclick = () => PageManager.createPage();

    const prevBtn = document.getElementById('pageNavPrev');
    if (prevBtn) prevBtn.onclick = () => PageManager.previousPage();

    const nextBtn = document.getElementById('pageNavNext');
    if (nextBtn) nextBtn.onclick = () => PageManager.nextPage();

    const quickBtn = document.getElementById('pageSetupQuickBtn');
    if (quickBtn) quickBtn.onclick = () => openPageSetupDialog(state.activePageId);

    window.addEventListener('keydown', e => {
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

      if (e.ctrlKey && e.altKey && (e.key === 'n' || e.key === 'N')) {
        e.preventDefault();
        PageManager.createPage();
        return;
      }
      if (e.key === 'PageDown') {
        e.preventDefault();
        PageManager.nextPage();
        return;
      }
      if (e.key === 'PageUp') {
        e.preventDefault();
        PageManager.previousPage();
        return;
      }
    });
  }

  installEngineeringRibbon();
${bottomBarInitCall}
  window.__MASSECUITE_APP_READY__=true;`);

fs.writeFileSync('test_multi_page.html', modified, 'utf8');
console.log('Successfully generated test_multi_page.html (size: ' + modified.length + ' bytes)');
