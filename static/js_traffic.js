let countdownInterval = null;
let tickInterval = null;

function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.className = `status-message status-${type}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';
}

function updateJunction(data) {
    // Update signals
    const roads = ['North', 'South', 'East', 'West'];
    roads.forEach(road => {
        const signal = document.getElementById(`signal${road}`);
        const state = data.signal_states[road] || 'RED';

        if (state === 'GREEN') {
            signal.className = `signal signal-${road.toLowerCase()} signal-green`;
            signal.textContent = '🟢';
        } else {
            signal.className = `signal signal-${road.toLowerCase()} signal-red`;
            signal.textContent = '🔴';
        }
    });

    // Update countdown
    document.getElementById('countdown').textContent = data.remaining_time || '--';

    // Update info panel
    document.getElementById('activeRoad').textContent = data.active_road || '--';
    document.getElementById('remainingTime').textContent = data.remaining_time || '--';

    if (data.densities) {
        const maxDensity = Math.max(...Object.values(data.densities));
        document.getElementById('maxDensity').textContent = (maxDensity * 100).toFixed(1) + '%';
    }

    document.getElementById('systemStatus').textContent = data.cycle_active ? 'Active' : 'Idle';
    document.getElementById('infoPanel').style.display = 'grid';
}

function startCountdown() {
    if (tickInterval) {
        clearInterval(tickInterval);
    }

    tickInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/tick', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                updateJunction(data);
            }
        } catch (error) {
            console.error('Error ticking:', error);
        }
    }, 1000);
}

async function uploadImages() {
    const northFile = document.getElementById('north').files[0];
    const southFile = document.getElementById('south').files[0];
    const eastFile = document.getElementById('east').files[0];
    const westFile = document.getElementById('west').files[0];

    if (!northFile || !southFile || !eastFile || !westFile) {
        showStatus('Please upload images for all 4 directions', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('north', northFile);
    formData.append('south', southFile);
    formData.append('east', eastFile);
    formData.append('west', westFile);

    const uploadBtn = document.getElementById('uploadBtn');
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="loading"></span> Processing...';

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showStatus('✅ Traffic analysis complete! System activated.', 'success');
            updateJunction(data);
            startCountdown();
        } else {
            showStatus('❌ Error: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showStatus('❌ Network error: ' + error.message, 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = '📤 Upload & Analyze Traffic';
    }
}

// Load initial state
async function loadState() {
    try {
        const response = await fetch('/api/state');
        if (response.ok) {
            const data = await response.json();
            if (data.cycle_active) {
                updateJunction(data);
                startCountdown();
            }
        }
    } catch (error) {
        console.error('Error loading state:', error);
    }
}

// Initialize
loadState();