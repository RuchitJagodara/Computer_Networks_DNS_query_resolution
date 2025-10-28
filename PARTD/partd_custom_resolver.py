#!/usr/bin/python3
"""
CS331 Custom DNS Resolver - Part D Solution
This version logs all required data to the console and 'dns_log.csv'.
"""
import socket
import socketserver
import time
import datetime
import os

# Real DNS server to forward queries to (e.g., Google's)
UPSTREAM_DNS_SERVER = "8.8.8.8"
UPSTREAM_DNS_PORT = 53
LOG_FILE = "dns_log.csv"

# --- For Bonus Part F: Caching ---
DNS_CACHE = {}
CACHE_ENABLED = False  # Set to False for Part D

# Clear the log file every time the resolver starts
try:
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    # Write the header for the CSV file
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,domain,mode,server_ip,step,response,rtt_ms,total_time_ms,cache_status,servers_visited\n")
except Exception as e:
    print(f"[Resolver] CRITICAL: Could not write to log file {LOG_FILE}: {e}")

class DNSRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles incoming DNS queries.
    This server acts as a proxy/forwarder.
    """
    
    def parse_dns_query(self, data):
        """A simple DNS query parser to get the domain name."""
        try:
            question = data[12:]
            qname_end = question.find(b'\x00')
            qname_raw = question[:qname_end]
            
            domain_parts = []
            i = 0
            while i < len(qname_raw):
                length = qname_raw[i]
                i += 1
                domain_parts.append(qname_raw[i : i + length].decode('utf-8'))
                i += length
            domain = ".".join(domain_parts)
            return domain
        except Exception as e:
            print(f"[Resolver] Error parsing domain: {e}")
            return None

    def handle(self):
        data, sock = self.request
        client_address = self.client_address
        
        # --- Part D Logging - Item (a) ---
        timestamp = datetime.datetime.now().isoformat()
        domain = self.parse_dns_query(data)
        
        if not domain:
            return

        # Initialize log variables
        log_mode = "Forwarding" #
        log_server_ip = "N/A" #
        log_step = "N/A" #
        log_response = "N/A" #
        log_rtt = 0 #
        log_total_time = 0 #
        log_cache_status = "MISS" #
        log_servers_visited = 0

        # --- Part D Logging (Console) ---
        print("\n--- New DNS Query ---")
        print(f"a. Timestamp:         {timestamp}")
        print(f"b. Domain Name:       {domain}")

        
        # --- Bonus F: Caching Logic ---
        # [This is where you would implement caching logic for Part F]
        # if CACHE_ENABLED and domain in DNS_CACHE:
        #    ...
        
        if not CACHE_ENABLED:
            log_cache_status = "MISS (Caching Disabled)"
        
        print(f"i. Cache Status:      {log_cache_status}")
        
        
        # --- Bonus E: Recursion Logic ---
        # [This is where you would implement recursion logic for Part E]
        # if recursive_mode:
        #    log_mode = "Recursive"
        #    ...
        # else:
        
        print(f"c. Resolution Mode:   {log_mode}")
        
        forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forward_sock.settimeout(2.0)
        
        try:
            start_fwd_time = time.time()
            
            log_server_ip = UPSTREAM_DNS_SERVER #
            log_step = "Forwarded to Upstream" #
            log_servers_visited = 1 # We only contact one server in this simple mode
            
            forward_sock.sendto(data, (UPSTREAM_DNS_SERVER, UPSTREAM_DNS_PORT))
            
            print(f"d. DNS Server Contacted: {log_server_ip}")
            print(f"e. Step of Resolution: {log_step}")
            
            # Get response from upstream
            response, _ = forward_sock.recvfrom(512)
            end_fwd_time = time.time()
            
            log_rtt = (end_fwd_time - start_fwd_time) * 1000 # in ms
            log_total_time = log_rtt # In a simple proxy, RTT is the total time
            log_response = "Response Received" #
            
            print(f"f. Response:          {log_response}")
            print(f"g. RTT to Server:     {log_rtt:.2f} ms")
            print(f"h. Total Time:        {log_total_time:.2f} ms")
            
            # --- TODO: Bonus F: Add to Cache ---

            # Send the response back to the original client
            sock.sendto(response, client_address)

        except socket.timeout:
            log_response = "Forwarding Timed Out"
            print(f"f. Response:          {log_response}")
        except Exception as e:
            log_response = f"Error: {e}"
            print(f"[Resolver] Error forwarding query: {e}")
        finally:
            forward_sock.close()
        
        # --- Log all data to CSV file ---
        try:
            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp},{domain},{log_mode},{log_server_ip},{log_step},"
                        f"{log_response},{log_rtt:.4f},{log_total_time:.4f},"
                        f"{log_cache_status},{log_servers_visited}\n")
        except Exception as e:
            print(f"[Resolver] FAILED to write to log file: {e}")


if __name__ == "__main__":
    HOST, PORT = "10.0.0.5", 53 # Listen on the 'dns' host's IP
    print(f"Custom DNS Resolver starting on {HOST}:{PORT}...")
    print(f"Logging data to {LOG_FILE}")
    
    try:
        with socketserver.UDPServer((HOST, PORT), DNSRequestHandler) as server:
            server.serve_forever()
    except Exception as e:
        print(f"!!! [Resolver] FAILED TO START: {e} !!!")
        print("!!! Did you forget to use 'sudo' to run the script? !!!")