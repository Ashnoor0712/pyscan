# PyScan

A multithreaded TCP port scanner with banner grabbing and JSON/CSV export, built from scratch in Python.

## Features

- **Multithreaded scanning** — uses `ThreadPoolExecutor` to scan ports concurrently instead of one at a time
- **Banner grabbing** — attempts to identify what's running on open ports by reading service responses (with an HTTP request fallback for web services)
- **Configurable via CLI** — target, port range, and thread count are all passed as arguments
- **Export results** — save scan results to JSON or CSV

## Usage

```bash
python3 pyscan.py -t <target> -p <port_range> --threads <num_threads> -o <output_file>
```

### Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `-t`, `--target` | Target IP or hostname (required) | — |
| `-p`, `--ports` | Port range to scan, e.g. `1-1024` | `1-1024` |
| `--threads` | Number of concurrent threads | `100` |
| `-o`, `--output` | Save results to a file (`.json` or `.csv`) | none |

### Examples

Scan localhost on the default port range:
```bash
python3 pyscan.py -t 127.0.0.1
```

Scan a wider range with more threads:
```bash
python3 pyscan.py -t 127.0.0.1 -p 1-8100 --threads 200
```

Scan and export results to JSON:
```bash
python3 pyscan.py -t 127.0.0.1 -p 1-8100 -o results.json
```

## Sample Output

Scanning 127.0.0.1 ...
Port 8000 is OPEN - HTTP/1.0 200 OK
Scan finished.
Results saved to results.json


## How It Works

For each port in the given range, PyScan opens a TCP socket and attempts a connection. If the connection succeeds, it tries to read a banner from the service — and if nothing comes back immediately (common for web servers), it sends a minimal HTTP `HEAD` request to prompt a response. All open ports and their banners are collected and optionally written to a JSON or CSV file.

## Roadmap

- UDP scanning support
- Service fingerprinting beyond basic HTTP banners
- Progress bar for large scans
