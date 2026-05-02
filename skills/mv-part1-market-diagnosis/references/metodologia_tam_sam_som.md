# Metodología TAM, SAM, SOM

## TAM (Total Addressable Market)
Demanda total teórica si se sirviera al 100% del universo de compradores potenciales globales del producto-servicio.

**Métodos de construcción:**

1. **Top-down**: tomar el mercado global o regional reportado en estudios sectoriales y desglosar por segmentos relevantes. Útil cuando hay datos publicados.
2. **Bottom-up por población**: número de individuos o empresas en el universo elegible × gasto medio anual. Útil para sectores no reportados.
3. **Por analogía**: extrapolar del tamaño de mercados comparables ajustando por factores de penetración y poder adquisitivo.

**Reglas:**
- Documentar siempre la fuente y el año de los datos.
- Declarar nivel de evidencia (primary, secondary, modeled).
- Expresar en rango (min-max), no en punto único.

## SAM (Serviceable Addressable Market)

Subconjunto del TAM al que el modelo de negocio realmente puede llegar dada su geografía, su canal y su capacidad operativa.

**Restricciones a aplicar (en este orden):**

1. **Geografía**: filtro de país, región o ciudad accesible.
2. **Capacidad de pago**: filtro de segmento socioeconómico al que el precio del producto-servicio es accesible (con o sin financiamiento).
3. **Accesibilidad de canal**: filtro de subgrupo al que el canal de adquisición puede llegar a costo razonable.
4. **Circunstancia clínica o situacional**: cuando aplica, filtro de momento o condición que activa la demanda.

**Cálculo:**

```
SAM_personas = TAM_personas × %_geografía × %_capacidad_pago × %_canal_accesible × %_circunstancia_activa
SAM_valor = SAM_personas × gasto_medio_anual_por_persona
```

## SOM (Serviceable Obtainable Market)

Cuota del SAM que el negocio puede capturar realistamente en el horizonte de evaluación.

**Construcción bottom-up obligatoria cuando es posible:**

1. **Capacidad operativa máxima por unidad de tiempo**: límite real de unidades servibles por la capacidad instalada (técnico, taller, equipo comercial, etc.).
2. **Curva de ramp-up**: tiempo que tarda en alcanzarse la capacidad estabilizada.
3. **Tasa de conversión del canal**: fracción de leads cualificados que se convierten en clientes.
4. **Tasa de retención**: fracción de clientes que generan ingresos recurrentes.

**Verificación cruzada top-down**:

```
SOM_top_down = SAM × cuota_capturable_estimada
```

donde `cuota_capturable_estimada` no debe superar el 1-3% del SAM en mercados maduros con competidores establecidos, ni el 5-10% en mercados fragmentados con sub-servicio agudo.

Si el SOM bottom-up y el top-down divergen significativamente, prevalece el bottom-up porque refleja la capacidad real, y se documenta la diferencia.

## Reglas anti-error

1. **Nunca presentar un SOM como porcentaje del TAM sin justificar el SAM intermedio**.
2. **Nunca proyectar SOM lineal**: el SOM tiene saltos porque la capacidad operativa tiene saltos (segundo técnico, segundo taller, etc.).
3. **Nunca inflar el SOM para cuadrar el modelo financiero**: si el SOM bottom-up no sostiene el negocio, el negocio no es viable bajo esas hipótesis.
4. **Documentar el factor de corrección entre disposición declarada y revelada** cuando se construye el SAM en valor.

## Ejemplo aplicado (caso prótesis Bolivia)

- **TAM**: 25.000-45.000 personas con amputación o limitación severa de movilidad en Bolivia (SIPRUNPCD + estimación post-censal).
- **Restricciones aplicadas para SAM**: geografía (eje Cochabamba/Santa Cruz/La Paz, ~60-65% de población con acceso a salud privada), capacidad de pago (~15-20% de población general, segmentos B y A), circunstancia clínica activa.
- **SAM**: 4.000-7.500 pacientes vivos en eje principal con capacidad de pago directa o financiable.
- **SAM en valor**: USD 9-19 M anuales (con gasto medio anual por paciente USD 1.800-2.800).
- **SOM bottom-up**: 80-150 Big Hire/año en fase 1 (capacidad de un técnico ortoprotesista por taller central por ciudad). En valor: USD 1,9-3,6 M/año en estado estable.
