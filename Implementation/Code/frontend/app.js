const state = { mode: 'encrypt', file: null };
const $ = (selector) => document.querySelector(selector);
const dropZone = $('#drop-zone');
const fileInput = $('#file-input');
const processing = $('#processing');

function setFile(file) {
  if (!file) return;
  state.file = file;
  $('#drop-title').textContent = file.name;
  $('#file-detail').textContent = `${file.type || 'FILE'}  ·  ${formatSize(file.size)}`;
  $('#file-detail').classList.remove('hidden');
  dropZone.classList.add('has-file');
}
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}
function setMode(mode) {
  state.mode = mode;
  document.querySelectorAll('.mode').forEach(button => button.classList.toggle('active', button.dataset.mode === mode));
  $('#submit-label').textContent = mode === 'encrypt' ? 'Encrypt file' : 'Decrypt file';
  $('.confirm-field').style.display = mode === 'encrypt' ? 'block' : 'none';
  $('#password').autocomplete = mode === 'encrypt' ? 'new-password' : 'current-password';
}
function updateStrength() {
  const value = $('#password').value;
  const score = Math.min(100, value.length * 7 + (/[A-Z]/.test(value) ? 12 : 0) + (/[0-9]/.test(value) ? 12 : 0) + (/[^A-Za-z0-9]/.test(value) ? 12 : 0));
  const bar = $('#strength-bar');
  bar.style.width = `${score}%`;
  bar.style.background = score > 75 ? '#55aa83' : score > 45 ? '#e3b665' : '#db806d';
  $('#strength-text').textContent = !value ? 'Use 12+ characters for a stronger vault key' : score > 75 ? 'Strong passphrase' : score > 45 ? 'Good start, add more variety' : 'Keep going, longer is stronger';
}
$('#browse').addEventListener('click', () => fileInput.click());
dropZone.addEventListener('click', event => { if (event.target !== $('#browse')) fileInput.click(); });
fileInput.addEventListener('change', () => setFile(fileInput.files[0]));
['dragenter', 'dragover'].forEach(eventName => dropZone.addEventListener(eventName, event => {
  event.preventDefault();
  event.stopPropagation();
  dropZone.classList.add('dragging');
}));
['dragleave', 'drop'].forEach(eventName => dropZone.addEventListener(eventName, event => {
  event.preventDefault();
  event.stopPropagation();
  dropZone.classList.remove('dragging');
}));
dropZone.addEventListener('drop', event => setFile(event.dataTransfer.files[0]));
document.addEventListener('dragover', event => event.preventDefault());
document.addEventListener('drop', event => event.preventDefault());
document.querySelectorAll('.mode').forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode)));
document.querySelectorAll('.eye').forEach(button => button.addEventListener('click', () => { const input = $(`#${button.dataset.target}`); input.type = input.type === 'password' ? 'text' : 'password'; }));
$('#password').addEventListener('input', updateStrength);
$('#vault-form').addEventListener('submit', async event => {
  event.preventDefault();
  const status = $('#status'); const password = $('#password').value;
  status.className = 'status'; status.textContent = '';
  if (!state.file || !password) { status.textContent = 'Choose a file and enter a password first.'; return; }
  if (state.mode === 'encrypt' && password !== $('#confirm').value) { status.textContent = 'The passwords do not match.'; return; }
  const button = $('#submit'); button.disabled = true; $('#submit-label').textContent = state.mode === 'encrypt' ? 'Encrypting...' : 'Decrypting...';
  processing.classList.remove('hidden');
  $('#processing-title').textContent = state.mode === 'encrypt' ? 'Securing your file' : 'Restoring your file';
  const form = new FormData(); form.append('file', state.file); form.append('password', password); form.append('operation', state.mode);
  try {
    const response = await fetch('/api/process', { method: 'POST', body: form });
    if (!response.ok) { const error = await response.json(); throw new Error(error.error || 'Operation failed.'); }
    const blob = await response.blob(); const disposition = response.headers.get('Content-Disposition') || ''; const match = disposition.match(/filename="?([^";]+)"?/); const filename = match ? match[1] : `${state.file.name}.enc`;
    const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = filename; link.click(); URL.revokeObjectURL(link.href);
    status.className = 'status success'; status.textContent = `Complete. ${filename} is ready in your downloads.`;
  } catch (error) { status.textContent = error.message; } finally { processing.classList.add('hidden'); button.disabled = false; $('#submit-label').textContent = state.mode === 'encrypt' ? 'Encrypt file' : 'Decrypt file'; }
});
