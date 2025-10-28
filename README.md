# S331: Computer Networks Assignment 2 – DNS Query Resolution

## Team Details
> **Team Members:**
> - Ruchit Jagodara (Roll No. 22110102)
> - Chiragkumar Patel (Roll No. 22110183)

## Repository Structure

```
create_topology.py
PARTA/
     dns_topo.py
PARTB/
     Benchmark.py
     dns_topo.py
PARTC/
     custom_resolver.py
     dns_topo_custom.py
PARTD/
     Benchmark.py
     dns_log.csv
     partd_custom_resolver.py
     partd_dns_topo_custom.py
     plot_logs.py
```

## Prerequisites
- Python 3.x
- Mininet
- Scapy
- Matplotlib
- Pandas

Install Python dependencies:
```bash
pip install scapy matplotlib pandas
```

---

## Step-by-Step Instructions to Regenerate Results

### **A. Simulate the Topology in Mininet**
1. **Run the topology script:**
    ```bash
    sudo python3 create_topology.py
    ```
    - This will launch Mininet with the required topology (5 hosts, 4 switches, NAT, and links with specified bandwidth/delay).
2. **Test connectivity:**
    - In the Mininet CLI, run:
      ```
      mininet> pingall
      ```
    - All hosts should be able to reach each other.
3. **Exit Mininet CLI:**
    - Type `exit` to stop the simulation.

### **B. DNS Benchmarking with Default Resolver**
1. **For each host, extract domains from the provided PCAP file and benchmark DNS resolution:**
    - Example for host h1:
      ```bash
      python3 PARTB/Benchmark.py PCAP_1_H1.pcap
      ```
    - Repeat for other hosts/PCAPs as needed.
2. **Record the following for each host:**
    - Average lookup latency
    - Average throughput
    - Number of successfully resolved queries
    - Number of failed resolutions

### **C. Use Custom DNS Resolver in Mininet**
1. **Modify DNS configuration:**
    - Use the topology script in `PARTC/dns_topo_custom.py` to set all hosts' `/etc/resolv.conf` to use your custom resolver (10.0.0.5).
2. **Start the custom resolver:**
    - In a separate terminal, run:
      ```bash
      sudo python3 PARTC/custom_resolver.py
      ```
    - Ensure the resolver is running on host `dns` (10.0.0.5).
3. **Demonstrate the configuration:**
    - Show the contents of `/etc/resolv.conf` on each host:
      ```bash
      mininet> h1 cat /etc/resolv.conf
      ```
    - Take screenshots for your report.

### **D. DNS Resolution with Custom Resolver & Logging**
1. **Use the Part D topology and resolver:**
    - Start Mininet with:
      ```bash
      sudo python3 PARTD/partd_dns_topo_custom.py
      ```
    - This will automatically start the enhanced resolver on 10.0.0.5.
2. **Benchmark DNS resolution:**
    - In the Mininet CLI, run:
      ```bash
      h1 python3 Benchmark.py PCAP_1_H1.pcap
      ```
    - Repeat for other hosts/PCAPs as needed.
3. **Logging:**
    - The resolver logs all required details (timestamp, domain, mode, server IP, step, response, RTT, total time, cache status, servers visited) to `PARTD/dns_log.csv`.
4. **Generate plots for PCAP_1_H1:**
    - After running the benchmark, generate plots:
      ```bash
      python3 PARTD/plot_logs.py
      ```
    - This will create `plot_latency.png` and `plot_servers_visited.png` for the first 10 unique URLs.

---

## Outputs
- **Benchmark Results:** Metrics such as average latency and throughput (Parts B & D).
- **Logs:** Detailed logs of DNS queries in `PARTD/dns_log.csv` (Part D).
- **Plots:** Visualizations of latency and servers visited (`plot_latency.png`, `plot_servers_visited.png`).

## Authors
- Ruchit Jagodara and Chiragkumar Patel

## License
This project is licensed under the MIT License.