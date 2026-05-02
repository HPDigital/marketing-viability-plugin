# Instalación del Marketing Viability Plugin

## 1. Instalar el plugin en Claude Code

### Vía marketplace (recomendado)

1. Sube este repositorio a GitHub (público o privado al que tengas acceso).
2. En Claude Code, ejecuta:

   ```
   /plugin marketplace add https://github.com/HPDigital/marketing-viability-plugin
   /plugin install marketing-viability-plugin@hpdigital-marketplace
   ```

3. Reinicia Claude Code para que detecte los skills.

### Vía carga directa

Copiar la carpeta `marketing-viability-plugin/` (la que contiene
`.claude-plugin/` y `skills/`) a `~/.claude/plugins/` y reiniciar Claude Code.

En Windows, la ruta equivalente es:
`C:\Users\<usuario>\.claude\plugins\`.

### Verificación de instalación

Tras reiniciar, los siguientes triggers deberían activar el orquestador:

- "Análisis de viabilidad de marketing para [caso]"
- "Estudio de viabilidad de un nuevo negocio"
- "Plan de marketing estratégico y operativo con análisis financiero"
- "Ejecuta el pipeline completo"

Si los triggers no responden, ejecuta `/plugin list` y confirma que
`marketing-viability-plugin` aparece como instalado y activo.

## 2. Instalar dependencias Python

Los scripts del plugin requieren Python 3.9+ y las siguientes librerías:

```bash
pip install pyyaml matplotlib numpy markdown weasyprint openpyxl
```

### Notas sobre weasyprint en Windows

`weasyprint` requiere las librerías GTK. Si la instalación falla, hay dos
caminos alternativos:

**Opción A — Instalar GTK runtime para Windows:**
1. Descargar el instalador GTK3-Runtime Win64 (gtk3-runtime).
2. Instalarlo y reiniciar la terminal.
3. Reintentar `pip install weasyprint`.

**Opción B — Fallback a pandoc:**
El script `build_part_pdf.py` cae automáticamente a pandoc si weasyprint
no está disponible. Instalar:

1. Descargar pandoc desde https://pandoc.org/installing.html.
2. Instalar también una distribución LaTeX (recomendada: MiKTeX para
   Windows, TinyTeX para entornos ligeros).
3. Confirmar con `pandoc --version` y `xelatex --version`.

### Notas sobre macOS / Linux

En macOS:

```bash
brew install pango libffi
pip install pyyaml matplotlib numpy markdown weasyprint openpyxl
```

En Ubuntu / Debian:

```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
pip install pyyaml matplotlib numpy markdown weasyprint openpyxl
```

## 3. Verificación end-to-end

Tras instalar plugin + dependencias, ejecuta la verificación estructural:

```bash
cd <ruta-al-plugin>
python scripts/verify_system.py .
```

Salida esperada:

```
OK: bundle válido. 0 advertencia(s).
```

Si hay errores, revisa el reporte y corrige. NO empieces a usar el plugin
si la verificación falla.

## 4. Caso de prueba mínimo

En `examples/` hay un brief mínimo (`case_brief.md`) y un YAML de inputs de
gráficos (`chart_inputs.yaml`). Ejecuta:

1. En Claude Code, invoca `marketing-viability-orchestrator` con el caso
   ejemplo.
2. Al finalizar las cuatro partes, verifica que se generaron:
   - `viability-workspace-<slug>/part1..part4/partN_output.md`
   - `viability-workspace-<slug>/part1..part4/partN_output.pdf`
   - `viability-workspace-<slug>/part1..part4/handoff_partN.yaml`
   - `viability-workspace-<slug>/dossier/dossier_viabilidad.md`
   - `viability-workspace-<slug>/dossier/dossier_viabilidad.pdf`
   - `viability-workspace-<slug>/dossier/cross_quality_report.md`

3. Abre el PDF del dossier y confirma que tiene gráficos incrustados, índice
   navegable y los cuatro bloques.

## 5. Soporte

Para incidencias o sugerencias: hpoleynpaz@gmail.com o abrir issue en el
repositorio GitHub correspondiente.

Para modificaciones del plugin con Claude Code, **leer primero
[WARNINGS-CLAUDE-CODE.md](WARNINGS-CLAUDE-CODE.md)** y pegarlo al inicio de
la sesión.
