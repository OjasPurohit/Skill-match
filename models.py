<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>SkillMatch — Admin Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Epilogue:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="styles.css"/>
</head>
<body>

<nav id="top-nav">
  <div class="logo" onclick="window.location='index.html'">Skill<b>Match</b></div>
  <div class="nav-links" id="desktop-nav">
    <a class="nav-pill" href="index.html">Home</a>
    <a class="nav-pill" href="student.html">Student</a>
    <a class="nav-pill" href="company.html">Companies</a>
    <a class="nav-pill active" href="admin.html">Admin</a>
    <a class="nav-cta" href="student.html">Get Started →</a>
  </div>
  <div class="hamburger" id="ham" onclick="toggleMenu()">
    <span></span><span></span><span></span>
  </div>
</nav>

<div id="mobile-menu">
  <a class="mobile-nav-item" href="index.html">🏠 Home</a>
  <a class="mobile-nav-item" href="student.html">🎓 Student Dashboard</a>
  <a class="mobile-nav-item" href="company.html">🏢 Company Portal</a>
  <a class="mobile-nav-item active" href="admin.html">⚙️ Admin Panel</a>
  <a class="mobile-nav-item cta-mobile" href="student.html">Get Started →</a>
</nav>

<div class="admin-grid">

  <!-- SIDEBAR -->
  <aside class="admin-sidebar">
    <div class="sidebar-section">
      <div class="sidebar-label">Overview</div>
      <button class="s-item active" id="sv-overview" onclick="showView('overview')">📊 Dashboard</button>
      <button class="s-item" id="sv-analytics" onclick="showView('analytics')">📈 Analytics</button>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-label">Manage</div>
      <button class="s-item" id="sv-students" onclick="showView('students')">🎓 Students</button>
      <button class="s-item" id="sv-listings" onclick="showView('listings')">📋 Listings</button>
    </div>
  </aside>

  <!-- MAIN -->
  <div class="admin-main">

    <!-- OVERVIEW -->
    <div id="av-overview" class="admin-view active">
      <div class="admin-view-title">Platform Overview</div>
      <div class="kpi-grid">
        <div class="kpi"><div class="kpi-icon" style="background:var(--accent-dim)">👥</div><div><div class="kpi-n" id="kpi-students">—</div><div class="kpi-l">Total Students</div></div></div>
        <div class="kpi"><div class="kpi-icon" style="background:var(--purple-dim)">📋</div><div><div class="kpi-n" id="kpi-listings">—</div><div class="kpi-l">Internship Listings</div></div></div>
        <div class="kpi"><div class="kpi-icon" style="background:var(--amber-dim)">⚡</div><div><div class="kpi-n" id="kpi-avg">—</div><div class="kpi-l">Avg Skills/Listing</div></div></div>
      </div>
      <div class="card" style="padding:1.4rem;margin-bottom:1.2rem">
        <div class="panel-head"><span class="panel-title">System Status</span></div>
        <div class="recent-row"><span class="recent-time">Live</span><span>🟢 Flask API running on <strong>localhost:5000</strong></span><span class="chip chip-green">Online</span></div>
        <div class="recent-row"><span class="recent-time">Active</span><span>📄 PyPDF2 resume parser <strong>ready</strong></span><span class="chip chip-green">Ready</span></div>
        <div class="recent-row"><span class="recent-time">Active</span><span>🤖 TF-IDF matching engine <strong>loaded</strong></span><span class="chip chip-purple">ML</span></div>
        <div class="recent-row" style="border:none"><span class="recent-time">Active</span><span>🗄️ JSON data store <strong>connected</strong></span><span class="chip chip-amber">Storage</span></div>
      </div>
    </div>

    <!-- ANALYTICS -->
    <div id="av-analytics" class="admin-view">
      <div class="admin-view-title">Analytics</div>
      <div class="grid-4" style="margin-bottom:1.5rem">
        <div class="stat-box"><div class="n" id="an-students">—</div><div class="l">Students</div></div>
        <div class="stat-box"><div class="n" style="color:var(--purple)" id="an-listings">—</div><div class="l">Listings</div></div>
        <div class="stat-box"><div class="n" style="color:var(--amber)" id="an-avg">—</div><div class="l">Avg Skills</div></div>
      </div>
      <div class="analytics-grid">
        <div class="analytics-card">
          <div class="ac-title">Top Skills in Demand <span style="font-size:0.72rem;color:var(--muted2)">(pandas value_counts)</span></div>
          <div id="top-skills-bars">
            <div style="color:var(--muted2);font-size:0.82rem">Loading...</div>
          </div>
        </div>
        <div class="analytics-card">
          <div class="ac-title">Quick Stats</div>
          <div id="quick-stats" style="font-size:0.85rem;color:var(--muted2)">Loading...</div>
        </div>
      </div>
    </div>

    <!-- STUDENTS -->
    <div id="av-students" class="admin-view">
      <div class="admin-view-title">Students</div>
      <div class="toolbar">
        <div class="search-input-wrap"><span>🔍</span><input class="search-input" placeholder="Search students..." oninput="filterStudents(this.value)"/></div>
        <span class="chip chip-green" id="student-count">Loading...</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Skills</th></tr></thead>
          <tbody id="students-tbody">
            <tr><td colspan="4" style="text-align:center;color:var(--muted2)">Loading...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- LISTINGS -->
    <div id="av-listings" class="admin-view">
      <div class="admin-view-title">Internship Listings</div>
      <div class="toolbar">
        <span class="chip chip-green" id="listing-count">Loading...</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Title</th><th>Skills Required</th><th>Description</th></tr></thead>
          <tbody id="listings-tbody">
            <tr><td colspan="3" style="text-align:center;color:var(--muted2)">Loading...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

  </div><!-- /admin-main -->
</div><!-- /admin-grid -->

<script src="main.js"></script>
<script>
  const API = 'http://localhost:5000';
  let allStudents = [];

  // ── Switch sidebar views
  function showView(name) {
    document.querySelectorAll('.admin-view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.s-item').forEach(s => s.classList.remove('active'));
    document.getElementById('av-' + name).classList.add('active');
    document.getElementById('sv-' + name).classList.add('active');
  }

  // ── Load overview KPIs
  async function loadOverview() {
    try {
      const res  = await fetch(`${API}/api/analytics`);
      const data = await res.json();

      document.getElementById('kpi-students').textContent = data.total_students ?? '—';
      document.getElementById('kpi-listings').textContent = data.total_internships ?? '—';
      document.getElementById('kpi-avg').textContent      = data.avg_skills_per_internship ?? '—';
    } catch (e) {
      document.getElementById('kpi-students').textContent = 'ERR';
    }
  }

  // ── Load analytics
  async function loadAnalytics() {
    try {
      const res  = await fetch(`${API}/api/analytics`);
      const data = await res.json();

      document.getElementById('an-students').textContent = data.total_students;
      document.getElementById('an-listings').textContent = data.total_internships;
      document.getElementById('an-avg').textContent      = data.avg_skills_per_internship;

      // Skill bars
      const skills = data.top_skills || {};
      const max    = Math.max(...Object.values(skills), 1);
      document.getElementById('top-skills-bars').innerHTML = Object.entries(skills)
        .slice(0, 8).map(([skill, count]) => `
          <div class="skill-bar-row">
            <span class="skb-label">${skill}</span>
            <div class="skb-track"><div class="skb-fill" style="width:${Math.round((count/max)*100)}%"></div></div>
            <span class="skb-n">${count}</span>
          </div>`).join('');

      document.getElementById('quick-stats').innerHTML = `
        <div style="margin-bottom:0.6rem">📋 <strong>${data.total_internships}</strong> internship listings in database</div>
        <div style="margin-bottom:0.6rem">👥 <strong>${data.total_students}</strong> registered students</div>
        <div style="margin-bottom:0.6rem">⚡ <strong>${data.avg_skills_per_internship}</strong> avg skills per listing</div>
        <div style="color:var(--accent);margin-top:0.8rem;font-size:0.78rem">Powered by pandas .value_counts() + numpy .mean()</div>`;

    } catch (e) {
      document.getElementById('top-skills-bars').innerHTML = '<div style="color:var(--red)">❌ Cannot reach backend</div>';
    }
  }

  // ── Load students table
  async function loadStudents() {
    try {
      const res  = await fetch(`${API}/api/students`);
      const data = await res.json();
      allStudents = data.students || [];

      document.getElementById('student-count').textContent = `${allStudents.length} total`;
      renderStudents(allStudents);
    } catch (e) {
      document.getElementById('students-tbody').innerHTML =
        '<tr><td colspan="4" style="color:var(--red)">❌ Cannot reach backend</td></tr>';
    }
  }

  function renderStudents(list) {
    document.getElementById('students-tbody').innerHTML = list.length === 0
      ? '<tr><td colspan="4" style="text-align:center;color:var(--muted2)">No students registered yet</td></tr>'
      : list.map(s => `
          <tr>
            <td><div style="font-weight:500">${s.name || '—'}</div></td>
            <td style="color:var(--muted2);font-size:0.82rem">${s.email || '—'}</td>
            <td><span class="chip chip-purple">${s.role || 'student'}</span></td>
            <td><span class="chip chip-green">${Array.isArray(s.skills) ? s.skills.length : 0} skills</span></td>
          </tr>`).join('');
  }

  function filterStudents(q) {
    const filtered = allStudents.filter(s =>
      (s.name || '').toLowerCase().includes(q.toLowerCase()) ||
      (s.email || '').toLowerCase().includes(q.toLowerCase())
    );
    renderStudents(filtered);
  }

  // ── Load listings table
  async function loadListings() {
    try {
      const res  = await fetch(`${API}/api/internships`);
      const data = await res.json();
      const list = data.internships || [];

      document.getElementById('listing-count').textContent = `${list.length} active`;
      document.getElementById('listings-tbody').innerHTML = list.length === 0
        ? '<tr><td colspan="3" style="text-align:center;color:var(--muted2)">No listings yet</td></tr>'
        : list.map(i => `
            <tr>
              <td style="font-weight:500">${i.title}</td>
              <td><div style="display:flex;flex-wrap:wrap;gap:0.3rem">
                ${(i.skills_required || '').split(' ').slice(0,4).map(s =>
                  `<span class="chip chip-green">${s}</span>`).join('')}
              </div></td>
              <td style="color:var(--muted2);font-size:0.82rem">${(i.description || '').substring(0,60)}...</td>
            </tr>`).join('');
    } catch (e) {
      document.getElementById('listings-tbody').innerHTML =
        '<tr><td colspan="3" style="color:var(--red)">❌ Cannot reach backend</td></tr>';
    }
  }

  // ── Load everything on page open
  loadOverview();
  loadAnalytics();
  loadStudents();
  loadListings();

  // Animate skill bars after load
  setTimeout(() => {
    document.querySelectorAll('.skb-fill').forEach(el => {
      const w = el.style.width; el.style.width = '0';
      setTimeout(() => { el.style.width = w; }, 100);
    });
  }, 500);
</script>
</body>
</html>