export async function getMatchInfo() {
    let response = await fetch('http://localhost:8000/currentmatch');
    return await response.json();
}

export function displayMatchInfo() {
    getMatchInfo().then(match => {
        console.log(`updating match`);
        document.getElementById('weight').innerText = match.weight;
        document.getElementById('red-bot').innerText = match.red_bot.display_name;
        document.getElementById('blue-bot').innerText = match.blue_bot.display_name;
    })
}