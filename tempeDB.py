# -*- coding:utf-8 -*


import mysql.connector as MS
import logging


class TempeDB(object):
    '''la base de données t-home
    '''
    def __init__(self, host = 'localhost', user = '', password = '', bdd = 'tempeDB'):
        self.bdd = bdd
        self.connection = MS.connect(user=user, host = host, buffered = True)

    def fetchall(self, req, params = None):
        '''Execute une requete SQL et renvoie tous les résultats
        '''
        cursor = self.connection.cursor()
        cursor.execute('USE %s'%self.bdd)
        logging.debug("Req : %s %s"%(req,params))
        cursor.execute(req, params)
        results =  cursor.fetchall()
        cursor.close()
        return results

    def historique(self, id, date_debut=None, date_fin = None):
        '''Renvoie l'historique d'un capteur entre date_debut et date_fin
        sous la forme d'une liste [[date, valeur]]
        '''
        logging.debug("Requete sur %s : id=%s, date_debut = %s, date_fin = %s"%(self.bdd, id, date_debut, date_fin))
        req = ("SELECT date, temperature FROM mesures WHERE capteur = %s")
        params = (id,)
        if date_debut:
            req += " AND date > %s"
            params += (date_debut,)
        if date_fin:
            req += " AND date < %s"
            params += (date_fin,)
        data = []
        for result in self.fetchall(req, params):
            data.append([str(result[0]), result[1]])
        return data

    def get_capteurs(self):
        '''renvoie la liste des capteurs
        '''
        req = "SELECT DISTINCTROW capteur FROM mesures"
        return [v[0] for v in self.fetchall(req)]
