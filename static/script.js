let currentFile = null;

function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

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
        
        // FIX: Check if response is valid JSON
        const contentType = res.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Server Database Error. Please Reset DB.");
        }

        const data = await res.json();
        if(data.success) location.reload();
        else alert("Error: " + data.message);
        
    } catch(err) { 
        alert("Login Failed: " + err.message); 
    }
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
        
        // FIX: Handle Server Crashes gracefully
        if (res.status === 500) throw new Error("Server Error (500). Please Reset Database.");
        
        const data = await res.json();
        if(data.error) alert("⚠️ " + data.error);
        else {
            document.getElementById('processedImg').src = data.image;
            if(document.getElementById('walletBalance')) document.getElementById('walletBalance').innerText = data.wallet;
        }
    } catch(err) { 
        alert("Generation Failed: " + err.message); 
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function pay(amount) {
    if(!confirm(`Pay ₹${amount} to StudioPro?`)) return;
    try {
        const res = await fetch('/pay', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({amount: amount})
        });
        const data = await res.json();
        if(data.success) { alert("✅ Success!"); location.reload(); }
    } catch(err) { alert("Transaction Failed"); }
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
