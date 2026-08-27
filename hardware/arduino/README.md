# Optional Arduino and ESP8266 relay examples

These sketches are optional hardware experiments and are not required by the desktop application.

- `access_point_relay.ino` creates a local setup access point.
- `router_relay.ino` connects an ESP8266 relay to an existing Wi-Fi network.
- `http_relay.ino` exposes a minimal HTTP-controlled relay example.

Replace the placeholder SSID and password locally before flashing a device. Do not commit real Wi-Fi credentials. Review the HTTP routes and add authentication before using any sketch outside an isolated development network.
