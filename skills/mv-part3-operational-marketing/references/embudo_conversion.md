# Embudo de conversión y tasas de referencia

## Estructura canónica del embudo

```
Lead bruto → Lead cualificado → Cita / contacto inicial → Evaluación / cotización → Cotización aceptada → Cliente firmado
```

Cada etapa tiene una tasa de conversión a la siguiente. La tasa global del embudo es el producto de las tasas etapa por etapa.

## Tasas de referencia por categoría de canal

Las siguientes son tasas de referencia para sectores con ciclo medio de decisión y ticket alto (servicios profesionales, salud privada, B2B). Para sectores muy distintos (e-commerce masivo, consumo cotidiano), aplicar tasas sectoriales propias.

| Etapa | Canal prescriptor | Canal B2B | Canal digital orgánico | Canal alianzas |
|---|---|---|---|---|
| Lead bruto → cualificado | 70-85% | 30-50% | 8-15% | 40-60% |
| Cualificado → cita inicial | 60-80% | 20-40% | 25-45% | 50-70% |
| Cita → evaluación | 70-90% | 60-80% | 50-70% | 60-80% |
| Evaluación → cotización aceptada | 50-70% | 30-50% | 30-50% | 40-60% |
| Cotización → firmado | 60-80% | 60-80% | 60-80% | 70-90% |

**Conversión global típica end-to-end**:
- Prescriptor: 15-30%
- B2B: 1-5%
- Digital orgánico: 0.5-2%
- Alianzas: 5-15%

## Cálculo del CAC por canal

```
CAC_canal = (presupuesto mensual del canal + costo del equipo asignado) / clientes firmados por mes
```

Reglas:
- Incluir costo de personal proporcional asignado al canal.
- Excluir costo de delivery (entrega del producto-servicio): pertenece a costo de servicio, no a CAC.
- Aplicar mensualmente y promediar a 12 meses para CAC anualizado.

## CAC blended

```
CAC_blended = sum(CAC_canal_i × volumen_canal_i) / sum(volumen_canal_i)
```

El CAC blended cambia con el mix proyectado. Tipicamente:
- Año 1: alto, dominado por canales caros (B2B, lanzamiento) y bajo volumen.
- Años 2-3: bajan por escala y porque la red prescriptora aporta volumen sin costo marginal.
- Años 4-5: estabilizado.

## Reglas anti-error

1. **No diluir CAC con leads no cualificados**: si el lead no encaja con el ICP, no entra al embudo de costos.
2. **No proyectar tasas de conversión de la mitad alta del rango**: usar el punto medio en escenario base, mitad baja en pesimista.
3. **No olvidar el costo del equipo en el CAC**: presupuesto publicitario no es CAC completo.
4. **Cuantificar el embudo por canal, no globalmente**: el embudo blended es opaco para diagnóstico.
