from app import db
from app.models import user, vegobjekttype, egenskapstype, vegkategori, vegsystem, fylke, område, kvalitetsnivå_1, kvalitetsnivå_2, kvalitetsparameter, skala
import requests

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
        return 0

        # Add vegkategori
        if not vegkategori.query.first():
            print("Filling in vegkategori")
            vegkategorier = [
                vegkategori(navn='Riksveg', kortnavn='R'),
                vegkategori(navn='Fylkesveg', kortnavn='F'),
                vegkategori(navn='Kommunal veg', kortnavn='K')
            ]
            db.session.add_all(vekkategorier)

        # Add fylke
        if not fylke.query.first():
            print("Filling in fylke")
