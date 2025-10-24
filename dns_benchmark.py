#!/usr/bin/python3

"""
CS331 Assignment 2: DNS Benchmark Script
This script reads a PCAP file, extracts DNS queries, and benchmarks
their resolution time using the system's default resolver.
"""

import sys
import socket
import time
from scapy.all import rdpcap, DNS, DNSQR

def extract_domains_from_pcap(filename):
    """
    Reads a pcap file and returns a set of unique domain names
    from DNS query packets.
    """
    domains = set()
    try:
        packets = rdpcap(filename)
    except FileNotFoundError:
        print(f"Error: PCAP file '{filename}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading PCAP file: {e}", file=sys.stderr)
        return None

    # Iterate through all packets in the pcap
    for pkt in packets:
        # Check if it's a DNS packet, is a query (qr=0),
        # and has a question (qdcount > 0)
        if pkt.haslayer(DNS) and pkt[DNS].qr == 0 and pkt.haslayer(DNSQR):
            try:
                # Scapy stores qname as bytes, decode it
                domain = pkt[DNS].qd.qname.decode('utf-8').rstrip('.')
                domains.add(domain)
            except Exception as e:
                print(f"Error decoding domain name: {e}", file=sys.stderr)
                
    return list(domains)

def benchmark_dns(domains, pcap_filename):
    """
    Resolves a list of domain names and calculates performance metrics.
    """
    if not domains:
        print(f"Error: No valid DNS queries found in '{pcap_filename}'.")
        return

    print(f"--- Starting DNS Benchmark for {pcap_filename} ---")
    
    total_queries = len(domains)
    successful_count = 0
    failed_count = 0
    total_latency = 0.0
    total_script_start_time = time.perf_counter()

    for domain in domains:
        try:
            start_time = time.perf_counter()
            # Use the default system resolver to get the IP
            # This fulfills the "default host resolver" requirement 
            socket.gethostbyname(domain)
            end_time = time.perf_counter()
            
            latency = end_time - start_time
            total_latency += latency
            successful_count += 1
            print(f"  [SUCCESS] {domain:<30} -> {latency:.4f} s")
            
        except socket.gaierror:
            # This exception is raised on name resolution failures
            failed_count += 1
            print(f"  [FAILED]  {domain:<30}")
    
    total_script_end_time = time.perf_counter()
    total_time = total_script_end_time - total_script_start_time

    # Calculate final metrics 
    avg_latency = (total_latency / successful_count) if successful_count > 0 else 0
    avg_throughput = (total_queries / total_time) if total_time > 0 else 0

    print("\n--- Benchmark Results ---")
    print(f"Total unique queries:    {total_queries}")
    print(f"Successfully resolved:     {successful_count}")
    print(f"Failed resolutions:        {failed_count}")
    print(f"Average lookup latency:    {avg_latency:.4f} s")
    print(f"Average throughput:        {avg_throughput:.2f} queries/s")
    print("-------------------------\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <pcap_file>", file=sys.stderr)
    else:
        pcap_file = sys.argv[1]
        domain_list = extract_domains_from_pcap(pcap_file)
        if domain_list:
            benchmark_dns(domain_list, pcap_file)