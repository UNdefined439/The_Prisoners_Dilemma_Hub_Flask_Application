games = {
    1: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },
    2: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },3: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },4: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },5: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },6: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },7: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    },8: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1
    }
}

async function play(strat_id, action) {
    const game = games[strat_id]

    // Return if game is completed.
    if (game.round == 11) {
        return
    }

    // Send POST request.
    const result = await fetch('api/game', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({strat_id, action: action, history: game.history, round: game.round})
    })

    // Log error if request failed.
    if (!result.ok) {
        console.error('Play() failed:', result.status)
        return
    }

    const data = await result.json()

    console.log(data)

    // Update score table
    const table = document.querySelector(`#strat_${strat_id} table`) 
    const row = table.querySelector('tbody').children[game.round - 1]
    row.children[1].innerText = data.player_score
    row.children[2].innerText = data.bot_score
    
    const total_row = table.querySelector('tfoot tr')
    total_row.children[1].innerText = Number(total_row.children[1].innerText) + data.player_score
    total_row.children[2].innerText = Number(total_row.children[2].innerText) + data.bot_score

    // Update round and explanation
    const round = document.querySelector(`#strat_${strat_id} .round_title`)
    round.innerText = `Round ${data.round}:`
    
    const explanation = document.querySelector(`#strat_${strat_id} .explanation`)
    explanation.innerText = data.explanation

    // Update game state
    games[strat_id].history[data.round - 1] = [action, data.response]
    games[strat_id].round = data.round

    return
}