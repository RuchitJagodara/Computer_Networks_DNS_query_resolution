#!/usr/bin/python3
"""
CS331 Assignment 2: Plotting Script
Reads 'dns_log.csv' and generates plots for Part D.
"""
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "dns_log.csv"
NUM_URLS_TO_PLOT = 10

def create_plots():
    print(f"Reading log data from '{LOG_FILE}'...")
    try:
        # Read the CSV log file
        df = pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        print(f"\n--- ERROR ---")
        print(f"Log file '{LOG_FILE}' not found.")
        print("Please run the benchmark first to generate the log:")
        print("1. sudo python3 dns_topo_custom.py")
        print("2. mininet> h1 python3 Benchmark.py PCAP_1_H1.pcap")
        print("3. mininet> exit")
        return
    except pd.errors.EmptyDataError:
        print(f"\n--- ERROR ---")
        print(f"Log file '{LOG_FILE}' is empty. Did the benchmark fail?")
        return
    except Exception as e:
        print(f"Error reading log file: {e}")
        return

    # --- Data Preparation ---
    # We only want to plot the first 10 URLs from PCAP_1_H1
    # We find the first 10 *unique* domains that were logged
    
    unique_domains = df['domain'].unique()
    if len(unique_domains) < NUM_URLS_TO_PLOT:
        print(f"Warning: Log file contains fewer than {NUM_URLS_TO_PLOT} unique domains.")
        domains_to_plot = unique_domains
    else:
        domains_to_plot = unique_domains[:NUM_URLS_TO_PLOT]

    # Filter the dataframe to only include the first logged entry for each of these 10 domains
    plot_data = df[df['domain'].isin(domains_to_plot)].drop_duplicates(subset='domain', keep='first')

    print(f"\nPlotting data for the first {len(plot_data)} unique domains...")
    
    # --- THIS IS THE CHANGE ---
    # We now print the *entire* plot_data DataFrame, not just a few columns.
    print(plot_data)

    # --- Plot 1: Latency per query ---
    # [This plot is required by cite: 50]
    plt.figure(figsize=(15, 7))
    plt.bar(plot_data['domain'], plot_data['total_time_ms'], color='skyblue')
    plt.xlabel('Domain Name')
    plt.ylabel('Total Resolution Latency (ms)')
    plt.title(f'DNS Latency for first {len(plot_data)} URLs (from PCAP_1_H1)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    latency_plot_file = 'plot_latency.png'
    plt.savefig(latency_plot_file)
    print(f"\nLatency plot saved to '{latency_plot_file}'")
    plt.close()

    # --- Plot 2: DNS Servers Visited ---
    # [This plot is required by cite: 50]
    plt.figure(figsize=(15, 7))
    plt.bar(plot_data['domain'], plot_data['servers_visited'], color='lightgreen')
    plt.xlabel('Domain Name')
    plt.ylabel('Total DNS Servers Visited')
    plt.title(f'DNS Servers Visited for first {len(plot_data)} URLs (from PCAP_1_H1)')
    # Set y-axis to be integers (e.g., 0, 1, 2)
    plt.yticks(range(0, int(plot_data['servers_visited'].max()) + 2))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    servers_plot_file = 'plot_servers_visited.png'
    plt.savefig(servers_plot_file)
    print(f"Servers visited plot saved to '{servers_plot_file}'")
    plt.close()

if __name__ == "__main__":
    create_plots()