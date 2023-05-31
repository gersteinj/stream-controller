
export async function getRobotList(weight = null) {
    if (weight == 'ANT' || weight == 'PLANT' || weight == 'BEETLE') {
        let response = await fetch(`http://localhost:8000/robots/${weight}`);
        return await response.json();
    } else {
        let response = await fetch(`http://localhost:8000/robots`);
        return await response.json();
    }
}

export async function postNewRobot(robot_name, weight) {
    let message = JSON.stringify({
        robot_name: robot_name,
        weight: weight
    });
    // console.log(`Creating a robot from ${message}`);
    fetch('http://localhost:8000/robots/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: message
    })
        .then(response => response.json())
        .then(json => console.log(json));
}

export async function postNewMatch(red_id, blue_id, weight) {
    let message = JSON.stringify({
        weight: weight,
        red_id: red_id,
        blue_id: blue_id
    });
    fetch('http://localhost:8000/matches/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: message
    })
    .then(response => response.json())
    .then(json => console.log(json));
}

export async function getLatestMatch() {
    let response = await fetch('http://localhost:8000/matches/latest');
    return await response.text()   
}