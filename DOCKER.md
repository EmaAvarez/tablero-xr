# Tablero XR en Docker / Docker Hub

Imagen estática (nginx) que sirve el tablero (`index.html`) + la bóveda (`policies.json`).

## Construir y probar en local
```bash
docker build -t tablero-xr:latest .
docker run --rm -p 8080:80 tablero-xr:latest
# abre http://localhost:8080  (en localhost SÍ arranca WebXR)
```
O con compose:
```bash
docker compose up --build
```

## Publicar en Docker Hub
```bash
docker login
docker build -t <tu-usuario>/tablero-xr:0.46 -t <tu-usuario>/tablero-xr:latest .
docker push <tu-usuario>/tablero-xr:0.46
docker push <tu-usuario>/tablero-xr:latest
```
Otra persona lo ejecuta con:
```bash
docker run --rm -p 8080:80 <tu-usuario>/tablero-xr:latest
```

## IMPORTANTE — WebXR necesita HTTPS
En las gafas Quest, `http://<ip>:8080` NO lanza la realidad mixta (requiere contexto seguro).
Opciones para poner HTTPS delante del contenedor:
- Túnel rápido para pruebas: `cloudflared tunnel --url http://localhost:8080` o `ngrok http 8080`.
- Reverse proxy con certificado (Caddy/Traefik/nginx + Let's Encrypt).
- Desplegar la imagen en una plataforma con TLS incluido: **Azure Container Apps**, Cloud Run, Render, Fly.io.
En `localhost` (navegador del PC) sí funciona sin más.

## IMPORTANTE — `policies.json` es IP de TCM
Si la imagen es PÚBLICA, la bóveda viaja dentro y cualquiera puede descargarla.
Para producto:
- Usa un **repositorio privado** en Docker Hub, o
- No hornees el JSON: comenta el `COPY policies.json ...` del Dockerfile y móntalo en runtime:
  ```bash
  docker run --rm -p 8080:80 \
    -v "$(pwd)/policies.json:/usr/share/nginx/html/policies.json:ro" \
    <tu-usuario>/tablero-xr:latest
  ```

## Siguiente nivel (opcional): backend para auto-auth
Para quitar el pegar-token-a-mano y el límite de ~1 h, un backend en contenedor
(MSAL confidential client o Managed Identity) refresca el token solo y hace de proxy
a Resource Graph / Defender, evitando además el CORS. Encaja especialmente en
**Azure Container Apps con Managed Identity**: la app lee su propio tenant sin credenciales
en el cliente y con HTTPS incluido. (Pendiente de construir.)
