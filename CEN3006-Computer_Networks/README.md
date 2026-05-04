# Wireless Network Simulation Analysis

This project follows the 14-step INET Framework tutorial to build and analyze a wireless network simulation using OMNeT++. The goal was to transition from a basic "perfect" connection to a realistic, high-fidelity environment involving mobile nodes, obstacles, and complex radio models.

## Key Features

- **Layered Stack:** Verified data flow from the application layer down to the physical WLAN interface.
- **Protocol Impact:** Analyzed how CSMA/CA and ACKs significantly improve reliability in shared wireless media.
- **Ad-Hoc Routing:** Implemented AODV to maintain connectivity dynamically as relay nodes move.
- **Environmental Realism:** Modeled signal interference (SINR), concrete obstacles, and antenna gain patterns.

## Core Takeaways

- **Theory vs. Reality:** Ideal radio models are great for logic testing but hide critical real-world issues like interference and path loss.
- **The Mobility Problem:** Static routing works fine until nodes move; dynamic protocols like AODV are essential for modern mobile ad-hoc networks (MANETs).
- **Physical Constraints:** Physical environments (walls, distance, noise) are often the biggest bottleneck for network performance.

## Tools Used

| Tool | Name |
|------|------|
| Simulator | OMNeT++ |
| Framework | INET |
| Analysis | AI-assisted log and scalar data interpretation |
