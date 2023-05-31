# GSCRL Stream Manager

## Websocket Messages

For consistency, send **all** websocket messages as JSON.

Websocket JSON message structure:

| key        | value                 |
| ---------- | --------------------- |
| event_type | new_match, disconnect |
| disconnect | null |
