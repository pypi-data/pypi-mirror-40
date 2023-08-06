class GeneratorDC:

    Pmasuk =''
    E=''
    V=''
    I=''
    Ia=''
    Ish=''
    Is=''
    Ra=''
    Rs=''
    Rsh=''


    def __init__(self):
        pass
    def Pjangkar(self):
        Pj= self.E*self.Ia
        print(str(Pj)+'Watt')
        return str(Pj)
    def Pkeluar(self):
        Po=self.V*self.I
        print (str(Po)+'Watt')
        return Po
class RugiTembaga(GeneratorDC):
    
    def rugi_jangkar(self):
        pj=self.Ia*self.Ra

        print(str(pj)+'Watt')
        return pj
    def rugi_shunt(self):
        psh= self.Ish*self.Rsh
        print(str(psh)+'Watt')
        return psh
    def rugi_seri(self):
        ps = self.Is*self.Rs
        print(str(ps)+'Watt')
        return ps
    @staticmethod
    def rugi_gesekan(Pmasuk,rugi_jangkar):
        pg = Pmasuk-rugi_jangkar
        print(str(pg)+'Watt')
        return pg
    @staticmethod
    def rugi_total(Pj,Pout):
        pt =Pj - Pout
        print (str(pt) +'Watt')
        return pt
    
class Efisiensi(GeneratorDC):

    def efisiensi_mekanis(self):
        mks = (self.Pjangkar/self.Pkeluar)*100
        print(str(mks)+'%')
        return mks
    def efisiensi_listrik(self):
        efl=(self.Pkeluar/self.Pjangkar)*100
        print(str(efl)+'%')
        return efl
    def efisiensi_total(self):
        eft=(self.Pkeluar/self.Pmasuk)*100
        print(str(eft)+'%')
        return eft

