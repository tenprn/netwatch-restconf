# NetWatch RESTCONF

NetWatch RESTCONF is a small Python network-health checker for Cisco IOS XE devices. It retrieves operational data through RESTCONF and presents a terminal report covering:

- Interface administrative and operational status
- Top memory-consuming processes
- CPU utilization over five seconds, one minute, and five minutes

The repository also includes utilities for discovering supported YANG modules, saving RESTCONF responses, and generating readable YANG trees with `pyang`.

## Requirements

- Python 3.10 or newer
- A Cisco IOS XE device with RESTCONF enabled
- Device credentials authorized to read the selected operational YANG models
- Network access to the device (and VPN access when required by a reserved DevNet sandbox)

## Setup

The easiest setup uses the included Makefile:

```bash
make setup
```

Then update `.env` with the current device hostname and credentials. Run `make help` to see every available command.

To set up the project manually, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install requests python-dotenv pyang
```

Create your local environment file:

```bash
cp .env.example .env
```

Update `.env` with credentials for one device:

```dotenv
HOST=your-ios-xe-device.example.com
USERNAME=your-device-username
PASSWORD=your-device-password
```

Keep the hostname, username, and password from the same device or sandbox reservation. The real `.env` file is excluded from Git.

## Run the health check

The current entry point is `netwatch/main.py`. Run it as a module from the repository root:

```bash
make run
```

The equivalent Python command is:

```bash
.venv/bin/python -m netwatch.main
```

## Supporting tools

| File | Purpose |
| ---- | ---- |
| `netwatch/main.py` | Retrieves live interface, CPU, and memory data and prints the health report |
| `scripts/supported_yang.py` | Retrieves the YANG modules advertised by the device |
| `scripts/dump_data.py` | Saves a selected RESTCONF response as formatted JSON for development and testing |
| `scripts/run_pyang.py` | Converts `.yang` files in `yang_module_schema/` into readable tree output |
| `netwatch/config.py` | Defines RESTCONF headers, YANG model names, and endpoint URLs |
| `netwatch/api.py` | Sends RESTCONF requests and parses JSON responses |
| `netwatch/display.py` | Evaluates and displays interface, CPU, and memory health |
| `netwatch/utils.py` | Contains response-extraction and formatting helpers |

Generate YANG trees with:

```bash
make pyang
```

Retrieve supported YANG modules or dump the selected RESTCONF data with:

```bash
make supported-yang
make dump-data
```

Generated trees are written to `yang_module_tree/`.

## Generated and confidential files

The following are intentionally excluded from Git:

- `.env` and environment-specific variants, because they may contain credentials
- `.venv/`, Python caches, and editor files, because they are machine-specific
- `output_files/`, because RESTCONF responses can expose device inventory and operational data
- `report/`, because health reports can reveal interface names and device state
- `yang_module_tree/`, because it is generated from the source YANG files
- Session logs, configuration exports, private keys, and credential containers

The `yang_module_schema/` directory is not ignored because its YANG models are inputs to `scripts/run_pyang.py`. Review their licensing and origin before publishing them.

## Security

`api.py` currently uses `verify=False` because Cisco lab devices may present self-signed HTTPS certificates. This disables TLS certificate verification and is appropriate only for a controlled lab. For production, install the device or organization CA certificate and pass its path through `verify` instead.

Never commit real usernames, passwords, device configuration exports, private keys, or raw production-device responses.

## Troubleshooting

- `401 access-denied`: the hostname and credentials do not match, credentials expired, or the user lacks RESTCONF permission.
- `403`: the authenticated user is not authorized for the requested data.
- `404`: the device or IOS XE release does not expose that YANG path.
- `502`: the gateway reached by the script cannot communicate with the device RESTCONF backend; this is common when a sandbox instance is unavailable.
- Connection timeout: confirm DNS, routing, firewall rules, sandbox reservation status, and VPN connectivity.
- `InsecureRequestWarning`: this is a warning caused by `verify=False`, not an authentication failure.

## License

See [LICENSE](LICENSE).
