from app import db
from app.models import user, vegobjekttype, egenskapstype, vegkategori, vegsystem, fylke, område, kvalitetsnivå_1, kvalitetsnivå_2, kvalitetsparameter, skala
import requests
from sqlalchemy import select
import tqdm

def add_base_data():
    """
    Add base data to the database.
    """
    with db.session.begin():
        # Add vegobjekttype
        if not vegobjekttype.query.first():
            print("Filling up vegobjekttype")
            t = requests.get("https://nvdbapiles.atlas.vegvesen.no/datakatalog/api/v1/vegobjekttyper", params={"inkluder": "minimum"})
            if t.status_code == 200:
                t = t.json()
                vegobjekttyper = [vegobjekttype(id=type['id'], navn=type['navn'], hovedkategori=type['hovedkategori']) for type in t]
            db.session.add_all(vegobjekttyper)

        # Add egenskapstype
        if not egenskapstype.query.first():
            print("Filling in egenskapstype")
            t = requests.get("https://nvdbapiles.atlas.vegvesen.no/datakatalog/api/v1/vegobjekttyper", params={"inkluder": "egenskapstyper"})
            if t.status_code == 200:
                t = t.json()
                egenskapstyper = []
                for type in t:
                    for egenskap in type.get('egenskapstyper', []):
                        if egenskap['id'] < 200000:
                            egenskapstyper.append(egenskapstype(id=egenskap['id'], navn=egenskap['navn'], vegobjekttype_id=type['id'], datatype=egenskap['egenskapstype'], viktighet=egenskap.get('viktighet', 'IKKE_ANGITT')))
            db.session.add_all(egenskapstyper)

        # Add fylke
        if not fylke.query.first():
            print("Filling in fylke")
            t = requests.get("https://nvdbapiles.atlas.vegvesen.no/uberiket/api/v1/vegobjekter/945", params={"inkluder": "egenskaper"})
            if t.status_code == 200:
                t = t.json()
                fylker = [fylke(id=f['egenskaper']['11764']['verdi'], navn=f['egenskaper']['11765']['verdi']) for f in t.get('vegobjekter', [])]
            db.session.add_all(fylker)

        #add vegkategori
        if not vegkategori.query.first():
            print("Filling in vegkategori")
            vegkategorier = [
                vegkategori(id=1, navn="Europaveg", kortnavn="E"),
                vegkategori(id=2, navn="Riksveg", kortnavn="R"),
                vegkategori(id=3, navn="Fylkesveg", kortnavn="F"),
                vegkategori(id=4, navn="Kommuneveg", kortnavn="K"),
                vegkategori(id=5, navn="Privat veg", kortnavn="P"),
                vegkategori(id=6, navn="Skogsveg", kortnavn="S")
            ]
            db.session.add_all(vegkategorier)

        # Add vegsystem
        if not vegsystem.query.first():
            print("Filling in vegsystem")
            print("Europaveg")
            ekskluder_vegnummer = "AND11277!=null"
            vegnummer_liste = []
            t = requests.get(f"https://nvdbapiles.atlas.vegvesen.no/vegobjekter/api/v4/vegobjekter/915?egenskap=11276=19024AND11278=19032{ekskluder_vegnummer}&inkluder=egenskaper&inkluder_egenskaper=basis&antall=1")
            if t.status_code == 200:
                t = t.json()
                antall = t['metadata']['returnert']
                while antall > 0:
                    vegnummer = next((i['verdi'] for i in t['objekter'][0]['egenskaper'] if i['id'] == 11277), None)
                    vegnummer_liste.append(vegnummer)
                    ekskluder_vegnummer += f"AND11277!={vegnummer}"
                    t = requests.get(f"https://nvdbapiles.atlas.vegvesen.no/vegobjekter/api/v4/vegobjekter/915?egenskap=11276=19024AND11278=19032{ekskluder_vegnummer}&inkluder=egenskaper&inkluder_egenskaper=basis&antall=1")
                    if t.status_code == 200:
                        t = t.json()
                        antall = t['metadata']['returnert']
                    else:
                        print(t.text)
                        break
            vegnummer_liste = sorted(vegnummer_liste)
            e_vegsystemer = [
                vegsystem(vegnummer=nr, vegkategori_id=1, vegfase="V") for nr in vegnummer_liste
            ]
            db.session.add_all(e_vegsystemer)

            print("Riksveg")
            ekskluder_vegnummer = "AND11277!=null"
            vegnummer_liste = []
            t = requests.get(f"https://nvdbapiles.atlas.vegvesen.no/vegobjekter/api/v4/vegobjekter/915?egenskap=11276=19025AND11278=19032{ekskluder_vegnummer}&inkluder=egenskaper&inkluder_egenskaper=basis&antall=1")
            if t.status_code == 200:
                t = t.json()
                antall = t['metadata']['returnert']
                while antall > 0:
                    vegnummer = next((i['verdi'] for i in t['objekter'][0]['egenskaper'] if i['id'] == 11277), None)
                    vegnummer_liste.append(vegnummer)
                    ekskluder_vegnummer += f"AND11277!={vegnummer}"
                    t = requests.get(f"https://nvdbapiles.atlas.vegvesen.no/vegobjekter/api/v4/vegobjekter/915?egenskap=11276=19025AND11278=19032{ekskluder_vegnummer}&inkluder=egenskaper&inkluder_egenskaper=basis&antall=1")
                    if t.status_code == 200:
                        t = t.json()
                        antall = t['metadata']['returnert']
                    else:
                        print(t.text)
                        break
            vegnummer_liste = sorted(vegnummer_liste)
            r_vegsystemer = [
                vegsystem(vegnummer=nr, vegkategori_id=2, vegfase="V") for nr in vegnummer_liste
            ]
            db.session.add_all(r_vegsystemer)

        # Add område
        if not område.query.first():
            print("Filling in område")
            fylker = fylke.query.all()
            vegsystemer = db.session.query(
                vegsystem, vegkategori
                ).join(
                    vegsystem, vegkategori.id == vegsystem.vegkategori_id
                    ).filter(
                        vegsystem.vegkategori_id.in_([1, 2])
                        ).all()
            områder = []
            for f in tqdm.tqdm(fylker):
                for vs, vk in vegsystemer:
                    vref = f"{vk.kortnavn}V{vs.vegnummer}"
                    t = requests.get(
                        f"https://nvdbapiles.atlas.vegvesen.no/vegnett/api/v4/veglenkesekvenser?fylke={f.id}&vegsystemreferanse={vref}&antall=1"
                    )
                    if t.status_code == 200:
                        t = t.json()
                        if t['metadata']['returnert'] > 0:
                            områder.append(
                                område(
                                    navn=f"{f.navn} {vk.kortnavn}V{vs.vegnummer}",
                                    fylke_id=f.id,
                                    vegkategori_id=vs.vegkategori_id,
                                    vegsystem_id=vs.id
                                )
                            )
            for f in fylker:
                områder.append(
                    område(
                        navn=f"{f.navn} Fylkesveg",
                        fylke_id=f.id,
                        vegkategori_id=3,
                        vegsystem_id=None
                    )
                )
            db.session.add_all(områder)
