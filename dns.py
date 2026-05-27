"""DNS helpers for PortHound.

This module centralizes hostname normalization and resolver transport
selection so the main application can stay focused on scan and UI logic.

Supported resolver transports:
- `udp://host[:port]`
- `tcp://host[:port]`
- `dot://host[:port]` or `tls://host[:port]`
- `doh://https://host[:port]/dns-query`
- plain `host[:port]` defaults to UDP
"""

from __future__ import annotations

import json
import random
import re
import socket
import ssl
from dataclasses import dataclass
from typing import Iterable
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

import settings
from wsbuilder import LocalDNSServer as WSBUILDER_LOCAL_DNS_SERVER


DNS_QTYPE_A = 1
DNS_QTYPE_CNAME = 5
DNS_QTYPE_PTR = 12
DNS_QTYPE_AAAA = 28
DNS_QTYPE_ANY = 255
DNS_QCLASS_IN = 1
DNS_QCLASS_ANY = 255

DNS_RESOLVER_HINTS = tuple(
    str(item).strip()
    for item in getattr(settings, "DNS_RESOLVERS", ())
    if str(item).strip()
)

DNS_TIMEOUT_SECONDS = float(getattr(settings, "DNS_TIMEOUT_SECONDS", 1.4) or 1.4)
DNS_USE_SYSTEM_RESOLVER = bool(getattr(settings, "DNS_USE_SYSTEM_RESOLVER", True))

REGEX_IPV4_EXACT = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
REGEX_DOMAIN_CANDIDATE = re.compile(r"^(?:\*\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)+\.?$", re.I)
REGEX_SINGLE_LABEL_HOST = re.compile(r"^[a-z][a-z0-9-]{0,62}$", re.I)
NON_DNS_SUFFIXES = {
    "ico",
    "icon",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "svg",
    "webp",
    "css",
    "js",
    "woff",
    "woff2",
    "ttf",
    "eot",
    "map",
    "txt",
    "json",
    "xml",
    "pdf",
    "zip",
    "bin",
    "exe",
}


@dataclass(frozen=True)
class ResolverSpec:
    transport: str
    host: str
    port: int
    url: str = ""

    @property
    def label(self) -> str:
        if self.transport in {"doh", "https"}:
            return self.url or self.host
        return f"{self.transport}://{self.host}:{self.port}"


def _normalize_name(name):
    return (name or "").strip().strip(".").lower()


def normalize_domain_candidate(value):
    raw = str(value or "").strip().lower()
    if not raw:
        return ""
    if raw.endswith("."):
        raw = raw[:-1]
    if raw.startswith("*."):
        raw = raw[2:]
    if not raw or "." not in raw:
        return ""
    if REGEX_IPV4_EXACT.match(raw):
        return ""
    if not REGEX_DOMAIN_CANDIDATE.match(raw):
        return ""
    labels = [part for part in raw.split(".") if part]
    if any(len(label) > 63 for label in labels):
        return ""
    if len(raw) > 253:
        return ""
    tld = labels[-1]
    if not re.match(r"^[a-z]{2,63}$", tld):
        return ""
    if tld in NON_DNS_SUFFIXES:
        return ""
    if not any(ch.isalpha() for ch in raw):
        return ""
    return raw


def normalize_nslookup_host(value):
    raw = str(value or "").strip().lower()
    if not raw:
        return ""
    if raw.endswith("."):
        raw = raw[:-1]
    domain_name = normalize_domain_candidate(raw)
    if domain_name:
        return domain_name
    if REGEX_SINGLE_LABEL_HOST.match(raw):
        return raw
    return ""


def encode_dns_name(name_value):
    labels = [part for part in str(name_value or "").strip(".").split(".") if part]
    output = bytearray()
    for label in labels:
        try:
            label_bytes = label.encode("idna")
        except Exception:
            return b""
        if not label_bytes or len(label_bytes) > 63:
            return b""
        output.append(len(label_bytes))
        output.extend(label_bytes)
    output.append(0)
    return bytes(output)


def dns_build_query(name_value, qtype):
    encoded_name = encode_dns_name(name_value)
    if not encoded_name:
        raise ValueError("invalid dns name")
    txid = random.randint(0, 65535)
    flags = 0x0100  # recursion desired
    header = (
        int(txid).to_bytes(2, "big")
        + int(flags).to_bytes(2, "big")
        + (1).to_bytes(2, "big")
        + (0).to_bytes(2, "big")
        + (0).to_bytes(2, "big")
        + (0).to_bytes(2, "big")
    )
    question = encoded_name + int(qtype).to_bytes(2, "big") + (1).to_bytes(2, "big")
    return txid, header + question


def dns_skip_name(packet_bytes, offset):
    steps = 0
    current = int(offset)
    while True:
        if current >= len(packet_bytes):
            raise ValueError("dns name overflow")
        length = int(packet_bytes[current])
        if length == 0:
            return current + 1
        if (length & 0xC0) == 0xC0:
            if current + 1 >= len(packet_bytes):
                raise ValueError("dns pointer overflow")
            return current + 2
        current += 1 + length
        steps += 1
        if steps > 255:
            raise ValueError("dns name loop")


def dns_read_name(packet_bytes, offset):
    labels = []
    current = int(offset)
    next_offset = int(offset)
    jumped = False
    jumps = 0
    while True:
        if current >= len(packet_bytes):
            raise ValueError("dns name overflow")
        length = int(packet_bytes[current])
        if length == 0:
            if not jumped:
                next_offset = current + 1
            break
        if (length & 0xC0) == 0xC0:
            if current + 1 >= len(packet_bytes):
                raise ValueError("dns pointer overflow")
            pointer = ((length & 0x3F) << 8) | int(packet_bytes[current + 1])
            if not jumped:
                next_offset = current + 2
            current = pointer
            jumped = True
            jumps += 1
            if jumps > 255:
                raise ValueError("dns pointer loop")
            continue
        current += 1
        label_bytes = packet_bytes[current : current + length]
        if len(label_bytes) < length:
            raise ValueError("dns label overflow")
        label = bytes(label_bytes).decode("idna", errors="ignore")
        if label:
            labels.append(label)
        current += length
        if not jumped:
            next_offset = current
    return ".".join(labels).strip(".").lower(), int(next_offset)


def dns_parse_response(packet_bytes, expected_txid):
    if not isinstance(packet_bytes, (bytes, bytearray)) or len(packet_bytes) < 12:
        raise ValueError("short dns response")
    txid = int.from_bytes(packet_bytes[0:2], "big")
    flags = int.from_bytes(packet_bytes[2:4], "big")
    qdcount = int.from_bytes(packet_bytes[4:6], "big")
    ancount = int.from_bytes(packet_bytes[6:8], "big")
    rcode = flags & 0x000F
    is_response = (flags >> 15) & 0x01
    if is_response != 1:
        raise ValueError("invalid dns response flag")
    if int(expected_txid) != int(txid):
        raise ValueError("dns txid mismatch")

    offset = 12
    for _ in range(qdcount):
        offset = dns_skip_name(packet_bytes, offset)
        if offset + 4 > len(packet_bytes):
            raise ValueError("short dns question")
        offset += 4

    answers = []
    for _ in range(ancount):
        _name, offset = dns_read_name(packet_bytes, offset)
        if offset + 10 > len(packet_bytes):
            raise ValueError("short dns answer")
        rtype = int.from_bytes(packet_bytes[offset : offset + 2], "big")
        rclass = int.from_bytes(packet_bytes[offset + 2 : offset + 4], "big")
        ttl = int.from_bytes(packet_bytes[offset + 4 : offset + 8], "big")
        rdlength = int.from_bytes(packet_bytes[offset + 8 : offset + 10], "big")
        rdata_offset = offset + 10
        rdata_end = rdata_offset + rdlength
        if rdata_end > len(packet_bytes):
            raise ValueError("short dns rdata")
        if rclass == 1:
            if rtype == DNS_QTYPE_A and rdlength == 4:
                value = ".".join(str(int(byte)) for byte in packet_bytes[rdata_offset:rdata_end])
                answers.append({"type": "A", "value": value, "ttl": ttl})
            elif rtype in {DNS_QTYPE_PTR, DNS_QTYPE_CNAME}:
                value, _ = dns_read_name(packet_bytes, rdata_offset)
                answer_type = "PTR" if rtype == DNS_QTYPE_PTR else "CNAME"
                answers.append({"type": answer_type, "value": value, "ttl": ttl})
        offset = rdata_end

    return {
        "rcode": int(rcode),
        "answers": answers,
    }


def parse_resolver_spec(resolver_value, default_transport="udp"):
    raw = str(resolver_value or "").strip()
    if not raw:
        return ResolverSpec(transport=default_transport, host="", port=53)
    if "://" not in raw:
        raw = f"{default_transport}://{raw}"
    parsed = urlsplit(raw)
    transport = str(parsed.scheme or default_transport).strip().lower() or default_transport
    host = str(parsed.hostname or "").strip()
    port = int(parsed.port or (853 if transport in {"dot", "tls"} else 53))
    url = ""
    if transport in {"doh", "https"}:
        netloc = str(parsed.netloc or "").strip()
        if not netloc and host:
            netloc = host if port in {53, 80, 443} else f"{host}:{port}"
        scheme = "https"
        path = str(parsed.path or "").strip() or "/dns-query"
        if not path.startswith("/"):
            path = f"/{path}"
        url = f"{scheme}://{netloc}{path}"
    return ResolverSpec(transport=transport, host=host, port=port, url=url)


def iter_resolver_specs(resolver_values=None):
    values = resolver_values
    if values is None:
        values = DNS_RESOLVER_HINTS
    if isinstance(values, str):
        values = [item.strip() for item in values.split(",")]
    for value in values or []:
        spec = parse_resolver_spec(value)
        if spec.host or spec.url:
            yield spec


def _build_dns_tcp_packet(query_packet):
    return len(query_packet).to_bytes(2, "big") + query_packet


def _read_dns_tcp_response(sock, timeout_seconds):
    sock.settimeout(max(0.3, float(timeout_seconds or DNS_TIMEOUT_SECONDS)))
    length_blob = sock.recv(2)
    if len(length_blob) < 2:
        raise RuntimeError("short dns tcp length")
    length = int.from_bytes(length_blob, "big")
    response = bytearray()
    while len(response) < length:
        chunk = sock.recv(min(4096, length - len(response)))
        if not chunk:
            break
        response.extend(chunk)
    if len(response) < length:
        raise RuntimeError("short dns tcp response")
    return bytes(response)


def dns_udp_query(name_value, qtype, resolver_ip, timeout_seconds=1.4):
    spec = parse_resolver_spec(resolver_ip, default_transport="udp")
    resolver = spec.host or str(resolver_ip or "").strip()
    if not resolver:
        return {
            "resolver": resolver,
            "transport": "udp",
            "rcode": None,
            "answers": [],
            "error": "empty resolver",
        }
    sock = None
    try:
        txid, query_packet = dns_build_query(name_value, qtype)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(max(0.3, float(timeout_seconds or DNS_TIMEOUT_SECONDS)))
        sock.sendto(query_packet, (resolver, int(spec.port or 53)))
        response_packet, _addr = sock.recvfrom(4096)
        parsed = dns_parse_response(response_packet, expected_txid=txid)
        return {
            "resolver": resolver,
            "transport": "udp",
            "rcode": parsed.get("rcode"),
            "answers": parsed.get("answers", []),
            "error": "",
        }
    except Exception as exc:
        return {
            "resolver": resolver,
            "transport": "udp",
            "rcode": None,
            "answers": [],
            "error": str(exc),
        }
    finally:
        try:
            if sock:
                sock.close()
        except Exception:
            pass


def dns_tcp_query(name_value, qtype, resolver_value, timeout_seconds=1.4):
    spec = parse_resolver_spec(resolver_value, default_transport="tcp")
    resolver = spec.host or str(resolver_value or "").strip()
    if not resolver:
        return {
            "resolver": resolver,
            "transport": "tcp",
            "rcode": None,
            "answers": [],
            "error": "empty resolver",
        }
    sock = None
    try:
        txid, query_packet = dns_build_query(name_value, qtype)
        sock = socket.create_connection((resolver, int(spec.port or 53)), timeout=float(timeout_seconds or DNS_TIMEOUT_SECONDS))
        sock.sendall(_build_dns_tcp_packet(query_packet))
        response_packet = _read_dns_tcp_response(sock, timeout_seconds)
        parsed = dns_parse_response(response_packet, expected_txid=txid)
        return {
            "resolver": resolver,
            "transport": "tcp",
            "rcode": parsed.get("rcode"),
            "answers": parsed.get("answers", []),
            "error": "",
        }
    except Exception as exc:
        return {
            "resolver": resolver,
            "transport": "tcp",
            "rcode": None,
            "answers": [],
            "error": str(exc),
        }
    finally:
        try:
            if sock:
                sock.close()
        except Exception:
            pass


def dns_dot_query(name_value, qtype, resolver_value, timeout_seconds=1.4):
    spec = parse_resolver_spec(resolver_value, default_transport="dot")
    resolver = spec.host or str(resolver_value or "").strip()
    if not resolver:
        return {
            "resolver": resolver,
            "transport": "dot",
            "rcode": None,
            "answers": [],
            "error": "empty resolver",
        }
    sock = None
    try:
        txid, query_packet = dns_build_query(name_value, qtype)
        plain_sock = socket.create_connection(
            (resolver, int(spec.port or 853)),
            timeout=float(timeout_seconds or DNS_TIMEOUT_SECONDS),
        )
        context = ssl.create_default_context()
        if hasattr(ssl, "TLSVersion") and hasattr(context, "minimum_version"):
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        else:
            context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        server_hostname = resolver if not REGEX_IPV4_EXACT.match(resolver) else None
        if server_hostname is None:
            context.check_hostname = False
        sock = context.wrap_socket(plain_sock, server_hostname=server_hostname)
        sock.sendall(_build_dns_tcp_packet(query_packet))
        response_packet = _read_dns_tcp_response(sock, timeout_seconds)
        parsed = dns_parse_response(response_packet, expected_txid=txid)
        return {
            "resolver": resolver,
            "transport": "dot",
            "rcode": parsed.get("rcode"),
            "answers": parsed.get("answers", []),
            "error": "",
        }
    except Exception as exc:
        return {
            "resolver": resolver,
            "transport": "dot",
            "rcode": None,
            "answers": [],
            "error": str(exc),
        }
    finally:
        try:
            if sock:
                sock.close()
        except Exception:
            pass


def dns_doh_query(name_value, qtype, resolver_value, timeout_seconds=1.4):
    spec = parse_resolver_spec(resolver_value, default_transport="doh")
    resolver_url = spec.url or str(resolver_value or "").strip()
    if not resolver_url:
        return {
            "resolver": resolver_url,
            "transport": "doh",
            "rcode": None,
            "answers": [],
            "error": "empty resolver",
        }
    try:
        txid, query_packet = dns_build_query(name_value, qtype)
        request = Request(
            resolver_url,
            data=query_packet,
            headers={
                "Content-Type": "application/dns-message",
                "Accept": "application/dns-message",
                "User-Agent": "PortHound/0.2 dns",
            },
            method="POST",
        )
        with urlopen(request, timeout=float(timeout_seconds or DNS_TIMEOUT_SECONDS)) as response:
            response_packet = response.read()
        parsed = dns_parse_response(response_packet, expected_txid=txid)
        return {
            "resolver": resolver_url,
            "transport": "doh",
            "rcode": parsed.get("rcode"),
            "answers": parsed.get("answers", []),
            "error": "",
        }
    except (URLError, OSError, ValueError, RuntimeError) as exc:
        return {
            "resolver": resolver_url,
            "transport": "doh",
            "rcode": None,
            "answers": [],
            "error": str(exc),
        }


def dns_query(name_value, qtype, resolver_value, timeout_seconds=1.4):
    spec = parse_resolver_spec(resolver_value)
    transport = spec.transport
    if transport in {"udp", "dns"}:
        return dns_udp_query(name_value, qtype, resolver_value, timeout_seconds=timeout_seconds)
    if transport == "tcp":
        return dns_tcp_query(name_value, qtype, resolver_value, timeout_seconds=timeout_seconds)
    if transport in {"dot", "tls"}:
        return dns_dot_query(name_value, qtype, resolver_value, timeout_seconds=timeout_seconds)
    if transport in {"doh", "https"}:
        return dns_doh_query(name_value, qtype, resolver_value, timeout_seconds=timeout_seconds)
    return dns_udp_query(name_value, qtype, resolver_value, timeout_seconds=timeout_seconds)


def dns_ptr_lookup_for_ip(ip_value, resolver_values=None, timeout_seconds=None):
    octets = str(ip_value or "").strip().split(".")
    if len(octets) != 4:
        return {
            "query_name": "",
            "domains": [],
            "attempts": [],
            "error": "invalid ipv4",
            "status": "invalid",
        }
    query_name = ".".join(reversed(octets)) + ".in-addr.arpa"
    found = set()
    attempts = []
    timeout_seconds = float(timeout_seconds or DNS_TIMEOUT_SECONDS)
    for resolver_spec in iter_resolver_specs(resolver_values):
        response = dns_query(query_name, DNS_QTYPE_PTR, resolver_spec.label, timeout_seconds=timeout_seconds)
        answer_values = []
        for answer in response.get("answers", []):
            value = normalize_nslookup_host(answer.get("value", ""))
            if value:
                found.add(value)
                answer_values.append(value)
        attempts.append(
            {
                "resolver": response.get("resolver", ""),
                "transport": response.get("transport", resolver_spec.transport),
                "rcode": response.get("rcode"),
                "answers": answer_values,
                "error": response.get("error", ""),
            }
        )
        if found:
            break

    errors = [str(item.get("error", "")).strip() for item in attempts if str(item.get("error", "")).strip()]
    if found:
        status = "ok"
        error = ""
    elif errors and len(errors) == len(attempts):
        status = "error"
        error = errors[0]
    else:
        status = "no_ptr"
        error = ""
    return {
        "query_name": query_name,
        "domains": sorted(found),
        "attempts": attempts[:8],
        "error": error,
        "status": status,
    }


def dns_a_lookup_for_host(host_value, resolver_values=None, timeout_seconds=None):
    host = str(host_value or "").strip().lower()
    if not host:
        return {
            "host": host,
            "ips": [],
            "attempts": [],
            "error": "empty host",
            "status": "invalid",
        }

    found = set()
    attempts = []
    pending = [host]
    visited = set()
    max_names = 4
    timeout_seconds = float(timeout_seconds or DNS_TIMEOUT_SECONDS)

    while pending and len(visited) < max_names:
        current_name = str(pending.pop(0) or "").strip().lower()
        if not current_name or current_name in visited:
            continue
        visited.add(current_name)

        for resolver_spec in iter_resolver_specs(resolver_values):
            response = dns_query(current_name, DNS_QTYPE_A, resolver_spec.label, timeout_seconds=timeout_seconds)
            next_names = []
            for answer in response.get("answers", []):
                answer_type = str(answer.get("type", "")).strip().upper()
                value = str(answer.get("value", "")).strip().lower()
                if answer_type == "A" and REGEX_IPV4_EXACT.match(value):
                    found.add(value)
                elif answer_type == "CNAME":
                    cname = normalize_nslookup_host(value)
                    if cname and cname not in visited and cname not in pending:
                        next_names.append(cname)
            attempts.append(
                {
                    "resolver": response.get("resolver", ""),
                    "transport": response.get("transport", resolver_spec.transport),
                    "name": current_name,
                    "rcode": response.get("rcode"),
                    "answers": response.get("answers", []),
                    "error": response.get("error", ""),
                }
            )
            if next_names:
                pending.extend(next_names)
            if found:
                break
        if found:
            break

    errors = [str(item.get("error", "")).strip() for item in attempts if str(item.get("error", "")).strip()]
    if found:
        status = "ok"
        error = ""
    elif errors and len(errors) == len(attempts):
        status = "error"
        error = errors[0]
    else:
        status = "no_a"
        error = ""
    return {
        "host": host,
        "ips": sorted(found),
        "attempts": attempts[:16],
        "error": error,
        "status": status,
    }


def resolve_ipv4_addresses_for_host(host_value, resolver_values=None, timeout_seconds=None):
    host = str(host_value or "").strip().lower()
    if not host:
        return [], "empty host"
    found = set()
    errors = []
    try:
        _hostname, _aliases, addr_list = socket.gethostbyname_ex(host)
        for addr in addr_list or []:
            candidate = str(addr or "").strip()
            if REGEX_IPV4_EXACT.match(candidate):
                found.add(candidate)
    except Exception as exc:
        errors.append(str(exc))
    try:
        for item in socket.getaddrinfo(host, None, socket.AF_INET):
            sockaddr = item[4] if len(item) > 4 else ()
            if not isinstance(sockaddr, tuple) or not sockaddr:
                continue
            candidate = str(sockaddr[0] or "").strip()
            if REGEX_IPV4_EXACT.match(candidate):
                found.add(candidate)
    except Exception as exc:
        errors.append(str(exc))

    if DNS_USE_SYSTEM_RESOLVER or not found:
        dns_data = dns_a_lookup_for_host(
            host,
            resolver_values=resolver_values,
            timeout_seconds=timeout_seconds,
        )
        for addr in dns_data.get("ips", []):
            candidate = str(addr or "").strip()
            if REGEX_IPV4_EXACT.match(candidate):
                found.add(candidate)
        dns_error = str(dns_data.get("error", "")).strip()
        if dns_error:
            errors.append(dns_error)

    unique_errors = [msg for msg in dict.fromkeys(errors) if msg]
    return sorted(found), unique_errors[0] if unique_errors else ""


def filter_domains_for_ip_socket(domains, ip_value, max_checks=48, resolver_values=None, timeout_seconds=None):
    verified = set()
    rejected = []
    checked = 0
    for domain in sorted({str(item or "").strip().lower() for item in (domains or []) if str(item or "").strip()}):
        normalized = normalize_domain_candidate(domain)
        if not normalized:
            continue
        if checked >= int(max_checks):
            break
        checked += 1
        resolved, lookup_error = resolve_ipv4_addresses_for_host(
            normalized,
            resolver_values=resolver_values,
            timeout_seconds=timeout_seconds,
        )
        if ip_value in resolved:
            verified.add(normalized)
            continue
        rejected.append(
            {
                "domain": normalized,
                "resolved_ipv4": resolved[:8],
                "error": lookup_error,
            }
        )
    return {
        "domains": sorted(verified),
        "checked": checked,
        "rejected": rejected[:24],
    }


def discover_reverse_dns_domains(ip_value, resolver_values=None, timeout_seconds=None):
    found = set()
    reverse_host = ""
    aliases = []
    addresses = []
    error = ""
    lookups = []
    ptr_lookup = {
        "query_name": "",
        "domains": [],
        "attempts": [],
        "error": "",
        "status": "unknown",
    }
    try:
        hostname, alias_list, address_list = socket.gethostbyaddr(ip_value)
        reverse_host = str(hostname or "").strip().lower()
        aliases = [str(item).strip().lower() for item in (alias_list or []) if str(item).strip()]
        addresses = [str(item).strip() for item in (address_list or []) if str(item).strip()]

        for candidate in [reverse_host, *aliases]:
            normalized = normalize_nslookup_host(candidate)
            if normalized:
                found.add(normalized)

        ptr_lookup = {
            "query_name": "",
            "domains": sorted(found),
            "attempts": [],
            "error": "",
            "status": "ok",
        }
        for host_value in sorted(found):
            lookups.append(
                {
                    "host": host_value,
                    "resolved_ipv4": addresses[:8],
                    "matches_ip": ip_value in addresses or (host_value == "localhost" and str(ip_value).startswith("127.")),
                    "error": "",
                }
            )
    except socket.herror as exc:
        error = f"No PTR configurado: {exc}"
        ptr_lookup = {
            "query_name": "",
            "domains": [],
            "attempts": [],
            "error": str(exc),
            "status": "no_ptr",
        }
    except Exception as exc:
        error = str(exc)
        ptr_lookup = {
            "query_name": "",
            "domains": [],
            "attempts": [],
            "error": str(exc),
            "status": "error",
        }

    return {
        "domains": sorted(found),
        "verified_domains": sorted(found),
        "candidates": sorted(found),
        "reverse_host": reverse_host,
        "fqdn_host": reverse_host,
        "aliases": sorted(set(aliases)),
        "addresses": addresses[:8],
        "lookups": lookups[:24],
        "ptr_lookup": ptr_lookup,
        "error": error,
    }


def build_local_dns_server(records=None, ttl=60, host="127.0.0.1", port=5533):
    """Return the bundled WSBuilder UDP DNS server.

    PortHound uses this when users want a tiny local resolver for internal names.
    It is intentionally separate from the outbound resolver logic above.
    """

    return WSBUILDER_LOCAL_DNS_SERVER(host=host, port=port, records=records, ttl=ttl)


__all__ = [
    "DNS_QTYPE_A",
    "DNS_QTYPE_CNAME",
    "DNS_QTYPE_PTR",
    "DNS_QTYPE_AAAA",
    "DNS_QTYPE_ANY",
    "DNS_QCLASS_IN",
    "DNS_QCLASS_ANY",
    "DNS_RESOLVER_HINTS",
    "DNS_TIMEOUT_SECONDS",
    "DNS_USE_SYSTEM_RESOLVER",
    "ResolverSpec",
    "build_local_dns_server",
    "dns_a_lookup_for_host",
    "dns_build_query",
    "dns_dot_query",
    "dns_doh_query",
    "dns_parse_response",
    "dns_ptr_lookup_for_ip",
    "dns_query",
    "dns_read_name",
    "dns_skip_name",
    "dns_tcp_query",
    "dns_udp_query",
    "discover_reverse_dns_domains",
    "encode_dns_name",
    "filter_domains_for_ip_socket",
    "iter_resolver_specs",
    "normalize_domain_candidate",
    "normalize_nslookup_host",
    "parse_resolver_spec",
    "resolve_ipv4_addresses_for_host",
]
