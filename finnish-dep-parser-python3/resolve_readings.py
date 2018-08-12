# -*- coding: utf-8 -*-
##TODO: Warning: if there are words with +-character and if that word gets more than one reading, I don't know what happens.
from builtins import str
from builtins import range
import re
import sys
import omorfi_pos
import omorfi_wrapper
import os

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))
OmorTransducer=omorfi_wrapper.OmorfiWrapper(os.path.join(SCRIPTDIR,"model/generation.finntreebank.hfstol"))

atRe=re.compile(r"@[A-Za-z.]+@",re.U) #The @....@ tags in the transducer output, want to get rid of them

############################################################################################
# SUPPORT FUNCTIONS:

#True, if one or more readings is compound
def isCompound(readings):
    for r in readings:
        if "<Cmpnd>" in r: return True
        elif "+#" in r: return True
    return False

#True, if one or more readings is derivation
def isDerivation(readings):
    for r in readings:
        if "<Der_" in r: return True
    return False

#Takes one reading and returns the reading of last member if compound and reading without lemma if normal
def give_last_one(r):
    if "+" in r:
        columns=r.split("+")
        ending=columns[len(columns)-1]
    else: ending=r
    index=0
    for char in ending:
        if char!="<": index+=1
        else: break
    ending=ending[index:len(ending)]
    return ending

#Makes all necessary der changes to reading r
def der_changes(r):
    regex="(<Der_[A-Za-z]+>)"
    if "<Der_" in r:
        m=re.findall(regex,r)
        Der=m[len(m)-1]
        columns=r.split(Der)
        r=columns[len(columns)-1]
        if Der=="<Der_u>": r="<N>"+r #because of missing <N>-tag
        elif Der=="<Der_llinen>": r=re.sub("<A>","<A><Pos>",r) #because of missing <Pos>-tag
        elif Der=="<Der_ton>": r=re.sub("<A>","<A><Pos>",r)
        elif Der=="<Der_tse>": r=re.sub("<Adv><Prl>","<Adv>",r)
        elif Der=="<Der_ttain>": r=re.sub("<Adv><Dis>","<Adv>",r)
        elif Der=="<Der_sti>": r=re.sub("<Adv><Comp>","<Adv>",r)
        if "[DRV=UUS]" in r: r=re.sub("\[DRV=UUS\]","",r) #deletes DRV=UUS-tag
    r=re.sub("<cap>","",r)
    r=re.sub("<Cap>","",r)
    r=re.sub("<CAP>","",r)
    return r

#Takes one COMPOUND-reading, returns lemma (like "raja jääkäri pataljoona")
def give_cmpnd_lemma(r):
    lemma=""
    columns=r.split("+")
    for col in columns:
        if "<" in col:
            c=col.split("<")
            lemma+=c[0]+" "
        else: lemma+=col+" "
    lemma=lemma.strip()
    lemma=re.sub("#","",lemma)
    return lemma
##############################################################################################
# COMPARING FUNCTIONS

#Takes two der-readings, returns True if considered as same
def der_vs_der(r1,r2):
    regex="(<Der_[A-Za-z]+>)"
    m1=re.findall(regex,r1)
    m2=re.findall(regex,r2)
    if len(m1)>len(m2):
        Der=m1[0]
        columns=r1.split(Der)
        if len(columns)==2: r1_ending=columns[1]
        else: return False
        r2_ending=give_last_one(r2)
        if r1_ending==r2_ending: return True
        else: return False
    elif len(r2)>len(r1):
        Der=m2[0]
        columns=r2.split(Der)
        if len(columns)==2: r2_ending=columns[1]
        else: return False
        r1_ending=give_last_one(r1)
        if r2_ending==r1_ending: return True
        else: return False
    else:
        cols=r1.split("<")
        lemma1=cols[0].lower()
        cols=r2.split("<")
        lemma2=cols[0].lower()
        if lemma1==lemma2: return True
        else: return False

#Takes two readings, checks if the readings of last members are same (this one just skips lemmas)
def isSameAnalysis(r1,r2):
    r1_ending=give_last_one(r1)
    r2_ending=give_last_one(r2)
    r1_ending=der_changes(r1_ending)
    r2_ending=der_changes(r2_ending)
    if r1_ending==r2_ending: return True
    else: return False

#Splits compounds to parts and compares those, returns True, if all parts match
def split_compounds(r1,r2):
    parts1=r1.split("+")
    parts2=r2.split("+")
    if len(parts1)==len(parts2):
        for i in range(0,len(parts1)):
            part1=parts1[i]
            part1=re.sub("#","",part1)
            part1=re.sub("<Cmpnd>","",part1)
            part2=parts2[i]
            part2=re.sub("#","",part2)
            part2=re.sub("<Cmpnd>","",part2)
            if "<" in part1 and "<" in part2: #both have reading, no talvi+#uni cases
                if "<Der_" in part1 or "<Der_" in part2: #if other have der-tag check also readings
                    if isSameLemma(part1,part2)==False or isSameAnalysis(part1,part2)==False: return False
                else:
                    if not isSameLemma(part1,part2): return False
            else: # other (or both) doesn't have tags, use omorfi generation if needed
                if "<" not in part1 and "<" not in part2: #both #-tag compounds
                    if part1 != part2: return False
                elif "<" in part1: #part1 has reading
                    cols=part1.split("<")
                    lemma1=cols[0]
                    if lemma1==part2: continue #lemma is same, continue to next part
                    #different lemma, try omorfi generation
                    if OmorTransducer==None: raise ValueError("Omorfi is not loaded correctly, cannot do lookup")
                    wordforms=[atRe.sub("",str(r,"utf-8")) for r,score in OmorTransducer.lookup(part1.encode("utf-8"))]
                    match=False
                    for form in wordforms:
                        form=re.sub("-","",form)
                        form=re.sub("\u2010","",form)
                        if form==part2:
                            match=True
                            break
                    if not match: return False #no match using omorfi generation
                else:#same but part2 has reading
                    cols=part2.split("<")
                    lemma2=cols[0]
                    if lemma2==part1: continue
                    if OmorTransducer==None: raise ValueError("Omorfi is not loaded correctly, cannot do lookup")
                    wordforms=[atRe.sub("",str(r,"utf-8")) for r,score in OmorTransducer.lookup(part2.encode("utf-8"))]
                    match=False
                    for form in wordforms:
                        form=re.sub("-","",form)
                        form=re.sub("\u2010","",form)
                        if form==part1:
                            match=True
                            break
                    if not match: return False
        #same len and all part matches --> is same
        return True
    else: return False # different len, can't be same

#Takes two readings and checks if lemmas are same
#NORMAL CMPND: Lemmas has to be exactly same, or omorfi generated
#NORMAL Der_: 1) If der vs. normal, returns always True (because lemmas are different, can't know for real) 2) If der vs der, calls der_vs_der()
#BOTH CMPND AND DER: splits to sub words and compare those
def isSameLemma(r1,r2):
    if "Cmpnd" in r1 or "+#" in r1:
        if "Cmpnd" in r2 or "+#" in r2:
            if "Der_" in r1 or "Der_" in r2: return split_compounds(r1,r2) #BOTH COMPOUNDS + DERIVATION AT LEAST IN OTHER
            else: #both are COMPOUNDS WITHOUT DERIVATIONS
                if give_cmpnd_lemma(r1).lower()==give_cmpnd_lemma(r2).lower(): return True
                else: return split_compounds(r1,r2) #try generated forms
        else: #r1 is compound, r2 isn't --> if lemmas are same, true --> isoisä vs. iso|isä
            compound=give_cmpnd_lemma(r1).lower()
            compound_lemma=re.sub("\s","",compound)
            compound_hash=re.sub("\s","-",compound) #try also put "-" between, beacause omorfi drops those
            columns=r2.split("<")
            lemma=columns[0].lower()
            if compound_lemma==lemma or compound_hash==lemma: return True
            else: return False
    elif "Cmpnd" in r2 or "+#" in r2: #r2 is compound, r1 isn't --> if lemmas are same, true
        compound=give_cmpnd_lemma(r2).lower()
        compound_lemma=re.sub("\s","",compound)
        compound_hash=re.sub("\s","-",compound)
        columns=r1.split("<")
        lemma=columns[0].lower()
        if compound_lemma==lemma or compound_hash==lemma: return True
        else: return False
    elif "Der_" in r1 or "Der_" in r2: #JUST DERIVATIONS:
        if "Der_" in r1 and "Der_" in r2: return der_vs_der(r1,r2) #both are derivations
        else: return True
    else:#both are NORMALS
        columns=r1.split("<")
        lemma1=columns[0].lower()
        columns=r2.split("<")
        lemma2=columns[0].lower()
        if lemma1==lemma2: return True
        else: return False

#compare 1vs1,return better or None if equal, better is the one with less Der_-tags or if same number, more #-tags
def compare(r1,r2):
    if isSameLemma(r1,r2) and isSameAnalysis(r1,r2):
        compound_count1=re.findall("\+",r1)
        compound_count2=re.findall("\+",r2)
        der_count1=re.findall("Der_",r1)
        der_count2=re.findall("Der_",r2)
        if len(compound_count1) < len(compound_count2): return r1
        elif len(compound_count2) < len(compound_count1): return r2
        elif len(der_count1) < len(der_count2): return r1
        elif len(der_count2) < len(der_count1): return r2
        else:
            hash_count1=re.findall("#",r1)
            hash_count2=re.findall("#",r2)
            if len(hash_count2)>len(hash_count1): return r2
            else: return r1
    else: return None

####################################################################################################
# MAINS, GO TROUGHT READINGS

#Takes readings (set) and compares those 1vs1 --> if same, marks notwanted with "???". Returns readings (set) with no "???" in them
def handle_cmpnds_and_ders(readings):
    readings=list(readings) #convert set to list, because we need indices.
    for index in range(0,len(readings)):
        r=re.sub("\+\+#","+#",readings[index]) #because some adj-der-cmpnd:s have ++# instead of +#
        #example: pidempijaksoinen    pitkä<A><Comp><Sg><Nom><Cmpnd>++#jaksoinen<A><Pos><Sg><Nom><cap>
        if r.startswith("???"): r=re.sub("\?\?\?","",r)
        for i in range(index+1,len(readings)):
            if readings[index].startswith("???") and readings[i].startswith("???"):
                continue #both discarded --> no need to compare berween these
            else:
                other=re.sub("\+\+#","+#",readings[i])
                other=re.sub("\?\?\?","",other)
                better=compare(r,other)
                if better!=None: #mark the reading we don't want choose
                    if better==r:
                        if not readings[i].startswith("???"):
                            readings[i]="???"+readings[i]
                    else:
                        if not readings[index].startswith("???"):
                            readings[index]="???"+readings[index]
    left_readings=set()
    for r in readings:
        if not r.startswith("???"): left_readings.add(r)
    assert len(left_readings)!=0, "Every reading discarded"
    return left_readings

# main function, calls handle_cmpnds_and_ders() if needed, otherwise just returns same set
def main(readings):
    if len(readings)>1:
        if isCompound(readings) or isDerivation(readings):
            return handle_cmpnds_and_ders(readings)
        else: #all readings are normal, return just same list
            return readings
    else: #just one reading, just return it
        return readings
