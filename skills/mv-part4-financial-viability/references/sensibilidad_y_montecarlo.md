# Análisis de sensibilidad y Monte Carlo simplificado

## Identificación de variables críticas

Las variables críticas son las que cumplen al menos uno de los siguientes criterios:

1. Una variación de ±20% altera el VAN base en más de 30%.
2. Una variación de ±20% cambia el signo del VAN.
3. Una variación de ±20% empuja la TIR por debajo de la tasa de descuento.
4. Una variación de ±20% extiende el payback más de 12 meses.

Las variables candidatas típicas en cualquier modelo:
- Tasa de conversión del embudo (impacto sobre volumen).
- Precio mid de la línea principal (impacto sobre ingresos y margen).
- CAC blended (impacto sobre estructura comercial).
- Costo variable unitario (impacto sobre margen contributivo).
- Capacidad operativa fase 1 (techo de SOM efectivo).
- Tasa de retención del cliente recurrente (impacto sobre LTV).

## Tornado chart

Visualización canónica del análisis de sensibilidad. Para cada variable:
- Calcular VAN con la variable a −20%.
- Calcular VAN con la variable a +20%.
- Mostrar la diferencia con el VAN base como barra horizontal.
- Ordenar las variables de mayor a menor impacto.

La forma del tornado revela el perfil de riesgo:
- Tornado simétrico: variable balanceada, riesgo aproximadamente igual al alza y a la baja.
- Tornado asimétrico negativo: variable con downside dominante, requiere mitigación.
- Tornado asimétrico positivo: variable con upside dominante, oportunidad de captura.

## Monte Carlo simplificado

Para los casos donde se justifica un análisis probabilístico:

1. Asignar una distribución de probabilidad a cada variable crítica (típicamente triangular: min, mode, max).
2. Ejecutar 1.000-10.000 iteraciones aleatorias.
3. Calcular el VAN en cada iteración.
4. Construir la distribución de VAN resultante.
5. Reportar:
   - Probabilidad de VAN > 0.
   - Percentil 5 (peor caso razonable).
   - Percentil 50 (mediana).
   - Percentil 95 (mejor caso razonable).

Implementación mínima en Python:

```python
import numpy as np

def monte_carlo_npv(n_iter, base_assumptions, variables_distributions, npv_function):
    npv_results = []
    for _ in range(n_iter):
        scenario = base_assumptions.copy()
        for var, dist in variables_distributions.items():
            scenario[var] = np.random.triangular(dist["min"], dist["mode"], dist["max"])
        npv_results.append(npv_function(scenario))
    return {
        "p5": np.percentile(npv_results, 5),
        "p50": np.percentile(npv_results, 50),
        "p95": np.percentile(npv_results, 95),
        "prob_positive": sum(1 for v in npv_results if v > 0) / n_iter
    }
```

## Umbrales de invalidación

Para cada variable crítica, declarar el umbral en el que el veredicto se invalida. Ejemplos:

- "Si la tasa de conversión cae bajo 12%, el VAN base se hace negativo."
- "Si el CAC blended supera USD 1.100, el LTV/CAC cae bajo 3."
- "Si la capacidad fase 1 está limitada a 60 Big Hire/año, el SOM es insuficiente para alcanzar el BE en 36 meses."

Estos umbrales se vuelven los criterios de paso/no-paso del programa de validación.

## Reglas anti-error

1. **No analizar sensibilidad solo sobre el VAN**: analizar también TIR y payback.
2. **No analizar variables aisladas si están correlacionadas**: precio y volumen suelen correlacionarse negativamente.
3. **No usar rango ±20% mecánicamente**: ajustar al rango plausible de cada variable.
4. **Reportar los umbrales de invalidación explícitamente**: son la guía operativa del programa de validación.
