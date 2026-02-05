import subprocess 
import pandas as pd
import re

domains = ['google.com', 'yandex.ru', 'github.com', 'stackoverflow.com', 
           'wikipedia.org', 'python.org', 'perplexity.ai', 'habr.com', 'vk.com', 'mail.ru']

def domain_ping(domain):
    command = ["ping", "-c", "1", domain]
    result = subprocess.run(command, capture_output=True, text= True, timeout= 5)
    output = result.stdout

    rtt_match = re.search(r'rtt min/avg/max/mdev = (\d+\.?\d*)/(\d+\.?\d*)/(\d+\.?\d*)/(\d+\.?\d*) ms', output)
    if rtt_match:
        min_rtt, avg_rtt, max_rtt, mdev_rtt = rtt_match.groups()
    else:
        min_rtt, avg_rtt, max_rtt, mdev_rtt = "N/A"

    packet_match = re.search(r'(\d)% packet loss', output)
    if packet_match:
        packet_loss = packet_match.group(1)
    else:
        packet_loss = "N/A"

    return {"domain" : domain, "min_rtt" : min_rtt, "avg_rtt": 
            avg_rtt, "max_rtt" : max_rtt, "mdev_rtt" : mdev_rtt, "packet_loss" : packet_loss}

def main():
    results = []  
    for domain in domains:
        res = domain_ping(domain)
        results.append(res)
    data = pd.DataFrame(results)  
    data.to_csv("result.csv", index=False)
    
main()
