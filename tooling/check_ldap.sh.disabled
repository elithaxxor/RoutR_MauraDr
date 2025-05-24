#!/bin/bash
# Basic LDAP and DNS configuration checks

GREEN="\e[32m"
DARK_GREEN="\e[32;1m"
BLUE="\e[34m"
RED="\e[31m"
NC="\e[0m"

info() {
  echo -e "${BLUE}[INFO] $1${NC}"
}

error() {
  echo -e "${RED}[ERROR] $1${NC}"
}

success() {
  echo -e "${DARK_GREEN}[SUCCESS] $1${NC}"
}

check_service() {
  local service_name="$1"
  if systemctl is-active --quiet "$service_name"; then
    success "$service_name is running."
  else
    error "$service_name is not running."
  fi
}

check_ldap_config_files() {
  local ldap_conf="/etc/ldap/ldap.conf"
  local slapd_conf="/etc/ldap/slapd.conf"
  local slapd_d_dir="/etc/ldap/slapd.d"

  if [ -f "$ldap_conf" ]; then
    info "LDAP client configuration file ($ldap_conf) found."
  else
    error "LDAP client configuration file ($ldap_conf) not found."
  fi

  if [ -f "$slapd_conf" ]; then
    info "LDAP server configuration file ($slapd_conf) found."
  elif [ -d "$slapd_d_dir" ]; then
    info "LDAP server configuration directory ($slapd_d_dir) found."
  else
    error "Neither slapd.conf file nor slapd.d directory found."
  fi
}

test_ldap_connection() {
  local ldap_host="localhost"
  local base_dn="dc=example,dc=com"
  local search_filter="(objectClass=*)"

  info "Testing LDAP connection to $ldap_host..."
  ldapsearch -x -H "ldap://$ldap_host" -b "$base_dn" "$search_filter" -s base >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    success "LDAP connection to $ldap_host successful."
  else
    error "Failed to connect to LDAP server at $ldap_host."
  fi
}

test_dns_resolution() {
  local test_domain="example.com"
  local ldap_server="ldap.example.com"

  info "Testing DNS resolution for $test_domain..."
  if host "$test_domain" >/dev/null 2>&1; then
    success "DNS resolution for $test_domain successful."
  else
    error "DNS resolution for $test_domain failed."
  fi

  info "Testing DNS resolution for $ldap_server..."
  if host "$ldap_server" >/dev/null 2>&1; then
    success "DNS resolution for $ldap_server successful."
  else
    error "DNS resolution for $ldap_server failed."
  fi
}

check_dns_netstat_ports() {
  local dns_port=53
  info "Checking if DNS is listening on TCP port $dns_port..."
  if ss -tln | awk '{print $4}' | grep -Eq ":${dns_port}$"; then
    success "DNS is listening on TCP port $dns_port."
  else
    error "DNS is not listening on TCP port $dns_port."
  fi

  info "Checking if DNS is listening on UDP port $dns_port..."
  if ss -uln | awk '{print $5}' | grep -Eq ":${dns_port}$"; then
    success "DNS is listening on UDP port $dns_port."
  else
    error "DNS is not listening on UDP port $dns_port."
  fi
}

add_ldap_user() {
  info "Add LDAP user functionality not implemented in this demo."
}

# Main execution
check_service "slapd"
check_ldap_config_files
test_ldap_connection
check_service "named"
test_dns_resolution
check_dns_netstat_ports
add_ldap_user

echo "LDAP, DNS, network configuration check complete."
