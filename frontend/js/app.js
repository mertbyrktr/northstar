// State
let currentTab = 'login';
let currentView = 'auth';
let isAuthed = false;
let globalWorkoutsData = [];
let progressChartInstance = null;
let volumeChartInstance = null;
let weightChartInstance = null;

// Timezone Helper: Backend sends naive UTC datetimes, we append 'Z' to parse as UTC exactly.
function parseUTCDate(dateStr) {
    if (!dateStr) return new Date();
    return new Date(dateStr.endsWith('Z') ? dateStr : dateStr + 'Z');
}

// DOM Elements
const views = {
    auth: document.getElementById('auth-view'),
    dashboard: document.getElementById('dashboard-view'),
    profile: document.getElementById('profile-view'),
    tracker: document.getElementById('tracker-view'),
    goals: document.getElementById('goals-view')
};
const navbar = document.getElementById('navbar');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();

    // Nav Binds
    document.getElementById('btn-dashboard').onclick = () => switchView('dashboard');
    document.getElementById('btn-goals').onclick = () => switchView('goals');
    document.getElementById('btn-profile').onclick = () => switchView('profile');
    document.getElementById('btn-tracker').onclick = () => switchView('tracker');
    document.getElementById('btn-logout').onclick = handleLogout;
});

function checkAuth() {
    isAuthed = !!API.getToken();
    if (isAuthed) {
        switchView('dashboard');
    } else {
        switchView('auth');
    }
}

// ------ Routing / Views ------
function switchView(viewName) {
    currentView = viewName;
    Object.values(views).forEach(v => v.classList.remove('active-view'));
    setTimeout(() => {
        Object.keys(views).forEach(k => {
            if (k !== viewName) views[k].classList.add('hidden');
        });
        views[viewName].classList.remove('hidden');
        views[viewName].classList.add('active-view');
    }, 50);

    if (viewName === 'auth') {
        navbar.classList.add('hidden');
    } else {
        navbar.classList.remove('hidden');
        document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`btn-${viewName}`).classList.add('active');

        if (viewName === 'dashboard' || viewName === 'tracker') loadWorkouts();
        if (viewName === 'profile') loadProfile();
        if (viewName === 'tracker') loadWeightChart();
        if (viewName === 'goals') loadGoals();
    }
}

// ------ Auth Logic ------
function switchAuthTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    const nameGroup = document.getElementById('name-group');
    const submitText = document.getElementById('auth-submit-text');
    const err = document.getElementById('auth-error');

    err.innerText = '';
    if (tab === 'register') {
        nameGroup.style.display = 'block';
        submitText.innerText = 'Create Account';
    } else {
        nameGroup.style.display = 'none';
        submitText.innerText = 'Login';
    }
}

async function handleAuth(e) {
    e.preventDefault();
    const btn = document.querySelector('#auth-form button');
    const err = document.getElementById('auth-error');
    err.innerText = '';

    const email = document.getElementById('auth-email').value;
    const pass = document.getElementById('auth-password').value;
    const name = document.getElementById('auth-name').value;

    btn.innerHTML = `<span class="spinner"></span> Processing...`;

    try {
        if (currentTab === 'register') {
            await API.register(name, email, pass);
            // Auto login after register
            await API.login(email, pass);
        } else {
            await API.login(email, pass);
        }
        document.getElementById('auth-form').reset();
        checkAuth();
    } catch (e) {
        err.innerText = e.message || 'Authentication failed';
    } finally {
        btn.innerHTML = currentTab === 'register' ? 'Create Account' : 'Login';
    }
}

function handleLogout() {
    API.logout();
    checkAuth();
}

// ------ Dashboard / Workouts ------
async function loadWorkouts() {
    const grid = document.getElementById('workouts-grid');
    if (grid) grid.innerHTML = '<div class="glow-text">Loading secure data...</div>';
    try {
        const workouts = await API.getWorkouts();
        globalWorkoutsData = workouts;
        updateGlobalExerciseData();

        if (workouts.length === 0) {
            if (grid) grid.innerHTML = '<div class="subtitle">No workouts found. Add one to start tracking!</div>';
            return;
        }

        if (grid) grid.innerHTML = workouts.map(w => `
            <div class="glass-card workout-card">
                <h3>
                    <span>Workout <span class="workout-date">(${parseUTCDate(w.date).toLocaleDateString()})</span></span>
                    <div style="display: flex; align-items: center;">
                        <button class="primary-btn small-btn" style="margin-right:0.6rem; padding: 0.3rem 0.6rem;" onclick="openWorkoutModal('${w.id}')">+ Exercise</button>
                        <button class="del-btn" onclick="deleteWorkout('${w.id}')">✖</button>
                    </div>
                </h3>
                <div class="exercises-list">
                    ${w.exercises.length === 0 ? '<em class="text-muted">Empty workout</em>' :
                w.exercises.map(ex => `
                        <div class="exercise-pill">
                            <span>${ex.name} <span class="exercise-meta">${ex.sets}x${ex.reps}</span></span>
                            <div style="display:flex; gap:10px; align-items:center;">
                                <span>${ex.weight}kg</span>
                                <button class="del-btn" onclick="deleteExercise('${ex.id}')">✖</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
    } catch (e) {
        grid.innerHTML = `<div class="error-msg">Failed to load: ${e.message}</div>`;
    }
}

async function deleteWorkout(id) {
    if (!confirm('Are you sure you want to delete this entire workout?')) return;
    await API.deleteWorkout(id);
    loadWorkouts();
}

async function deleteExercise(id) {
    await API.deleteExercise(id);
    loadWorkouts();
}

// ------ Modals ------
function openWorkoutModal(workoutId = '') {
    document.getElementById('ex-workout-id').value = workoutId;
    document.getElementById('modal-backdrop').classList.remove('hidden');
}
function closeModal(e) {
    if (e.target.id === 'modal-backdrop') {
        document.getElementById('modal-backdrop').classList.add('hidden');
    }
}

async function handleAddExercise(e) {
    e.preventDefault();
    const btn = document.querySelector('#exercise-form button');

    const wid = document.getElementById('ex-workout-id').value;
    const name = document.getElementById('ex-name').value;
    const sets = document.getElementById('ex-sets').value;
    const reps = document.getElementById('ex-reps').value;
    const weight = document.getElementById('ex-weight').value;

    const actualWid = wid.trim() === '' ? '000000000000000000000000'.replace(/0/g, () => (~~(Math.random() * 16)).toString(16)) : wid; // Generate fake 24 char hex if empty

    btn.innerText = 'Saving...';
    try {
        await API.addExercise(actualWid, name, sets, reps, weight);
        document.getElementById('exercise-form').reset();
        document.getElementById('modal-backdrop').classList.add('hidden');
        loadWorkouts();
    } catch (err) {
        alert("Error adding exercise: " + err.message);
    } finally {
        btn.innerText = 'Save Exercise';
    }
}

// ------ Modals / Goals Logic ------
function openGoalModal() {
    document.getElementById('goal-modal-backdrop').classList.remove('hidden');
}
function closeGoalModal(e) {
    if (e.target.id === 'goal-modal-backdrop') {
        document.getElementById('goal-modal-backdrop').classList.add('hidden');
    }
}

async function loadGoals() {
    const grid = document.getElementById('goals-grid');
    if (grid) grid.innerHTML = '<div class="glow-text">Loading goals...</div>';
    try {
        const goals = await API.getGoals();
        if (goals.length === 0) {
            if (grid) grid.innerHTML = '<div class="subtitle">No goals mapped yet. Add one!</div>';
            return;
        }
        if (grid) grid.innerHTML = goals.map(g => `
            <div class="glass-card workout-card" style="border: 2px solid ${g.is_completed ? '#22c55e' : 'var(--glass-border)'}; opacity: ${g.is_completed ? 0.6 : 1}">
                <h3 style="text-decoration: ${g.is_completed ? 'line-through' : 'none'}">${g.title}</h3>
                <div style="display:flex; justify-content:space-between; margin-top:20px;">
                    <button class="secondary-btn small-btn" onclick="toggleGoal('${g.id}')">${g.is_completed ? 'Undo' : 'Complete'}</button>
                    <button class="del-btn" onclick="deleteGoal('${g.id}')">✖</button>
                </div>
            </div>
        `).join('');
    } catch (e) {
        if (grid) grid.innerHTML = `<div class="error-msg">Failed: ${e.message}</div>`;
    }
}

async function handleAddGoal(e) {
    e.preventDefault();
    const btn = document.querySelector('#goal-form button');
    const title = document.getElementById('goal-title').value;
    btn.innerText = 'Saving...';
    try {
        await API.addGoal(title);
        document.getElementById('goal-form').reset();
        document.getElementById('goal-modal-backdrop').classList.add('hidden');
        loadGoals();
    } catch(err) {
        alert("Error adding goal: " + err.message);
    } finally {
        btn.innerText = 'Save Goal';
    }
}

async function toggleGoal(id) {
    await API.toggleGoal(id);
    loadGoals();
}

async function deleteGoal(id) {
    await API.deleteGoal(id);
    loadGoals();
}

// ------ AI & Profile ------
async function loadProfile() {
    try {
        const profile = await API.getProfile();
        if (profile) {
            document.getElementById('profile-welcome-tag').innerText = `Welcome, ${profile.name}`;
            document.getElementById('prof-weight').value = profile.weight || '';
            document.getElementById('prof-height').value = profile.height || '';
            document.getElementById('prof-age').value = profile.age || '';

            document.getElementById('disp-weight').innerText = profile.weight || '--';
            document.getElementById('disp-height').innerText = profile.height || '--';
            document.getElementById('disp-age').innerText = profile.age || '--';
        }
    } catch (e) { console.error("Profile load failed", e); }
}

function toggleProfileEdit() {
    const disp = document.getElementById('profile-display-card');
    const edit = document.getElementById('profile-edit-card');
    if (disp.classList.contains('hidden')) {
        disp.classList.remove('hidden');
        edit.classList.add('hidden');
    } else {
        disp.classList.add('hidden');
        edit.classList.remove('hidden');
    }
}

async function handleProfileUpdate(e) {
    e.preventDefault();
    const btn = document.querySelector('#profile-form button');
    const w = document.getElementById('prof-weight').value;
    const h = document.getElementById('prof-height').value;
    const a = document.getElementById('prof-age').value;

    btn.innerText = 'Saving...';
    try {
        await API.updateProfile(w, h, a);
        if (w) await API.logWeight(w); // Push to metrics folder for graph
        alert('Profile saved!');
        toggleProfileEdit();
        loadProfile();
    } catch (err) {
        alert('Failed: ' + err.message);
    } finally {
        btn.innerText = 'Save Profile';
    }
}



// ------ Chart & Global Data ------
function capitalize(str) { return str.charAt(0).toUpperCase() + str.slice(1); }

function updateGlobalExerciseData() {
    const uniqueNames = new Set();
    globalWorkoutsData.forEach(w => {
        w.exercises.forEach(ex => uniqueNames.add(ex.name.trim().toLowerCase()));
    });
    const sortedNames = Array.from(uniqueNames).sort();

    const datalist = document.getElementById('exercise-suggestions');
    if (datalist) {
        datalist.innerHTML = sortedNames.map(name => `<option value="${capitalize(name)}">`).join('');
    }

    const select = document.getElementById('tracker-exercise-select');
    if (select) {
        const currentVal = select.value;
        select.innerHTML = '<option value="">Select an exercise...</option>' +
            sortedNames.map(name => `<option value="${name}" ${currentVal === name ? 'selected' : ''}>${capitalize(name)}</option>`).join('');

        if (currentVal && sortedNames.includes(currentVal)) {
            updateTrackerGraph();
        } else if (sortedNames.length > 0 && currentView === 'tracker') {
            select.value = sortedNames[0];
            updateTrackerGraph();
        }
    }
}

function updateTrackerGraph() {
    const select = document.getElementById('tracker-exercise-select');
    const selectedName = select.value;
    if (!selectedName) return;

    const dataPoints = [];
    const volumePoints = [];
    globalWorkoutsData.forEach(w => {
        const matchingExercises = w.exercises.filter(ex => ex.name.trim().toLowerCase() === selectedName);
        if (matchingExercises.length > 0) {
            const maxWeight = Math.max(...matchingExercises.map(ex => ex.weight));
            dataPoints.push({ x: parseUTCDate(w.date), y: maxWeight });

            const totalVolume = matchingExercises.reduce((sum, ex) => sum + (ex.sets * ex.reps * ex.weight), 0);
            volumePoints.push({ x: parseUTCDate(w.date), y: totalVolume });
        }
    });
    dataPoints.sort((a, b) => a.x - b.x);
    volumePoints.sort((a, b) => a.x - b.x);

    const ctxProgress = document.getElementById('progressChart').getContext('2d');
    if (progressChartInstance) progressChartInstance.destroy();

    progressChartInstance = new Chart(ctxProgress, {
        type: 'line',
        data: {
            labels: dataPoints.map(dp => dp.x.toLocaleDateString()),
            datasets: [{
                label: 'Max Weight (kg)',
                data: dataPoints.map(dp => dp.y),
                borderColor: '#c084fc',
                backgroundColor: 'rgba(192, 132, 252, 0.2)',
                borderWidth: 3,
                pointBackgroundColor: '#60a5fa',
                pointRadius: 6,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { labels: { color: '#f8fafc', font: { size: 14 } } } }
        }
    });

    const ctxVolume = document.getElementById('volumeChart').getContext('2d');
    if (volumeChartInstance) volumeChartInstance.destroy();

    volumeChartInstance = new Chart(ctxVolume, {
        type: 'bar',
        data: {
            labels: volumePoints.map(dp => dp.x.toLocaleDateString()),
            datasets: [{
                label: 'Total Volume Lifted (kg)',
                data: volumePoints.map(dp => dp.y),
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: '#38bdf8',
                borderWidth: 2,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { labels: { color: '#f8fafc', font: { size: 14 } } } }
        }
    });
}

async function loadWeightChart() {
    try {
        const metrics = await API.getWeightMetrics();
        const container = document.getElementById('weightChart').parentElement;

        if (metrics.length === 0) {
            if (weightChartInstance) { weightChartInstance.destroy(); weightChartInstance = null; }
            container.innerHTML = '<canvas id="weightChart"></canvas><div class="glow-text" style="position:absolute; top:40%; left:0; right:0; text-align:center;">No weight history logged yet.<br>Go to Profile > Edit Profile to log!</div>';
            return;
        } else {
            if (!document.getElementById('weightChart')) {
                container.innerHTML = '<canvas id="weightChart"></canvas>';
            }
        }

        const dataPoints = metrics.map(m => ({ x: parseUTCDate(m.date), y: m.weight }));
        dataPoints.sort((a, b) => a.x - b.x);

        const ctx = document.getElementById('weightChart').getContext('2d');
        if (weightChartInstance) weightChartInstance.destroy();

        weightChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dataPoints.map(dp => dp.x.toLocaleDateString()),
                datasets: [{
                    label: 'Body Weight (kg)',
                    data: dataPoints.map(dp => dp.y),
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderWidth: 3,
                    pointBackgroundColor: '#f8fafc',
                    pointRadius: 5,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                },
                plugins: { legend: { labels: { color: '#f8fafc', font: { size: 14 } } } }
            }
        });
    } catch (e) {
        console.error("Weight chart load failed", e);
    }
}
