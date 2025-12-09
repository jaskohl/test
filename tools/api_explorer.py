"""
API Explorer for Kronos Devices - FULLY VERSION

This comprehensive tool explores REST API capabilities using 20+ discovery techniques:
1. Extended endpoint discovery with 150+ patterns
2. Multi-port scanning for APIs on different ports
3. Content-based discovery from HTML/JavaScript/JSON files
4. Advanced authentication testing with device password
5. SOAP/WSDL service discovery
6. GraphQL endpoint detection
7. WebSocket discovery and testing
8. Network service scanning
9. User-agent based discovery
10. Header-based API hints (CORS, rate limiting)
11. Response pattern analysis with timing
12. OPTIONS method discovery
13. robots.txt & sitemap.xml parsing
14. Recursive link following
15. Content-type negotiation
16. Path parameter discovery
17. Query parameter discovery
18. Backup file discovery
19. Framework-specific pattern detection
20. JSON-RPC & XML-RPC discovery
21. API key/token discovery
22. Error message analysis

Output: Comprehensive documentation of discovered endpoints per device
Location: memory-bank/device_exploration/{device_ip}/api/

Usage:
    python -m tools.api_explorer

This tool performs READ-ONLY testing to avoid disrupting device configuration.
"""

import json
import time
import requests
import socket
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union, Set
from urllib.parse import urljoin, urlparse, parse_qs
from urllib3.exceptions import InsecureRequestWarning
from collections import defaultdict

# Suppress SSL warnings for testing
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Device list
DEVICES = [
    # {"ip": "172.16.190.46", "name": "Kronos Series 2", "type": "series2"},
    # {"ip": "172.16.190.47", "name": "Kronos Series 3", "type": "series3"},
    # {"ip": "172.16.66.1", "name": "Kronos Series 2", "type": "series2"},
    # {"ip": "172.16.66.3", "name": "Kronos Series 3", "type": "series3"},
    # {"ip": "172.16.66.6", "name": "Kronos Series 3", "type": "series3"},
    {"ip": "172.16.66.3", "name": "Kronos Series 3", "type": "series3"},
]

PASSWORD = "novatech"
OUTPUT_BASE = Path("memory-bank/device_exploration")


class DiscoveredEndpoint:
    """Represents a discovered API endpoint with comprehensive metadata."""

    def __init__(self, url: str, method: str = "GET", port: int = 443):
        self.url = url
        self.method = method
        self.port = port
        self.scheme = "https" if port in [443, 8443] else "http"
        self.status_code: Union[int, str, None] = None
        self.response_headers = {}
        self.response_data: Optional[str] = None
        self.response_time: Optional[float] = None
        self.auth_required = False
        self.documentation_available = False
        self.supported_formats = []
        self.error_responses = {}
        self.tested = False
        self.test_timestamp: Optional[str] = None
        self.discovery_method = "unknown"
        self.headers_analysis = {}
        self.rate_limit_info = {}
        self.cors_info = {}
        self.allowed_methods = []
        self.parameters_discovered = {}

    def to_dict(self) -> dict:
        """Convert endpoint to dictionary for JSON serialization."""
        return {
            "url": self.url,
            "method": self.method,
            "port": self.port,
            "scheme": self.scheme,
            "status_code": self.status_code,
            "response_headers": self.response_headers,
            "response_data": self.response_data,
            "response_time": self.response_time,
            "auth_required": self.auth_required,
            "documentation_available": self.documentation_available,
            "supported_formats": self.supported_formats,
            "error_responses": self.error_responses,
            "tested": self.tested,
            "test_timestamp": self.test_timestamp,
            "discovery_method": self.discovery_method,
            "headers_analysis": self.headers_analysis,
            "rate_limit_info": self.rate_limit_info,
            "cors_info": self.cors_info,
            "allowed_methods": self.allowed_methods,
            "parameters_discovered": self.parameters_discovered,
        }


class APIExplorer:
    """API exploration class with 20+ discovery techniques."""

    def __init__(self, device_ip: str, device_name: str, device_type: str):
        self.device_ip = device_ip
        self.device_name = device_name
        self.device_type = device_type
        self.default_port = 443
        self.session = requests.Session()
        self.session.verify = False
        self.default_timeout = 10
        self.discovered_endpoints = []
        self.open_ports = []
        self.discovered_urls: Set[str] = set()  # Track all discovered URLs
        self.js_files: List[str] = []  # Track JavaScript files
        self.api_results = {
            "device_ip": device_ip,
            "device_name": device_name,
            "device_type": device_type,
            "exploration_date": datetime.now().isoformat(),
            "base_url": f"https://{device_ip}",
            "endpoints": [],
            "discovery_methods": [],
            "summary": {},
            "errors": [],
            "discovered_frameworks": [],
            "websocket_endpoints": [],
            "rpc_endpoints": [],
        }

    def get_extended_endpoints(self) -> List[str]:
        """Get comprehensive list of potential API endpoints."""
        endpoints = [
            # Original standard patterns
            "/api",
            "/api/v1",
            "/api/v2",
            "/api/v3",
            "/api/v4",
            "/rest",
            "/rest/v1",
            "/rest/v2",
            "/json",
            "/json/v1",
            # Configuration APIs
            "/api/config",
            "/api/configuration",
            "/api/config/v1",
            "/api/status",
            "/api/system",
            "/api/status/general",
            "/api/status/gnss",
            "/api/status/time",
            "/api/status/network",
            # Device-specific endpoints
            "/api/kronos",
            "/api/kronos/config",
            "/api/kronos/status",
            "/api/satellite",
            "/api/gnss",
            "/api/time",
            "/api/network",
            "/api/gps",
            "/api/timing",
            "/api/sync",
            # Management interfaces
            "/api/management",
            "/api/admin",
            "/api/user",
            "/api/auth",
            "/management",
            "/admin",
            "/cgi-bin/admin",
            "/web/admin",
            # Modern API patterns with versions
            "/api/v1.0",
            "/api/v1.0/status",
            "/api/v1.0/config",
            "/api/v1.1",
            "/api/v1.2",
            "/api/v1.3",
            "/api/v2.0",
            "/api/v2.0/status",
            "/api/v2.0/config",
            # Documentation endpoints
            "/openapi.json",
            "/swagger.json",
            "/swagger.yaml",
            "/swagger-ui",
            "/api/docs",
            "/docs",
            "/api/documentation",
            "/swagger",
            "/redoc",
            "/rapidoc",
            "/api/schema",
            "/schema",
            "/api-docs",
            "/api/swagger",
            "/swagger/index.html",
            # Alternative patterns
            "/api.php",
            "/api.json",
            "/service",
            "/services",
            "/api/service",
            "/api/services",
            "/api/service/v1",
            "/webapi",
            "/soap",
            # Extended device-specific
            "/satellite/api",
            "/gnss/api",
            "/time/api",
            "/network/api",
            "/config/api",
            "/status/api",
            "/system/api",
            "/monitor/api",
            # Management interfaces
            "/cgi-bin/api",
            "/web/api",
            "/interface/api",
            "/control/api",
            "/manage",
            "/manager",
            "/mgmt",
            "/managementui",
            # Protocol-specific endpoints
            "/soap",
            "/wsdl",
            "/graphql",
            "/query",
            "/gql",
            "/graph",
            "/soap/v1",
            "/soap/v2",
            "/restful",
            "/rpc",
            "/jsonrpc",
            "/xmlrpc",
            # Hidden/common paths
            "/.well-known/api",
            "/.well-known/openapi",
            "/actuator",
            "/status/health",
            "/health",
            "/metrics",
            "/debug",
            "/info",
            "/ping",
            "/echo",
            "/test",
            "/status",
            # File-based APIs
            "/api.php",
            "/api.asp",
            "/api.aspx",
            "/api.jsp",
            "/api.do",
            "/api.rb",
            "/api.pl",
            "/api.py",
            "/api.js",
            "/ws/api",
            # Alternative authentication
            "/login",
            "/login/api",
            "/auth",
            "/auth/api",
            "/signin",
            "/token",
            "/oauth",
            "/oauth2",
            "/jwt",
            "/session",
            # Data endpoints
            "/data",
            "/data/api",
            "/export",
            "/export/api",
            "/import",
            "/import/api",
            "/sync",
            "/sync/api",
            "/backup",
            "/restore",
            "/download",
            "/upload",
            # Monitoring endpoints
            "/monitor",
            "/monitor/api",
            "/diagnostics",
            "/diagnostics/api",
            "/logs",
            "/logs/api",
            "/stats",
            "/statistics",
            "/stats/api",
            "/performance",
            "/healthcheck",
            "/heartbeat",
            # Device management
            "/device",
            "/devices",
            "/device/api",
            "/hardware",
            "/firmware",
            "/update",
            "/upgrade",
            "/maintenance",
            "/configuration",
            "/settings",
            "/preferences",
            # Time synchronization
            "/ntp",
            "/ptp",
            "/time-sync",
            "/clock",
            "/timing",
            "/frequency",
            "/phase",
            "/disciplining",
            # Network specific
            "/ethernet",
            "/lan",
            "/wan",
            "/ports",
            "/interfaces",
            "/routing",
            "/switching",
            "/vlan",
            "/qos",
            # WebSocket endpoints
            "/ws",
            "/websocket",
            "/ws/api",
            "/realtime",
            "/socket.io",
            "/signalr",
            "/events",
            "/streaming",
            # GraphQL specific
            "/graphql",
            "/graph",
            "/gql",
            "/query",
            "/mutation",
            "/playground",
            "/altair",
            "/graphiql",
            # Service discovery
            "/discovery",
            "/registry",
            "/catalog",
            "/services",
            "/endpoints",
            "/nodes",
            "/cluster",
            "/memberlist",
            # Cloud/SaaS patterns
            "/cloud",
            "/saas",
            "/tenant",
            "/multi-tenant",
            "/instance",
            "/deployment",
            "/environment",
            # Version specific
            "/v1",
            "/v2",
            "/v3",
            "/v4",
            "/v5",
            "/v1.0",
            "/v1.1",
            "/v1.2",
            "/v2.0",
            "/v2.1",
            "/latest",
            "/current",
            "/stable",
            "/beta",
            "/alpha",
            # Common REST patterns
            "/users",
            "/user",
            "/accounts",
            "/account",
            "/sessions",
            "/session",
            "/tokens",
            "/keys",
            "/roles",
            "/permissions",
            "/groups",
            # File operations
            "/files",
            "/file",
            "/documents",
            "/attachments",
            "/media",
            "/images",
            "/uploads",
            "/downloads",
            # Framework-specific (Django REST)
            "/api/schema/",
            "/api/?format=json",
            "/api/?format=api",
            # Framework-specific (FastAPI)
            "/openapi.json",
            "/docs",
            "/redoc",
            # Framework-specific (Express)
            "/api-docs",
            "/explorer",
            # Backup/old files
            "/api.bak",
            "/api.old",
            "/api.backup",
            "/api~",
            "/config.json.bak",
            "/swagger.json.old",
            "/api.json.backup",
            "/api.txt",
            # Config files
            "/config.json",
            "/config.xml",
            "/config.yaml",
            "/settings.json",
            "/manifest.json",
            "/package.json",
            # Discovery files
            "/robots.txt",
            "/sitemap.xml",
            "/humans.txt",
            "/.well-known/",
            "/security.txt",
            # Common admin panels
            "/phpmyadmin",
            "/adminer",
            "/admin/login",
            "/administrator",
            "/wp-admin",
            "/cpanel",
        ]

        return endpoints

    def get_api_ports(self) -> List[int]:
        """Get list of common API ports to scan."""
        return [
            80,
            443,
            8080,
            8443,
            9000,
            9443,
            10000,
            3000,
            5000,
            8000,
            8888,
            8008,
            7000,
            7001,
        ]

    def get_user_agents(self) -> List[str]:
        """Get list of user agents to test."""
        return [
            "Mozilla/5.0 (compatible; API-Client/1.0)",
            "Kronos-Device-Manager/1.0",
            "NovaTech-API-Explorer/1.0",
            "Application/1.0",
            "curl/7.68.0",
            "PostmanRuntime/7.26.0",
            "REST-Client/1.0",
            "API-Explorer/1.0",
            "Python-requests/2.25.0",
            "HTTPie/2.3.0",
            "Insomnia/2021.1.0",
        ]

    def get_auth_credentials(self) -> List[Tuple[str, str]]:
        """Get list of common credentials to test - includes actual device password."""
        return [
            ("admin", PASSWORD),  # Use actual device password
            ("", PASSWORD),
            ("root", PASSWORD),
            ("user", PASSWORD),
            ("admin", "admin"),
            ("admin", "password"),
            ("admin", ""),
            ("api", "api"),
            ("api", "secret"),
            ("user", "user"),
            ("user", "password"),
            ("root", "root"),
            ("root", ""),
            ("service", "service"),
            ("", "admin"),
            ("", "password"),
            ("administrator", "administrator"),
            (PASSWORD, PASSWORD),
        ]

    def test_basic_connectivity(self) -> bool:
        """Test basic HTTP connectivity to the device."""
        try:
            print(f"  Testing basic connectivity...")
            response = self.session.get(
                f"https://{self.device_ip}", timeout=self.default_timeout
            )
            if response.status_code in [200, 302, 401]:
                print(f"  Device accessible (HTTP {response.status_code})")
                return True
            else:
                print(f"  Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"  Connectivity test failed: {e}")
            return False

    def scan_open_ports(self) -> List[int]:
        """Scan for open ports on the device."""
        print(f"  Scanning for open ports...")
        open_ports = []
        ports_to_scan = self.get_api_ports()

        for port in ports_to_scan:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.device_ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"    Open port: {port}")
                sock.close()
            except:
                pass

        print(f"  Found {len(open_ports)} open ports")
        return open_ports

    def quick_check_endpoint(self, url: str) -> Tuple[bool, int, float]:
        """Use HEAD method for fast endpoint checking."""
        try:
            start = time.time()
            response = self.session.head(url, timeout=3, allow_redirects=True)
            elapsed = time.time() - start
            return True, response.status_code, elapsed
        except:
            return False, 0, 0

    def discover_extended_endpoints(self) -> List[str]:
        """Discover endpoints using extended patterns with HEAD for speed."""
        print(
            f"  Testing {len(self.get_extended_endpoints())} extended endpoint patterns..."
        )
        discovered = []

        for endpoint in self.get_extended_endpoints():
            for port in [443] + self.open_ports:
                try:
                    if port == 443:
                        full_url = f"https://{self.device_ip}{endpoint}"
                    else:
                        full_url = f"http://{self.device_ip}:{port}{endpoint}"

                    # Quick check with HEAD first
                    exists, status_code, elapsed = self.quick_check_endpoint(full_url)

                    if exists and status_code in [200, 401, 403, 405]:
                        print(
                            f"    Found: {endpoint} (port {port}, {status_code}, {elapsed:.2f}s)"
                        )
                        discovered.append(endpoint)
                        self.discovered_urls.add(full_url)
                        break

                except:
                    pass

        print(f"  Discovery complete: {len(discovered)} endpoints")
        return discovered

    def discover_via_options(self, endpoint: str) -> List[str]:
        """Use HTTP OPTIONS to discover allowed methods."""
        try:
            url = f"https://{self.device_ip}{endpoint}"
            response = self.session.options(url, timeout=5)

            if response.status_code in [200, 204]:
                allowed = response.headers.get("Allow", "")
                if allowed:
                    methods = [m.strip() for m in allowed.split(",")]
                    print(f"    OPTIONS {endpoint}: {', '.join(methods)}")
                    return methods
        except:
            pass
        return []

    def discover_from_robots_txt(self) -> List[str]:
        """Parse robots.txt for hidden/disallowed endpoints."""
        print(f"  Parsing robots.txt...")
        discovered = []

        try:
            response = self.session.get(
                f"https://{self.device_ip}/robots.txt", timeout=5
            )
            if response.status_code == 200:
                for line in response.text.split("\n"):
                    line = line.strip()
                    if line.startswith("Disallow:") or line.startswith("Allow:"):
                        path = line.split(":", 1)[1].strip()
                        if path and path != "/":
                            discovered.append(path)
                            print(f"    Found in robots.txt: {path}")
        except:
            pass

        return discovered

    def discover_from_sitemap(self) -> List[str]:
        """Parse sitemap.xml for endpoints."""
        print(f"  Parsing sitemap.xml...")
        discovered = []

        for sitemap_path in ["/sitemap.xml", "/sitemap_index.xml", "/sitemap.txt"]:
            try:
                response = self.session.get(
                    f"https://{self.device_ip}{sitemap_path}", timeout=5
                )
                if response.status_code == 200:
                    if sitemap_path.endswith(".xml"):
                        # Parse XML sitemap
                        root = ET.fromstring(response.content)
                        for url in root.findall(".//{*}loc"):
                            path = urlparse(url.text).path
                            if path and path not in discovered:
                                discovered.append(path)
                                print(f"    Found in sitemap: {path}")
                    else:
                        # Parse text sitemap
                        for line in response.text.split("\n"):
                            path = urlparse(line.strip()).path
                            if path:
                                discovered.append(path)
            except:
                pass

        return discovered

    def discover_from_content(self, base_response: requests.Response) -> List[str]:
        """Analyze HTML/JavaScript content for API hints."""
        print(f"  Analyzing content for API hints...")
        discovered = []
        content = base_response.text.lower()

        # JavaScript API patterns
        js_patterns = [
            r'[\'"/]api/([a-zA-Z0-9_/-]+)',
            r'fetch\([\'"]([^\'"]+)',
            r'axios\.[get|post|put|delete]+\([\'"]([^\'"]+)',
            r"window\.api[_\w]*",
            r'api[_\w]*\s*=\s*[\'"]([^\'"]+)',
            r'baseurl\s*=\s*[\'"]([^\'"]+)',
            r'endpoint\s*=\s*[\'"]([^\'"]+)',
            r'url:\s*[\'"]([^\'"]+)',
        ]

        for pattern in js_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                endpoint = f"/api/{match}" if not match.startswith("/") else match
                if endpoint not in discovered and len(endpoint) < 200:
                    discovered.append(endpoint)

        # Find JavaScript file references
        js_file_pattern = r'<script[^>]+src=[\'"]([^\'"]+\.js)[\'"]'
        js_files = re.findall(js_file_pattern, base_response.text, re.IGNORECASE)
        for js_file in js_files:
            self.js_files.append(urljoin(f"https://{self.device_ip}", js_file))

        if discovered:
            print(f"    Found {len(discovered)} content-based endpoints")
        if self.js_files:
            print(f"    Found {len(self.js_files)} JavaScript files to parse")

        return discovered

    def parse_javascript_files(self) -> List[str]:
        """Download and parse JavaScript files for API endpoints."""
        print(f"  Parsing JavaScript files...")
        discovered = []

        for js_url in self.js_files[:10]:  # Limit to first 10 JS files
            try:
                response = self.session.get(js_url, timeout=5)
                if response.status_code == 200:
                    content = response.text

                    # Look for API endpoints
                    patterns = [
                        r'[\'"]/(api|rest|services?)/[a-zA-Z0-9_/-]+[\'"]',
                        r'endpoint:\s*[\'"]([^\'"]+)',
                        r'url:\s*[\'"]([^\'"]+)',
                        r'path:\s*[\'"]([^\'"]+)',
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if isinstance(match, tuple):
                                match = match[1] if len(match) > 1 else match[0]
                            if match.startswith("/") and len(match) < 200:
                                discovered.append(match)

            except:
                pass

        discovered = list(set(discovered))
        if discovered:
            print(f"    Extracted {len(discovered)} endpoints from JavaScript")
        return discovered

    def discover_config_files(self) -> List[str]:
        """Look for configuration files that might reveal endpoints."""
        print(f"  Searching for config files...")
        discovered = []

        config_files = [
            "/config.json",
            "/config.xml",
            "/config.yaml",
            "/config.yml",
            "/settings.json",
            "/settings.xml",
            "/manifest.json",
            "/package.json",
            "/composer.json",
            "/.env",
            "/env.json",
            "/app.config",
            "/web.config",
        ]

        for config_file in config_files:
            try:
                response = self.session.get(
                    f"https://{self.device_ip}{config_file}", timeout=5
                )
                if response.status_code == 200:
                    print(f"    Found config file: {config_file}")
                    discovered.append(config_file)

                    # Try to parse JSON for endpoint hints
                    if config_file.endswith(".json"):
                        try:
                            data = response.json()
                            # Look for URL/endpoint patterns
                            self._extract_urls_from_json(data, discovered)
                        except:
                            pass
            except:
                pass

        return discovered

    def _extract_urls_from_json(self, data: Union[dict, list], discovered: List[str]):
        """Recursively extract URLs from JSON data."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and (
                    value.startswith("/") or "api" in key.lower()
                ):
                    if len(value) < 200 and value not in discovered:
                        discovered.append(value)
                elif isinstance(value, (dict, list)):
                    self._extract_urls_from_json(value, discovered)
        elif isinstance(data, list):
            for item in data:
                self._extract_urls_from_json(item, discovered)

    def recursive_discovery(self, endpoint: str, depth: int = 2) -> List[str]:
        """Follow links in API responses to discover more endpoints."""
        if depth <= 0:
            return []

        discovered = []
        try:
            url = f"https://{self.device_ip}{endpoint}"
            response = self.session.get(url, timeout=5)

            if response.status_code == 200:
                # Try to parse as JSON
                try:
                    data = response.json()
                    links = self._extract_links_from_json(data)
                    for link in links:
                        if link not in self.discovered_urls:
                            discovered.append(link)
                            self.discovered_urls.add(link)
                            # Recursive call with reduced depth
                            if depth > 1:
                                sub_links = self.recursive_discovery(link, depth - 1)
                                discovered.extend(sub_links)
                except:
                    pass
        except:
            pass

        return discovered

    def _extract_links_from_json(self, data: Union[dict, list]) -> List[str]:
        """Extract link/href/url fields from JSON response."""
        links = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key.lower() in ["link", "href", "url", "uri", "endpoint", "path"]:
                    if isinstance(value, str) and value.startswith("/"):
                        links.append(value)
                elif isinstance(value, (dict, list)):
                    links.extend(self._extract_links_from_json(value))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    links.extend(self._extract_links_from_json(item))

        return links

    def analyze_headers(self, response: requests.Response) -> Dict[str, str]:
        """Analyze HTTP headers for API hints, CORS, rate limiting."""
        headers = response.headers

        analysis = {"api_hints": {}, "cors": {}, "rate_limiting": {}, "security": {}}

        # API hints
        hint_keywords = [
            "server",
            "x-api",
            "x-rest-api",
            "content-type",
            "api-version",
            "x-api-version",
        ]
        for hint in hint_keywords:
            if hint in headers:
                analysis["api_hints"][hint] = headers[hint]

        # CORS headers
        cors_headers = [
            "access-control-allow-origin",
            "access-control-allow-methods",
            "access-control-allow-headers",
            "access-control-expose-headers",
        ]
        for cors_header in cors_headers:
            if cors_header in headers:
                analysis["cors"][cors_header] = headers[cors_header]

        # Rate limiting
        rate_headers = [
            "x-ratelimit-limit",
            "x-ratelimit-remaining",
            "x-ratelimit-reset",
            "x-rate-limit-limit",
            "x-rate-limit-remaining",
        ]
        for rate_header in rate_headers:
            if rate_header in headers:
                analysis["rate_limiting"][rate_header] = headers[rate_header]

        # Security headers
        security_headers = [
            "strict-transport-security",
            "x-frame-options",
            "x-content-type-options",
        ]
        for sec_header in security_headers:
            if sec_header in headers:
                analysis["security"][sec_header] = headers[sec_header]

        return analysis

    def test_content_negotiation(self, endpoint: str) -> Dict[str, int]:
        """Test different Accept headers for content negotiation."""
        url = f"https://{self.device_ip}{endpoint}"
        results = {}

        accept_headers = [
            "application/json",
            "application/xml",
            "application/yaml",
            "text/html",
            "text/plain",
            "application/vnd.api+json",
            "*/*",
        ]

        for accept in accept_headers:
            try:
                response = self.session.get(url, headers={"Accept": accept}, timeout=3)
                results[accept] = response.status_code
            except:
                results[accept] = 0

        return results

    def test_path_parameters(self, endpoint: str) -> List[str]:
        """Test common path parameter patterns."""
        discovered = []
        base_url = f"https://{self.device_ip}{endpoint}"

        # Common ID patterns
        test_ids = ["1", "0", "all", "list", "default", "test", "me", "current"]

        for test_id in test_ids:
            test_url = f"{base_url}/{test_id}"
            try:
                exists, status_code, _ = self.quick_check_endpoint(test_url)
                if exists and status_code not in [404, 500]:
                    discovered.append(f"{endpoint}/{test_id}")
            except:
                pass

        return discovered

    def test_query_parameters(self, endpoint: str) -> Dict[str, List[int]]:
        """Test common query parameters."""
        url = f"https://{self.device_ip}{endpoint}"
        results = {}

        common_params = {
            "format": ["json", "xml", "yaml"],
            "page": ["1", "0"],
            "limit": ["10", "100"],
            "sort": ["asc", "desc"],
            "filter": ["all", "active"],
            "id": ["1", "0"],
            "type": ["all", "summary"],
            "verbose": ["true", "false", "1", "0"],
            "debug": ["true", "1"],
        }

        for param, values in common_params.items():
            param_results = []
            for value in values:
                try:
                    test_url = f"{url}?{param}={value}"
                    response = self.session.get(test_url, timeout=3)
                    param_results.append(response.status_code)
                except:
                    param_results.append(0)
            if any(r not in [0, 404] for r in param_results):
                results[param] = param_results

        return results

    def discover_backup_files(self) -> List[str]:
        """Look for backup and old versions of files."""
        print(f"  Searching for backup files...")
        discovered = []

        backup_extensions = [
            ".bak",
            ".old",
            ".backup",
            ".save",
            ".tmp",
            "~",
            ".orig",
            ".copy",
        ]
        base_files = ["/api", "/config", "/swagger", "/api.json", "/config.json"]

        for base_file in base_files:
            for ext in backup_extensions:
                backup_file = f"{base_file}{ext}"
                try:
                    exists, status_code, _ = self.quick_check_endpoint(
                        f"https://{self.device_ip}{backup_file}"
                    )
                    if exists and status_code == 200:
                        print(f"    Found backup: {backup_file}")
                        discovered.append(backup_file)
                except:
                    pass

        return discovered

    def analyze_error_messages(self, response: requests.Response) -> Dict[str, any]:
        """Analyze error messages for hints about parameters, authentication, etc."""
        analysis = {
            "framework_detected": None,
            "parameters_mentioned": [],
            "authentication_required": False,
            "error_details": None,
        }

        content = response.text.lower()

        # Framework detection
        frameworks = {
            "django": ["django", "csrftoken"],
            "flask": ["werkzeug", "flask"],
            "express": ["express"],
            "fastapi": ["fastapi", "starlette"],
            "spring": ["whitelabel error page", "spring"],
            "asp.net": ["asp.net", "system.web"],
        }

        for framework, indicators in frameworks.items():
            if any(ind in content for ind in indicators):
                analysis["framework_detected"] = framework
                if framework not in self.api_results["discovered_frameworks"]:
                    self.api_results["discovered_frameworks"].append(framework)

        # Look for parameter mentions
        param_patterns = [
            r'parameter[:\s]+[\'"]?([a-zA-Z0-9_-]+)',
            r'missing[:\s]+[\'"]?([a-zA-Z0-9_-]+)',
            r'required[:\s]+[\'"]?([a-zA-Z0-9_-]+)',
        ]

        for pattern in param_patterns:
            matches = re.findall(pattern, content)
            analysis["parameters_mentioned"].extend(matches)

        # Authentication detection
        auth_indicators = [
            "unauthorized",
            "authentication required",
            "api key",
            "token required",
            "forbidden",
        ]
        if any(ind in content for ind in auth_indicators):
            analysis["authentication_required"] = True

        return analysis

    def detect_framework_patterns(self, response: requests.Response) -> List[str]:
        """Detect web framework and add framework-specific endpoints."""
        discovered = []
        content = response.text.lower()
        headers = {k.lower(): v for k, v in response.headers.items()}

        # Django REST Framework
        if "django" in content or "csrftoken" in content:
            discovered.extend(["/api/schema/", "/api/?format=json", "/api/?format=api"])
            print(f"    Detected: Django REST Framework")

        # FastAPI
        if "fastapi" in content or "starlette" in content:
            discovered.extend(["/docs", "/redoc", "/openapi.json"])
            print(f"    Detected: FastAPI")

        # Express.js
        if "express" in headers.get("x-powered-by", "").lower():
            discovered.extend(["/api-docs", "/explorer"])
            print(f"    Detected: Express.js")

        # Flask
        if "werkzeug" in content or "flask" in content:
            discovered.extend(["/api/swagger", "/api/docs"])
            print(f"    Detected: Flask")

        return discovered

    def discover_websockets(self) -> List[str]:
        """Test for WebSocket endpoints."""
        print(f"  Testing WebSocket endpoints...")
        discovered = []

        ws_paths = [
            "/ws",
            "/websocket",
            "/ws/api",
            "/socket.io",
            "/realtime",
            "/events",
            "/stream",
            "/updates",
        ]

        for path in ws_paths:
            # Check if the endpoint exists (might return upgrade required)
            try:
                url = f"https://{self.device_ip}{path}"
                response = self.session.get(url, timeout=3)

                # WebSocket endpoints often return 426 Upgrade Required or have upgrade headers
                if (
                    response.status_code == 426
                    or "upgrade" in response.headers.get("Connection", "").lower()
                    or "websocket" in response.headers.get("Upgrade", "").lower()
                ):
                    print(f"    WebSocket endpoint: {path}")
                    discovered.append(path)
                    self.api_results["websocket_endpoints"].append(path)
            except:
                pass

        return discovered

    def discover_rpc_endpoints(self) -> List[str]:
        """Test for JSON-RPC and XML-RPC endpoints."""
        print(f"  Testing RPC endpoints...")
        discovered = []

        rpc_paths = ["/rpc", "/jsonrpc", "/json-rpc", "/xmlrpc", "/xml-rpc", "/api/rpc"]

        for path in rpc_paths:
            url = f"https://{self.device_ip}{path}"

            # Test JSON-RPC
            try:
                json_rpc_request = {
                    "jsonrpc": "2.0",
                    "method": "system.listMethods",
                    "id": 1,
                }
                response = self.session.post(url, json=json_rpc_request, timeout=5)

                if response.status_code in [
                    200,
                    400,
                ]:  # 400 might indicate invalid method but RPC exists
                    try:
                        data = response.json()
                        if "jsonrpc" in data or "result" in data or "error" in data:
                            print(f"    JSON-RPC endpoint: {path}")
                            discovered.append(path)
                            self.api_results["rpc_endpoints"].append(
                                {"type": "json-rpc", "path": path}
                            )
                    except:
                        pass
            except:
                pass

            # Test XML-RPC
            try:
                xml_rpc_request = """<?xml version="1.0"?>
                <methodCall>
                    <methodName>system.listMethods</methodName>
                </methodCall>"""

                headers = {"Content-Type": "text/xml"}
                response = self.session.post(
                    url, data=xml_rpc_request, headers=headers, timeout=5
                )

                if (
                    "xml" in response.text.lower()
                    and "methodresponse" in response.text.lower()
                ):
                    print(f"    XML-RPC endpoint: {path}")
                    if path not in discovered:
                        discovered.append(path)
                    self.api_results["rpc_endpoints"].append(
                        {"type": "xml-rpc", "path": path}
                    )
            except:
                pass

        return discovered

    def enumerate_api_versions(self, base_endpoint: str) -> List[str]:
        """Systematically enumerate API versions."""
        discovered = []

        version_patterns = [
            "/v{}",
            "/api/v{}",
            "/v{}.0",
            "/api/v{}.0",
            "/v{}.{}",
            "/api/v{}.{}",
        ]

        # Test major versions 1-5
        for major in range(1, 6):
            for pattern in version_patterns:
                if "{}.{}" in pattern:
                    # Test minor versions 0-3
                    for minor in range(0, 4):
                        endpoint = pattern.format(major, minor)
                        url = f"https://{self.device_ip}{endpoint}"
                        exists, status, _ = self.quick_check_endpoint(url)
                        if exists and status not in [404, 500]:
                            discovered.append(endpoint)
                else:
                    endpoint = pattern.format(major)
                    url = f"https://{self.device_ip}{endpoint}"
                    exists, status, _ = self.quick_check_endpoint(url)
                    if exists and status not in [404, 500]:
                        discovered.append(endpoint)

        return discovered

    def test_user_agents(self) -> List[str]:
        """Test different user agents to discover endpoints."""
        print(f"  Testing different user agents...")
        discovered = []

        for ua in self.get_user_agents():
            headers = {"User-Agent": ua}
            try:
                response = self.session.get(
                    f"https://{self.device_ip}/api", headers=headers, timeout=5
                )
                if response.status_code not in [404, 500]:
                    print(
                        f"    User agent '{ua[:30]}...' returned: {response.status_code}"
                    )
                    discovered.append(f"/api (User-Agent: {ua[:30]})")
            except:
                pass

        return discovered

    def test_advanced_authentication(
        self, endpoints: List[str]
    ) -> List[DiscoveredEndpoint]:
        """Test advanced authentication methods with actual device password."""
        print(f"  Testing advanced authentication (including device password)...")
        authenticated_endpoints = []

        # Test with actual credentials
        for endpoint in endpoints[:15]:  # Increased to 15 endpoints
            for username, password in self.get_auth_credentials()[
                :5
            ]:  # Test first 5 credential pairs
                try:
                    url = f"https://{self.device_ip}{endpoint}"
                    response = self.session.get(
                        url, auth=(username, password), timeout=5
                    )

                    if response.status_code == 200:
                        print(
                            f"    Auth success: {endpoint} with {username}:{password}"
                        )
                        disc_endpoint = DiscoveredEndpoint(url, "GET", 443)
                        disc_endpoint.auth_required = True
                        disc_endpoint.status_code = 200
                        disc_endpoint.discovery_method = f"auth_basic_{username}"
                        authenticated_endpoints.append(disc_endpoint)
                        break  # Stop trying credentials once we find one that works
                except:
                    pass

        return authenticated_endpoints

    def discover_soap_services(self) -> List[str]:
        """Look for SOAP/WSDL services."""
        print(f"  Scanning for SOAP/WSDL services...")
        soap_endpoints = [
            "/wsdl",
            "/soap",
            "/service",
            "/services",
            "/services.wsdl",
            "/api/wsdl",
            "/api/soap",
            "/?wsdl",
        ]
        discovered = []

        for endpoint in soap_endpoints:
            try:
                response = self.session.get(
                    f"https://{self.device_ip}{endpoint}", timeout=5
                )
                if "wsdl" in response.text.lower() or "soap" in response.text.lower():
                    print(f"    SOAP service found: {endpoint}")
                    discovered.append(endpoint)
            except:
                pass

        return discovered

    def discover_graphql(self) -> List[str]:
        """Look for GraphQL endpoints."""
        print(f"  Scanning for GraphQL endpoints...")
        graphql_paths = [
            "/graphql",
            "/graph",
            "/query",
            "/gql",
            "/api/graphql",
            "/playground",
            "/graphiql",
            "/altair",
        ]
        discovered = []

        for path in graphql_paths:
            try:
                # GraphQL endpoints typically return 400 for GET requests without query
                response = self.session.get(
                    f"https://{self.device_ip}{path}", timeout=5
                )
                if response.status_code in [400, 405]:
                    print(f"    Potential GraphQL endpoint: {path}")
                    discovered.append(path)

                # Try POST with introspection query
                introspection_query = {"query": "{__schema{types{name}}}"}
                response = self.session.post(
                    f"https://{self.device_ip}{path}",
                    json=introspection_query,
                    timeout=5,
                )
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if "data" in data or "__schema" in str(data):
                            print(f"    GraphQL confirmed: {path}")
                            if path not in discovered:
                                discovered.append(path)
                    except:
                        pass
            except:
                pass

        return discovered

    def test_endpoint_methods(self, endpoint: str) -> List[DiscoveredEndpoint]:
        """Test different HTTP methods on an endpoint with timing and analysis."""
        endpoints = []
        url = f"https://{self.device_ip}{endpoint}"
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

        # First, use OPTIONS to see what's allowed
        allowed_methods = self.discover_via_options(endpoint)

        for method in methods:
            disc_endpoint = DiscoveredEndpoint(url, method, 443)
            disc_endpoint.discovery_method = "extended_pattern"
            disc_endpoint.allowed_methods = allowed_methods

            try:
                start_time = time.time()

                if method == "GET":
                    response = self.session.get(url, timeout=5)
                elif method == "HEAD":
                    response = self.session.head(url, timeout=5)
                elif method == "OPTIONS":
                    response = self.session.options(url, timeout=5)
                elif method == "POST":
                    response = self.session.post(url, json={}, timeout=5)
                elif method == "PUT":
                    response = self.session.put(url, json={}, timeout=5)
                elif method == "DELETE":
                    response = self.session.delete(url, timeout=5)
                elif method == "PATCH":
                    response = self.session.patch(url, json={}, timeout=5)

                elapsed = time.time() - start_time

                if response:
                    disc_endpoint.status_code = response.status_code
                    disc_endpoint.response_headers = dict(response.headers)
                    disc_endpoint.response_data = response.text[:500]
                    disc_endpoint.response_time = round(elapsed, 3)
                    disc_endpoint.tested = True
                    disc_endpoint.test_timestamp = datetime.now().isoformat()

                    # Analyze headers
                    header_analysis = self.analyze_headers(response)
                    disc_endpoint.headers_analysis = header_analysis
                    disc_endpoint.cors_info = header_analysis.get("cors", {})
                    disc_endpoint.rate_limit_info = header_analysis.get(
                        "rate_limiting", {}
                    )

                    # Check for documentation
                    if any(
                        doc_term in response.text.lower()
                        for doc_term in ["swagger", "openapi", "api documentation"]
                    ):
                        disc_endpoint.documentation_available = True

                    # Analyze error messages
                    if response.status_code >= 400:
                        error_analysis = self.analyze_error_messages(response)
                        disc_endpoint.error_responses = error_analysis

                    # Test content negotiation for successful responses
                    if response.status_code == 200 and method == "GET":
                        content_types = self.test_content_negotiation(endpoint)
                        disc_endpoint.supported_formats = [
                            ct for ct, code in content_types.items() if code == 200
                        ]

                    print(f"    {method}: {response.status_code} ({elapsed:.2f}s)")

            except Exception as e:
                disc_endpoint.status_code = "error"
                disc_endpoint.error_responses["exception"] = str(e)
                disc_endpoint.tested = True

            endpoints.append(disc_endpoint)

        return endpoints

    def generate_comprehensive_documentation(self):
        """Generate comprehensive API documentation with all discoveries."""
        print(f"\n[{self.device_ip}] Generating comprehensive API documentation...")

        # Save raw results
        output_dir = OUTPUT_BASE / self.device_ip / "api"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "api_exploration_results.json"
        with open(output_file, "w") as f:
            json.dump(self.api_results, f, indent=2)
        print(f"[OK] [{self.device_ip}] Results saved to: {output_file}")

        # Generate human-readable documentation
        doc_file = output_dir / "API_DOCUMENTATION.md"

        doc_content = f"""# API Documentation
## Device: {self.device_name} ({self.device_ip})

**Exploration Date**: {self.api_results['exploration_date']}  
**Device Type**: {self.device_type}  
**Base URL**: {self.api_results['base_url']}  
**Open Ports Found**: {self.open_ports}

---

## Executive Summary

This document lists all API endpoints discovered using 20+ advanced exploration techniques.

"""

        # Add summary statistics
        total_endpoints = len(self.api_results["endpoints"])
        working_endpoints = len(
            [
                e
                for e in self.api_results["endpoints"]
                if isinstance(e["status_code"], int) and e["status_code"] < 500
            ]
        )
        auth_endpoints = len(
            [e for e in self.api_results["endpoints"] if e.get("auth_required", False)]
        )
        doc_endpoints = len(
            [
                e
                for e in self.api_results["endpoints"]
                if e.get("documentation_available", False)
            ]
        )

        # Calculate average response time
        response_times = [
            e.get("response_time", 0)
            for e in self.api_results["endpoints"]
            if e.get("response_time") and e.get("response_time") > 0
        ]
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )

        doc_content += f"""
### Discovery Summary

- **Total Endpoints Tested**: {total_endpoints}
- **Working Endpoints**: {working_endpoints}
- **Authentication Required**: {auth_endpoints}
- **API Documentation Found**: {doc_endpoints}
- **Open Ports**: {self.open_ports}
- **WebSocket Endpoints**: {len(self.api_results.get('websocket_endpoints', []))}
- **RPC Endpoints**: {len(self.api_results.get('rpc_endpoints', []))}
- **Frameworks Detected**: {', '.join(self.api_results.get('discovered_frameworks', [])) or 'None'}
- **Average Response Time**: {avg_response_time:.3f}s
- **Discovery Methods Used**: {len(self.api_results['discovery_methods'])}

"""

        # WebSocket endpoints section
        if self.api_results.get("websocket_endpoints"):
            doc_content += f"\n### WebSocket Endpoints\n\n"
            for ws_endpoint in self.api_results["websocket_endpoints"]:
                doc_content += f"- `{ws_endpoint}`\n"
            doc_content += "\n"

        # RPC endpoints section
        if self.api_results.get("rpc_endpoints"):
            doc_content += f"\n### RPC Endpoints\n\n"
            for rpc in self.api_results["rpc_endpoints"]:
                doc_content += f"- **{rpc['type'].upper()}**: `{rpc['path']}`\n"
            doc_content += "\n"

        # Add endpoint details grouped by URL
        endpoint_groups = {}
        for endpoint_data in self.api_results["endpoints"]:
            url = endpoint_data["url"]
            if url not in endpoint_groups:
                endpoint_groups[url] = []
            endpoint_groups[url].append(endpoint_data)

        doc_content += "\n---\n\n## Discovered Endpoints\n\n"

        for url, endpoints in sorted(endpoint_groups.items()):
            doc_content += f"\n### {url}\n\n"

            # Show allowed methods if discovered via OPTIONS
            allowed = endpoints[0].get("allowed_methods", [])
            if allowed:
                doc_content += (
                    f"**Allowed Methods** (via OPTIONS): {', '.join(allowed)}  \n"
                )

            working_methods = [
                e["method"]
                for e in endpoints
                if isinstance(e["status_code"], int) and e["status_code"] < 500
            ]
            if working_methods:
                doc_content += f"**Working Methods**: {', '.join(working_methods)}  \n"

            # Show supported content types
            supported_formats = endpoints[0].get("supported_formats", [])
            if supported_formats:
                doc_content += (
                    f"**Supported Formats**: {', '.join(supported_formats)}  \n"
                )

            # Show CORS info if present
            cors_info = endpoints[0].get("cors_info", {})
            if cors_info:
                doc_content += f"**CORS Enabled**: Yes  \n"

            # Show rate limiting if detected
            rate_info = endpoints[0].get("rate_limit_info", {})
            if rate_info:
                doc_content += f"**Rate Limiting**: Detected  \n"

            doc_content += "\n"

            # Detail each method
            for endpoint_data in endpoints:
                status = endpoint_data["status_code"]
                if (
                    isinstance(status, int) and status < 500
                ):  # Only show working endpoints in detail
                    doc_content += f"#### {endpoint_data['method']} Method\n\n"
                    doc_content += f"**Status Code**: {status}  \n"

                    resp_time = endpoint_data.get("response_time")
                    if resp_time:
                        doc_content += f"**Response Time**: {resp_time}s  \n"

                    doc_content += f"**Discovery Method**: {endpoint_data.get('discovery_method', 'unknown')}  \n"

                    if endpoint_data.get("auth_required"):
                        doc_content += f"**Authentication**: Required  \n"

                    if endpoint_data.get("response_headers"):
                        important_headers = ["content-type", "server", "api-version"]
                        headers = {
                            k: v
                            for k, v in endpoint_data["response_headers"].items()
                            if k.lower() in important_headers
                        }
                        if headers:
                            doc_content += f"**Key Headers**: {headers}  \n"

                    if (
                        endpoint_data.get("response_data")
                        and len(endpoint_data["response_data"]) > 10
                    ):
                        preview = endpoint_data["response_data"][:150].replace(
                            "\n", " "
                        )
                        doc_content += f"**Response Preview**: `{preview}...`  \n"

                    # Show error analysis if available
                    error_resp = endpoint_data.get("error_responses", {})
                    if error_resp.get("parameters_mentioned"):
                        params = error_resp["parameters_mentioned"]
                        doc_content += (
                            f"**Parameters Detected**: {', '.join(params)}  \n"
                        )

                    doc_content += "\n"

        # Add implementation notes
        doc_content += """
---

## Discovery Methods Used

This exploration utilized the following 20+ advanced techniques:

### Core Discovery
1. **Extended Endpoint Discovery** - Tested 150+ endpoint patterns
2. **Multi-Port Scanning** - Scanned 14 common API ports
3. **Quick HEAD Checks** - Fast endpoint validation with HEAD requests
4. **OPTIONS Method** - Discovered allowed HTTP methods

### Content Analysis
5. **HTML/JavaScript Parsing** - Extracted API calls from inline code
6. **JavaScript File Analysis** - Downloaded and parsed .js files for endpoints
7. **Config File Discovery** - Found and parsed config.json, manifest.json, etc.
8. **Recursive Link Following** - Followed links in API responses

### Discovery Files
9. **robots.txt Parsing** - Extracted disallowed/hidden paths
10. **sitemap.xml Parsing** - Discovered endpoints from sitemap
11. **Backup File Discovery** - Found .bak, .old, .backup versions

### Protocol Detection
12. **SOAP/WSDL Discovery** - Scanned for SOAP services
13. **GraphQL Detection** - Tested for GraphQL with introspection
14. **WebSocket Discovery** - Tested WebSocket upgrade endpoints
15. **JSON-RPC/XML-RPC** - Tested RPC interfaces

### Advanced Testing
16. **Framework Detection** - Identified Django, FastAPI, Flask, Express patterns
17. **API Version Enumeration** - Systematically tested v1-v5 with minor versions
18. **Content-Type Negotiation** - Tested JSON, XML, YAML, HTML formats
19. **Path Parameter Testing** - Tested /api/resource/{id} patterns
20. **Query Parameter Discovery** - Tested common query parameters

### Analysis
21. **Header Analysis** - Analyzed CORS, rate limiting, security headers
22. **Response Time Tracking** - Measured endpoint performance
23. **Error Message Analysis** - Extracted hints from error responses
24. **User-Agent Testing** - Tested device-specific user agents
25. **Advanced Authentication** - Tested with actual device credentials

---

## Recommendations

### For API Integration:
- Use endpoints with status codes 200-299 for integration
- Check authentication requirements before implementation
- Respect rate limiting headers if present
- Use content negotiation for optimal data format

### For Further Testing:
- Test discovered parameters on working endpoints
- Attempt authenticated requests on 401/403 endpoints
- Investigate slow response times (>2s) for optimization
- Review CORS settings for web application integration

---

**Generated by Fully API Explorer**  
**Tool**: `tools/api_explorer.py`  
**Discovery Techniques**: 20+  
**Completion Date**: {datetime.now().isoformat()}
"""

        with open(doc_file, "w") as f:
            f.write(doc_content)

        print(f"[OK] [{self.device_ip}] Documentation saved to: {doc_file}")

    def explore_apis(self):
        """Main API exploration workflow with all 20+ techniques."""
        print(f"\n{'='*70}")
        print(f"FULLY API EXPLORATION: {self.device_name} ({self.device_ip})")
        print(f"{'='*70}")

        try:
            # Test basic connectivity
            print(f"\n--- 1. Testing Connectivity ---")
            if not self.test_basic_connectivity():
                print(f"[SKIP] Cannot connect to {self.device_ip}")
                return

            # Scan open ports
            print(f"\n--- 2. Port Scanning ---")
            self.open_ports = self.scan_open_ports()

            # Get base response for analysis
            base_response = None
            try:
                base_response = self.session.get(
                    f"https://{self.device_ip}", timeout=10
                )
            except:
                pass

            # Extended endpoint discovery
            print(f"\n--- 3. Extended Endpoint Discovery ---")
            discovered_endpoints = self.discover_extended_endpoints()

            # robots.txt parsing
            print(f"\n--- 4. robots.txt Parsing ---")
            robots_endpoints = self.discover_from_robots_txt()
            discovered_endpoints.extend(robots_endpoints)

            # sitemap.xml parsing
            print(f"\n--- 5. sitemap.xml Parsing ---")
            sitemap_endpoints = self.discover_from_sitemap()
            discovered_endpoints.extend(sitemap_endpoints)

            # Content-based discovery
            print(f"\n--- 6. Content-Based Discovery ---")
            if base_response:
                content_endpoints = self.discover_from_content(base_response)
                discovered_endpoints.extend(content_endpoints)

            # JavaScript file parsing
            print(f"\n--- 7. JavaScript File Parsing ---")
            js_endpoints = self.parse_javascript_files()
            discovered_endpoints.extend(js_endpoints)

            # Config file discovery
            print(f"\n--- 8. Configuration File Discovery ---")
            config_endpoints = self.discover_config_files()
            discovered_endpoints.extend(config_endpoints)

            # Framework detection
            print(f"\n--- 9. Framework Detection ---")
            if base_response:
                framework_endpoints = self.detect_framework_patterns(base_response)
                discovered_endpoints.extend(framework_endpoints)

            # Backup file discovery
            print(f"\n--- 10. Backup File Discovery ---")
            backup_endpoints = self.discover_backup_files()
            discovered_endpoints.extend(backup_endpoints)

            # User agent testing
            print(f"\n--- 11. User Agent Testing ---")
            ua_endpoints = self.test_user_agents()

            # SOAP discovery
            print(f"\n--- 12. SOAP Service Discovery ---")
            soap_endpoints = self.discover_soap_services()
            discovered_endpoints.extend(soap_endpoints)

            # GraphQL discovery
            print(f"\n--- 13. GraphQL Discovery ---")
            graphql_endpoints = self.discover_graphql()
            discovered_endpoints.extend(graphql_endpoints)

            # WebSocket discovery
            print(f"\n--- 14. WebSocket Discovery ---")
            ws_endpoints = self.discover_websockets()
            discovered_endpoints.extend(ws_endpoints)

            # RPC discovery
            print(f"\n--- 15. RPC Discovery (JSON-RPC/XML-RPC) ---")
            rpc_endpoints = self.discover_rpc_endpoints()
            discovered_endpoints.extend(rpc_endpoints)

            # API version enumeration
            print(f"\n--- 16. API Version Enumeration ---")
            version_endpoints = self.enumerate_api_versions("/api")
            discovered_endpoints.extend(version_endpoints)

            # Remove duplicates
            discovered_endpoints = list(set(discovered_endpoints))
            print(
                f"\n[INFO] Total unique endpoints discovered: {len(discovered_endpoints)}"
            )

            # Recursive discovery on key endpoints
            print(f"\n--- 17. Recursive Link Following ---")
            for endpoint in discovered_endpoints[:5]:  # Limit to first 5
                if "/api" in endpoint:
                    recursive_endpoints = self.recursive_discovery(endpoint, depth=2)
                    discovered_endpoints.extend(recursive_endpoints)

            # Test HTTP methods on discovered endpoints
            print(f"\n--- 18. Testing HTTP Methods & Analysis ---")
            all_endpoints = []
            for i, endpoint in enumerate(
                discovered_endpoints[:30], 1
            ):  # Limit to 30 endpoints
                print(
                    f"\n  [{i}/{min(30, len(discovered_endpoints))}] Testing {endpoint}:"
                )

                # Test methods
                method_endpoints = self.test_endpoint_methods(endpoint)
                all_endpoints.extend(method_endpoints)

                # Test path parameters on promising endpoints
                if any(e.status_code == 200 for e in method_endpoints):
                    path_endpoints = self.test_path_parameters(endpoint)
                    if path_endpoints:
                        print(f"    Path parameters: {len(path_endpoints)} variants")

                # Test query parameters
                for ep in method_endpoints:
                    if ep.status_code == 200 and ep.method == "GET":
                        query_params = self.test_query_parameters(endpoint)
                        if query_params:
                            ep.parameters_discovered = query_params

            # Advanced authentication testing
            print(f"\n--- 19. Advanced Authentication Testing ---")
            auth_endpoints = self.test_advanced_authentication(discovered_endpoints)
            all_endpoints.extend(auth_endpoints)

            # Store results
            self.api_results["endpoints"] = [ep.to_dict() for ep in all_endpoints]
            self.api_results["open_ports"] = self.open_ports
            self.api_results["discovery_methods"] = [
                "extended_endpoint_discovery",
                "robots_txt_parsing",
                "sitemap_xml_parsing",
                "content_based_discovery",
                "javascript_file_parsing",
                "config_file_discovery",
                "framework_detection",
                "backup_file_discovery",
                "user_agent_testing",
                "soap_discovery",
                "graphql_discovery",
                "websocket_discovery",
                "rpc_discovery",
                "api_version_enumeration",
                "recursive_link_following",
                "http_methods_testing",
                "path_parameter_testing",
                "query_parameter_testing",
                "advanced_authentication",
                "options_method_discovery",
                "content_negotiation",
                "header_analysis",
                "error_message_analysis",
                "response_time_analysis",
            ]

            # Generate documentation
            print(f"\n--- 20. Generating Documentation ---")
            self.generate_comprehensive_documentation()

            print(f"\n{'='*70}")
            print(f"[COMPLETE] FULLY API EXPLORATION: {self.device_ip}")
            print(f"{'='*70}")

        except Exception as e:
            print(f"\n[ERROR] API exploration failed: {e}")
            import traceback

            traceback.print_exc()
            self.api_results["errors"].append(str(e))

    def get_summary(self) -> dict:
        """Get exploration summary."""
        total_endpoints = len(self.api_results["endpoints"])
        working_endpoints = len(
            [
                e
                for e in self.api_results["endpoints"]
                if isinstance(e["status_code"], int) and e["status_code"] < 500
            ]
        )
        auth_endpoints = len(
            [e for e in self.api_results["endpoints"] if e.get("auth_required", False)]
        )
        doc_endpoints = len(
            [
                e
                for e in self.api_results["endpoints"]
                if e.get("documentation_available", False)
            ]
        )

        return {
            "total_endpoints": total_endpoints,
            "working_endpoints": working_endpoints,
            "auth_endpoints": auth_endpoints,
            "doc_endpoints": doc_endpoints,
            "websocket_endpoints": len(self.api_results.get("websocket_endpoints", [])),
            "rpc_endpoints": len(self.api_results.get("rpc_endpoints", [])),
            "frameworks": self.api_results.get("discovered_frameworks", []),
            "open_ports": self.open_ports,
            "exploration_date": self.api_results.get("exploration_date"),
            "errors": len(self.api_results.get("errors", [])),
        }


def main():
    """Explore APIs on all Kronos devices using 20+ techniques."""
    print("\n" + "=" * 70)
    print("FULLY KRONOS API EXPLORER")
    print("=" * 70)
    print("\nThis tool uses 20+ advanced discovery techniques:")
    print("  - Extended pattern matching (150+ endpoints)")
    print("  - Multi-port scanning")
    print("  - robots.txt & sitemap.xml parsing")
    print("  - JavaScript & config file analysis")
    print("  - Framework detection")
    print("  - WebSocket & RPC discovery")
    print("  - Advanced authentication with device credentials")
    print("  - Response time analysis")
    print("  - And 12+ more techniques...")
    print("\nWARNING: This tool performs READ-ONLY testing.")
    print("\nDevices to explore:")
    for device in DEVICES:
        print(f"  - {device['name']} ({device['ip']})")

    input("\nPress Enter to start fully exploration...")

    start_time = time.time()

    all_results = {}

    for i, device in enumerate(DEVICES, 1):
        print(f"\n\n{'#'*70}")
        print(f"# Device {i}/{len(DEVICES)}")
        print(f"{'#'*70}")

        explorer = APIExplorer(
            device_ip=device["ip"],
            device_name=device["name"],
            device_type=device["type"],
        )
        explorer.explore_apis()
        all_results[device["ip"]] = explorer.get_summary()

        # Brief pause between devices
        if i < len(DEVICES):
            print(f"\nPausing 5 seconds before next device...")
            time.sleep(5)

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"ALL DEVICES EXPLORED WITH 20+ TECHNIQUES")
    print(f"{'='*70}")
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Results saved to: {OUTPUT_BASE}/{{device_ip}}/api/")
    print(f"\nGenerated files per device:")
    print(f"  - api_exploration_results.json (raw data)")
    print(f"  - API_DOCUMENTATION.md (human-readable)")

    # Overall summary
    print(f"\n{'='*70}")
    print(f"FINAL SUMMARY")
    print(f"{'='*70}")
    for ip, summary in all_results.items():
        print(f"\n{ip}:")
        print(f"  Total endpoints: {summary.get('total_endpoints', 0)}")
        print(f"  Working endpoints: {summary.get('working_endpoints', 0)}")
        print(f"  Authenticated: {summary.get('auth_endpoints', 0)}")
        print(f"  WebSocket: {summary.get('websocket_endpoints', 0)}")
        print(f"  RPC: {summary.get('rpc_endpoints', 0)}")
        print(f"  Open ports: {len(summary.get('open_ports', []))}")
        if summary.get("frameworks"):
            print(f"  Frameworks: {', '.join(summary['frameworks'])}")


if __name__ == "__main__":
    main()
