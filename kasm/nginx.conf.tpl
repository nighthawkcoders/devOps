server {
    server_name ${subdomain}.nighthawkcodingsociety.com;
    listen 80;

    location / {
         # The following configurations must be configured when proxying to Kasm Workspaces

         # WebSocket Support
         proxy_set_header        Upgrade $http_upgrade;
         proxy_set_header        Connection "upgrade";

         # Host and X headers
         proxy_set_header        Host $host;
         proxy_set_header        X-Real-IP $remote_addr;
         proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header        X-Forwarded-Proto $scheme;

         # Connectivity Options
         proxy_http_version      1.1;
         proxy_read_timeout      1800s;
         proxy_send_timeout      1800s;
         proxy_connect_timeout   1800s;
         proxy_buffering         off;

         # Allow large requests to support file uploads to sessions
         client_max_body_size 10M;

         # Endpoint of service
         proxy_pass https://localhost:8443;
    }
}