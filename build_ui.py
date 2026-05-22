import json

with open("d:/cricket/players.json", "r", encoding="utf-8") as f:
    players_data = f.read()

main_js_content = f"""import './style.css'

const playersData = {players_data};

playersData.forEach(p => {{
  if (p.registrationId && p.registrationId.trim() === 'BCA23078') {{
    p.photoUrl = '/darshan_BCA23078.jpg';
  }}
}});

function getImageUrl(url, size) {{
  if (!url) return '';
  if (url.includes('drive.google.com')) return url.replace('/uc?id=', '/thumbnail?id=') + '&sz=w' + size;
  return url;
}}

document.querySelector('#app').innerHTML = `
  <div class="overlay"></div>
  <div class="container">
    <h1>BBHC League</h1>
    <p class="subtitle">Official Player Database</p>
    
    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="Search player name..." autocomplete="off" />
      <ul id="searchDropdown" class="search-dropdown"></ul>
    </div>

    <div class="result-container" id="resultContainer">
      <div id="emptyState" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>
        <p>Search for a player to view their profile</p>
      </div>
      <div id="playerProfile" class="player-profile" style="display: none;"></div>
    </div>
  </div>
`

const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');
const emptyState = document.getElementById('emptyState');
const playerProfile = document.getElementById('playerProfile');

// Close dropdown on outside click
document.addEventListener('click', (e) => {{
  if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {{
    searchDropdown.style.display = 'none';
  }}
}});

searchInput.addEventListener('input', (e) => {{
  const query = e.target.value.toLowerCase().trim();
  
  if (query.length < 1) {{
    searchDropdown.style.display = 'none';
    return;
  }}

  const matches = playersData.filter(p => p.name.toLowerCase().includes(query));

  if (matches.length > 0) {{
    searchDropdown.innerHTML = matches.map((match, idx) => `
      <li class="dropdown-item" data-index="${{idx}}">
        <div class="dropdown-avatar">
          <img src="${{match.photoUrl ? getImageUrl(match.photoUrl, 150) : 'https://ui-avatars.com/api/?name=' + encodeURIComponent(match.name) + '&background=random'}}" onerror="this.src='https://ui-avatars.com/api/?name=${{encodeURIComponent(match.name)}}&background=random'" />
        </div>
        <div class="dropdown-info">
          <span class="dropdown-name">${{match.name}}</span>
          <span class="dropdown-role">${{match.class}} &bull; ${{match.role}}</span>
        </div>
      </li>
    `).join('');
    searchDropdown.style.display = 'block';
    
    // Add click listeners to items
    const items = searchDropdown.querySelectorAll('.dropdown-item');
    items.forEach(item => {{
      item.addEventListener('click', () => {{
        const player = matches[item.getAttribute('data-index')];
        renderPlayer(player);
        searchDropdown.style.display = 'none';
        searchInput.value = player.name;
      }});
    }});
    
  }} else {{
    searchDropdown.innerHTML = `<li class="dropdown-no-results">No players found</li>`;
    searchDropdown.style.display = 'block';
  }}
}});

function renderPlayer(player) {{
  emptyState.style.display = 'none';
  playerProfile.style.display = 'block';
  
  const fallbackImg = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(player.name) + '&background=random&size=200';
  const imgUrl = player.photoUrl ? getImageUrl(player.photoUrl, 800) : fallbackImg;
  
  playerProfile.innerHTML = `
    <div class="profile-card">
      <div class="profile-layout">
        <!-- Left Side: Portrait -->
        <div class="profile-visual">
          <img src="${{imgUrl}}" alt="${{player.name}}" onerror="this.src='${{fallbackImg}}'" class="profile-portrait" />
        </div>
        
        <!-- Right Side: Information -->
        <div class="profile-info">
          <div class="profile-titles">
            <h2 class="profile-name">${{player.name}}</h2>
            <div class="profile-badges">
              <span class="badge role-badge">${{player.role}}</span>
              <span class="badge class-badge">${{player.class}}</span>
            </div>
          </div>
          
          <h3 class="section-title">Player Details</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 011.97 1.658l.68 3.82a2 2 0 001.97 1.658H20a2 2 0 012 2v5a2 2 0 01-2 2h-6l-2.4 4.8a2 2 0 01-3.578-.002L10 14z" /></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Registration ID</span>
                <span class="stat-value">${{player.registrationId || 'N/A'}}</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Contact</span>
                <span class="stat-value">${{player.phone || 'N/A'}}</span>
              </div>
            </div>

            <div class="stat-card full-width">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Class</span>
                <span class="stat-value highlight">${{player.class}}</span>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Trigger animation
  playerProfile.style.animation = 'none';
  playerProfile.offsetHeight;
  playerProfile.style.animation = 'slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards';
}}
"""

style_css_content = """
:root {
  --primary-color: #00d2ff;
  --secondary-color: #3a7bd5;
  --bg-dark: #07090d;
  --panel-bg: rgba(16, 22, 30, 0.75);
  --panel-border: rgba(255, 255, 255, 0.1);
  --text-main: #ffffff;
  --text-muted: #8b9eb5;
  --accent: #f39c12;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Outfit', sans-serif;
}

body {
  background-color: var(--bg-dark);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-image: url('/stadium_background_1779209136119.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  overflow-x: hidden;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(7, 9, 13, 0.7) 0%, rgba(7, 9, 13, 0.95) 100%);
  z-index: -1;
  backdrop-filter: blur(8px);
}

.container {
  width: 100%;
  max-width: 1100px;
  padding: 50px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  font-size: 4rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 4px;
  margin-bottom: 5px;
  background: linear-gradient(90deg, #fff, #b3cdd1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
}

p.subtitle {
  color: var(--primary-color);
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin-bottom: 50px;
  text-align: center;
}

.search-box {
  position: relative;
  width: 100%;
  max-width: 650px;
  margin-bottom: 40px;
  z-index: 100;
}

.search-input {
  width: 100%;
  padding: 22px 30px;
  font-size: 1.2rem;
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  outline: none;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.search-input:focus {
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(0, 210, 255, 0.2), 0 10px 30px rgba(0, 0, 0, 0.3);
}

.search-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  width: 100%;
  background: rgba(15, 20, 28, 0.95);
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
  list-style: none;
  max-height: 400px;
  overflow-y: auto;
  display: none;
}

.search-dropdown::-webkit-scrollbar { width: 8px; }
.search-dropdown::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: background 0.2s;
}

.dropdown-item:last-child { border-bottom: none; }
.dropdown-item:hover { background: rgba(0, 210, 255, 0.1); }

.dropdown-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
  border: 2px solid rgba(255,255,255,0.2);
}

.dropdown-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-info {
  display: flex;
  flex-direction: column;
}

.dropdown-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
}

.dropdown-role {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 3px;
}

.dropdown-no-results {
  padding: 20px;
  text-align: center;
  color: var(--text-muted);
}

.result-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--text-muted);
  opacity: 0.5;
  margin-top: 50px;
}

.empty-state svg { width: 48px; height: 48px; margin-bottom: 15px; }
.empty-state p { font-size: 1.2rem; }

.player-profile {
  width: 100%;
  max-width: 950px;
  opacity: 0;
}

.profile-card {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.1);
  backdrop-filter: blur(25px);
}

.profile-layout {
  display: flex;
  flex-direction: column;
  padding: 40px;
  gap: 40px;
}

@media (min-width: 768px) {
  .profile-layout {
    flex-direction: row;
    align-items: center;
  }
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.profile-visual {
  flex: 0 0 350px;
  height: 450px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(0,0,0,0.3);
}

.profile-portrait {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}

.profile-titles {
  margin-bottom: 40px;
}

.profile-name {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
  text-shadow: 0 4px 10px rgba(0,0,0,0.5);
  background: linear-gradient(45deg, #fff, var(--primary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.profile-badges {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.role-badge {
  background: rgba(0, 210, 255, 0.15);
  color: var(--primary-color);
  border: 1px solid rgba(0, 210, 255, 0.3);
}

.class-badge {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-title {
  font-size: 1.1rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
}

.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,0.1);
  margin-left: 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.stat-card {
  background: rgba(0,0,0,0.2);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  transition: transform 0.2s, background 0.2s;
}

.stat-card:hover {
  transform: translateY(-3px);
  background: rgba(0,0,0,0.4);
}

.stat-card.full-width {
  grid-column: 1 / -1;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(0, 210, 255, 0.1);
  color: var(--primary-color);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
}

.stat-value.highlight {
  color: var(--accent);
}

@keyframes slideUp {
  0% { opacity: 0; transform: translateY(40px) scale(0.98); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
"""

with open("d:/cricket/src/main.js", "w", encoding="utf-8") as f:
    f.write(main_js_content)

with open("d:/cricket/src/style.css", "w", encoding="utf-8") as f:
    f.write(style_css_content)
print("UI Built successfully")
