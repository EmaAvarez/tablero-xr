# Tablero XR — imagen estática (nginx) del mapa holográfico + cockpit de cumplimiento
# Build:  docker build -t <tu-usuario>/tablero-xr:0.46 -t <tu-usuario>/tablero-xr:latest .
# Run:    docker run --rm -p 8080:80 <tu-usuario>/tablero-xr:latest   ->  http://localhost:8080
FROM nginx:1.27-alpine

# App (una sola página) + datos de la bóveda
COPY index.html /usr/share/nginx/html/index.html
# policies.json: IP de TCM. Para imagen PÚBLICA, comenta la línea siguiente y
# móntalo en runtime:  -v $(pwd)/policies.json:/usr/share/nginx/html/policies.json:ro
COPY policies.json /usr/share/nginx/html/policies.json
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
