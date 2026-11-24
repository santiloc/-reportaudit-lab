# Laboratorio 1 — Bitácora de auditoría de la cadena de suministro

- **Autor/a:** ESCRIBE_AQUÍ_TU_NOMBRE_Y_APELLIDOS
- **Repositorio:** https://github.com/TU-USUARIO/reportaudit-lab
- **Sistema operativo y versión de Python usados:**

> Completa cada sección en el momento en que la guía te lo pide, no al final.
> Una bitácora escrita "de memoria" al terminar no sirve como evidencia.

---

## Parte B — Auditoría manual (antes de usar ninguna herramienta)

| # | Función | Línea | Qué sospechas | Dato de entrada (*source*) | Destino peligroso (*sink*) |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

**Impacto en el negocio:** para cada sospecha, explica en una frase qué
consecuencia tendría para ReportAudit y sus clientes si fuera real (qué datos,
qué sistema o qué credencial quedarían expuestos).

---

## Matriz de detección (se completa a lo largo del laboratorio)

Marca ✓ (lo detectó, anota la regla) o ✗ (no lo detectó) en cada columna cuando
llegues a la parte correspondiente.

| Hallazgo | Manual (B) | SonarQube for IDE sin conexión (D) | SonarQube for IDE en Connected Mode (E) | SonarQube Cloud (F) | CodeQL (F) | Semgrep (G) | Trivy (K) |
|---|---|---|---|---|---|---|---|
| H1 Inyección SQL en `buscar_reportes_cliente` |  |  |  |  |  |  | n/a |
| H2 Inyección de comandos en `convertir_a_pdf` |  |  |  |  |  |  | n/a |
| H3 Deserialización YAML insegura en `cargar_configuracion` |  |  |  |  |  |  | n/a |
| H4 Hash MD5 en `hash_password_legacy` |  |  |  |  |  |  | n/a |
| H5 Clave de API escrita en el código |  |  |  |  |  |  |  |
| H6 Contraseña SMTP escrita en el código |  |  |  |  |  |  |  |

**Conclusión de la matriz** (Parte K): ¿alguna herramienta lo detectó todo? ¿Qué
te dice eso sobre depender de una sola herramienta?

---

## Parte J — SBOM: el iceberg medido

| Dato | Valor |
|---|---|
| Dependencias directas (`requirements.in`) |  |
| Componentes Python en el SBOM |  |
| Otros componentes que aparezcan en el SBOM (si los hay) y de dónde salen |  |
| Formato y versión de especificación del SBOM (`bomFormat`, `specVersion`) |  |

---

## Parte J — Triage de vulnerabilidades de dependencias (Grype)

| Paquete | Versión | ¿Directa o transitiva? (usa `# via`) | CVE / GHSA | Severidad | Corregida en | ¿Explotable en ReportAudit? ¿Por qué? | Decisión |
|---|---|---|---|---|---|---|---|
| `werkzeug` | 3.0.1 | Transitiva (`# via flask`) | GHSA-2g68-c3qc-8985 | High | 3.0.3 | **Sí/Posible.** Es una vulnerabilidad de DoS al procesar peticiones web. Flask usa Werkzeug para recibir el tráfico. | Actualizar con el PR de Dependabot. |
| `jinja2` | 3.1.2 | Transitiva (`# via flask`) | GHSA-h75v-3vvj-5mfj | Medium | 3.1.4 | **No.** Afecta al motor de plantillas HTML. ReportAudit es una API que devuelve JSON, no renderiza plantillas. | Actualizar y documentar con VEX. |
| `flask` | 3.0.0 | Directa (`requirements.in`) | GHSA-68rp-wp8r-4726 | Low | 3.1.3 | **Poco probable.** Es de severidad baja, pero al ser el núcleo de la API web conviene mantenerla limpia. | Actualizar con el PR de Dependabot. |
| `pip` | 24.0 | Transitiva (Entorno) | GHSA-wf93-45jw-7689 | Medium | 26.1.2 | **No.** Pip solo instala cosas en el entorno virtual, no forma parte del código que corre en producción. | Ignorar / Riesgo aceptado. |

**Comparación con Dependabot** (Parte H): ¿las alertas coinciden con Grype? Explica
cualquier diferencia.

**Documento VEX:** copia `plantillas/reportaudit.openvex.json` a
`docs/evidencias/`, rellénalo, enlázalo aquí y resume en una frase la
justificación.

---

## Parte L y M — Antes y después

| Medida | Antes | Después |
|---|---|---|
| Hallazgos de Semgrep en `app/` |  |  |
| Alertas abiertas de CodeQL (Security → Code scanning) |  |  |
| Vulnerabilidades en SonarQube Cloud (rama main) |  |  |
| Security Hotspots por revisar en SonarQube Cloud |  |  |
| Vulnerabilidades de Grype sobre el SBOM |  |  |
| Alertas abiertas de Dependabot |  |  |

---

## Preguntas de comprobación (Sección 7 de la guía)

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
12.

## Backlog del laboratorio (Issues)

| Issue | Título | PR o evidencia de cierre |
|---|---|---|
| #1 | Adopt an international pull request template | |
| #2 | Run SAST (SonarQube Cloud and CodeQL) on every pull request | |
| #3 | Block insecure commits with a Semgrep pre-commit hook | |
| #4 | Enable Dependabot alerts and security updates | |
| #5 | Remediate the findings of the security audit | |
| #6 | Upgrade the vulnerable dependencies | |
| #7 | Publish the audit log and the before/after evidence | |
| #8 | Detect ReportAudit credentials in the whole Git history | |
| #9 | Make SCA and secret scanning required checks on main | |
| #10 | Publish a security policy and a private vulnerability reporting channel | |
| #11 | Release v1.0.0 with an SBOM and signed provenance | |
