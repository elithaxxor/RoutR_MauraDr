#!/bin/bash

# Simple LDAP and DNS checks

info() { echo "[INFO] $1"; }
error() { echo "[ERROR] $1"; }
success() { echo "[SUCCESS] $1"; }

check_service() {
    local svc="$1"
    if systemctl is-active --quiet "$svc"; then
        success "$svc is running"
    else
        error "$svc is not running"
    fi
}

test_ldap_connection() {
    if ldapsearch -x -LLL -H ldap://localhost -b "" >/dev/null 2>&1; then
        success "LDAP server reachable"
    else
        error "Unable to connect to LDAP server"
    fi
}

test_dns_resolution() {
    local host_to_check="example.com"
    if host "$host_to_check" >/dev/null 2>&1; then
        success "DNS resolution works for $host_to_check"
    else
        error "DNS resolution failed for $host_to_check"
    fi
}

check_dns_netstat_ports() {
    if netstat -tuln | grep -q ':53'; then
        success "DNS service listening on port 53"
    else
        error "DNS service not listening on port 53"
    fi
}

main() {
    info "Checking LDAP and DNS configuration..."
    check_service "slapd"
    test_ldap_connection
    test_dns_resolution
    check_dns_netstat_ports
}

main "$@"
