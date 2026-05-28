"""Shared utilities for PortHound.

Keep this module focused on small reusable helpers that are not tied to the
web runtime or to network scanning transport details.
"""

from __future__ import annotations

import time
from ipaddress import IPv4Network, ip_network

import settings


def clamp_int(value, default, minimum, maximum):
    try:
        number = int(value)
    except Exception:
        number = default
    if number < minimum:
        return minimum
    if number > maximum:
        return maximum
    return number


def utc_iso(ts_value):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts_value))


def current_role():
    value = str(getattr(settings, "ROLE", "master") or "master").strip().lower()
    if value in {"master", "agent", "standalone"}:
        return value
    return "master"


def is_master_role():
    return current_role() in {"master", "standalone"}


def normalize_target_payload(
    item,
    require_id=False,
    *,
    cidr_match,
    valid_target_types,
    valid_target_protos,
    valid_target_statuses,
    valid_target_port_modes,
    valid_target_agent_modes,
    normalize_target_port_config,
    normalize_target_agent_config,
):
    if not isinstance(item, dict):
        raise ValueError("Invalid target body")
    output = dict(item)

    if require_id:
        try:
            output["id"] = int(output.get("id"))
        except Exception:
            raise ValueError("Invalid target id")

    network = str(output.get("network", "")).strip()
    if not cidr_match.match(network):
        raise ValueError("Invalid CIDR format")
    try:
        network_obj = ip_network(network, strict=False)
    except Exception:
        raise ValueError("Invalid CIDR format")
    if not isinstance(network_obj, IPv4Network):
        raise ValueError("Only IPv4 CIDR is supported")
    output["network"] = str(network_obj)

    target_type = str(output.get("type", "")).strip().lower()
    if target_type not in valid_target_types:
        raise ValueError("Invalid type. Use common, not_common or full")
    output["type"] = target_type

    proto = str(output.get("proto", "")).strip().lower()
    if proto == "stcp":
        proto = "sctp"
    if proto not in valid_target_protos:
        allowed = ", ".join(sorted(valid_target_protos))
        raise ValueError(f"Invalid proto. Use {allowed}")
    output["proto"] = proto

    try:
        timesleep = float(output.get("timesleep", 1.0))
    except Exception:
        raise ValueError("Invalid timesleep")
    if timesleep < 0:
        raise ValueError("timesleep must be >= 0")
    output["timesleep"] = timesleep

    target_status = str(output.get("status", "active")).strip().lower()
    if target_status not in valid_target_statuses:
        allowed = ", ".join(sorted(valid_target_statuses))
        raise ValueError(f"Invalid status. Use {allowed}")
    output["status"] = target_status

    port_config = normalize_target_port_config(output, proto=proto)
    if port_config["port_mode"] not in valid_target_port_modes:
        allowed = ", ".join(sorted(valid_target_port_modes))
        raise ValueError(f"Invalid port_mode. Use {allowed}")
    output["port_mode"] = port_config["port_mode"]
    output["port_start"] = port_config["port_start"]
    output["port_end"] = port_config["port_end"]
    agent_config = normalize_target_agent_config(output)
    if agent_config["agent_mode"] not in valid_target_agent_modes:
        allowed = ", ".join(sorted(valid_target_agent_modes))
        raise ValueError(f"Invalid agent_mode. Use {allowed}")
    output["agent_mode"] = agent_config["agent_mode"]
    output["agent_id"] = agent_config["agent_id"]

    return output


__all__ = [
    "clamp_int",
    "utc_iso",
    "current_role",
    "is_master_role",
    "normalize_target_payload",
]
