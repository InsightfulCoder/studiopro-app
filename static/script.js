let currentFile = null;

function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

function previewImage(input) {
    if (input.files && input.files[0]) {
        currentFile = input.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            // Set source
            const orig = document.getElementById('originalImg');
            const proc = document.getElementById('processedImg');
            
            orig.src = e.target.result;
            proc.src = e.target.result;
            
            // Add 'loaded' class to make them visible (removes broken icon)
            orig.classList.add('loaded');
            proc.classList.add('loaded');
            
            document.getElementById('uploadText').innerText = "✅ Image Loaded";
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function moveSlider(val) {
    document.getElementById('overlayLayer').style.width = val + "%";
    document.getElementById('sliderHandle').style.left = val + "%";
}

function loadHistory(url) {
    const proc = document.getElementById('processedImg');
    proc.src = url;
    proc.classList.add('loaded'); // Make visible
    closeModal('historyModal');
}

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
    } catch(err) { alert("Connection Error"); }
}

async function generate() {
    if(!currentFile) return alert("⚠️ Please upload an image first!");
    const btn = document.querySelector('.btn-generate');
    const originalText = btn.innerText;
    btn.innerText = "⏳ Processing...";
    btn.disabled = true;

    const fd = new FormData();
    fd.append('file', currentFile);
    fd.append('style', document.querySelector('input[name="style"]:checked').value);

    try {
        const res = await fetch('/process', { method: 'POST', body: fd });
        if (res.status === 500) throw new Error("Server Error. Check API Key.");
        
        const data = await res.json();
        
        if(data.auth_required) {
            alert("🛑 " + data.error);
            openModal('authModal');
        } else if(data.error) {
            alert("⚠️ " + data.error);
        } else {
            const proc = document.getElementById('processedImg');
            proc.src = data.image;
            proc.classList.add('loaded'); // Ensure visible
            
            const wElement = document.getElementById('walletBalance');
            if(wElement) wElement.innerText = data.wallet;
        }
    } catch(err) { 
        alert("Failed: " + err.message); 
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function pay(amount) {
    if(!confirm(`Pay ₹${amount}?`)) return;
    try {
        const res = await fetch('/pay', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amount})
        });
        const data = await res.json();
        if(data.success) { alert("✅ Success!"); location.reload(); }
    } catch(err) { alert("Failed"); }
}

async function loadAdmin() {
    openModal('adminModal');
    try {
        const res = await fetch('/admin_data');
        const data = await res.json();
        if(data.error) return document.getElementById('adminData').innerHTML = data.error;
        let html = `<h4>Users</h4><table><tr><th>User</th><th>Wallet</th><th>Role</th></tr>
        ${data.users.map(u => `<tr><td>${u.username}</td><td>₹${u.wallet}</td><td>${u.role}</td></tr>`).join('')}</table>`;
        document.getElementById('adminData').innerHTML = html;
    } catch(err) { document.getElementById('adminData').innerHTML = "Error loading data"; }
}
