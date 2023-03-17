import requests, json
import asyncio
from pyppeteer import launch
from websockets import client

base_url = 'BASE_URL.magister.net'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Magister login Pyppeteer
async def interceptResponse(request):
    if request.url == f"https://{base_url}/api/m6/applicatietoegang":
        global headers
        headers = request.headers
async def main():
    browser = await launch({"headless": True, "args": ["--start-maximized"]})
    page = await browser.newPage()
    #await page.setRequestInterception(True)

    await page.goto(f"https://{base_url}")
    # locate the search box
    entry_box = await page.waitForXPath("""//*[@id="username"]""")

    await entry_box.type(username)
    await asyncio.sleep(1)
    await page.click('button')
    entry_box = await page.waitForXPath("""//*[@id="password"]""")
    await entry_box.type(password)
    await asyncio.sleep(1)

    await page.click('#password_submit')
    page.on('request',
            lambda request: asyncio.ensure_future(interceptResponse(request)))
    await asyncio.sleep(1)
    await browser.close()
print("Logging in to Magister...")
asyncio.get_event_loop().run_until_complete(main())


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
        json.dump(req, f,indent=4)

    print("Downloading Rooster")
    r = requests.get(
        f"https://{base_url}/api/personen/{person_id}/afspraken?status=1&van={start}&tot={einde}",
        headers=headers).json()
    with open(f'Rooster_{start}-{einde}.json', 'w') as f:
        json.dump(r, f,indent=4)

    print("Downloading Absenties")
    r = requests.get(
        f"https://{base_url}/api/personen/{person_id}/absenties?status=1&van={start}&tot={einde}",
        headers=headers).json()
    with open(f'Absenties_{start}-{einde}.json', 'w') as f:
        json.dump(r, f, indent=4)

