```markdown
# ENGINEERING SPECIFICATION: THERMAL-INTERLOCKS-V4
**System:** Kartarpur-0 Post-Scarcity Commune  
**Subsystem:** Subarctic Environmental & Thermal Management (SE&TM)  
**Document ID:** `infrastructure/specs/thermal-interlocks.md`  
**Classification:** Critical Life-Safety / Infrastructure Architecture  
**Status:** PRODUCTION READY  

---

## 1. Passive Fail-Open / Fail-Closed Hydronic Bypass Valves (-50°C Rated)

### 1.1 Operational Parameters
All hydronic loop bypass assemblies operating within exterior utility corridors or unconditioned sub-grade vaults must maintain structural and mechanical integrity down to an ambient extreme of $-50^\circ\text{C}$.

*   **Working Fluid:** 40/60 Propylene Glycol/Water mix (Freeze point: $-33^\circ\text{C}$; Burst point: $<-57^\circ\text{C}$).
*   **Operating Pressure:** PN25 (2.5 MPa / 362 PSI) nominal, proof tested to 3.8 MPa.
*   **Materials Specification:** 
    *   Body/Trim: 316L Electro-Polished Stainless Steel (preventing brittle martensitic transformation at sub-zero temps).
    *   Seals: PTFE / Viton-ETP hybrid low-temp elastomer rated to $-60^\circ\text{C}$.
    *   Fasteners: A4-80 Stainless Steel.

### 1.2 Fail-Mode Architecture
Valves are categorized into two explicit mechanical failure topologies based on life-safety zoning:

```
[Primary Loop] ---> [Wax-Motor / Spring Actuator] ---> [Valve Body]
                             |
                     (Power/Signal Loss)
                             |
              +--------------+--------------+
              |                             |
      [FAIL-CLOSED: Zone A]        [FAIL-OPEN: Zone B]
     (Prevents habitat flood)     (Prevents loop freeze-up)
```

1.  **Fail-Closed (Zone Isolation - Habitat Boundaries):**
    *   *Mechanism:* Dual-opposed Inconel-X750 compression springs acting directly on the valve stem, mechanically counter-weighted against a bi-metallic thermal expansion trigger.
    *   *Action:* Upon loss of control power or loop over-pressure/rupture detection, mechanical energy stored in the spring forces the plug to the fully seated position, isolating high-delta-T internal loops from sub-zero exterior mains.
2.  **Fail-Open (Emergency Core Heat Rejection Loop):**
    *   *Mechanism:* Normally-closed holding solenoid backed by a high-tension spring-return mechanical actuator pre-loaded with a memory-alloy (Nitinol) or wax-expansion thermal element.
    *   *Action:* Loss of electrical holding current or drop in upstream fluid temperature below $+2^\circ\text{C}$ forces the mechanical bypass valve open, ensuring continuous zero-resistance fluid migration through emergency thermal dumps (walipini greenhouses).

---

## 2. Air-Gapped Mechanical Thermal Fuses (Microcontroller-Independent)

To eliminate software-loop deadlocks, firmware lockups, or single-event upsets (SEU) from radiation/EM interference, all high-density compute loops feature hard-wired thermal fuses operating completely isolated from any silicon-based controller.

### 2.1 Direct Mechanical Thermal Interlock Specification
*   **Trigger Element:** Eutectic binary alloy link (Indium-Bismuth-Tin matrix) with a sharp, invariant phase change point at $+74^\circ\text{C}$ ($\pm 0.5^\circ\text{C}$).
*   **Actuation Mechanism:** 
    1. The eutectic link holds a loaded shear-pin lever assembly under 1,200 N of spring tension.
    2. Upon reaching $74^\circ\text{C}$, the alloy undergoes rapid liquefaction (viscosity breakdown).
    3. The shear pin shears cleanly, releasing a guillotine-style slide gate that physically severs the flexible corrugated stainless steel primary coolant line and diverts flow into a local passive phase-change thermal ballast.
*   **Electrical Interlock:** The physical movement of the guillotine blade trips a heavy-duty, normally-closed mechanical snap-action switch (UL/CSA rated) that cuts all DC contactor power to the local compute blade racks ($\ge 48\text{V DC}$ main bus), completely de-energizing the heat source before mechanical rupture occurs.
*   **Isolation Verification:** Zero wiring, zero buses (I2C, SPI, CAN), and zero logic gates exist between the eutectic sensor and the mechanical actuator. 

---

## 3. Subterranean Glycol Loop Isolation Zoning (150-Person Subarctic Node)

The Anandgarh node relies on a compartmentalized, hierarchical distribution topology to prevent catastrophic thermal drainage during a hull breach or primary line shear in permafrost conditions.

```
                  [Anandgarh Central Compute Hub]
                                |
             +------------------+------------------+
             | (Primary Main)                      | (Primary Main)
     [Zone 1: Habitat Core]              [Zone 2: Walipini Agri-Dome]
             |                                     |
     [Sub-Zone 1.1 - 1.4]                  [Sub-Zone 2.1 - 2.4]
    (Pneumatic Isolation)                 (Pneumatic Isolation)
```

### 3.1 Zoning Hierarchy & Compartmentalization
*   **Primary Mains:** Dual-redundant concentric piping (vacuum-insulated inner supply/return encased in a high-density polyethylene secondary containment jacket with continuous leak-detection fiber).
*   **Zonal Isolation Valves (ZIVs):** Installed at every structural bulkhead and thermal expansion joint. Spaced at maximum intervals of 25 meters.
*   **Actuation & Control:** ZIVs are pneumatically driven using compressed dry nitrogen stored in local accumulator tanks (independent of site electrical grid). In the event of a pressure drop exceeding $15\text{ kPa/sec}$ or a zone temperature drop below $-10^\circ\text{C}$, pneumatic dump valves vent line pressure, snapping all ZIVs shut within $400\text{ms}$.
*   **Drain-Down Subsystem:** Each isolated zone is rigged with a gravity-drain low-point collection sump equipped with an automated mechanical float valve, ensuring that isolated fluid drains safely into underground holding tanks rather than freezing in-situ and bursting distribution headers.

---

## 4. Redundant Thermal Sink Routing: Compute Nodes to Walipini Greenhouses

To achieve net-zero exergy waste, heat generated by the Anandgarh compute clusters must be continuously scavenged and routed to sub-grade, earth-sheltered walipini greenhouses for microclimate stabilization.

### 4.1 Hydraulic Circuitry & Heat Exchanger Topology
*   **Primary Loop (Compute):** High-temperature closed loop operating at $55^\circ\text{C}$ supply / $65^\circ\text{C}$ return, optimized for direct-to-chip liquid cooling blocks (Invar/Copper micro-channel cold plates).
*   **Secondary Loop (Agricultural):** Low-temperature circulating loop operating at $18^\circ\text{C}$ supply / $28^\circ\text{C}$ return, optimized for sub-soil PEX-a radiant heating grids buried 600mm below the walipini growing bed root zones.
*   **Intermediary Exchange:** Brazed Plate Heat Exchangers (BPHE) constructed of 316L stainless steel with copper braze, providing complete hydraulic isolation between compute dielectric/glycol loops and agricultural wash water/glycol loops.

### 4.2 Automated Fail-Safe Routing Matrix
To manage dynamic compute loads versus agricultural heating demands, the system utilizes a 3-way proportional thermostatic mixing valve driven by a wax-thermal capsule system backed by pneumatic overrides.

```
                 [Compute Exhaust: 65°C]
                            |
                     [BPHE Core Heat]
                            |
            +---------------+---------------+
            |                               |
     (Agri-Demand High)              (Agri-Demand Low / Dump)
            |                               |
    [Walipini Sub-Soil Grid]        [Borehole Thermal Energy Storage /
     (Radiant Floor Zones)           Permafrost Melt Prevention Loop]
```

1.  **Primary Routing (Normal Operation):** Compute waste heat is pumped directly through the BPHE into the walipini sub-soil radiant grid, maintaining root-zone temperatures at a constant $+21^\circ\text{C}$ despite outside ambient air temperatures of $-40^\circ\text{C}$.
2.  **Over-Capacity Dump (High Compute Load / Summer Mode):** When agricultural soil saturation limits are reached ($>26^\circ\text{C}$ root-zone temp), the thermostatic diversion valve automatically routes excess thermal energy away from the walipini and into:
    *   *Borehole Thermal Energy Storage (BTES):* Deep bedrock arrays for seasonal inter-phase thermal banking.
    *   *Permafrost Stabilization Loops:* Perimeter thermosyphons surrounding the foundation pilings to prevent thaw-settlement of structural foundations.
3.  **Deficit Heating Mode (Low Compute Load / Extreme Cold):** If compute output drops below agricultural thermal demand thresholds, geothermal heat pumps (ground-source heat pumps tied to the BTES array) automatically cycle on, blending low-grade earth heat with residual compute energy to maintain absolute baseline agricultural survival thresholds ($+15^\circ\text{C}$ ambient greenhouse dome floor).
