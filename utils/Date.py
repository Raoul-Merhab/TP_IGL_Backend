import datetime

class Date():
    Jour : int
    Mois : int
    Annee : int

    def __init__(self, Jour : int, Mois : int, Annee : int):
        self.Jour = Jour
        self.Mois = Mois
        self.Annee = Annee
    
    def __init__(self, date):
        temp = date.split("/")
        self.Jour = int(temp[0])
        self.Mois = int(temp[1])
        self.Annee = int(temp[2])

    def get_date(self):
        return self.Jour + "/" + self.Mois + "/" + self.Annee
    
    def is_before(self, date):
        if self.Annee < date.Annee:
            return True
        elif self.Annee == date.Annee:
            if self.Mois < date.Mois:
                return True
            elif self.Mois == date.Mois:
                if self.Jour < date.Jour:
                    return True
        return False
    
    def is_before_today(self):
        today = Date(datetime.date.today().strftime("%d/%m/%Y"))
        return self.is_before(today)
    
    def date_after_days(self, days):
        date = datetime.date(self.Annee, self.Mois, self.Jour)
        date += datetime.timedelta(days=days)
        return Date(date.strftime("%d/%m/%Y"))
    
    def today():
        return Date(datetime.date.today().strftime("%d/%m/%Y"))