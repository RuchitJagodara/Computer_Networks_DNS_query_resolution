#!/usr/bin/python3
"""
DNS Benchmark Script - PCAP Edition
Usage: python3 benchmark.py <pcap_file.pcap>
"""
import sys
import subprocess
import time
import re
from scapy.all import rdpcap, DNS, DNSQR

def extract_domains_from_pcap(pcap_file):
    """Reads a pcap file and returns a unique set of DNS query domains."""
    domains = set()
    try:
        packets = rdpcap(pcap_file)
        
        # Filter for DNS Query packets
        for pkt in packets:
            if pkt.haslayer(DNS) and pkt.haslayer(DNSQR) and pkt[DNS].qr == 0:
                # pkt[DNS].qr == 0 means it's a query
                try:
                    # qname is like b'google.com.' - decode and strip trailing dot
                    domain = pkt[DNSQR].qname.decode('utf-8').rstrip('.')
                    domains.add(domain)
                except Exception as e:
                    print(f"Error decoding domain name: {e}", file=sys.stderr)
                    
    except FileNotFoundError:
        print(f"Error: File not found: {pcap_file}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading PCAP file {pcap_file}: {e}", file=sys.stderr)
        return []
        
    if not domains:
        print(f"No DNS queries found in {pcap_file}", file=sys.stderr)
        
    return list(domains)

def benchmark(urls):
    """Runs the dig benchmark on a list of URLs."""
    if not urls:
        print("Error: No URLs to benchmark.")
        return

    latencies = []
    success_count = 0
    fail_count = 0
    start_total_time = time.time()

    for url in urls:
        try:
            # Use 'dig' to query. The +time=2 sets a 2-second timeout.
            cmd = ['dig', '+short', '+time=2', url]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            # Parse 'dig' output for query time
            if proc.returncode == 0 and proc.stdout.strip():
                # We need to run again with +stats to get query time
                stat_cmd = ['dig', '+stats', '+time=2', url]
                stat_proc = subprocess.run(stat_cmd, capture_output=True, text=True, timeout=5)
                
                match = re.search(r'Query time: (\d+) msec', stat_proc.stdout)
                if match:
                    latency = int(match.group(1))
                    latencies.append(latency)
                    success_count += 1
                else:
                    fail_count += 1 # 'dig' worked but couldn't parse time
            else:
                fail_count += 1
                
        except Exception as e:
            # print(f"Error resolving {url}: {e}")
            fail_count += 1

    end_total_time = time.time()
    
    total_time = end_total_time - start_total_time
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    # Throughput as queries per second
    avg_throughput = (success_count + fail_count) / total_time if total_time > 0 else 0

    print("--- DNS Benchmark Results ---")
    print(f"Total Unique Queries: {len(urls)}")
    print(f"Successful:           {success_count}")
    print(f"Failed:               {fail_count}")
    print(f"Average Latency:      {avg_latency:.2f} ms")
    print(f"Average Throughput:   {avg_throughput:.2f} queries/sec")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <pcap_file.pcap>")
        sys.exit(1)
        
    pcap_file = sys.argv[1]
    print(f"Extracting domains from {pcap_file}...")
    domains_to_test = extract_domains_from_pcap(pcap_file)
    
    if domains_to_test:
        print(f"Found {len(domains_to_test)} unique domains. Starting benchmark...")
        benchmark(domains_to_test)
    else:
        print("Benchmark aborted.")