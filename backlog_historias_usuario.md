# Backlog - Módulo de Transacciones Energéticas P2P

## Épica 1: Gestión de Datos Energéticos
Objetivo: Permitir el registro, consulta y balance de datos energéticos dentro de la comunidad.

### HU01 – Registro de datos de energía
**Descripción:** Como **prosumer**, quiero **registrar la energía importada y exportada**, para que el sistema pueda calcular mis excedentes.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] El sistema debe permitir registrar datos de energía importada y exportada.  
- [ ] Los datos deben asociarse al usuario y a la comunidad correspondiente.  
- [ ] Los registros deben guardarse con marca de tiempo válida (ej. cada 15 minutos).  
- [ ] Si los datos no cumplen validación, el sistema debe rechazarlos.  

**Checklist Técnico:**  
- [ ] Tabla `energy_records` implementada.  
- [ ] Endpoints de registro y consulta definidos.  
- [ ] Validaciones de integridad aplicadas (no valores negativos).  

**Checklist de Usuario (UAT):**  
- [ ] El prosumer puede ingresar datos desde la interfaz.  
- [ ] Puede consultar sus registros históricos.  
- [ ] Los errores y confirmaciones son claros.  


### HU02 – Asignación de PDE
**Descripción:** Como **administrador de comunidad**, quiero **asignar porcentajes de distribución de excedentes (PDE) a cada miembro**, para que los beneficios se repartan conforme al acuerdo comunitario.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] El sistema debe permitir asignar PDE a cada usuario.  
- [ ] El total de PDE asignado debe sumar 100%.  
- [ ] El PDE debe poder cambiarse mensualmente.  

**Checklist Técnico:**  
- [ ] Tabla `pde_allocations` implementada.  
- [ ] Validación de suma total = 100%.  
- [ ] Control de versiones por periodo.  

**Checklist de Usuario (UAT):**  
- [ ] El administrador puede modificar PDE.  
- [ ] Los usuarios pueden consultar su PDE asignado.  
- [ ] Se reflejan cambios en la facturación.  


### HU03 – Consulta de balance energético
**Descripción:** Como **miembro de comunidad**, quiero **consultar mi balance de energía (importada, exportada, asignada vía PDE)**, para entender mi posición neta en la comunidad.  
**Prioridad:** Media  

**Criterios de Aceptación:**  
- [ ] El sistema muestra balance importación/exportación/PDE.  
- [ ] El balance debe calcularse por periodo (mes).  

**Checklist Técnico:**  
- [ ] Query balance implementado.  
- [ ] Datos integrados con `energy_records` y `pde_allocations`.  

**Checklist de Usuario (UAT):**  
- [ ] El usuario visualiza su balance en la interfaz.  
- [ ] Puede descargar o exportar el reporte.  


## Épica 2: Contratos P2P
Objetivo: Habilitar transacciones bilaterales entre prosumers y consumidores.

### HU04 – Creación de contrato P2P
**Descripción:** Como **prosumer**, quiero **ofrecer parte de mis excedentes a un consumidor mediante un contrato bilateral**, para obtener mejor remuneración.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] El sistema debe permitir crear contratos bilaterales.  
- [ ] Se deben registrar precio, energía y duración.  

**Checklist Técnico:**  
- [ ] Tabla `p2p_contracts` implementada.  
- [ ] Validaciones de campos obligatorios.  

**Checklist de Usuario (UAT):**  
- [ ] El prosumer puede crear una oferta P2P.  
- [ ] Recibe confirmación de creación.  


### HU05 – Negociación de contrato P2P
**Descripción:** Como **consumidor**, quiero **aceptar o rechazar una oferta de contrato P2P**, para acceder a energía más barata que la tarifa regulada.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] El consumidor puede aceptar o rechazar la oferta.  
- [ ] El estado del contrato cambia según la acción.  

**Checklist Técnico:**  
- [ ] Actualización de `p2p_contracts.contract_status`.  
- [ ] Validación de usuario autorizado.  

**Checklist de Usuario (UAT):**  
- [ ] El consumidor visualiza las ofertas disponibles.  
- [ ] Puede aceptar/rechazar fácilmente.  


### HU06 – Liquidación de transacciones
**Descripción:** Como **sistema**, quiero **liquidar las transacciones P2P y PDE al final de cada periodo**, para generar facturas claras a cada miembro.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] El sistema liquida contratos P2P y PDE.  
- [ ] La liquidación se guarda en `transactions`.  

**Checklist Técnico:**  
- [ ] Lógica de liquidación implementada.  
- [ ] Integración con facturación.  

**Checklist de Usuario (UAT):**  
- [ ] Los miembros ven su resumen mensual.  
- [ ] Se distinguen transacciones P2P y PDE.  


## Épica 3: Facturación y Reportes
Objetivo: Consolidar la información en facturas y reportes.

### HU07 – Facturación mensual
**Descripción:** Como **miembro de comunidad**, quiero **recibir mi factura consolidada (importación, compensación, P2P, PDE)**, para conocer mi costo o ingreso final.  
**Prioridad:** Alta  

**Criterios de Aceptación:**  
- [ ] Factura mensualmente.  
- [ ] Incluye importación, exportación, PDE, P2P.  

**Checklist Técnico:**  
- [ ] Tabla `billing` implementada.  
- [ ] Servicio de generación de facturas.  

**Checklist de Usuario (UAT):**  
- [ ] El usuario recibe su factura completa.  
- [ ] Puede descargarla en PDF/Excel.  


### HU08 – Historial de transacciones
**Descripción:** Como **miembro**, quiero **acceder a mi historial de transacciones energéticas y económicas**, para tener trazabilidad y transparencia.  
**Prioridad:** Media  

**Criterios de Aceptación:**  
- [ ] El usuario puede ver todas sus transacciones pasadas.  
- [ ] Filtrado por periodo y tipo.  

**Checklist Técnico:**  
- [ ] Endpoint de consulta histórica.  
- [ ] Integración con `transactions`.  

**Checklist de Usuario (UAT):**  
- [ ] El usuario visualiza historial completo.  
- [ ] Puede exportar registros.  


### HU09 – Reportes comunitarios
**Descripción:** Como **administrador**, quiero **ver reportes agregados de la comunidad (generación, consumo, transacciones, ahorros)**, para evaluar la eficiencia del modelo.  
**Prioridad:** Media  

**Criterios de Aceptación:**  
- [ ] Reporte comunitario con métricas clave.  
- [ ] Datos agregados por periodo.  

**Checklist Técnico:**  
- [ ] Servicio de generación de reportes.  
- [ ] Dashboard comunitario.  

**Checklist de Usuario (UAT):**  
- [ ] El administrador accede a reportes gráficos.  
- [ ] Puede exportar los resultados.
