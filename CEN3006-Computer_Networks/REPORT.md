# Wireless Network Simulation

**INET Framework Wireless Tutorial**
**Course:** Computer Networks | **Date:** 05/05/2026

**Source:** https://inet.omnetpp.org/docs/tutorials/wireless/doc/index.html

---

## 1. Overview

This tutorial introduces wireless network simulation in OMNeT++ using the INET Framework. Starting with two hosts on an ideal radio link, each of 14 steps adds a new layer of realism: multi-hop topology, IPv4/static routing, SINR interference, CSMA, MAC ACKs, energy modelling, mobility, AODV routing, obstacles, dimensional radio, two-ray path loss, and antenna gain.

## 2. Simulation Scenario

A 4-node wireless chain in a 500×500m area:

| Node | Role | Description |
|------|------|-------------|
| hostA | Sender | UdpBasicApp, 1000B UDP every 1.2ms (~800 kbps) |
| R1, R2 | Relays | Forward packets; mobile from Step 9 |
| hostB | Receiver | UdpSink; counts received packets |

Configuration evolves across three dimensions:
- **IP & Routing:** None → Static IPv4 → AODV dynamic
- **MAC & Radio:** UnitDiskRadio + AckingMac → APSK + CSMA + ACKs
- **Physical Environment:** Free-space → Obstacles + Two-ray + Antenna gain

---

## 3. Step-by-Step Walkthrough

### Step 1 — Two Hosts Communicating Wirelessly

Minimum viable setup: two hosts, IdealMedium, UnitDiskRadio (500m range). Binary reception — 100% within range, 0% beyond. IPv4NetworkConfigurator assigns `10.0.0.1/24` and `10.0.0.2/24`.

| Category | Detail |
|----------|--------|
| Radio | UnitDiskRadio, 500m, binary |
| MAC | AckingMac |
| Delivery | 100% |

### Step 2 — Setting Up Animations

Added IntegratedCanvasVisualizer: data link arrows, physical link lines, radio wave circles. No networking changes — purely diagnostic.

### Step 3 — Adding More Nodes, Decreasing Range

Added R1 and R2. Range cut to 250m. hostA can't reach hostB directly. No routing layer exists, so R1 drops frames — **0 packets delivered**.

| Category | Detail |
|----------|--------|
| Topology | hostA → R1 → R2 → hostB |
| Range | 250m (hostA↔hostB = 400m, unreachable) |
| Delivery | 0% — no forwarding mechanism |

### Step 4 — Static Routing

IPv4NetworkConfigurator assigns IPs and installs shortest-path static routes. Multi-hop forwarding now works: hostA→R1→R2→hostB.

| Node | IP | Next Hop to hostB |
|------|----|--------------------|
| hostA | 10.0.0.1 | R1 (10.0.0.3) |
| R1 | 10.0.0.3 | R2 (10.0.0.4) |
| R2 | 10.0.0.4 | Direct |
| hostB | 10.0.0.2 | — |

**Result:** ~1,650 packets delivered. Multi-hop works.

### Step 5 — Taking Interference into Account

Replaced UnitDiskRadio with APSK radio + ScalarAnalogModel. Receiver now calculates SINR. Simultaneous transmissions cause interference and potential frame loss.

| Category | Detail |
|----------|--------|
| Radio | APSKScalarRadio, SINR-based reception |
| Path Loss | Free-space (Friis) |
| Delivery | < 100% (first realistic packet loss) |

### Step 6 — Using CSMA

Introduced CsmaCaMac: nodes sense the channel before transmitting. Random backoff on busy channel prevents most collisions. Delivery improves.

### Step 7 — Turning On ACKs

`mac.useAck = true`. Receiver sends ACK after each frame. Sender retransmits on timeout. Converts best-effort link to reliable Layer 2. Delivery near 100%, but ACK overhead roughly doubles transmissions (~3,255 TX for ~1,627 received).

### Step 8 — Modeling Energy Consumption

Added SimpleEpEnergyStorage + StateBasedEpEnergyConsumer. Tracks power per radio state (TX: 100mW, RX: 50mW, Idle: 10mW, Sleep: 1mW). No protocol changes.

### Step 9 — Node Mobility

R1/R2 given LinearMobility (12 m/s). As nodes move, links break. Static routes become stale — **delivery degrades sharply**. No route repair mechanism exists.

### Step 10 — AODV Ad-Hoc Routing

Replaced static routing with AODV. Route discovery via RREQ broadcast → RREP unicast. RERR on link break triggers re-discovery. Self-healing connectivity restored.

| Mechanism | Description |
|-----------|-------------|
| RREQ | Broadcast route request, flooded network-wide |
| RREP | Unicast reply back to source, installs routes |
| RERR | Invalidates broken routes, triggers re-discovery |
| Timeout | Routes expire after 3s if unused |

**Result:** ~1,636 packets delivered despite mobility.

### Step 11 — Adding Obstacles

PhysicalEnvironment with walls (XML). Signals attenuated by material thickness. Coverage becomes irregular. AODV works harder — more RREQs needed.

**Result:** ~829 packets (~50% drop from Step 10).

### Step 12 — Dimensional Radio Model

Upgraded to APSK radio with ScalarAnalogModel, background noise at -90dBm, BPSK modulation at 2GHz, sensitivity -85dBm, SINR threshold 4dB. Bit-level error model applied.

**Result:** ~307 packets (significant drop — many signals too weak).

### Step 13 — Two-Ray Ground Reflection Path Loss

Replaced free-space (d⁻²) with two-ray model (d⁻⁴ beyond crossover distance). Signal drops much faster with distance. Effective range shrinks.

| Parameter | Value |
|-----------|-------|
| Path Loss | TwoRayGroundReflection |
| Antenna Height | 1.5m |
| Crossover Distance | ~144m (beyond this: d⁻⁴) |

**Result:** ~420 packets (partial recovery due to constructive ground reflection at some distances).

### Step 14 — Antenna Gain

Replaced isotropic antenna with ConstantGainAntenna (3dB ≈ 2× power). Effective range doubled to ~500m. More stable AODV routes.

**Result:** ~879 packets (109% improvement over Step 13).

---

## 4. Results Summary

| Step | Feature | Delivery | Trend |
|------|---------|----------|-------|
| 1 | Basic wireless | 100% | Baseline |
| 2 | Visualizers | 100% | → |
| 3 | Multi-hop, no routing | 0% | ↓↓ |
| 4 | Static IPv4 routing | ~100% | ↑↑ |
| 5 | SINR interference | < 100% | ↓ |
| 6 | CSMA | Improved | ↑ |
| 7 | CSMA + ACKs | ~100% | ↑ |
| 8 | Energy model | Same | → |
| 9 | Node mobility | Degrades | ↓↓ |
| 10 | AODV routing | Recovers | ↑↑ |
| 11 | Obstacles | ~50% | ↓ |
| 12 | Realistic radio | ~19% | ↓ |
| 13 | Two-ray path loss | ~26% | ↑ |
| 14 | Antenna gain | ~54% | ↑ |

---

## 5. Key Takeaways

- **Routing:** Static routing breaks under mobility. AODV provides self-healing via RREQ/RREP/RERR.
- **MAC Layer:** CSMA prevents collisions; ACKs add reliability at the cost of doubled airtime.
- **Radio Models:** UnitDiskRadio is useful for testing logic but unrealistic. APSK + SINR reveals true wireless behavior. Dimensional models capture frequency-domain effects.
- **Physical Environment:** Obstacles, ground reflections, and antenna patterns determine real-world performance as much as protocol design.
- **Full-Stack Problem:** Wireless performance emerges from the interaction of physical propagation, MAC access control, routing, and application traffic.
