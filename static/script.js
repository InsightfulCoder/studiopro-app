// --- 1. GLOBAL VARIABLES ---
let currentFile = null;

// --- 2. UI FUNCTIONS (Modals & Slider) ---
function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.add('hidden');
    }
}

function previewImage(input) {
    if (input.files && input.files[0]) {
        currentFile = input.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('originalImg').src = e.target.result;
            document.getElementById('processedImg').src = e.target.result;
            document.getElementById('uploadText').innerText = "✅ Image Loaded";
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function moveSlider(val) {
    document.getElementById('overlayLayer').style.width = val + "%";
    document.getElementById('sliderHandle').style.left = val + "%";
}

// --- 3. AUTHENTICATION ---
async function auth(endpoint) {
    const u = document.getElementById('authUser').value;
    const p = document.getElementById('authPass').value;
    if(!u || !p) return alert("Please enter Username and Password");

    try {
        const res = await fetch('/' + endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: u, password: p})
        });
        const data = await res.json();
        if(data.success) location.reload();
        else alert("Error: " + data.message);
    } catch(err) { alert("Connection Error. Please try again."); }
}

// --- 4. AI GENERATION ---
async function generate() {
    if(!currentFile) return alert("⚠️ Please upload an image first!");
    const btn = document.querySelector('.btn-generate');
    const originalText = btn.innerText;
    btn.innerText = "⏳ Processing (Please Wait)...";
    btn.disabled = true;

    const fd = new FormData();
    fd.append('file', currentFile);
    fd.append('style', document.querySelector('input[name="style"]:checked').value);

    try {
        const res = await fetch('/process', { method: 'POST', body: fd });
        const data = await res.json();
        
        if(data.error) alert("⚠️ " + data.error);
        else {
            document.getElementById('processedImg').src = data.image;
            if(document.getElementById('walletBalance')) document.getElementById('walletBalance').innerText = data.wallet;
        }
    } catch(err) { alert("Server Error. Please check your internet."); }
    finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

// --- 5. MOCK PAYMENT ---
async function pay(amount) {
    if(!confirm(`🏦 MOCK GATEWAY\n\nPay ₹${amount} to StudioPro?`)) return;
    try {
        const res = await fetch('/pay', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amount})
        });
        const data = await res.json();
        if(data.success) { alert("✅ Payment Successful!"); location.reload(); }
        else alert("Payment Failed.");
    } catch(err) { alert("Transaction Error."); }
}

// --- 6. ADMIN PANEL ---
async function loadAdmin() {
    openModal('adminModal');
    document.getElementById('adminData').innerHTML = "Loading Data...";
    try {
        const res = await fetch('/admin_data');
        const data = await res.json();
        if(data.error) { document.getElementById('adminData').innerHTML = `<p style="color:red">${data.error}</p>`; return; }

        let html = `
            <div style="display:grid; gap:20px;">
                <div>
                    <h4 style="border-bottom:1px solid #334155; padding-bottom:5px;">User Database</h4>
                    <table><tr><th>Username</th><th>Wallet</th><th>Role</th></tr>
                    ${data.users.map(u => `<tr><td>${u.username}</td><td>₹${u.wallet}</td><td>${u.role}</td></tr>`).join('')}
                    </table>
                </div>
                <div>
                    <h4 style="border-bottom:1px solid #334155; padding-bottom:5px;">Transactions</h4>
                    <table><tr><th>User ID</th><th>Amount</th><th>Date</th></tr>
                    ${data.transactions.map(t => `<tr><td>${t.user}</td><td>₹${t.amount}</td><td>${t.date}</td></tr>`).join('')}
                    </table>
                </div>
            </div>`;
        document.getElementById('adminData').innerHTML = html;
    } catch(err) { document.getElementById('adminData').innerHTML = "Error fetching Admin Data."; }
}

// --- 7. HISTORY LOADER ---
function loadHistory(url) {
    document.getElementById('processedImg').src = url;
    alert("Loaded asset from history!");
}
