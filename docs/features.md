# Features

| Feature        | Hotkey | Notes                                                    |
| -------------- | ------ | -------------------------------------------------------- |
| Godmode        | F1     | Freezes health writes to player struct.                  |
| Noclip         | F2     | Disables collision on the player ped.                    |
| Money drop     | —      | Spawns a money pickup at player coords.                  |
| Vehicle spawn  | —      | Spawns a horse/wagon by model name.                      |

All features are single-player only. They will not work (and are not supported)
in Red Dead Online — Rockstar's anti-cheat will flag any memory writes there.

Feature toggles are written to `config/menu.toml` under `features = [...]`.
Removing a feature from that list simply skips registering its processor.