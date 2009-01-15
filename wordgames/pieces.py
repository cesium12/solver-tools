from bayesinator.recognize import puzzle_logprob
import random

def try_order(things):
    things = list(things)
    random.shuffle(things)
    answer = ''
    while things:
        current = things.pop()
        things.sort(key=lambda next: puzzle_logprob(current+next))
        answer += current
    print answer
    return answer

def best_order(things):
    tries = [try_order(things) for i in range(100)]
    tries.sort(key=lambda answer: -puzzle_logprob(answer))
    
    return tries[0], puzzle_logprob(tries[0])

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
