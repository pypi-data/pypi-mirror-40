import json
import os


def _rujaqik_json(wuj, chuwäch=None):
    if chuwäch is not None:
        if len(os.path.splitext(chuwäch)[1]):
            chuwäch = os.path.split(chuwäch)[0]
        chuwäch = os.path.dirname(chuwäch)
        wuj = os.path.join(chuwäch, wuj)
    with open(wuj, encoding='utf8') as w:
        return json.load(w)


class Wuj(object):
    def __init__(ri, reta=None, chuwäch=None):
        ri.retamabal = _rujaqik_json(os.path.join(os.path.split(__file__)[0], "kinuk'.json"))
        if isinstance(reta, dict):
            ri.retamabal.update(reta)
        elif reta is not None:
            ri.retamabal.update(_rujaqik_json(reta, chuwäch))

    def chabäl_ko_wi(ri):
        return list(ri.retamabal)

    def kinuk_ko_wi(ri, rubanikil="nuchab'äl"):
        rubanikil = ri._tatojtobej_rubanikil(rubanikil)
        return [x[rubanikil] for x in ri.retamabal.values() if rubanikil in x]

    def ruchabäl(ri, runuk, rubanikil=None):

        if rubanikil is None:
            chabäl = next((x for x, d in ri.retamabal.items() if any(s == runuk for s in d.values())), None)
        else:
            rubanikil = ri._tatojtobej_rubanikil(rubanikil)
            chabäl = next((x for x, w in ri.retamabal.items() if w[rubanikil] == runuk), None)
        if chabäl is None:
            raise ValueError(runuk, rubanikil)
        else:
            return chabäl

    @staticmethod
    def _tatojtobej_rubanikil(système):
        if système == "nuchab'äl":
            return "runuk'"
        if système == 'iso':
            return "rumajaju"
        elif système in ["rumajaju", "glottolog"]:
            return système
        raise ValueError(système)

    def _tatojtobej_chabäl(ri, chabäl):
        if chabäl not in ri.chabäl_ko_wi():
            chabäl = ri.ruchabäl(chabäl)
        return chabäl

    def runuk(ri, chabäl, système="nuchab'äl"):
        chabäl = ri._tatojtobej_chabäl(chabäl)
        système = ri._tatojtobej_rubanikil(système)
        return ri.retamabal[chabäl][système]

    def rajilanïk(ri, chabäl):
        chabäl = ri._tatojtobej_chabäl(chabäl)
        try:
            return ri.retamabal[chabäl]["ajilanïk"]
        except KeyError:
            return chabäl

    def tatojtobej(ri):
        assert all(ba in w for w in ri.retamabal.values() for ba in ["nuchab'äl", "rumajaju", "glottolog"])
        assert len(ri.chabäl_ko_wi()) == len(set(ri.chabäl_ko_wi()))
        for ba in ["nuchab'äl", "rumajaju", "glottolog"]:
            assert len(ri.kinuk_ko_wi(ba)) == len(set(ri.kinuk_ko_wi(ba)))


chijun = Wuj()
