import requests, json

base_url = 'NAME_HERE.magister.net'

headers = {'Authorization':'Bearer TOKEN_HERE'}

r = requests.get(f"https://{base_url}/api/sessions/current", headers=headers)
account_href = r.json()['links']['account']['href']

r = requests.get(f"https://{base_url}{account_href}", headers=headers)
leerling_href = r.json()['links']['leerling']['href']

r = requests.get(f"https://{base_url}{leerling_href}", headers=headers)

print(f"Naam: {r.json()['roepnaam']} {r.json()['achternaam']}")
print(f"Stamnummer: {r.json()['stamnummer']}\nID:{r.json()['id']}")
print(f"Rollen: {r.json()['rollenVanGebruiker']}")


person_id = r.json()['id']

r = requests.get(f"https://{base_url}/api/personen/{person_id}/aanmeldingen", headers=headers)

data = r.json()
#print(data)
first_year = False
for item in data['Items']:

    url = f"https://{base_url}/api/aanmeldingen/{item['Id']}"
    year_data = requests.get(url, headers=headers).json()
    einde = year_data['einde']
    start = year_data['begin']
    url = f"https://{base_url}/api/personen/{person_id}/aanmeldingen/{item['Id']}/cijfers/cijferoverzichtvooraanmelding?actievePerioden=true&alleenBerekendeKolommen=false&alleenPTAKolommen=false&peildatum={einde}"
    print(url)

    print("Downlading cijferlijst")
    req = requests.get(url, headers=headers).json()
    with open(f'Cijfers_{start}-{einde}.json', 'w') as f:
        json.dump(req, f)

    print("Downloading Rooster")
    r = requests.get(
        f"https://{base_url}/api/personen/{person_id}/afspraken?status=1&van={start}&tot={einde}",
        headers=headers).json()
    with open(f'Rooster_{start}-{einde}.json', 'w') as f:
        json.dump(r, f)

    print("Downloading Absenties")
    r = requests.get(
        f"https://{base_url}/api/personen/{person_id}/absenties?status=1&van={start}&tot={einde}",
        headers=headers).json()
    with open(f'Absenties_{start}-{einde}.json', 'w') as f:
        json.dump(r, f)

