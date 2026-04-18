import socket
import subprocess
import csv
import os

domains = [
    'google.com', 
    'yandex.ru', 
    'github.com', 
    'stackoverflow.com', 
    'wikipedia.org'
]

def resolve_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[DNS] {domain} -> {ip}")
        return ip
    except socket.gaierror:
        print(f"[DNS] Ошибка: Не удалось разрешить {domain}")
        return None

def run_traceroute(ip):
    print(f"[Traceroute] Начало для {ip}...")
    try:
        
        result = subprocess.run(
            ["traceroute", "-n", "-q", "1", ip], 
            capture_output=True, 
            text=True, 
            timeout=60
        )
        return result.stdout
    except Exception as e:
        return f"Ошибка при выполнении traceroute: {str(e)}"

def main():
    results = []
    
    for domain in domains:
        ip = resolve_dns(domain)
        if ip:
            route = run_traceroute(ip)
            results.append({
                'domain': domain,
                'ip': ip,
                'traceroute': route
            })
        else:
            results.append({
                'domain': domain,
                'ip': 'N/A',
                'traceroute': 'DNS Error'
            })


    output_file = "/home/cyberpsychoz/Computer_Networks/task_10/traceroute_results.csv"
    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['domain', 'ip', 'traceroute'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nГотово! Результаты сохранены в {output_file}")

if __name__ == "__main__":
    main()
