# Metodología VAN, TIR, payback

## Valor Actual Neto (VAN)

Suma de los flujos de caja libre futuros descontados al presente, menos la inversión inicial.

```
VAN = sum(FCF_t / (1 + r)^t) - I0
```

donde:
- `FCF_t` es el flujo de caja libre del período t.
- `r` es la tasa de descuento.
- `I0` es la inversión inicial (CAPEX inicial + capital de trabajo permanente).

**Criterio**: VAN > 0 indica que el proyecto crea valor sobre la tasa de descuento. VAN = 0 indica indiferencia. VAN < 0 indica destrucción de valor.

**Uso obligatorio en este sistema**:
- VAN base, pesimista, optimista.
- Documentar la tasa de descuento elegida y su justificación.
- En mercados emergentes con riesgo medio-alto: 15%. Mercados desarrollados: 12%. Sectores muy volátiles o pre-revenue: 18-20%.

## Tasa Interna de Retorno (TIR)

Tasa de descuento que hace VAN = 0. Es decir, la rentabilidad implícita del proyecto bajo los flujos proyectados.

```
0 = sum(FCF_t / (1 + TIR)^t) - I0
```

**Criterio**: TIR > tasa de descuento (mínima exigida) indica viabilidad. La diferencia (TIR − r) se llama spread de rentabilidad.

**Reglas anti-error**:
- Cuando los FCF tienen múltiples cambios de signo, puede haber múltiples TIR. En esos casos, usar TIR modificada (MIRR) o complementar con VAN.
- Una TIR muy alta (>50%) en un modelo de servicio establecido es señal de error en los supuestos, no de oportunidad excepcional. Revisar.

## Payback simple

Período en el cual el FCF acumulado iguala la inversión inicial.

```
Payback = mes/año en que cumulative_fcf >= 0
```

**Criterio**:
- Payback < 24 meses: muy rápido, generalmente solo en negocios de margen alto y CAPEX bajo.
- Payback 24-36 meses: típico en servicios con CAPEX moderado.
- Payback 36-60 meses: aceptable en negocios con CAPEX alto.
- Payback > 60 meses: requiere justificación estratégica (barrera de entrada, posicionamiento de largo plazo).

## Payback descontado

Igual que el simple pero usando FCF descontados al presente.

```
Payback_d = mes/año en que cumulative_discounted_fcf >= 0
```

Siempre es mayor que el payback simple. Es la métrica más conservadora.

## Punto de equilibrio (Break-even)

Tres definiciones a presentar:

1. **En volumen**: unidades a vender por mes para cubrir costos fijos.
   ```
   BE_volumen = Costos_fijos_mensuales / Margen_contributivo_unitario
   ```

2. **En valor**: ingresos mensuales para cubrir costos totales.
   ```
   BE_valor = Costos_fijos_mensuales / (1 - Costos_variables / Ingresos)
   ```

3. **Temporal**: mes en que se alcanza el BE en volumen sostenido (típicamente cuando el ramp-up se estabiliza).

## Reglas anti-error globales

1. **Calcular siempre en los tres escenarios**.
2. **Documentar la tasa de descuento**: nunca usar una tasa arbitraria.
3. **No mezclar moneda en el cálculo**: si hay flujos en USD y en BOB, convertir consistentemente.
4. **Considerar el horizonte completo**: cortar en el año 5 sin valor terminal puede subestimar el VAN. Si se usa valor terminal, documentarlo.
5. **El payback no es indicador suficiente solo**: combinar con VAN y TIR.
