games = {
    1: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },
    2: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },3: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },4: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },5: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },6: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },7: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
    },8: {
        history: Array.from({length: 10}, ()=>[null, null]),
        round: 1,
        player_total: 0,
        bot_total: 0
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
        body: JSON.stringify({strat_id, action: action, history: game.history, round: game.round, player_total: game.player_total, bot_total: game.bot_total})
    })

    // Log error if request failed.
    if (!result.ok) {
        console.error('Play() failed:', result.status)
        return
    }

    const data = await result.json()

    // Update score table
    const table = document.querySelector(`#strat_${strat_id} table`) 
    const row = table.querySelector('tbody').children[game.round - 1]
    row.children[1].innerText = data.player_score
    row.children[2].innerText = data.bot_score
    
    const total_row = table.querySelector('tfoot tr')   
    game.player_total += data.player_score
    game.bot_total += data.bot_score
    total_row.children[1].innerText = game.player_total
    total_row.children[2].innerText = game.bot_total

    // Update round and explanation
    const round = document.querySelector(`#strat_${strat_id} .round_title`)
    round.innerText = `Round ${game.round}:`
    
    const explanation = document.querySelector(`#strat_${strat_id} .explanation`)
    explanation.innerText = data.explanation

    // Update game state
    games[strat_id].history[game.round - 1] = [action, data.response]
    games[strat_id].round++

    console.log(games[strat_id])
    return
}