# Eclipse Attack Detection on Bitcoin via Community Detection

Research artifact for the paper:

> **Community Detection Algorithm for Mitigating Eclipse Attacks on Blockchain-enabled Metaverse.**
> *IEEE International Conference on Metaverse Computing, Networking and Applications (MetaCom)*, July 2023.
> [IEEE Xplore](https://ieeexplore.ieee.org/document/10271782)

---

## Overview

An **eclipse attack** is a network-level attack in which an adversary monopolizes all of a victim node's peer connections, isolating it from the honest Bitcoin network. Once eclipsed, the victim sees only a view of the blockchain controlled by the attacker, enabling double-spending, selfish-mining amplification, and consensus disruption.

This project proposes a **community-detection-based approach** for identifying eclipse attacks on the Bitcoin network. The workflow is:

1. **Simulate a Bitcoin network** under eclipse conditions, generating peer-connection topology data.
2. **Apply a community detection algorithm** (Louvain) to the resulting peer graph.
3. **Flag anomalous community structures** that correspond to an eclipsed victim — a node whose neighborhood forms a tightly clustered, isolated community dominated by adversarial peers.

The intuition is that an eclipsed node exhibits an unusual local graph structure distinct from honest nodes in the network. Community detection exposes that structure at scale.

## Approach

- **Network simulation** — a Bitcoin peer-to-peer network is simulated with both honest and malicious nodes. Malicious nodes attempt to eclipse target victims by saturating their connection slots.
- **Graph construction** — the peer-connection graph is built from the simulation output.
- **Community detection** — the [Louvain algorithm](https://en.wikipedia.org/wiki/Louvain_method) is applied to the graph to identify community structure based on modularity optimization.
- **Eclipse detection** — nodes belonging to small, dense, adversary-dominated communities are flagged as candidates for being eclipsed.

## Repository Structure

```
Eclipse_Attack_Detection/
├── btc-network-master/      # Simulated Bitcoin network (code + configs)
├── samples/                 # Example input data and test scenarios
├── results/                 # Output figures and detection results
├── graph-tool/              # Graph-tool submodule dependency
├── my_networkx.py           # NetworkX helpers for graph construction
├── test5.py                 # Main Eclipse attack detection script
├── file.json                # Configuration / input data
├── .gitmodules              # Git submodule configuration
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.x
- [NetworkX](https://networkx.org/)
- [python-louvain](https://github.com/taynaud/python-louvain) (community detection)
- Standard scientific Python stack (NumPy, Pandas, Matplotlib)

Install dependencies:

```bash
pip install networkx python-louvain numpy pandas matplotlib
```

### Running the detection

1. Clone the repository with submodules:

   ```bash
   git clone --recurse-submodules https://github.com/erfan38/Eclipse_Attack_Detection.git
   cd Eclipse_Attack_Detection
   ```

2. Prepare or generate the simulated network data in `btc-network-master/`.

3. Run the detection script:

   ```bash
   python test5.py
   ```

4. Results and figures are written to the `results/` folder.

## Related Work

This paper is part of a broader research program on **blockchain attack detection and mitigation**:

- **Selfish mining detection (ML-based)** — *Efficient Detection of Selfish Mining Attacks on Large-Scale Blockchain Networks*, IEEE QRS, 2024.
- **Selfish mining mitigation (game-theoretic)**
- **Retaliation Game for Mitigating Selfish Mining Attacks in Blockchain Networks**, Springer GameNet, 2025.
- **Sybil attack defense** — *Sybil Attack Defense in Blockchain-based Industrial IoT Systems using Decentralized Federated Learning*, *Internet of Things*, Elsevier, 2026.
- **Smart contract vulnerability detection (LLM-based)**
- **Fine-Tuned Large Language Model and Comprehensive Dataset for Securing Ethereum Smart Contracts**, *Blockchain: Research and Applications*, Elsevier, 2026.

Together, these works cover detection, mitigation, and prevention across major classes of blockchain attacks.

## Citation

If you use this code or approach in your research, please cite:

```
Erfan, F. et al. Community Detection Algorithm for Mitigating Eclipse Attacks
on Blockchain-enabled Metaverse. In IEEE International Conference on Metaverse
Computing, Networking and Applications (MetaCom), July 2023.
```

## Acknowledgments

This project uses the [`leidenalg`]([https://github.com/vtraag/leidenalg.git)) library for community detection. We gratefully acknowledge this open-source contribution.

## Contact

Fatemeh Erfan — fatemeh.erfan@polymtl.ca
Postdoctoral Fellow, Polytechnique Montréal
