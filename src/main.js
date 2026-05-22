import './style.css'
import playersData from '../players.json'

function getImageUrl(url, size) {
  if (!url) return '';
  if (url.includes('drive.google.com')) return url.replace('/uc?id=', '/thumbnail?id=') + '&sz=w' + size;
  return url;
}

function parsePlayerRole(role) {
  const defaults = { hand: 'Right', category: 'Batter', categoryKey: 'batsman' };
  if (!role) return defaults;

  const hand = role.toLowerCase().startsWith('left') ? 'Left' : 'Right';
  let category = 'Batter';
  let categoryKey = 'batsman';

  if (/all-rounder/i.test(role)) {
    category = 'All-rounder';
    categoryKey = 'allrounder';
  } else if (/bowler/i.test(role)) {
    category = 'Bowler';
    categoryKey = 'bowler';
  }

  return { hand, category, categoryKey };
}

document.querySelector('#app').innerHTML = `
  <div class="overlay"></div>
  <div class="container">
    <h1>BBHC League</h1>
    <p class="subtitle">Official Player Database</p>
    <p class="player-count" id="playerCount">${playersData.length} Players</p>
    
    <div class="search-box">
      <input type="text" id="searchInput" class="search-input" placeholder="Search name or type &quot;all&quot;..." autocomplete="off" />
      <button type="button" id="showAllBtn" class="show-all-btn">All</button>
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
const showAllBtn = document.getElementById('showAllBtn');
const emptyState = document.getElementById('emptyState');
const playerProfile = document.getElementById('playerProfile');

const sortedPlayers = [...playersData].sort((a, b) =>
  a.name.localeCompare(b.name, undefined, { sensitivity: 'base' })
);

function getMatches(query) {
  if (query === 'all') return sortedPlayers;
  return sortedPlayers.filter(p => p.name.toLowerCase().includes(query));
}

function renderSearchResults(matches, totalCount) {
  const countLabel =
    matches.length === totalCount
      ? `${totalCount} Players`
      : `${matches.length} of ${totalCount} Players`;

  if (matches.length === 0) {
    searchDropdown.innerHTML = `
      <li class="dropdown-header">${countLabel}</li>
      <li class="dropdown-no-results">No players found</li>
    `;
    searchDropdown.style.display = 'block';
    return;
  }

  searchDropdown.innerHTML = `
    <li class="dropdown-header">${countLabel}</li>
    ${matches
      .map((match, idx) => {
        const { hand, category, categoryKey } = parsePlayerRole(match.role);
        return `
      <li class="dropdown-item" data-index="${idx}">
        <div class="dropdown-avatar">
          <img src="${match.photoUrl ? getImageUrl(match.photoUrl, 150) : 'https://ui-avatars.com/api/?name=' + encodeURIComponent(match.name) + '&background=random'}" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(match.name)}&background=random'" />
        </div>
        <div class="dropdown-info">
          <span class="dropdown-name">${match.name}</span>
          <span class="dropdown-meta">${match.class} · ${match.registrationId || 'N/A'}</span>
          <span class="dropdown-tags">
            <span class="tag-mini category-${categoryKey}">${category}</span>
            <span class="tag-mini hand-${hand.toLowerCase()}">${hand} Hand</span>
          </span>
        </div>
      </li>
    `;
      })
      .join('')}
  `;
  searchDropdown.style.display = 'block';

  searchDropdown.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', () => {
      const player = matches[item.getAttribute('data-index')];
      renderPlayer(player);
      searchDropdown.style.display = 'none';
      searchInput.value = player.name;
    });
  });
}

function runSearch() {
  const query = searchInput.value.toLowerCase().trim();
  if (query.length < 1) {
    searchDropdown.style.display = 'none';
    return;
  }
  renderSearchResults(getMatches(query), playersData.length);
}

function showAllPlayers() {
  searchInput.value = 'all';
  renderSearchResults(sortedPlayers, playersData.length);
  searchInput.focus();
}

// Close dropdown on outside click
document.addEventListener('click', (e) => {
  if (
    !searchInput.contains(e.target) &&
    !searchDropdown.contains(e.target) &&
    !showAllBtn.contains(e.target)
  ) {
    searchDropdown.style.display = 'none';
  }
});

searchInput.addEventListener('input', runSearch);
showAllBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  showAllPlayers();
});

function renderPlayer(player) {
  emptyState.style.display = 'none';
  playerProfile.style.display = 'block';
  
  const fallbackImg = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(player.name) + '&background=random&size=200';
  const imgUrl = player.photoUrl ? getImageUrl(player.photoUrl, 800) : fallbackImg;
  const { hand, category, categoryKey } = parsePlayerRole(player.role);
  
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
          </div>
          
          <h3 class="section-title">Player Details</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon stat-icon-category">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M5 16L3 5l5.5 2L12 4l3.5 3L21 5l-2 11H5zm2.7-2h8.6l.9-5.4-2.2.8L12 8.5 8.9 9.4 6.7 8.6l.9 5.4z"/></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Category</span>
                <span class="stat-value stat-value-category category-${categoryKey}">${category}</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon stat-icon-hand">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 11.5V14m0-2.5v-6a1.5 1.5 0 013 0V10m0-5.5v-1a1.5 1.5 0 013 0V10m0-5.5a1.5 1.5 0 013 0V14m0-8.5a1.5 1.5 0 013 0V14m0-2.5a1.5 1.5 0 013 0V14m0-2.5v-1a1.5 1.5 0 013 0V14"/></svg>
              </div>
              <div class="stat-details">
                <span class="stat-label">Right / Left</span>
                <span class="stat-value stat-value-hand hand-${hand.toLowerCase()}">${hand} Hand</span>
              </div>
            </div>

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
