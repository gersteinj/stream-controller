async function getMatchInfo() {
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

export async function getRobotList(weight = null) {
    if (weight == 'ANT' || weight == 'PLANT' || weight == 'BEETLE') {
        let response = await fetch(`http://localhost:8000/robots/${weight}`);
        return await response.json();
    } else {
        let response = await fetch(`http://localhost:8000/robots`);
        return await response.json();
    }
}

export async function postNewRobot(display_name, weight) {
    fetch('http://localhost:8000/robots/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
            display_name: display_name,
            weight: weight
        })
    })
        .then(response => response.json())
        .then(json => console.log(json));
}