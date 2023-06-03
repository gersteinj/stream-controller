const MQTT_HOST = '192.168.2.3';
const MQTT_PORT = '9001';
export const MQTT_WS_URL = `ws://${MQTT_HOST}:${MQTT_PORT}`;
// export MQTT_WS_URL;

const API_HOST = '192.168.2.5';
// const API_HOST = '192.168.184.41';
const API_PORT = '8000';
export const API_URL = `http://${API_HOST}:${API_PORT}`;
export const WS_URL = `ws://${API_HOST}:${API_PORT}/ws`;
// export API_URL;
// export WS_URL;

export async function postNewRobot(robot_name, weight) {
    let message = JSON.stringify({
        robot_name: robot_name,
        weight: weight
    });
    let response = await fetch(`${API_URL}/robots/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: message
    })
    return await response.json();
}

export async function getRobotList(weight=null) {
    if (weight == 'ANT' || weight == 'PLANT' || weight == 'BEETLE') {
        let response = await fetch(`${API_URL}/robots/${weight}`);
        return await response.json();
    } else {
        let response = await fetch(`${API_URL}/robots`);
        return await response.json();
    }
}

export async function getLatestMatchID() {
    let response = await fetch(`${API_URL}/matches/latest`);
    return await response.text();
}

export async function getMatchDetails(match_id) {
    let response = await fetch(`${API_URL}/matches/${match_id}/detail`);
    return await response.json();
}

export async function postNewMatch(red_id, blue_id, weight) {
    let message = JSON.stringify({
        weight: weight,
        red_id: red_id,
        blue_id: blue_id
    });
    console.log(message);
    let response = await fetch(`${API_URL}/matches/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: message
    });

    return await response.json();
}
