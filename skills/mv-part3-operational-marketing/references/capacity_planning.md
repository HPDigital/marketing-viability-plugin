# Capacity planning: cuellos de botella y saltos no lineales

## Identificación de cuellos de botella secuenciales

En cualquier negocio de servicio o producto-servicio existe una secuencia de procesos. La capacidad efectiva es la del proceso más restrictivo.

**Pasos para identificarlo:**
1. Listar todos los procesos secuenciales del flujo de servicio.
2. Calcular la capacidad máxima de cada proceso (unidades por unidad de tiempo).
3. El proceso con menor capacidad es el cuello de botella inmediato.
4. Aliviar el cuello desplaza la restricción al siguiente proceso. Se reidentifica.

**Ejemplos típicos por sector:**
- Servicios profesionales: número de consultores senior con la calificación requerida.
- Salud privada: número de profesionales certificados, capacidad de quirófano, stock crítico.
- Manufactura: capacidad de la línea de producción más lenta, lead time de proveedor crítico.
- B2B SaaS: capacidad del equipo de implementación, no del software per se.

## Saltos de capacidad no lineales

La capacidad no escala linealmente con el volumen. Aumentar capacidad implica decisiones discretas (contratar a otro técnico, abrir un segundo taller, agregar una línea, comprar otra licencia) que tienen costos discretos asociados.

**Patrón típico:**
- Año 1-2: capacidad fase 1 estable, ramp-up de aprovechamiento.
- Año 3: salto de capacidad fase 2 (segundo recurso crítico) cuando aprovechamiento de fase 1 supera 80%.
- Año 4-5: salto de capacidad fase 3 cuando geografía o segmento adicional lo justifica.

Cada salto requiere documentar:
- Año en que se ejecuta.
- Acción concreta (contratación, instalación, inversión).
- CAPEX asociado.
- OPEX incremental mensual.
- Plazo de ramp-up del nuevo recurso (típicamente 3-6 meses).

## Implicaciones para el modelo financiero (Parte 4)

1. **El SOM efectivo está limitado por la capacidad fase 1 hasta que se ejecute el primer salto**.
2. **Cada salto implica disrupción de margen** durante el ramp-up del nuevo recurso.
3. **Decidir el momento del salto es decisión estratégica**: salto temprano = sobrecapacidad costosa; salto tardío = pérdida de oportunidad y servicio degradado.
4. **El programa de validación debe verificar la demanda antes de cada salto mayor**.

## Reglas anti-error

1. **No proyectar capacidad lineal**: el modelo financiero con capacidad lineal es engañoso.
2. **Documentar cada cuello de botella**: si en Parte 3 no aparece el cuello, en Parte 4 el modelo será infiable.
3. **No subestimar el ramp-up**: un técnico nuevo no produce a capacidad plena desde el día 1.
4. **No ocultar el CAPEX de expansión en el OPEX**: separar inversión discreta de costo recurrente.
