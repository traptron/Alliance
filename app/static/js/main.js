document.addEventListener(
    "DOMContentLoaded",
    () => {

        const tournamentSelect = document.getElementById(
            "tournament-select"
        )

        if (!tournamentSelect) {
            return
        }

        tournamentSelect.addEventListener(
            "change",
            async event => {

                const tournamentId = event.target.value

                const response = await fetch(
                    `/api/tournament/${tournamentId}`
                )

                const data = await response.json()

                if (data.error) {
                    return
                }

                updateTournamentMeta(data.tournament)
                updateLeagueTable(data.standings)
                updateStandingsTable(data.standings)
                updateTeamCards(data.teams)
                updateMatches(data.matches)
                updatePlayers(data.players)

                const url = new URL(window.location.href)
                url.searchParams.set("tournament", tournamentId)
                window.history.replaceState({}, "", url)
            }
        )
    }
)


function updateTournamentMeta(tournament) {

    const name = document.getElementById(
        "tournament-name"
    )

    const season = document.getElementById(
        "tournament-season"
    )

    const status = document.getElementById(
        "tournament-status"
    )

    const sport = document.getElementById(
        "tournament-sport"
    )

    if (name) {
        name.textContent = tournament.name || "—"
    }

    if (season) {
        season.textContent = tournament.season || "—"
    }

    if (status) {
        status.textContent = tournament.status || "—"
    }

    if (sport) {
        sport.textContent = tournament.sport || "—"
    }
}


function updateLeagueTable(standings) {

    const table = document.getElementById(
        "league-teams-table"
    )

    if (!table) {
        return
    }

    table.innerHTML = ""

    standings.forEach((row, index) => {

        const logoMarkup = row.logo
            ? `<img src="/static/uploads/${row.logo}" width="40" height="40" class="rounded me-2" alt="">`
            : ""

        table.innerHTML += `

            <tr>

                <td>${index + 1}</td>

                <td>
                    ${logoMarkup}
                    ${row.name}
                </td>

                <td>${row.points}</td>

            </tr>
        `
    })
}


function updateStandingsTable(standings) {

    const table =
        document.getElementById(
            "teams-table"
        )

    table.innerHTML = ""

    standings.forEach((row, index) => {

        table.innerHTML += `

            <tr>

                <td>${index + 1}</td>

                <td>${row.name}</td>

                <td>${row.wins}</td>

                <td>${row.draws}</td>

                <td>${row.losses}</td>

                <td>${row.points}</td>

                <td>${row.goal_difference}</td>

            </tr>
        `
    })
}


function updateTeamCards(teams) {

    const container =
        document.getElementById(
            "teams-list"
        )

    container.innerHTML = ""

    teams.forEach(team => {

        container.innerHTML += `

            <div class="col-md-4">

                <div class="card mb-3">

                    <div class="card-body">

                        <h5>
                            ${team.name}
                        </h5>

                        <p>
                            Спорт: ${team.sport || ""}
                        </p>

                    </div>

                </div>

            </div>
        `
    })
}


function updateMatches(matches) {

    const container =
        document.getElementById(
            "matches-list"
        )

    container.innerHTML = ""

    matches.forEach(match => {

        container.innerHTML += `

            <div class="col-md-6">

                <div class="card mb-3">

                    <div class="card-body">

                        <h5>
                            ${match.team1}
                            vs
                            ${match.team2}
                        </h5>

                        <p>
                            ${match.date}
                        </p>

                        <p>
                            ${match.score1}
                            :
                            ${match.score2}
                        </p>

                    </div>

                </div>

            </div>
        `
    })
}


function updatePlayers(players) {

    const container =
        document.getElementById(
            "players-list"
        )

    container.innerHTML = ""

    players.forEach(player => {

        container.innerHTML += `

            <div class="col-md-4">

                <div class="card mb-3">

                    <div class="card-body">

                        <h5>
                            ${player.name}
                        </h5>

                        <p>
                            ${player.team}
                        </p>

                        <p>
                            Голы:
                            ${player.goals}
                        </p>

                    </div>

                </div>

            </div>
        `
    })
}
