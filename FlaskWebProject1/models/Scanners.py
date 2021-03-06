from datetime import date, timedelta, datetime
from FlaskWebProject1.models.StockQuote import StockQuote as st
import sys

portfolio_OL = ["ASC.OL","APCL.OL","AFG.OL","AGA.OL","AKA.OL","AKER.OL","AKPS.OL","AKSO.OL",
"AKVA.OL","AMSC.OL","ABT.OL","ARCHER.OL","AFK.OL","ASETEK.OL","ATEA.OL","AURLPG.OL","AUSS.OL","AVANCE.OL","AVM.OL","AWDR.OL","BAKKA.OL","BEL.OL",
"BERGEN.OL","BIONOR.OL","BIOTEC.OL","BIRD.OL","BLO.OL","BON.OL","BRG.OL","BWLPG.OL","BWO.OL","BMA.OL","CECON.OL","DAT.OL","DESSC.OL",
"DETNOR.OL","DNB.OL","DNO.OL","DOF.OL","DOLP.OL","EAM.OL","ECHEM.OL","EKO.OL","EMGS.OL","ELT.OL","EMAS.OL","ENTRA.OL","EVRY.OL","FAR.OL","FLNG.OL",
"FOE.OL","FRO.OL","FUNCOM.OL","GRO.OL","GJF.OL","GOGL.OL","GOD.OL","GSF.OL","HNB.OL","HFISK.OL","HAVI.OL","HEX.OL","HBC.OL","HLNG.OL","IDEX.OL",
"IOX.OL","ITX.OL","IMSK.OL","JIN.OL","KOA.OL","KOG.OL","KVAER.OL","LSG.OL","MHG.OL","NAPA.OL","NATTO.OL","NAVA.OL","NEL.OL","NEXT.OL","NMG.OL",
"NIO.OL","NOM.OL","NOD.OL","NSG.OL","NHY.OL","NOF.OL","NRS.OL","NAS.OL","NOR.OL","NPRO.OL","NTS.OL","OCY.OL","ODL.OL","ODF.OL","ODFB.OL","OLT.OL",
"OPERA.OL","ORK.OL","PEN.OL","PCIB.OL","PGS.OL","PDR.OL","PHO.OL","PLCS.OL","POL.OL","PRS.OL","PROS.OL","PROTCT.OL","PSI.OL","QFR.OL","QEC.OL","RAKP.OL",
"REC.OL","RECSOL.OL","RENO.OL","REPANT.OL","RGT.OL","RCL.OL","SALM.OL","SCI.OL","SSHIP.OL","SSO.OL","SCH.OL",
"SDRL.OL","SBO.OL","SENDEX.OL","SER.OL","SEVDR.OL","SEVAN.OL","SIOFF.OL","SKI.OL","SOFF.OL","SOLV.OL","SONG.OL","SRBANK.OL","SPU.OL","STL.OL","SNI.OL",
"STB.OL","STORM.OL","SUBC.OL","TIL.OL","TEL.OL","TELIO.OL","TGS.OL","SSC.OL","THIN.OL","TOM.OL","TTS.OL","VARDIA.OL","VEI.OL","VIZ.OL","WEIFA.OL","WRL.OL",
"WBULK.OL","WWASA.OL","WWI.OL","WWIB.OL","XXL.OL","YAR.OL","ZAL.OL","ZONC.OL"]

#portfolio = ["AGA.OL","ABT.OL","AVANCE.OL","FRO.OL","GOGL.OL","HLNG.OL"]

portfolio = ["BAKKA.OL","BIOTEC.OL","SOLV.OL","EVRY.OL","GOGL.OL", "XXL.OL"]

class Scanner(object):
    def __init__(self, prereqs, triggers, length):
        self.found = []
        self.portfolio = portfolio_OL
        self.length = length
        self.prereqs = prereqs

        self.scan()

    def scan(self):
        s= Scraper()

        self.portfolio = s.OL()

        for item in self.portfolio:

            print(item)
            try:
                #s = st("GSF.OL", None, self.length)
                s = st(item, None, self.length)
                s.df['test'] = 0
                s.df['test'][0] = 1
                l = len(s.df)


                #Execute all calculatation methods before scanning
                for prereq in self.prereqs:
                    func = getattr(s, prereq)
                    func()
                if s.df.iloc[l-1][self.triggers] == 1:
                    print("Found")
                    self.found.append(item)
            except:
                print("Import Error")

            print("---------------------------------------")
        #self.found


class ScannerDoublecross(Scanner):
    def __init__(self):
        self.prereqs = ['stoch_crossover', 'macd_crossover', 'doublecross']
        self.triggers = 'doublecross'
        self.length = 60
        Scanner.__init__(self, self.prereqs, self.triggers, self.length)



class ScannerRSI(Scanner):
    def __init__(self):
        self.prereqs = ['scan_rsi_over_70']
        self.triggers = 'rsi_over_70'
        self.length = 60
        Scanner.__init__(self, self.prereqs, self.triggers, self.length)

class ScannerCrossings(Scanner):
    def __init__(self):
        self.prereqs = ['inter']
        self.triggers = 'ann_cross'
        self.length = 30
        Scanner.__init__(self, self.prereqs, self.triggers, self.length)


class ScannerStoploss(Scanner):
    def __init__(self):
        self.prereqs = ['slowk_drops_under_80', 'atr_stoploss']
        self.triggers = 'rsi_over_70'
        self.length = 60
        Scanner.__init__(self, self.prereqs, self.triggers, self.length)

'''
def scanner_stoploss():
    found = []
    for item in portfolio_OL:

        print(item)

        try:
            s = st(item, 1, 31)
            t = s.scan_stoploss()
            if t == True:
                found.append(item)
        except:
            print("Import Error")
        print("---------------------------------------")

    return found


def scanner_obv():
    found = []
    for item in portfolio_OL:
    
        print(item)
        today = datetime.today()
        day = timedelta(days=1)
        year = timedelta(days=365)
        start = today-year
        end = today-day

        try:
            s = st(item, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))
            t = s.scan_wma_obv()
            if t == True:
                found.append(item)
        except:
            print("Import Error")

        print("---------------------------------------")

    return found

def scanner_doublecross():
    found = []
    #portfolio_OL = ['ODF.OL']
    for item in portfolio_OL:
    
        print(item)

        try:
            s = st(item, 1, 49)
            t = s.scan_doublecross()
            if t == True:
                found.append(item)
        except:
            print("Import Error")
    
        
        print("---------------------------------------")

    return found

def scanner_rsi():
    found = []
    for item in portfolio_OL:
    
        print(item)

        try:
            s = st(item, 1, 31)
            t = s.scan_rsi()
            if t == True:
                found.append(item)
        except:
            print("Import Error")
        print("---------------------------------------")

    return found

def scanner_stoploss():
    found = []
    for item in portfolio_OL:

        print(item)

        try:
            s = st(item, 1, 31)
            t = s.scan_stoploss()
            if t == True:
                found.append(item)
        except:
            print("Import Error")
        print("---------------------------------------")

    return found
'''

