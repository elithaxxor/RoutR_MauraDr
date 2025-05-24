#!/bin/bash

# Check LDAP client and server configuration

info() { echo "[INFO] $1"; }
error() { echo "[ERROR] $1"; }
success() { echo "[SUCCESS] $1"; }

check_config_files() {
    local client_conf="/etc/ldap/ldap.conf"
    local server_conf="/etc/ldap/slapd.conf"
    local server_dir="/etc/ldap/slapd.d"

    if [[ -f "$client_conf" ]]; then
        success "Found client config $client_conf"
    else
        error "Missing client config $client_conf"
    fi

    if [[ -f "$server_conf" ]]; then
        success "Found server config $server_conf"
    elif [[ -d "$server_dir" ]]; then
        success "Found server config directory $server_dir"
    else
        error "Missing LDAP server configuration"
    fi
}

main() {
    info "Checking LDAP configuration files..."
    check_config_files
}

main "$@"
