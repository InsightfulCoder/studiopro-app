// --- Modal Logic ---
const authModal = document.getElementById('authModal');
const payModal = document.getElementById('paymentModal');

function openAuth(mode) { if(authModal) { authModal.classList.remove('hidden'); switchMode(mode); } }
function closeAuth() { if(authModal) authModal.classList.add('hidden'); }
function openPayment() { if(payModal) payModal.classList.remove('hidden'); }
function closePayment() { if(payModal) payModal.classList.add('hidden'); }

function switchMode(mode) {
    document.getElementById('loginForm').classList.toggle('hidden', mode !== 'login');
    document.getElementById('registerForm').classList.toggle('hidden', mode !== 'register');
}

// --- Image & Slider Logic ---
let currentFile = null;
const fileInput = document.getElementById('fileInput');

if (fileInput) fileInput.addEventListener('change', (e) => {
    currentFile = e.target.files[0];
    const url = URL.createObjectURL(currentFile);
    document.getElementById('originalImg').src = url;
    document.getElementById('processedImg').src = url; 
});

window.addEventListener('paste', e => {
    if(e.clipboardData.items[0].type.indexOf('image')!==-1) {
        currentFile = e.clipboardData.items[0].getAsFile();
        const url = URL.createObjectURL(currentFile);
        document.getElementById('originalImg').src = url;
        document.getElementById('processedImg').src = url;
    }
});

function moveSlider() {
    const val = document.getElementById('compareSlider').value;
    document.getElementById('foregroundWrapper').style.width = `${val}%`;
    document.getElementById('sliderBtn').style.left = `${val}%`;
}

// --- MAIN GENERATE FUNCTION ---
async function generate() {
    if (!currentFile) return alert("Upload an image first!");
    
    const loader = document.getElementById('loader');
    if(loader) loader.classList.remove('hidden'); 
    
    const fd = new FormData();
    fd.append('file', currentFile);
    const styleInput = document.querySelector('input[name="style"]:checked');
    fd.append('style', styleInput ? styleInput.value : 'cartoon');

    try {
        const res = await fetch('/process', { method: 'POST', body: fd });
        const data = await res.json();
        
        if(loader) loader.classList.add('hidden');

        if (data.auth_required) {
            alert(data.message);
            openAuth('login');
        } else if (data.error) {
            alert("Error: " + data.error);
        } else {
            // Success! Show Image from Cloudinary
            document.getElementById('processedImg').src = data.image;
            
            const dlBtn = document.getElementById('dlBtn');
            if(dlBtn) { 
                dlBtn.href = data.image; 
                dlBtn.classList.remove('hidden'); 
            }
            
            // Add to history list UI immediately
            if(data.id) addToHistory(data);
        }
    } catch (e) {
        if(loader) loader.classList.add('hidden');
        alert("Error connecting to server.");
    }
}

function addToHistory(data) {
    let grid = document.querySelector('.history-grid');
    if (!grid) {
        // Create history section if it doesn't exist
        const section = document.getElementById('history') || document.createElement('div');
        section.id = 'history'; section.className = 'history-section';
        section.innerHTML = `<h3>📂 Project History</h3><div class="history-grid"></div>`;
        if(!document.getElementById('history')) document.querySelector('.main-content').appendChild(section);
        grid = section.querySelector('.history-grid');
    }
    
    const styleName = data.style.charAt(0).toUpperCase() + data.style.slice(1);
    const card = document.createElement('div');
    card.className = 'h-card';
    card.id = `card-${data.id}`;
    card.innerHTML = `
        <img src="${data.image}">
        <div class="h-info">
            <span style="font-size: 12px; color: var(--primary);">${styleName}</span>
            <div class="h-actions">
                <a href="${data.image}" target="_blank" class="btn-icon">⬇️</a>
                <button onclick="deleteAsset(${data.id})" class="btn-icon delete">🗑️</button>
            </div>
        </div>
    `;
    grid.prepend(card);
}

// --- Auth & Payment ---
async function submitAuth(endpoint) {
    const prefix = endpoint === '/login' ? 'l' : 'r';
    const username = document.getElementById(prefix + '_user').value;
    const password = document.getElementById(prefix + '_pass').value;
    const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) });
    const data = await res.json();
    if (data.success) location.reload(); else document.getElementById('authError').innerText = data.message;
}

async function deleteAsset(id) {
    if(!confirm("Delete this project?")) return;
    const res = await fetch('/delete_history', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: id }) });
    const data = await res.json();
    if(data.success) { 
        document.getElementById(`card-${id}`).remove(); 
        if(document.querySelectorAll('.h-card').length === 0) location.reload(); 
    }
}

async function processMockPayment() {
    alert("Payment Successful! ✅");
    location.reload();
}

// --- QR Code ---
function showQRCode() {
    const url = window.location.href;
    const qrImage = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${url}`;
    const modalContent = `
        <div style="text-align:center; color: white;">
            <h2 style="margin-bottom:10px;">📲 Install StudioPro</h2>
            <p style="color:#94a3b8; margin-bottom:20px; font-size: 14px;">Scan this to open on your phone!</p>
            <div style="background: white; padding: 10px; display: inline-block; border-radius: 10px;">
                <img src="${qrImage}" style="display:block;">
            </div>
            <p style="margin-top:20px; font-size:12px; color:#64748b;">Tap "Add to Home Screen" on your mobile browser.</p>
            <button id="closeQR" style="margin-top:20px; background:transparent; border:1px solid #334155; color:white; padding:8px 20px; border-radius:8px; cursor:pointer;">Close</button>
        </div>
    `;
    const modalBox = document.querySelector('#authModal .modal-box');
    if(!window.originalAuthContent) window.originalAuthContent = modalBox.innerHTML;
    modalBox.innerHTML = modalContent;
    document.getElementById('authModal').classList.remove('hidden');
    document.getElementById('closeQR').onclick = () => {
        document.getElementById('authModal').classList.add('hidden');
        setTimeout(() => modalBox.innerHTML = window.originalAuthContent, 300);
    };
}
