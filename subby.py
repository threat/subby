import requests
from bs4 import BeautifulSoup
import re
import subprocess
import json
import argparse
import datetime
import os

myssl_url = 'https://myssl.com/api/v1/discover_sub_domain?domain={domain}'
rapid_url = 'https://rapiddns.io/subdomain/{domain}?full=1'
hackertarget_url = 'https://api.hackertarget.com/hostsearch/?q={domain}'
anubis_url = 'https://jldc.me/anubis/subdomains/{domain}'
alienvault_url = 'https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list?limit=4000'

combined_domains_file = 'combined_domains.txt'
httpx_output_file = 'httpx_output.txt'
final_output_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f"_scan.txt"

def myssl_domains(domain):
    print (f"[OPERATION] Starting script for {domain}")
    response = requests.get(myssl_url.format(domain=domain))
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            return {entry['domain'] for entry in data['data']}
    return set()

def rapiddns_domains(domain):
    response = requests.get(rapid_url.format(domain=domain))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return {match.group() for td in soup.find_all('td')
                for match in re.finditer(r'\b[\w.-]+\.{}\.*\b'.format(re.escape(domain)), td.get_text())}
    return set()

def subfinder_domains(domain):
    try:
        result = subprocess.run(['subfinder', '-d', domain], capture_output=True, text=True, check=True)
        return set(result.stdout.splitlines())
    except subprocess.CalledProcessError:
        return set()

def hackertarget_domains(domain):
    response = requests.get(hackertarget_url.format(domain=domain))
    if response.status_code == 200:
        return {line.split(',')[0].strip() for line in response.text.splitlines() if line.endswith(f'.{domain}')}
    return set()

def anubis_domains(domain):
    url = anubis_url.format(domain=domain)
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return {match.group() for item in data
                    for match in re.finditer(r'\b[\w.-]*\.' + re.escape(domain) + r'\b', json.dumps(item))}
        except json.JSONDecodeError:
            return set()
    return set()

def alienvault_urls(domain):
    response = requests.get(alienvault_url.format(domain=domain))
    if response.status_code == 200:
        try:
            data = response.json()
            return {entry.get('url') for entry in data.get('url_list', []) if entry.get('url')}
        except json.JSONDecodeError:
            return set()
    return set()

def savedomains(domains, filename):
    with open(filename, 'w') as file:
        file.write('\n'.join(sorted(domains)))
    print("[OPERATION] Domains saved to file.")

def run_httpx():
    subprocess.run(['httpx', '-l', combined_domains_file, '-t', '400', '-o', final_output_file], check=True)
    print("[INFO] httpx Operation Completed.")

def cleanup():
    print("[OPERATION] Cleaning Files...")
    os.remove("combined_domains.txt")

    print("[INFO] Finished.")

def main():
    
    parser = argparse.ArgumentParser(description="Domain scanning tool.")
    parser.add_argument('-f', '--file', type=str, help="File containing list of domains.")
    parser.add_argument('-d', '--domain', type=str, help="Single domain to scan.")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as file:
            domains = set(line.strip() for line in file)
    elif args.domain:
        domains = {args.domain}
    else:
        print("Error: Either -f or -d must be provided.")
        return
    combined_domains = set()

    for domain in domains:
        combined_domains.update(myssl_domains(domain))
        print(f"[INFO] MySSL Operation Completed for {domain}.")

        combined_domains.update(rapiddns_domains(domain))
        print(f"[INFO] RapidDNS Operation Completed for {domain}.")

        combined_domains.update(subfinder_domains(domain))
        print(f"[INFO] Subfinder Operation Completed for {domain}.")

        combined_domains.update(hackertarget_domains(domain))
        print(f"[INFO] HackerTarget Operation Completed for {domain}.")

        combined_domains.update(anubis_domains(domain))
        print(f"[INFO] Anubis Operation Completed for {domain}.")

        combined_domains.update(alienvault_urls(domain))
        print(f"[INFO] AlienVault Operation Completed for {domain}.")

    savedomains(combined_domains, combined_domains_file)

    run_httpx()

    cleanup()

    print("[INFO] All operations complete and saved to file.")

if __name__ == "__main__":
    main()
