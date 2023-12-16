import requests
import pandas as pd
import sys

baseurl = 'https://www.cvedetails.com/cve/'
file = sys.argv[1]


s = requests.Session()

def getVulnType(cve):
    response = s.get(f'{baseurl}{cve}').text
    response = response[response.find('Vulnerability Type(s)'):]
    response = response[response.find('<span'):]
    response = response[response.find('>') + 1:]
    response = response[:response.find('</')]
    return response.strip()

def getHeader(arr):
    for field in arr:
        if field.strip().upper() == 'CVE':
            return field
    return False

csv = pd.read_csv(file)
cve_dict = {}
vuln_types = []

header = getHeader(csv.head())
if header:
    cvelist = csv[header]
    uniq_cvelist = list(set(cvelist))
    total_count = len(cvelist)
    uniq_count = len(uniq_cvelist)
    print(f"[*] {total_count} CVEs found")
    print(f"[*] {uniq_count} unique CVEs found")
    for cve in cvelist:
        print(f'\r[*] {total_count} CVEs remaining....', end='')
        if cve not in cve_dict:
            cve_dict[cve] = getVulnType(cve)
        vuln_types.append(cve_dict[cve])
        total_count -= 1
    print()
    csv['Vulnerability Type'] = vuln_types
    out_file = f"{file.split('.')[0]}_output.csv"
    print(f'[*] Writing to {out_file}...', end=' ')
    csv.to_csv(out_file, index=False)
    print('[SUCCESS]')
else:
    print("[!] No field called 'CVE'")
