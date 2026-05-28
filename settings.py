from os import getenv


def _env(key, default=""):
    return getenv(key, default)


def _as_int(value, default):
    try:
        return int(value)
    except Exception:
        return int(default)


def _as_bool(value, default=False):
    raw = str(value if value is not None else "").strip().lower()
    if not raw:
        return bool(default)
    return raw in {"1", "true", "yes", "on"}


def _as_float(value, default):
    try:
        return float(value)
    except Exception:
        return float(default)


HOST = str(_env("PORTHOUND_HOST", _env("HOST", "127.0.0.1"))).strip() or "127.0.0.1"
PORT = _as_int(_env("PORTHOUND_PORT", _env("PORT", "45678")), 45678)
SCAN_DB_PATH = str(_env("PORTHOUND_DB_PATH", "Standalone.db")).strip() or "Standalone.db"
DEBUG = _as_bool(_env("PORTHOUND_DEBUG", "1"), default=True)
API_TOKEN = str(_env("PORTHOUND_API_TOKEN", "")).strip()
API_REQUIRE_TOKEN = _as_bool(_env("PORTHOUND_API_REQUIRE_TOKEN", "0"), default=False)
CORS_ALLOW_ORIGIN = str(_env("PORTHOUND_CORS_ALLOW_ORIGIN", "")).strip()

# PortHound now runs in standalone mode only.
ROLE = "standalone"

PORTHOUND_CA = str(_env("PORTHOUND_CA", "")).strip()
PORTHOUND_CA_ONELINE = str(_env("PORTHOUND_CA_ONELINE", "")).strip()
PORTHOUND_MASTER = str(_env("PORTHOUND_MASTER", "")).strip()
PORTHOUND_IP = str(_env("PORTHOUND_IP", "")).strip()

TLS_ENABLED = _as_bool(_env("PORTHOUND_TLS_ENABLED", "0"), default=False)
TLS_CERT_FILE = str(
    _env("PORTHOUND_TLS_CERT_FILE", "certs/master/master.cert.pem")
).strip()
TLS_KEY_FILE = str(_env("PORTHOUND_TLS_KEY_FILE", "certs/master/master.key.pem")).strip()
TLS_REQUIRE_CLIENT_CERT = _as_bool(
    _env("PORTHOUND_TLS_REQUIRE_CLIENT_CERT", "0"),
    default=False,
)

AGENT_CERT_FILE = str(_env("PORTHOUND_AGENT_CERT", "certs/agent/agent.cert.pem")).strip()
AGENT_KEY_FILE = str(_env("PORTHOUND_AGENT_KEY", "certs/agent/agent.key.pem")).strip()
AGENT_ID = str(_env("PORTHOUND_AGENT_ID", "")).strip()
AGENT_TOKEN = str(
    _env("PORTHOUND_AGENT_TOKEN", _env("PORTHOUND_AGENT_SHARED_KEY", ""))
).strip()
AGENT_SHARED_KEY = AGENT_TOKEN
AGENT_POLL_SECONDS = max(2, _as_int(_env("PORTHOUND_AGENT_POLL_SECONDS", "8"), 8))
AGENT_HTTP_TIMEOUT = max(2.0, _as_float(_env("PORTHOUND_AGENT_HTTP_TIMEOUT", "20.0"), 20.0))
AGENT_TASK_LEASE_SECONDS = max(
    30,
    _as_int(_env("PORTHOUND_AGENT_TASK_LEASE_SECONDS", "300"), 300),
)
AGENT_TASK_STALL_SECONDS = max(
    90.0,
    _as_float(_env("PORTHOUND_AGENT_TASK_STALL_SECONDS", "300"), 300.0),
)
AGENT_TLS_CHECK_HOSTNAME = _as_bool(
    _env("PORTHOUND_AGENT_TLS_CHECK_HOSTNAME", "1"),
    default=True,
)

_dns_resolvers_raw = str(
    _env(
        "PORTHOUND_DNS_RESOLVERS",
        "udp://1.1.1.1,udp://8.8.8.8,udp://9.9.9.9",
    )
).strip()
DNS_RESOLVERS = tuple(
    item.strip()
    for item in _dns_resolvers_raw.split(",")
    if item.strip()
)
DNS_TIMEOUT_SECONDS = max(
    0.3,
    _as_float(_env("PORTHOUND_DNS_TIMEOUT_SECONDS", "1.4"), 1.4),
)
DNS_USE_SYSTEM_RESOLVER = _as_bool(
    _env("PORTHOUND_DNS_USE_SYSTEM_RESOLVER", "1"),
    default=True,
)
