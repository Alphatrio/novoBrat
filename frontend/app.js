const API_BASE = 'http://localhost:5000';
const labels = ['PERSON', 'ORG', 'LOC'];
const labelColors = {
  PERSON: '#ffd54f',
  ORG: '#81c784',
  LOC: '#4fc3f7'
};

let documentText = '';
let annotations = [];

const textEl = document.getElementById('text');
const menuEl = document.getElementById('label-menu');

function escapeHtml(str) {
  return str.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
}

function renderText() {
  if (!documentText) return;
  annotations.sort((a, b) => a.start - b.start);
  let html = '';
  let last = 0;
  annotations.forEach(a => {
    html += escapeHtml(documentText.slice(last, a.start));
    const color = labelColors[a.label] || '#ffd54f';
    html += `<span class="entity" data-id="${a.id || ''}" style="background:${color}">` +
            `${escapeHtml(documentText.slice(a.start, a.end))}` +
            `<span class="label">${a.label}</span></span>`;
    last = a.end;
  });
  html += escapeHtml(documentText.slice(last));
  textEl.innerHTML = html;
}

function loadDocument() {
  fetch(`${API_BASE}/documents/1`)
    .then(r => r.json())
    .then(doc => {
      documentText = doc.text || '';
      renderText();
      loadAnnotations();
    })
    .catch(() => {
      documentText = 'Sample text to annotate.';
      renderText();
      loadAnnotations();
    });
}

function loadAnnotations() {
  fetch(`${API_BASE}/annotations`)
    .then(r => r.json())
    .then(data => {
      annotations = data.map(a => ({id: a.id, start: a.start, end: a.end, label: a.label}));
      renderText();
    })
    .catch(() => {});
}

function saveAnnotation(ann) {
  fetch(`${API_BASE}/annotations`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(ann)
  })
    .then(r => r.json())
    .then(data => { ann.id = data.id; })
    .catch(() => {});
}

function hideMenu() {
  menuEl.classList.add('hidden');
}

function showMenu(x, y, selection) {
  menuEl.innerHTML = '';
  labels.forEach(label => {
    const btn = document.createElement('button');
    btn.textContent = label;
    btn.onclick = () => {
      const ann = {start: selection.start, end: selection.end, label};
      annotations.push(ann);
      renderText();
      saveAnnotation(ann);
      hideMenu();
    };
    menuEl.appendChild(btn);
  });
  menuEl.style.left = `${x}px`;
  menuEl.style.top = `${y}px`;
  menuEl.classList.remove('hidden');
}

function getSelectionOffsets() {
  const sel = window.getSelection();
  if (sel.rangeCount === 0) return null;
  const range = sel.getRangeAt(0);
  if (!textEl.contains(range.commonAncestorContainer)) return null;
  const pre = range.cloneRange();
  pre.selectNodeContents(textEl);
  pre.setEnd(range.startContainer, range.startOffset);
  const start = pre.toString().length;
  const end = start + range.toString().length;
  return {start, end};
}

textEl.addEventListener('mouseup', () => {
  const offsets = getSelectionOffsets();
  const selection = window.getSelection();
  if (offsets && offsets.start !== offsets.end) {
    const rect = selection.getRangeAt(0).getBoundingClientRect();
    showMenu(rect.right + window.scrollX, rect.bottom + window.scrollY, offsets);
  } else {
    hideMenu();
  }
});

document.addEventListener('click', (e) => {
  if (!menuEl.contains(e.target)) {
    hideMenu();
  }
});

loadDocument();
