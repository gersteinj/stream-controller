# GSCRL Stream Manager

## Websocket Messages

For consistency, send **all** websocket messages as JSON.

Websocket JSON message structure:

| key        | value                 |
| ---------- | --------------------- |
| event_type | new_match, disconnect |
| disconnect | null                  |

# MQTT Topics & Messages

At least for now, MQTT is still needed for communicating with the arena controller

| topic       | description                             | format                                                                                                            |
| ----------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| timecontrol | Send time-related signals               | `r` for reset, `a<int>` to add `int` seconds.                                                                     |
| botcontrol  | Receive time and match state from arena | `{"Mills":374962,"Match_State_Code":12,"Match_State":"system_startup","Match_Sec_remain":150,"Match_Length":150}` |
