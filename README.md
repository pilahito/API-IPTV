# API-IPTV

Proyecto web de código abierto para explorar una lista de canales IPTV. La interfaz estática está en `index.html`, el reproductor en `player.html` y el catálogo de canales en `channels.json`.

> **Aviso:** este proyecto no aloja transmisiones. Antes de usar o compartir un enlace, comprueba que tienes derecho a acceder a ese contenido y que su distribución está autorizada en tu país. Los enlaces pueden dejar de funcionar en cualquier momento.

## Usar el sitio

Abre el sitio publicado en GitHub Pages, selecciona un país y elige un canal. También puedes abrir `channels.json` directamente para consultar el catálogo.

## Actualizar el catálogo

`channels.json` contiene un objeto cuyas claves son países y cuyos valores son listas de canales. Para mantener la compatibilidad con la interfaz y el reproductor, conserva los campos usados por cada uno (`canal`, `enlace`, `codigo`, `ruta` y `m3u8`) y el formato de los enlaces existentes.

Ejemplo orientativo:

```json
{
  "pais": [
    {
      "canal": "Nombre del canal",
      "enlace": "player.html?=tv-pais-canal",
      "codigo": "pais",
      "ruta": "canal",
      "m3u8": "https://ejemplo.invalid/transmision.m3u8"
    }
  ]
}
```

Usa únicamente URLs de transmisiones legítimas y autorizadas. Comprueba que el JSON sea válido antes de publicar cambios.

## Ejecutar localmente

Como el sitio carga `channels.json` con `fetch`, sírvelo mediante un servidor HTTP local en vez de abrir el HTML como archivo. Por ejemplo, con Python:

```bash
python -m http.server 8000
```

Luego visita `http://localhost:8000`.

## Publicar con GitHub Pages

En la configuración del repositorio, habilita GitHub Pages para la rama y carpeta donde están `index.html`, `player.html` y `channels.json`. Cuando Pages termine la publicación, abre la URL indicada en la configuración.

## Reportar problemas y contribuir

Si un canal falla, primero considera que puede estar fuera de horario o que su enlace haya cambiado. Para proponer una mejora, abre un issue o un pull request con una descripción clara y verifica que los enlaces propuestos sean autorizados.

## Licencia

No se especifica una licencia en este repositorio. La disponibilidad pública del código no implica por sí sola permiso para reutilizarlo; consulta al propietario antes de redistribuirlo.
