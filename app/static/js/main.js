document.addEventListener("DOMContentLoaded", () => {
    const tournamentSelect = document.getElementById("tournament-select")
    if (!tournamentSelect) return

    tournamentSelect.addEventListener("change", async event => {
        const tournamentId = event.target.value
        const response = await fetch(`/api/tournament/${tournamentId}`)
        const data = await response.json()

        if (data.error) return

        updateTournamentMeta(data.tournament)
        updateStandingsTable(data.standings)
        updateTeamCards(data.teams)
        updateMatches(data.matches)
        updatePlayers(data.players)

        const url = new URL(window.location.href)
        url.searchParams.set("tournament", tournamentId)
        window.history.replaceState({}, "", url)
    })
})


function updateTournamentMeta(tournament) {
    const name   = document.getElementById("tournament-name")
    const season = document.getElementById("tournament-season")
    const status = document.getElementById("tournament-status")
    const sport  = document.getElementById("tournament-sport")

    if (name)   name.textContent   = tournament.name   || "—"
    if (season) season.textContent = tournament.season || "—"
    if (status) status.textContent = tournament.status || "—"
    if (sport)  sport.textContent  = tournament.sport  || "—"
}


function rankClass(index) {
    if (index === 0) return "row-rank--gold"
    if (index === 1) return "row-rank--silver"
    if (index === 2) return "row-rank--bronze"
    return ""
}


function updateStandingsTable(standings) {
    const table = document.getElementById("teams-table")
    if (!table) return

    table.innerHTML = standings.map((row, i) => {
        const gd = row.goal_difference
        const gdClass = gd > 0 ? "stat-val--pos" : gd < 0 ? "stat-val--neg" : ""
        const gdText  = gd > 0 ? `+${gd}` : `${gd}`
        const logoMarkup = row.logo
            ? `<img src="/static/uploads/${row.logo}" class="team-logo" alt="">`
            : `<div class="team-logo-placeholder">${row.name ? row.name[0] : ""}</div>`

        return `
            <tr>
                <td class="row-rank">${i + 1}</td>
                <td>
                    <div class="team-cell">
                        ${logoMarkup}
                        <span class="team-name">${row.name}</span>
                    </div>
                </td>
                <td><span class="stat-val stat-val--pos">${row.wins}</span></td>
                <td><span class="stat-val">${row.draws}</span></td>
                <td><span class="stat-val stat-val--neg">${row.losses}</span></td>
                <td><span class="points-badge">${row.points}</span></td>
                <td><span class="stat-val ${gdClass}">${gdText}</span></td>
            </tr>
        `
    }).join("")
}


function updateTeamCards(teams) {
    const container = document.getElementById("teams-list")
    if (!container) return

    container.innerHTML = teams.map(team => `
        <div class="alliance-card animate-in">
            <div class="card-sport-tag">${team.sport || ""}</div>
            <div class="card-title">${team.name}</div>
            <div class="card-sub">Участник турнира</div>
        </div>
    `).join("")
}


function updateMatches(matches) {
    const container = document.getElementById("matches-list")
    if (!container) return

    container.innerHTML = matches.map(match => {
        const finished = match.score1 !== null && match.score2 !== null
        const statusClass = finished ? "match-status--finished" : "match-status--upcoming"
        const statusText  = finished ? "finished" : "upcoming"
        const score1 = match.score1 ?? "—"
        const score2 = match.score2 ?? "—"

        return `
            <div class="match-card animate-in">
                <div class="match-teams">
                    <div class="match-team">
                        <div class="match-team-name">${match.team1}</div>
                    </div>
                    <div class="match-score">
                        <div class="score-display">${score1}<span class="score-separator"> : </span>${score2}</div>
                    </div>
                    <div class="match-team">
                        <div class="match-team-name">${match.team2}</div>
                    </div>
                </div>
                <div class="match-meta">
                    <span class="match-date">${match.date || "—"}</span>
                    <span class="match-status ${statusClass}">${statusText}</span>
                </div>
            </div>
        `
    }).join("")
}


function updatePlayers(players) {
    const container = document.getElementById("players-list")
    if (!container) return

    container.innerHTML = players.map((player, i) => {
        const rankClass = i < 3 ? `player-rank-badge--${i + 1}` : ""

        return `
            <div class="player-card animate-in">
                <div class="player-rank-badge ${rankClass}">${i + 1}</div>
                <div class="player-info">
                    <div class="player-name">${player.name}</div>
                    <div class="player-team">${player.team}</div>
                </div>
                <div class="player-goals">
                    <span class="goals-num">${player.primary_value ?? "—"}</span>
                    <span class="goals-label">${player.primary_label || ""}</span>
                </div>
            </div>
        `
    }).join("")
}