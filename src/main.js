import './style.css'
import playersData from '../players.json'

playersData.forEach(p => {
  if (p.registrationId && p.registrationId.trim() === 'BCA23078') {
    p.photoUrl = '/darshan_BCA23078.jpg';
  }
});

function getImageUrl(url, size) {
  if (!url) return '';
  if (url.includes('drive.google.com')) return url.replace('/uc?id=', '/thumbnail?id=') + '&sz=w' + size;
  return url;
}

document.querySelector('#app').innerHTML = `
  <div class="overlay"></div>
  <div class="container">
    <h1>BBHC League</h1>
    <p class="subtitle">Official Player Database</p>
    
    <div class="search-box">
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="Search player name..." autocomplete="off" />
        <button id="showAllBtn" class="show-all-btn">All</button>
      </div>
      <ul id="searchDropdown" class="search-dropdown"></ul>
    </div>

    <div id="playerCount" class="player-count" style="display: none;"></div>

    <div class="result-container" id="resultContainer">
      <div id="emptyState" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>
        <p>Search for a player to view their profile</p>
      </div>
      <div id="playerProfile" class="player-profile" style="display: none;"></div>
      <div id="allPlayersGrid" class="all-players-grid" style="display: none;"></div>
    </div>
  </div>
`

const searchInput = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');
const emptyState = document.getElementById('emptyState');
const playerProfile = document.getElementById('playerProfile');
const showAllBtn = document.getElementById('showAllBtn');
const playerCount = document.getElementById('playerCount');
const allPlayersGrid = document.getElementById('allPlayersGrid');

// Close dropdown on outside click
document.addEventListener('click', (e) => {
  if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
    searchDropdown.style.display = 'none';
  }
});

showAllBtn.addEventListener('click', () => {
  renderAllPlayers(playersData);
});

searchInput.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  
  if (query.length < 1) {
    searchDropdown.style.display = 'none';
    allPlayersGrid.style.display = 'none';
    playerCount.style.display = 'none';
    if (playerProfile.style.display === 'none') {
      emptyState.style.display = 'flex';
    }
    return;
  }

  const matches = playersData.filter(p => p.name.toLowerCase().includes(query));

  if (matches.length > 0) {
    searchDropdown.innerHTML = matches.map((match, idx) => `
      <li class="dropdown-item" data-index="${idx}">
        <div class="dropdown-avatar">
          <img src="${match.photoUrl ? getImageUrl(match.photoUrl, 150) : 'https://ui-avatars.com/api/?name=' + encodeURIComponent(match.name) + '&background=random'}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.name)}&background=random'" />
        </div>
        <div class="dropdown-info">
          <span class="dropdown-name">${match.name}</span>
          <span class="dropdown-role">${match.class} &bull; ${match.role}</span>
        </div>
      </li>
    `).join('');
    searchDropdown.style.display = 'block';
    
    // Add click listeners to items
    const items = searchDropdown.querySelectorAll('.dropdown-item');
    items.forEach(item => {
      item.addEventListener('click', () => {
        const player = matches[item.getAttribute('data-index')];
        renderPlayer(player);
        searchDropdown.style.display = 'none';
        searchInput.value = player.name;
      });
    });
    
  } else {
    searchDropdown.innerHTML = `<li class="dropdown-no-results">No players found</li>`;
    searchDropdown.style.display = 'block';
  }
});

function renderAllPlayers(players) {
  emptyState.style.display = 'none';
  playerProfile.style.display = 'none';
  allPlayersGrid.style.display = 'grid';
  searchDropdown.style.display = 'none';
  searchInput.value = '';

  playerCount.style.display = 'block';
  playerCount.innerHTML = `<span class="count-number">${players.length}</span> Players Found`;

  allPlayersGrid.innerHTML = players.map((player, idx) => {
    const fallbackImg = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(player.name) + '&background=random&size=150';
    const imgUrl = player.photoUrl ? getImageUrl(player.photoUrl, 300) : fallbackImg;
    return `
      <div class="player-card" data-idx="${idx}">
        <div class="player-card-img">
          <img src="${imgUrl}" alt="${player.name}" onerror="this.src='${fallbackImg}'" />
        </div>
        <div class="player-card-body">
          <h3 class="player-card-name">${player.name}</h3>
          <span class="player-card-role">${player.role}</span>
          <span class="player-card-class">${player.class}</span>
        </div>
      </div>
    `;
  }).join('');

  allPlayersGrid.querySelectorAll('.player-card').forEach(card => {
    card.addEventListener('click', () => {
      const player = players[card.getAttribute('data-idx')];
      allPlayersGrid.style.display = 'none';
      playerCount.style.display = 'none';
      renderPlayer(player);
      searchInput.value = player.name;
    });
  });

  allPlayersGrid.style.animation = 'none';
  allPlayersGrid.offsetHeight;
  allPlayersGrid.style.animation = 'slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards';
}

function renderPlayer(player) {
  emptyState.style.display = 'none';
  allPlayersGrid.style.display = 'none';
  playerCount.style.display = 'none';
  playerProfile.style.display = 'block';
  
  const fallbackImg = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(player.name) + '&background=random&size=200';
  const imgUrl = player.photoUrl ? getImageUrl(player.photoUrl, 800) : fallbackImg;
  
  playerProfile.innerHTML = `
    <div class="profile-card">
      <div class="profile-layout">
        <!-- Left Side: Portrait -->
        <div class="profile-visual">
          <img src="${imgUrl}" alt="${player.name}" onerror="this.src='${fallbackImg}'" class="profile-portrait" />
        </div>
        
        <!-- Right Side: Information -->
        <div class="profile-info">
          <div class="profile-titles">
            <h2 class="profile-name">${player.name}</h2>
            <div class="profile-badges">
              <span class="badge role-badge">${player.role}</span>
              <span class="badge class-badge">${player.class}</span>
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
                <span class="stat-value">${player.registrationId || 'N/A'}</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Contact</span>
                <span class="stat-value">${player.phone || 'N/A'}</span>
              </div>
            </div>

            <div class="stat-card full-width">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Class</span>
                <span class="stat-value highlight">${player.class}</span>
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
}
