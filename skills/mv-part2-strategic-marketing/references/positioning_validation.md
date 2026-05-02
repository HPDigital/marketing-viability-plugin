# Validación lingüística del posicionamiento

## Estructura canónica de la declaración de posicionamiento

```
Para [segmento target]
que [problema o necesidad relevante],
[nombre del producto-servicio] es [categoría descriptiva]
que [beneficio diferenciador clave]
porque [razón para creer principal].
A diferencia de [competidor de referencia],
nuestra propuesta [diferenciador competitivo].
```

Cada elemento debe rastrearse a un campo del `handoff_part1.yaml`:

| Elemento | Origen en handoff_part1 |
|---|---|
| Segmento target | `preliminary_segments[entry].name` |
| Problema o necesidad | `customer_understanding.job_statement.functional_outcome` |
| Categoría descriptiva | construcción propia, debe ser legible al cliente |
| Beneficio diferenciador | `customer_understanding.outcomes_prioritized` (tier hiper-decisivo) |
| Razón para creer | `competitive_landscape.price_benchmark` + activos del posicionamiento |
| Competidor de referencia | `competitive_landscape.direct_competitors[0]` o el más relevante |
| Diferenciador competitivo | derivado del Strategy Canvas (factores con mayor delta to-be vs as-is) |

Una declaración de posicionamiento que no puede mapear cada componente a su origen es una declaración no rastreable y debe rechazarse.

## Reglas del tagline operativo

El tagline es una versión condensada del posicionamiento, destinada a uso comercial. Reglas:

1. **Longitud**: entre 4 y 9 palabras. Más largo no es operativo; más corto generalmente carece de información.
2. **Contiene al menos uno de los outcomes hiper-decisivos** del JTBD (referencia a `outcomes_prioritized` con OS ≥ 12).
3. **No usa términos genéricos vacíos**: "calidad", "excelencia", "compromiso", "innovador", "líder" son adjetivos sin contenido. Sustituirlos por especificidades verificables.
4. **Es defendible operativamente**: si el tagline promete algo, la operación debe poder cumplirlo. "Técnico siempre cerca" requiere que efectivamente haya un técnico cerca; si no, el tagline es publicidad engañosa.
5. **Es defendible competitivamente**: si cualquier competidor puede decir lo mismo sin perjuicio, el tagline no diferencia. Test: ¿el competidor directo podría firmar este tagline? Si sí, no diferencia.

## Test de validación lingüística

Aplicar este test antes de fijar el tagline:

| Criterio | Pregunta | Pasa si... |
|---|---|---|
| 1. Longitud | ¿Cuántas palabras tiene? | 4-9 palabras |
| 2. Outcome hiper | ¿Contiene un outcome OS ≥ 12? | Sí |
| 3. Especificidad | ¿Usa términos genéricos vacíos? | No |
| 4. Operatividad | ¿La operación puede cumplir lo prometido? | Sí, con activos verificables |
| 5. Defensibilidad competitiva | ¿El competidor directo podría firmar lo mismo? | No |
| 6. Memorabilidad | ¿Es repetible al primer escucha? | Sí |
| 7. Coherencia con segmento | ¿Resuena con el lenguaje del segmento target? | Sí |

Si falla alguno de los criterios 1-5, reescribir. Los criterios 6 y 7 son señales de alerta pero no descalifican automáticamente.

## Ejemplo aplicado (caso prótesis)

**Tagline propuesto**: "Movilidad europea con técnico siempre cerca."
- Longitud: 6 palabras. ✓
- Contiene outcome hiper (proximidad técnica = O01 OS 13). ✓
- Sin términos genéricos vacíos. ✓
- Operatividad: requiere taller local con técnico ortoprotesista. Verificable. ✓
- Defensibilidad: ningún competidor combina componente europeo con técnico local en un solo proveedor. ✓
- Memorabilidad: alta. ✓
- Coherencia con segmento: lenguaje del paciente (no jerga técnica). ✓

Pasa el test.
