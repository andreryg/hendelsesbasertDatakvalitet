from . import db

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    

class vegobjekttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(80), nullable=False)
    hovedkategori = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Vegobjekttype {self.navn}>"
    
class egenskapstype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegobjekttype_id = db.Column(db.Integer, db.ForeignKey('vegobjekttype.id'), nullable=False)
    navn = db.Column(db.String(80), nullable=False)
    datatype = db.Column(db.String(80), nullable=False)
    viktighet = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Egenskapstype {self.navn}>"
    
class vegkategori(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)
    kortnavn = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"<Vegkategori {self.navn}>"
    
class vegsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vegkategori_id = db.Column(db.Integer, db.ForeignKey('vegkategori.id'), nullable=False)
    vegfase = db.Column(db.String(1), nullable=False)
    vegnummer = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Vegsystem {self.vegsystem}>"
    
class fylke(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Fylke {self.navn}>"
    
class område(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)
    fylke_id = db.Column(db.Integer, db.ForeignKey('fylke.id'), nullable=True)
    vegkategori_id = db.Column(db.Integer, db.ForeignKey('vegkategori.id'), nullable=True)
    vegsystem_id = db.Column(db.Integer, db.ForeignKey('vegsystem.id'), nullable=True)

    def __repr__(self):
        return f"<Område {self.navn}>"
    
class kvalitetsnivå_1(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Kvalitetsnivå 1 {self.navn}>"
    
class kvalitetsnivå_2(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Kvalitetsnivå 2 {self.navn}>"
    
class kvalitetsparameter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    navn = db.Column(db.String(80), nullable=False)
    kvalitetsnivå_1_id = db.Column(db.Integer, db.ForeignKey('kvalitetsnivå_1.id'), nullable=False)
    kvalitetsnivå_2_id = db.Column(db.Integer, db.ForeignKey('kvalitetsnivå_2.id'), nullable=False)
    kvalitetsnivå_3_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Kvalitetsparameter {self.navn}>"
    
class kvalitetsmåling(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    område_id = db.Column(db.Integer, db.ForeignKey('område.id'), nullable=False)
    kvalitetsparameter_id = db.Column(db.Integer, db.ForeignKey('kvalitetsparameter.id'), nullable=False)
    dato = db.Column(db.Date, nullable=False, default=db.func.current_date())
    vegobjekttype_id = db.Column(db.Integer, db.ForeignKey('vegobjekttype.id'), nullable=False)
    egenskapstype_id = db.Column(db.Integer, db.ForeignKey('egenskapstype.id'), nullable=True)
    verdi = db.Column(db.Integer, nullable=False)
    ref_verdi = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Kvalitetsmåling {self.id}>"
    
class skala(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    område_id = db.Column(db.Integer, db.ForeignKey('område.id'), nullable=True)
    kvalitetsparameter_id = db.Column(db.Integer, db.ForeignKey('kvalitetsparameter.id'), nullable=True)
    vegobjekttype_id = db.Column(db.Integer, db.ForeignKey('vegobjekttype.id'), nullable=True)
    egenskapstype_id = db.Column(db.Integer, db.ForeignKey('egenskapstype.id'), nullable=True)
    sep_1 = db.Column(db.Integer, nullable=False)
    sep_2 = db.Column(db.Integer, nullable=False)
    sep_3 = db.Column(db.Integer, nullable=False)
    sep_4 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Skala {self.id}>"