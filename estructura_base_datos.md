# Estructura de la Base de Datos - Módulo de Transacciones Energéticas P2P

## Tablas Clave (Se propone)

## communities
La comunidad energetica en donde esta inscrito el usuario (Con el fin de generar ofertas en un contexto cerrado)
- id
- name
- description
- location
- created_at

## community_members (pivote users–communities)
 Con quien podemos negociar
- id
- community_id (FK → communities)
- user_id (FK → users)
- role (prosumer | consumer | admin)
- pde_share (%)
- installed_capacity (kW)
- created_at

## energy_records (registro de energía)
 Registros cada 15 m x usuario
- id
- user_id (FK → users)
- community_id (FK → communities)
- energy_exported (kWh)
- energy_imported (kWh)
- period (mes/año o timestamp)

## pde_allocations (distribución de excedentes)
 CREG 101 072 2025 - Aca se almacena el PDE para el periodo con el fin de saber cuanto del porcentaje de distrib de excedentes le corresponde a cada usuario comunitario
- id
- community_id
- user_id
- allocated_energy (kWh)
- allocation_period
- created_at

## p2p_contracts (contratos bilaterales)
 Definer las reglas de negocio
- id
- seller_id (FK → users)
- buyer_id (FK → users)
- community_id
- agreed_price ($/kWh)
- energy_committed (kWh)
- contract_status (active, completed, cancelled)
- created_at

## transactions (ejecución de contratos)
 Recib energia, el precio almacenado desde dos dirreciónes (por eso el contract_id) con el fin de generar una logic fuerte 
 Para respaldo
- id
- contract_id (FK → p2p_contracts, nullable si es PDE directo)
- seller_id
- buyer_id
- energy_transacted (kWh)
- price ($/kWh)
- total_value ($)
- transaction_type (pde | p2p | settlement)
- transaction_date

## billing (liquidación mensual)
- id
- user_id
- community_id
- period
- imported_cost ($)
- exported_income ($)
- p2p_balance ($)
- final_bill ($)
- status (pending, paid, credited)
