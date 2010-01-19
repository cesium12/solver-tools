from bayesinator.recognize import puzzle_logprob
from collections import defaultdict
import heapq
import random

def best_order(things):
    heap = []
    costs = defaultdict(dict)
    for thing in things:
        for thing2 in things:
            if costs[thing].has_key(thing2): continue
            costs[thing][thing2] = -puzzle_logprob(thing+thing2)
    same = 0
    while True:
        i, j = random.sample(xrange(1, len(things)), 2)
        if j < i: i,j = j,i

        bestorderscore = 1e300
        bestorder = None
        pieces = [things[:i], things[i:j], things[j:]]
        for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1),
        (2, 1, 0)):
            attach = ( costs[pieces[order[0]][-1]][pieces[order[1]][0]]
                     + costs[pieces[order[1]][-1]][pieces[order[2]][0]])
            if attach < bestorderscore:
                bestorderscore = attach
                bestorder = order
        if bestorder == (0, 1, 2):
            same += 1
            if same == 1000: return things
        else:
            same = 0
        newpieces = [pieces[bestorder[0]], pieces[bestorder[1]],
        pieces[bestorder[2]]]
        things = newpieces[0] + newpieces[1] + newpieces[2]
        print same, ' '.join(things)

hard = """
ACO ADM ADR AND APA ARU ASD ATT ATY AVE AYO AYS BEE BER CAP CKS CLO DEA DIA DLI
DLI DNT DON DOW DSH DTU DVI DWH EBO EBO EDA EDI EEN EIN EMA ENI ENT EOF EPO
ERN ERT ERU ERY ESA ESD ESE ESI EYO FIF FOU GEV GHT GOT GPS GTI HAT HAT HEB HEG
HEL HEN HER HES HHI HIR HTB ICS IDI IDI IGN IHE IKI INC INE INK INK ION ION ISW
ITO ITO ITT ITU ITW IVE IWA IXS KEI KEM KET KIS KIT KNO KSH LDH LDM LEB LES LLE
LLI LOP LOV MAG MAN MEA MGO MIX NAN NDA NDG NED NEH NEI NES NET NGI NGL NIG NIN
NNA NTH NTI NUM OFL OKE OKM OLD ONE ONN OOK OOK OTI OTT OUR OVE OWN OWT PAL PED
POT PRI RNI RNI RPE RTD RTH RTY SAF SAI SEI SEM SHE SIN SIN SLO SME SSD STA THE
THI THI THN THS THT TLO TMY TOM TOO TTL TTL TYF TYS UBL UKN UMB UMB UTW VEP VIN
WIF WIN WIT YEY YLI YNO YTR YWI 
"""

def demo():
    print best_order(hard.split())
demo()
