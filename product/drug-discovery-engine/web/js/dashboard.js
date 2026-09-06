/**
 * Therapeutic-AI Executive Dashboard — JavaScript
 * Handles data fetching, chart rendering, and real-time updates.
 */

// Global chart instances
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    // Auto-refresh every 30 seconds
    setInterval(refreshDashboard, 30000);
});

async function initDashboard() {
    await Promise.all([
        loadDDEMetrics(),
        loadSystemHealth(),
        loadWetlabStatus(),
        loadProjectTimeline(),
        loadCICDStatus(),
    ]);
    updateLastRefresh();
}

async function refreshDashboard() {
    await initDashboard();
}

// Load DDE Metrics
async function loadDDEMetrics() {
    try {
        const res = await fetch('/api/v1/dashboard/dde');
        const data = await res.json();
        
        document.getElementById('dataset-size').textContent = data.dataset_size;
        document.getElementById('properties-count').textContent = data.properties.length;
        document.getElementById('r2-logp').textContent = data.r2_scores.logp.toFixed(4);
        document.getElementById('r2-logs').textContent = data.r2_scores.logS.toFixed(4);
        document.getElementById('r2-tpsa').textContent = data.r2_scores.tpsa.toFixed(4);
        
        // Render gauges
        renderGauge('gauge-logp', data.r2_scores.logp, '#00C853');
        renderGauge('gauge-logs', data.r2_scores.logS, '#2196F3');
        renderGauge('gauge-tpsa', data.r2_scores.tpsa, '#FFB300');
    } catch (err) {
        console.error('Failed to load DDE metrics:', err);
    }
}

// Load System Health
async function loadSystemHealth() {
    try {
        const res = await fetch('/api/v1/dashboard/health');
        const data = await res.json();
        
        const passRate = data.pytest_passed / data.pytest_total;
        document.getElementById('pytest-result').textContent = `${data.pytest_passed}/${data.pytest_total}`;
        document.getElementById('regression-gate').textContent = data.regression_gate;
        document.getElementById('validation-gate').textContent = data.validation_gate;
        
        const badge = document.getElementById('health-badge');
        badge.textContent = passRate === 1 ? 'PASS' : 'REVIEW';
        badge.className = `badge ${passRate === 1 ? 'success' : 'warning'}`;
    } catch (err) {
        console.error('Failed to load system health:', err);
    }
}

// Load WetlabLoop Status
async function loadWetlabStatus() {
    try {
        const res = await fetch('/api/v1/dashboard/wetlab');
        const data = await res.json();
        
        document.getElementById('current-cycle').textContent = data.current_cycle;
        document.getElementById('candidates-tested').textContent = data.total_candidates;
        document.getElementById('best-score').textContent = data.best_candidate.score.toFixed(4);
        
        // Render cycle chart
        renderCycleChart();
    } catch (err) {
        console.error('Failed to load wetlab status:', err);
    }
}

// Load Project Timeline
async function loadProjectTimeline() {
    try {
        const res = await fetch('/api/v1/dashboard');
        const data = await res.json();
        
        const timeline = data.project_timeline;
        // Timeline is rendered in HTML, but we could update dynamically
    } catch (err) {
        console.error('Failed to load project timeline:', err);
    }
}

// Load CI/CD Status
async function loadCICDStatus() {
    try {
        const res = await fetch('/api/v1/dashboard');
        const data = await res.json();
        
        const cicd = data.ci_cd;
        document.getElementById('cicd-last-run').textContent = new Date(cicd.last_run).toLocaleString();
        document.getElementById('cicd-duration').textContent = cicd.duration;
        document.getElementById('cicd-badge').textContent = cicd.status;
        document.getElementById('cicd-badge').className = `badge ${cicd.status === 'PASS' ? 'success' : 'error'}`;
    } catch (err) {
        console.error('Failed to load CI/CD status:', err);
    }
}

// Render gauge chart
function renderGauge(canvasId, value, color) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    // Destroy existing chart
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    charts[canvasId] = new Chart(canvas, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 1 - value],
                backgroundColor: [color, '#2A2A2B'],
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false },
            },
        },
        plugins: [{
            id: 'gaugeText',
            afterDraw(chart) {
                const { ctx, chartArea } = chart;
                const centerX = (chartArea.left + chartArea.right) / 2;
                const centerY = (chartArea.top + chartArea.bottom) / 2;
                ctx.save();
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = 'bold 16px Inter';
                ctx.fillStyle = '#F7F6F3';
                ctx.fillText(value.toFixed(2), centerX, centerY);
                ctx.restore();
            }
        }]
    });
}

// Render cycle chart
function renderCycleChart() {
    const canvas = document.getElementById('cycle-chart');
    if (!canvas) return;
    
    if (charts['cycle-chart']) {
        charts['cycle-chart'].destroy();
    }
    
    charts['cycle-chart'] = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Cycle 1', 'Cycle 2', 'Cycle 3'],
            datasets: [{
                label: 'Candidates Tested',
                data: [4, 4, 4],
                backgroundColor: '#2196F3',
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#2A2A2B' },
                    ticks: { color: '#A0A0A0' },
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#A0A0A0' },
                },
            },
        },
    });
}

// Update last refresh time
function updateLastRefresh() {
    const now = new Date();
    document.getElementById('last-refresh').textContent = now.toLocaleTimeString();
}

// Manual refresh
function refreshDashboard() {
    const btn = document.querySelector('.btn-refresh');
    btn.textContent = 'Refreshing...';
    btn.disabled = true;
    
    initDashboard().then(() => {
        btn.textContent = 'Refresh';
        btn.disabled = false;
    });
}
