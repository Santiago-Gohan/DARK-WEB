# ImpactMind Enterprise

Interfaz para consultar indicadores empresariales desde un backend propio y mostrar cotizaciones cambiarias publicadas por bancos centrales. No inventa perfiles ni métricas cuando la base no está conectada.

## Qué funciona ahora

- Consulta real de USD frente a EUR, MXN, COP, CLP, PEN y BRL desde [Frankfurter](https://frankfurter.dev/), sin API key. Las tasas se actualizan diariamente según sus proveedores; no son precios intradía.
- Panel empresarial conectado por API: resumen, compañías, proyectos, análisis y evidencia.
- Estados vacíos y errores explícitos si falta el backend. El análisis queda deshabilitado hasta recibir empresas reales.
- Revisión y guardado explícito de proyectos; la web no ejecuta cambios operativos automáticamente.

## Ejecutar localmente

Abre `index.html` en un navegador. Las cotizaciones del dólar requieren Internet. Sin backend, el panel empresarial mostrará «Conecta tu base de datos» y no mostrará valores ficticios.

## Conectar el backend

Edita `config.js` para indicar la URL pública de tu API:

```js
window.IMPACTMIND_CONFIG = { apiBase: "https://tu-api.example.com" };
```

No incluyas contraseñas, claves privadas ni credenciales de base de datos en `config.js` ni en el frontend. La API debe autenticar al usuario y consultar la base del lado del servidor, o aplicar políticas de acceso estrictas si usas una plataforma con cliente público.

### Endpoints esperados

- `GET /api/analytics/summary` → `{ "companyCount": 12, "criticalNeedCount": 2, "projectCount": 4, "updatedAt": "ISO-8601", "signals": [] }`
- `GET /api/companies` → lista o `{ "items": [] }`; cada empresa: `id`, `name`, `sector`, `needClass`, `needScore`, `needSummary`, `updatedAt`.
- `GET /api/projects` → lista o `{ "items": [] }`; cada proyecto incluye `id`, `companyName`, `title`, `objective`, `priority`, `score`, `duration`, `kpis`, `integrations`, `phases`, `status`, `updatedAt`.
- `POST /api/companies/{id}/analysis` recibe `{ "question": "..." }` y devuelve `id`, `priority`, `score`, `summary`, `evidence` y, si corresponde, una propuesta `project` con título, objetivo, fases e indicadores.
- `POST /api/companies/{id}/projects` recibe `{ "analysisId": "..." }` y guarda la propuesta tras la acción del usuario.

El backend debe producir puntuaciones y planes a partir de datos empresariales autorizados, devolver las fuentes y fechas usadas y validar permisos. Configura CORS si frontend y API tienen dominios distintos. Para desplegar la interfaz como sitio estático, publica también un backend accesible; GitHub Pages por sí solo no ejecuta estos endpoints.
