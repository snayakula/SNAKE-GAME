import sys
import pandas as pd
import json

# Usage: python convert_trivy_json_to_excel.py <input_json> <output_excel>
input_json = sys.argv[1]
output_excel = sys.argv[2]

def flatten_vulns(data):
    vulns = []
    for result in data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            vulns.append({
                'Target': result.get('Target'),
                'Type': result.get('Type'),
                'VulnerabilityID': vuln.get('VulnerabilityID'),
                'PkgName': vuln.get('PkgName'),
                'InstalledVersion': vuln.get('InstalledVersion'),
                'Severity': vuln.get('Severity'),
                'Title': vuln.get('Title'),
                'Description': vuln.get('Description'),
                'PrimaryURL': vuln.get('PrimaryURL'),
            })
    return vulns

def flatten_secrets(data):
    secrets = []
    for result in data.get('Results', []):
        for secret in result.get('Secrets', []):
            secrets.append({
                'Target': result.get('Target'),
                'Type': result.get('Type'),
                'RuleID': secret.get('RuleID'),
                'Severity': secret.get('Severity'),
                'Title': secret.get('Title'),
                'Match': secret.get('Match'),
            })
    return secrets

def flatten_config(data):
    configs = []
    for result in data.get('Results', []):
        for misconfig in result.get('Misconfigurations', []):
            configs.append({
                'Target': result.get('Target'),
                'Type': result.get('Type'),
                'ID': misconfig.get('ID'),
                'Severity': misconfig.get('Severity'),
                'Title': misconfig.get('Title'),
                'Description': misconfig.get('Description'),
            })
    return configs

with open(input_json, 'r') as f:
    data = json.load(f)

if 'vuln' in output_excel:
    df = pd.DataFrame(flatten_vulns(data))
elif 'secret' in output_excel:
    df = pd.DataFrame(flatten_secrets(data))
else:
    df = pd.DataFrame(flatten_config(data))

df.to_excel(output_excel, index=False)
