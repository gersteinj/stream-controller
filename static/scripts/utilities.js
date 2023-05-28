export async function getLatestMatch() {
    let response = await fetch('http://localhost:8000/matches/latest');
    return await response.json();
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

export async function postNewMatch(red_bot, blue_bot, weight) {
    let message = JSON.stringify({
        weight: weight,
        red_bot: red_bot,
        blue_bot: blue_bot
    });
    fetch('http://localhost:8000/matches/', {
        method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: message
    }).then(response => response.json()).then(json => console.log(json));
}