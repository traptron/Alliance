document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".nav-toggle")
    const navbar = document.querySelector(".alliance-navbar")
    const navClose = document.querySelector(".nav-close")
    const navLinks = document.querySelectorAll(".nav-menu .nav-link")
    const footer = document.querySelector(".site-footer")

    if (navToggle && navbar) {
        navToggle.addEventListener("click", () => {
            const isOpen = navbar.classList.toggle("nav-open")
            navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false")
        })
    }

    if (navClose && navbar && navToggle) {
        navClose.addEventListener("click", () => {
            navbar.classList.remove("nav-open")
            navToggle.setAttribute("aria-expanded", "false")
        })
    }

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (navbar && navToggle) {
                navbar.classList.remove("nav-open")
                navToggle.setAttribute("aria-expanded", "false")
            }
        })
    })

    if (footer) {
        const updateFooterVisibility = () => {
            const scrollBottom = window.innerHeight + window.scrollY
            const pageHeight = document.documentElement.scrollHeight
            const isAtBottom = scrollBottom >= pageHeight - 2

            footer.classList.toggle("footer-visible", isAtBottom)
        }

        updateFooterVisibility()
        window.addEventListener("scroll", updateFooterVisibility, { passive: true })
        window.addEventListener("resize", updateFooterVisibility)
    }

    const tournamentSelect = document.getElementById("tournament-select")
    const sportSelect = document.getElementById("sport-select")
    if (!tournamentSelect) return

    const fetchTournament = async (tournamentId, tournamentSportId) => {
        const url = new URL(`/api/tournament/${tournamentId}`, window.location.origin)

        if (tournamentSportId) {
            url.searchParams.set("sport", tournamentSportId)
        }

        const response = await fetch(url)
        const data = await response.json()

        if (data.error) return

        updateTournamentMeta(data.tournament)
        updateStandingsTable(data.standings)
        updateTeamCards(data.teams)
        updateMatches(data.matches)
        updatePlayers(data.players)
        updateSportSelect(data.sports, data.tournament.tournament_sport_id)

        const pageUrl = new URL(window.location.href)
        pageUrl.searchParams.set("tournament", tournamentId)
        if (data.tournament.tournament_sport_id) {
            pageUrl.searchParams.set("sport", data.tournament.tournament_sport_id)
        }
        window.history.replaceState({}, "", pageUrl)
    }

    tournamentSelect.addEventListener("change", async event => {
        const tournamentId = event.target.value
        await fetchTournament(tournamentId, null)
    })

    if (sportSelect) {
        sportSelect.addEventListener("change", async event => {
            const tournamentId = tournamentSelect.value
            const tournamentSportId = event.target.value
            await fetchTournament(tournamentId, tournamentSportId)
        })
    }
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


function updateSportSelect(sports, selectedId) {
    const sportSelect = document.getElementById("sport-select")
    if (!sportSelect || !Array.isArray(sports)) return

    sportSelect.innerHTML = sports.map(sport => {
        const selected = sport.id === selectedId ? "selected" : ""
        return `<option value="${sport.id}" ${selected}>${sport.name}</option>`
    }).join("")
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
        const statusText = match.status || "upcoming"
        const finished = statusText === "finished"
        const statusClass = finished ? "match-status--finished" : "match-status--upcoming"
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