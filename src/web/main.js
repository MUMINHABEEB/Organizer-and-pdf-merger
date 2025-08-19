console.log('[MAIN_JS] loaded');
const statusEl = document.getElementById('status');
if(statusEl){
  statusEl.textContent = 'main.js loaded';
} else {
  document.body.insertAdjacentHTML('afterbegin','<div style="color:#f55">status element missing</div>');
}
// Simple button test
const dryBtn = document.getElementById('runDryBtn');
if(dryBtn){
  dryBtn.addEventListener('click', ()=>{
    console.log('[MAIN_JS] Dry Run click');
    const sum = document.getElementById('orgSummary');
    sum.style.display='block';
    sum.textContent='JS is working (test message).';
    statusEl.textContent='Dry run test clicked';
  });
}

(function(){
  const $ = s => document.querySelector(s);
  const statusEl = $('#status');
  const runDryBtn = $('#runDryBtn');
  const runRealBtn = $('#runRealBtn');
  const folderInput = $('#folderInput');
  const schemeSel = $('#scheme');
  const orgSummary = $('#orgSummary');
  const orgStats = $('#orgStats');
  const orgFolderStats = document.getElementById('orgFolderStats');
  const orgRaw = $('#orgRawJson');
  const toggleRawBtn = $('#toggleRawBtn');
  const orgHint = $('#orgHint');
  const orgDetailsTools = document.getElementById('orgDetailsTools');
  const orgFilterInput = document.getElementById('orgFilter');
  const orgExportCsvBtn = document.getElementById('orgExportCsvBtn');
  const orgFilterCount = document.getElementById('orgFilterCount');
  const orgDetailsTable = document.getElementById('orgDetailsTable');
  const orgProgressWrap = document.getElementById('orgProgress');
  const orgProgressBar = document.getElementById('orgProgressBar');
  const orgProgressLabel = document.getElementById('orgProgressLabel');
  const orgCancelBtn = document.getElementById('orgCancelBtn');
  let orgLogs = [];
  let orgProgressTimer = null;
  const mergeResult = $('#mergeResult');
  // === PDF Merge New Grid ===
  const pdfGrid = document.getElementById('pdfGrid');
  const pdfMergeBtn = document.getElementById('pdfMergeBtn');
  const pdfUpBtn = document.getElementById('pdfUpBtn');
  const pdfDownBtn = document.getElementById('pdfDownBtn');
  const pdfRemoveBtn = document.getElementById('pdfRemoveBtn');
  const pdfRemoveAllBtn = document.getElementById('pdfRemoveAllBtn');
  let pdfItems = []; // [{path, name, canvasReady:false, loading:true, error:null}]
  let pdfSelectedIndex = -1;

  function escapeHtml(str){
    return str.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
  }

  function setStatus(msg){ statusEl.textContent = msg; }
  // Toast system
  const toastContainer = document.getElementById('toastContainer');
  function toast(message, opts={}){
    if(!toastContainer) { console.warn('toast:', message); return; }
    const {type='info', timeout=5000, actions=[]} = opts;
    const el = document.createElement('div');
    el.className = 'toast '+(type==='error'?'err':type==='warn'?'warn':type==='success'?'good':'');
    el.innerHTML = `<div class="t-msg"></div><div style="display:flex;align-items:flex-start;gap:4px;">${actions.map((a,i)=>`<button data-i="${i}">${a.label}</button>`).join('')}<button data-close>×</button></div>`;
    el.querySelector('.t-msg').textContent = message;
    toastContainer.appendChild(el);
    const timer = timeout? setTimeout(()=>dismiss(), timeout):null;
    function dismiss(){ if(timer) clearTimeout(timer); if(el.parentNode) el.parentNode.removeChild(el); }
    el.addEventListener('click', e=>{
      if(e.target.matches('button[data-close]')){ dismiss(); }
      const btn = e.target.closest('button[data-i]');
      if(btn){ const idx=parseInt(btn.getAttribute('data-i')); try{ actions[idx].onClick?.(); }catch{} dismiss(); }
    });
    return dismiss;
  }
  function apiReady(){
    if(!window.pywebview || !window.pywebview.api) throw new Error('API not ready');
    return window.pywebview.api;
  }

  // Tabs
  function switchTab(tab){
    document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('active', b.getAttribute('data-tab')===tab));
    document.querySelectorAll('section.panel').forEach(sec=>{
      const active = sec.id === 'tab-'+tab;
      if(active){ sec.classList.add('active'); sec.style.display='block'; }
      else { sec.classList.remove('active'); sec.style.display='none'; }
    });
    setStatus('Ready');
  }
  document.querySelectorAll('#tabs button').forEach(btn=>{
    btn.addEventListener('click', ()=> switchTab(btn.getAttribute('data-tab')) );
  });
  // Home CTA buttons
  document.querySelectorAll('[data-goto]').forEach(el=>{
    el.addEventListener('click', ()=>{
      const target = el.getAttribute('data-goto');
      if(target==='services') switchTab('services');
      else if(target) switchTab(target);
    });
  });

  window.addEventListener('pywebviewready', ()=>setStatus('Ready'));
  // Settings load after pywebviewready
  window.addEventListener('pywebviewready', async () => {
    try {
      const s = await apiReady().load_settings();
      const lf = document.getElementById('setLastFolder');
      const ps = document.getElementById('setPreferredScheme');
      const th = document.getElementById('setTheme');
      const ao = document.getElementById('setAutoOpenMerged');
      if(lf && typeof s.last_folder === 'string') lf.value = s.last_folder;
      if(ps && s.preferred_scheme) ps.value = s.preferred_scheme;
      if(th && s.theme) th.value = s.theme;
      if(ao && typeof s.auto_open_merged === 'boolean') ao.checked = s.auto_open_merged;
      const st = document.getElementById('settingsStatus');
      if(st) st.textContent = 'Loaded';
      // Apply scheme to organizer select if empty
      if(schemeSel && !schemeSel.value && s.preferred_scheme){
        schemeSel.value = s.preferred_scheme;
      }
      applyTheme(s.theme || 'dark');
      // About info
      try {
        const info = await apiReady().app_info();
        const aboutBox = document.getElementById('aboutInfo');
        if(aboutBox){
          aboutBox.textContent = `Version: ${info.version}\nPython: ${info.python}\nPlatform: ${info.platform}\nBackend: ${info.backend_used || 'n/a'}`;
        }
      } catch(e){}
    } catch(e){
      const st = document.getElementById('settingsStatus');
      if(st) st.textContent = 'Load error: '+e.message;
    }
  });

  // Debounced save
  let saveTimer = null;
  function queueSave(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(async ()=>{
      try{
        const payload = {
          last_folder: document.getElementById('setLastFolder')?.value || '',
            preferred_scheme: document.getElementById('setPreferredScheme')?.value || 'standard',
          theme: document.getElementById('setTheme')?.value || 'dark',
          auto_open_merged: !!document.getElementById('setAutoOpenMerged')?.checked
        };
        const st = document.getElementById('settingsStatus');
        if(st) st.textContent = 'Saving…';
        const r = await apiReady().save_settings(payload);
        if(st) st.textContent = r && r.ok ? 'Saved' : 'Save error';
  applyTheme(payload.theme);
      }catch(e){
        const st = document.getElementById('settingsStatus');
        if(st) st.textContent = 'Save error: '+e.message;
      }
    }, 450);
  }
  ['setLastFolder','setPreferredScheme','setTheme','setAutoOpenMerged'].forEach(id=>{
    const el = document.getElementById(id);
    if(!el) return;
    const evt = el.type === 'checkbox' ? 'change' : 'input';
    el.addEventListener(evt, queueSave);
  });

  function applyTheme(theme){
    if(theme === 'light'){
      document.body.classList.add('light');
    } else {
      document.body.classList.remove('light');
    }
    const logo = document.getElementById('logoImg');
    if(logo){
      const light = '../resources/images/ramidos_logo_dark.png';
      const dark = '../resources/images/ramidos_logo_light.png';
      logo.setAttribute('src', document.body.classList.contains('light') ? dark : light);
    }
  }

  // Organizer dry run
  runDryBtn && runDryBtn.addEventListener('click', async ()=>{
    const path = folderInput.value.trim();
  if(!path){ toast('Enter a folder path',{type:'warn'}); return; }
    orgSummary.style.display='none';
    runDryBtn.disabled = true;
    runRealBtn.disabled = true;
    showOrgProgress(0,0,'Starting…');
    setStatus('Dry run starting…');
    try {
      const resp = await apiReady().organize(path, true, schemeSel.value);
      if(resp.status === 'started'){
        pollResult(true);
        startProgressPolling();
      } else {
        showSummary(resp);
      }
    } catch(e){
      showSummary({error:e.message});
      runDryBtn.disabled = false;
      hideOrgProgress();
    }
  });

  // Organizer commit
  runRealBtn && runRealBtn.addEventListener('click', async ()=>{
    const path = folderInput.value.trim();
  if(!path){ toast('Enter a folder path',{type:'warn'}); return; }
    if(!confirm('Proceed with actual organize?')) return;
    orgSummary.style.display='none';
    runDryBtn.disabled = true;
    runRealBtn.disabled = true;
    showOrgProgress(0,0,'Starting…');
    setStatus('Commit starting…');
    try {
      const resp = await apiReady().organize(path, false, schemeSel.value);
      if(resp.status === 'started'){
        pollResult(false);
        startProgressPolling();
      } else {
        showSummary(resp);
      }
    } catch(e){
      showSummary({error:e.message});
      hideOrgProgress();
    }
  });

  function pollResult(isDry){
    const start = Date.now();
    const id = setInterval(async ()=>{
      try {
        const r = await apiReady().last_result();
        if(r){
          clearInterval(id);
          setStatus('Done in '+(Date.now()-start)+' ms');
          showSummary(r);
          runDryBtn.disabled = false;
          runRealBtn.disabled = false;
          if(isDry) runRealBtn.disabled = false;
          stopProgressPolling();
          hideOrgProgress();
        }
      } catch {
        clearInterval(id);
        setStatus('Polling failed');
        runDryBtn.disabled = false;
        stopProgressPolling();
        hideOrgProgress();
      }
    }, 600);
  }

  function showOrgProgress(done,total,label){
    if(!orgProgressWrap) return;
    orgProgressWrap.style.display='flex';
    if(total>0){
      const pct = Math.min(100, Math.round((done/total)*100));
      if(orgProgressBar) orgProgressBar.style.width = pct+'%';
      if(orgProgressLabel) orgProgressLabel.textContent = `${done} / ${total} (${pct}%)`;
    } else {
      if(orgProgressBar) orgProgressBar.style.width = '0%';
      if(orgProgressLabel) orgProgressLabel.textContent = label || '0 / 0';
    }
  }
  function hideOrgProgress(){ if(orgProgressWrap) orgProgressWrap.style.display='none'; }

  async function pollOrganizerProgress(){
    try{
      const p = await apiReady().organizer_progress();
      if(p && p.running){
        showOrgProgress(p.done||0, p.total||0);
      } else {
        stopProgressPolling();
      }
    }catch{
      // ignore
    }
  }
  function startProgressPolling(){
    stopProgressPolling();
    pollOrganizerProgress();
    orgProgressTimer = setInterval(pollOrganizerProgress, 500);
    if(orgCancelBtn){
      orgCancelBtn.disabled = false;
    }
  }
  function stopProgressPolling(){
    if(orgProgressTimer){ clearInterval(orgProgressTimer); orgProgressTimer=null; }
    if(orgCancelBtn){ orgCancelBtn.disabled=true; }
  }
  orgCancelBtn && orgCancelBtn.addEventListener('click', async ()=>{
    try{ await apiReady().organizer_cancel(); toast('Cancellation requested',{type:'warn'}); }catch{}
    orgCancelBtn.disabled = true;
  });

  function showSummary(data){
    // Show stat grid + summary text
    const core = {
      moved: data.moved || 0,
      copied_only: data.copied_only || 0,
      skipped: data.skipped || 0,
      errors: data.errors || 0,
      total: data.total || 0
    };
    let grid = '<div class="stat-grid">';
    const statDef = [
      ['Moved','moved','good'],
      ['Copied','copied_only','good'],
      ['Skipped','skipped','warn'],
      ['Errors','errors','err'],
      ['Total','total','']
    ];
    statDef.forEach(([label,key,cls])=>{
      grid += `<div class="stat ${cls}"><h3>${label}</h3><div class="value">${core[key]}</div></div>`;
    });
    grid += '</div>';
    orgStats.innerHTML = grid;
    orgStats.style.display='block';
    orgSummary.style.display='block';
    orgSummary.textContent = data.error ? ('Error: '+data.error) : 'Dry run result. Use Commit to apply changes.';
    // Raw JSON
    orgRaw.textContent = JSON.stringify(data, null, 2);
    // Toggle button logic
    toggleRawBtn.style.display='inline-block';
    toggleRawBtn.textContent = 'Show Raw JSON';
    orgRaw.style.display='none';
    toggleRawBtn.onclick = () => {
      const show = orgRaw.style.display==='none';
      orgRaw.style.display = show? 'block':'none';
      toggleRawBtn.textContent = show? 'Hide Raw JSON':'Show Raw JSON';
    };
    // Enable commit if dry run and no error
    if(!data.error && runRealBtn) {
      runRealBtn.disabled = false;
      orgHint.style.display='inline';
    }

    // Render details table if logs present
    if(Array.isArray(data.logs) && data.logs.length){
      orgLogs = data.logs;
      orgDetailsTools.style.display='flex';
      orgDetailsTable.style.display='block';
      renderOrgDetails();
  buildFolderView();
    }
  }

  function renderOrgDetails(){
    if(!orgLogs.length){ orgDetailsTable.innerHTML=''; return; }
    const filter = (orgFilterInput?.value||'').trim().toLowerCase();
    let shown = orgLogs;
    if(filter){
      shown = orgLogs.filter(l=>{
        const st = l.error? 'error' : l.skipped? 'skipped' : (l.reason||'moved');
        return (l.file||'').toLowerCase().includes(filter) || (l.to||'').toLowerCase().includes(filter) || st.toLowerCase().includes(filter);
      });
    }
    const rows = shown.slice(0,1000).map(log=>{
      const file = escapeHtml(log.file||'');
      const to = escapeHtml((log.to||'').toString());
      let status = 'MOVED';
      if(log.skipped) status = 'SKIPPED';
      if(log.error) status = 'ERROR';
      if(log.reason) status = log.reason.toUpperCase();
      let badgeClass = 'badge-move';
      if(status.startsWith('SKIP')) badgeClass='badge-skip';
      else if(status==='ERROR') badgeClass='badge-err';
      else if(status.includes('COPY')) badgeClass='badge-copy';
      return `<tr><td>${file}</td><td>${to||''}</td><td><span class="badge-status ${badgeClass}">${escapeHtml(status)}</span></td></tr>`;
    }).join('');
    orgDetailsTable.innerHTML = `<div class="details-wrap" style="max-height:340px;"><table class="detail-table"><thead><tr><th style="width:46%">File</th><th style="width:46%">Destination</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div><div class="details-hint">Showing ${Math.min(shown.length,1000)} of ${shown.length} matched (Total logs: ${orgLogs.length}).</div>`;
    if(orgFilterCount){ orgFilterCount.textContent = filter? `${shown.length} match(es)` : `${orgLogs.length} total`; }
  }

  function buildFolderView(){
    if(!orgLogs.length){ orgFolderStats.style.display='none'; return; }
    // Aggregate by destination top-level client/type path fragment (up to client folder)
    const folders = new Map();
    orgLogs.forEach(l=>{
      if(!l.to) return;
      const parts = String(l.to).split(/\\|\//).filter(Boolean);
      // Capture last 4 segments (year, month, day, client) if present
      let key = parts.slice(-4,-3).join('/');
      // Better: join year/month/day/client
      if(parts.length>=4){
        key = parts.slice(-5).join('/');
      }
      if(!key) key = '(unknown)';
      const rec = folders.get(key) || {folder:key,total:0,moved:0,skipped:0,errors:0};
      rec.total += 1;
      if(l.error) rec.errors += 1; else if(l.skipped) rec.skipped += 1; else rec.moved += 1;
      folders.set(key, rec);
    });
    const rows = [...folders.values()].sort((a,b)=>b.total-a.total).slice(0,500).map(r=>{
      return `<tr data-folder="${r.folder}"><td>${r.folder}</td><td>${r.total}</td><td>${r.moved}</td><td>${r.skipped}</td><td>${r.errors}</td></tr>`;
    }).join('');
    orgFolderStats.style.display='block';
    orgFolderStats.innerHTML = `<div style="font-size:12px;color:var(--muted);margin-bottom:4px;">Folders summary (click a row to filter details)</div><div class="details-wrap" style="max-height:200px;">\n<table class="detail-table"><thead><tr><th>Folder</th><th>Total</th><th>Moved</th><th>Skipped</th><th>Errors</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    orgFolderStats.querySelectorAll('tbody tr').forEach(tr=>{
      tr.addEventListener('click', ()=>{
        const f = tr.getAttribute('data-folder');
        if(!f) return;
        orgFilterInput.value = f.split('/').pop();
        renderOrgDetails();
      });
    });
  }

  orgFilterInput && orgFilterInput.addEventListener('input', ()=>{
    renderOrgDetails();
  });

  orgExportCsvBtn && orgExportCsvBtn.addEventListener('click', ()=>{
    if(!orgLogs.length) return;
    const header = ['file','destination','status','error'];
    const lines = [header.join(',')];
    orgLogs.forEach(l=>{
      let status = l.error? 'ERROR' : l.skipped? 'SKIPPED' : l.reason? String(l.reason).toUpperCase() : 'MOVED';
      const row = [l.file||'', l.to||'', status, l.error||''].map(val=>`"${String(val).replace(/"/g,'""')}"`).join(',');
      lines.push(row);
    });
    const blob = new Blob([lines.join('\n')], {type:'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'organizer_logs.csv'; a.click();
    setTimeout(()=>URL.revokeObjectURL(url), 5000);
  });

  // Legacy simple PDF merge UI removed (replaced by advanced button set)

  // Dynamically load PDF.js (slim) via CDN once
  let pdfjsReady = null;
  async function ensurePdfJs(){
    if(pdfjsReady) return pdfjsReady;
    pdfjsReady = new Promise((resolve, reject)=>{
      const s = document.createElement('script');
      s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.min.js';
      s.onload = ()=>{
        if(window['pdfjsLib']){
          window['pdfjsLib'].GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.worker.min.js';
          resolve(window['pdfjsLib']);
        } else reject(new Error('pdfjsLib missing'));
      };
      s.onerror = ()=>reject(new Error('Failed to load pdf.js'));
      document.head.appendChild(s);
    });
    return pdfjsReady;
  }

  function renderPdfGrid(){
    if(!pdfGrid) return;
    pdfGrid.innerHTML = '';
    // Add existing items
    pdfItems.forEach((item, idx)=>{
      const card = document.createElement('div');
      card.className = 'pdf-card'+(idx===pdfSelectedIndex?' active':'');
      card.dataset.idx = String(idx);
  card.setAttribute('draggable','true');
      card.innerHTML = `<div class="pdf-badge">${idx+1}</div><button class="pdf-remove-btn" data-remove="${idx}">Remove</button><div class="pdf-thumb"><canvas style="display:${item.canvasReady?'block':'none'}"></canvas></div><div class="pdf-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>`;
      pdfGrid.appendChild(card);
      if(item.loading){
        const overlay = document.createElement('div');
        overlay.style.position='absolute';
        overlay.style.top='0';overlay.style.left='0';overlay.style.right='0';overlay.style.bottom='0';
        overlay.style.display='flex';overlay.style.alignItems='center';overlay.style.justifyContent='center';
        overlay.style.fontSize='12px';overlay.style.color='var(--muted)';
        overlay.textContent = item.error? 'Error' : 'Loading…';
        card.appendChild(overlay);
        item._overlay = overlay;
      }
    });
    // Add the Add card
    const addCard = document.createElement('div');
    addCard.className = 'pdf-add-card';
    addCard.id = 'pdfAddCard';
    addCard.innerHTML = '<div class="pdf-add-plus">+</div><div style="font-size:12px;font-weight:500;letter-spacing:.5px;">Add more files</div>';
    pdfGrid.appendChild(addCard);
    pdfMergeBtn.disabled = pdfItems.length < 2;
  }

  function selectIndex(i){
    pdfSelectedIndex = i;
    renderPdfGrid();
  }

  async function addFiles(paths){
    if(!paths || !paths.length) return;
    const newOnes = [];
    paths.forEach(p=>{
      if(!pdfItems.some(it=>it.path===p)){
        newOnes.push({path:p, name:p.split(/[/\\\\]/).pop(), loading:true, canvasReady:false, error:null});
      }
    });
    if(!newOnes.length){
      selectIndex(pdfItems.length?pdfItems.length-1:-1);
      return;
    }
    pdfItems.push(...newOnes);
    selectIndex(pdfItems.length-1);
    // Start rendering thumbnails
    ensurePdfJs().then(async pdfjs=>{
      for(const item of newOnes){
        try{
          const loadingTask = pdfjs.getDocument(item.path);
          const pdf = await loadingTask.promise;
            const page = await pdf.getPage(1);
          const viewport = page.getViewport({scale:0.3});
          const cardIdx = pdfItems.indexOf(item);
          const cardEl = pdfGrid.querySelector(`.pdf-card[data-idx="${cardIdx}"]`);
          if(!cardEl) continue;
          const canvas = cardEl.querySelector('canvas');
          canvas.width = viewport.width; canvas.height = viewport.height;
          const ctx = canvas.getContext('2d');
          await page.render({canvasContext:ctx, viewport}).promise;
          item.loading=false; item.canvasReady=true;
          if(item._overlay) item._overlay.remove();
        }catch(err){
          console.warn('Thumbnail error', err);
          item.loading=false; item.error=String(err);
          if(item._overlay){ item._overlay.textContent='Error'; }
        }
      }
    }).catch(err=>console.warn('pdf.js load/render failed', err));
  }

  // Event delegation
  pdfGrid && pdfGrid.addEventListener('click', e=>{
    const removeBtn = e.target.closest('button.pdf-remove-btn');
    if(removeBtn){
      const idx = parseInt(removeBtn.getAttribute('data-remove'));
      if(!isNaN(idx)){
        pdfItems.splice(idx,1);
        if(pdfSelectedIndex>=pdfItems.length) pdfSelectedIndex = pdfItems.length-1;
        renderPdfGrid();
      }
      return;
    }
    const card = e.target.closest('.pdf-card');
    if(card){
      selectIndex(parseInt(card.dataset.idx));
      return;
    }
    if(e.target.closest('#pdfAddCard')){
      openAddDialog();
    }
  });

  // Double-click to open PDF (requires backend open_path)
  pdfGrid && pdfGrid.addEventListener('dblclick', e=>{
    const card = e.target.closest('.pdf-card');
    if(!card) return;
    const idx = parseInt(card.dataset.idx);
    if(isNaN(idx) || !pdfItems[idx]) return;
    apiReady().open_path(pdfItems[idx].path).catch(()=>{});
  });

  // Drag & Drop reordering
  let dragIndex = null;
  pdfGrid && pdfGrid.addEventListener('dragstart', e=>{
    const card = e.target.closest('.pdf-card');
    if(!card) return;
    dragIndex = parseInt(card.dataset.idx);
    e.dataTransfer.effectAllowed = 'move';
    try{ e.dataTransfer.setData('text/plain', String(dragIndex)); }catch(_){ }
  });
  pdfGrid && pdfGrid.addEventListener('dragover', e=>{
    if(dragIndex==null) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    const over = e.target.closest('.pdf-card');
    pdfGrid.querySelectorAll('.pdf-card.drag-over').forEach(el=>el.classList.remove('drag-over'));
    if(over && over.dataset.idx !== undefined && parseInt(over.dataset.idx)!==dragIndex){
      over.classList.add('drag-over');
    }
  });
  pdfGrid && pdfGrid.addEventListener('dragleave', e=>{
    const card = e.target.closest('.pdf-card');
    if(card) card.classList.remove('drag-over');
  });
  pdfGrid && pdfGrid.addEventListener('drop', e=>{
    if(dragIndex==null) return;
    e.preventDefault();
    const targetCard = e.target.closest('.pdf-card');
    pdfGrid.querySelectorAll('.pdf-card.drag-over').forEach(el=>el.classList.remove('drag-over'));
    if(!targetCard){ dragIndex=null; return; }
    const dropIndex = parseInt(targetCard.dataset.idx);
    if(!isNaN(dropIndex) && dropIndex!==dragIndex){
      const [moved] = pdfItems.splice(dragIndex,1);
      pdfItems.splice(dropIndex,0,moved);
      selectIndex(dropIndex);
    }
    dragIndex=null;
  });

  // Keyboard shortcuts (when PDF tab active)
  document.addEventListener('keydown', e=>{
    const pdfTabActive = document.getElementById('tab-pdf')?.classList.contains('active');
    if(!pdfTabActive) return;
    if(!pdfItems.length) return;
    // Navigation
    if(['ArrowLeft','ArrowUp'].includes(e.key)){
      if(pdfSelectedIndex>0){ selectIndex(pdfSelectedIndex-1); e.preventDefault(); }
    } else if(['ArrowRight','ArrowDown'].includes(e.key)){
      if(pdfSelectedIndex < pdfItems.length-1){ selectIndex(pdfSelectedIndex+1); e.preventDefault(); }
    } else if(e.key==='Delete'){
      if(pdfSelectedIndex>=0){ pdfItems.splice(pdfSelectedIndex,1); selectIndex(Math.min(pdfSelectedIndex,pdfItems.length-1)); e.preventDefault(); }
    } else if(e.key==='Home'){
      selectIndex(0); e.preventDefault();
    } else if(e.key==='End'){
      selectIndex(pdfItems.length-1); e.preventDefault();
    } else if(e.key==='Enter'){
      // Enter starts merge if enabled
      if(!pdfMergeBtn.disabled){ pdfMergeBtn.click(); }
    } else if((e.ctrlKey||e.metaKey) && (e.key==='ArrowUp' || e.key==='ArrowLeft')){
      // reorder up
      if(pdfSelectedIndex>0){ const i=pdfSelectedIndex; [pdfItems[i-1],pdfItems[i]]=[pdfItems[i],pdfItems[i-1]]; selectIndex(i-1); e.preventDefault(); }
    } else if((e.ctrlKey||e.metaKey) && (e.key==='ArrowDown' || e.key==='ArrowRight')){
      if(pdfSelectedIndex>=0 && pdfSelectedIndex < pdfItems.length-1){ const i=pdfSelectedIndex; [pdfItems[i+1],pdfItems[i]]=[pdfItems[i],pdfItems[i+1]]; selectIndex(i+1); e.preventDefault(); }
    }
  });

  async function openAddDialog(){
    setStatus('Opening file dialog…');
    try{
      const res = await apiReady().pick_pdfs();
      if(res && Array.isArray(res.files)){
        await addFiles(res.files);
      } else if(res && res.error){
        toast(res.error,{type:'error'});
      }
    }catch(e){ toast(e.message,{type:'error'}); }
    setStatus('Ready');
    renderPdfGrid();
  }

  // Toolbar buttons
  pdfUpBtn && pdfUpBtn.addEventListener('click', ()=>{
    if(pdfSelectedIndex<=0) return;
    const i = pdfSelectedIndex; [pdfItems[i-1], pdfItems[i]] = [pdfItems[i], pdfItems[i-1]]; selectIndex(i-1);
  });
  pdfDownBtn && pdfDownBtn.addEventListener('click', ()=>{
    if(pdfSelectedIndex<0 || pdfSelectedIndex>=pdfItems.length-1) return;
    const i = pdfSelectedIndex; [pdfItems[i+1], pdfItems[i]] = [pdfItems[i], pdfItems[i+1]]; selectIndex(i+1);
  });
  pdfRemoveBtn && pdfRemoveBtn.addEventListener('click', ()=>{
    if(pdfSelectedIndex<0) return; pdfItems.splice(pdfSelectedIndex,1); selectIndex(pdfSelectedIndex>=pdfItems.length?pdfItems.length-1:pdfSelectedIndex);
  });
  pdfRemoveAllBtn && pdfRemoveAllBtn.addEventListener('click', ()=>{
    if(!pdfItems.length) return; if(!confirm('Remove all PDFs?')) return; pdfItems=[]; selectIndex(-1);
  });
  pdfMergeBtn && pdfMergeBtn.addEventListener('click', async ()=>{
    if(pdfItems.length<2) return;
    const ordered = pdfItems.map(it=>it.path);
    setStatus('Choosing output…');
    try{
      const resSave = await apiReady().pick_save_pdf(ordered[0].split(/[/\\\\]/).pop().replace(/\.pdf$/i,'_merged.pdf'));
      if(!resSave || !resSave.output){ setStatus('Merge canceled'); return; }
      setStatus('Merging…');
      const res = await apiReady().merge_pdfs(ordered, resSave.output);
      mergeResult.style.display='block';
      mergeResult.textContent = JSON.stringify(res,null,2);
      setStatus(res.status==='ok'?'Merge complete':'Merge error');
  if(res.error) toast(res.error,{type:'error'});
      if(res.status==='ok'){
        try{ const s = await apiReady().load_settings(); if(s && s.auto_open_merged){ await apiReady().open_path(res.output); } }catch(_){ }
      }
  }catch(e){ toast(e.message,{type:'error'}); setStatus('Merge failed'); }
  });

  renderPdfGrid();

})();