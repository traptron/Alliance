document.addEventListener(
    "DOMContentLoaded",
    () => {

        const buttons = document.querySelectorAll(
            ".sport-button"
        )

        buttons.forEach(button => {

            button.addEventListener(
                "click",
                async () => {

                    const sport =
                        button.dataset.sport

                    const response =
                        await fetch(
                            `/api/sport/${sport}`
                        )

                    const data =
                        await response.json()

                    updateTeamCards(data.teams)

                    updateTeams(data.teams)

                    updateMatches(data.matches)

                    updatePlayers(data.players)
                }
            )
        })
    }
)


function updateTeams(teams) {

    const table =
        document.getElementById(
            "teams-table"
        )

    table.innerHTML = ""

    teams.forEach((team, index) => {

        table.innerHTML += `

            <tr>

                <td>${index + 1}</td>

                <td>${team.name}</td>

                <td>${team.wins}</td>

                <td>${team.draws}</td>

                <td>${team.losses}</td>

                <td>${team.points}</td>

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

                        <p>
                            Институт: ${team.institute || ""}
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
