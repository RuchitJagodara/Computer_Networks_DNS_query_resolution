#!/usr/bin/python3
"""
CS331 Custom DNS Resolver - Starter Code
Author: [Your Name]
"""
import socket
import socketserver
import time
import datetime

# Real DNS server to forward queries to (e.g., Google's)
UPSTREAM_DNS_SERVER = "8.8.8.8"
UPSTREAM_DNS_PORT = 53

# --- For Bonus Part F: Caching ---
# A simple cache: {domain: (ip, ttl_expiration_time)}
DNS_CACHE = {}
# Set CACHE_ENABLED to True when you implement Part F
CACHE_ENABLED = False  

class DNSRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles incoming DNS queries.
    This server acts as a proxy/forwarder.
    """
    
    def parse_dns_query(self, data):
        """A simple DNS query parser to get the domain name."""
        try:
            # DNS queries have a 12-byte header
            # QNAME starts at byte 13 (index 12)
            header = data[:12]
            question = data[12:]
            
            # QNAME is null-terminated
            qname_end = question.find(b'\x00')
            qname_raw = question[:qname_end]
            
            # Convert QNAME from b'\x03www\x06google\x03com' to 'www.google.com'
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
        
        timestamp = datetime.datetime.now().isoformat()
        domain = self.parse_dns_query(data)
        
        if not domain:
            return # Ignore unparseable packet

        # --- THIS IS WHERE YOU ADD YOUR PART D LOGGING ---
        # You must add code here to log all the items (a-i)
        # to a file or to the console.
        print("--- New DNS Query Log (Starter) ---")
        print(f"a. Timestamp:         {timestamp}")
        print(f"b. Domain Name:       {domain}")

        cache_status = "MISS"
        
        # --- TODO: Bonus F: Caching Logic ---
        # if CACHE_ENABLED and domain in DNS_CACHE:
        #    ... (your caching code here) ...
        
        if cache_status != "HIT":
            print("i. Cache Status:      CACHE_MISS")
        
        # --- TODO: Bonus E: Recursion Logic ---
        # if recursive_mode:
        #    ... (your recursion code here) ...
        # else:
        
        print("c. Resolution Mode:   Forwarding (Iterative)")
        
        # Create a new socket to forward the query
        forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forward_sock.settimeout(2.0)
        
        try:
            start_fwd_time = time.time()
            
            forward_sock.sendto(data, (UPSTREAM_DNS_SERVER, UPSTREAM_DNS_PORT))
            print(f"d. DNS Server Contacted: {UPSTREAM_DNS_SERVER}")
            print("e. Step:              Forwarded to Upstream")
            
            # Get response from upstream
            response, _ = forward_sock.recvfrom(512)
            end_fwd_time = time.time()
            
            rtt = (end_fwd_time - start_fwd_time) * 1000 # in ms
            
            print(f"f. Response:          Response Received")
            print(f"g. RTT to Server:     {rtt:.2f} ms")
            print(f"h. Total Time:        {rtt:.2f} ms") # Same as RTT in this simple case
            
            # --- TODO: Bonus F: Add to Cache ---
            # if CACHE_ENABLED and cache_status != "HIT":
            #    ... (your cache-adding code here) ...

            # Send the response back to the original client
            sock.sendto(response, client_address)

        except socket.timeout:
            print("f. Response:          Forwarding Timed Out")
        except Exception as e:
            print(f"[Resolver] Error forwarding query: {e}")
        finally:
            forward_sock.close()
            print("------------------------\n")


if __name__ == "__main__":
    HOST, PORT = "10.0.0.5", 53 # Listen on the 'dns' host's IP
    print(f"Custom DNS Resolver starting on {HOST}:{PORT}...")
    
    # Listen on UDP
    try:
        with socketserver.UDPServer((HOST, PORT), DNSRequestHandler) as server:
            server.serve_forever()
    except Exception as e:
        print(f"!!! [Resolver] FAILED TO START: {e} !!!")
        print("!!! Did you forget to use 'sudo' to run the script? !!!")