import sys
from numpy.core.umath import ERR_CALL
sys.path.append("../")

import pdb
import csv
import glob
from datetime import datetime



"""
0    pos
1    country_code
2    country
3    localite
4    category
5    value
6    date
7    sources
8    link
9    sdr_id
10    sdr_name
11    sdr_level
"""
def fetchCasualtyInfo(infilepath):
    d = {}
    d_level = {}
    csvReader = csv.reader(open(infilepath, 'rb'))
    
    good = 0
    missing_ids = 0
    bad_date = 0
    bad = 0
    
    header = csvReader.next()
        
    for row in csvReader:
        (id, name, level)   = row[-3:]
        #pdb.set_trace()
        if id == '0':
            missing_ids += 1
            continue
        
        try:
            rep_date     = datetime.strptime(row[6], '%m/%d/%Y')
        except ValueError:
            bad_date += 1
            continue
    
        
        """ [4]
            Cases
            Confirmed cases
            Deaths
            New cases
            Probable cases
            Suspected cases
        """
        
        category = row[4]
        value    = row[5]
         
        if category == "Confirmed cases" or category == "Deaths":
            try:
                d[id][rep_date][category] = value
            except KeyError:
                try:
                    d[id][rep_date] = {category: value}
                except KeyError:
                    d[id] = {rep_date: {category: value}}
            good += 1
        else:
            bad += 1
            
        d_level[id] = [level, name]
        
        
    #print good, bad, missing_ids, bad_date
    #pdb.set_trace()
    return d, d_level
    
    
    
"""
Count of source    Column Labels            
Row Labels    Area Blockade    Border Closure    National Law    Grand Total
Community Response            7    7
Flight Restrictions        85        85
Land Border        15        15
Local Border Crossing        3        3
Movement Order            18    18
Potential    4            4
Quarantine    39            39
Restricted Movement    15            15
Sea Border        11        11
Grand Total    58    114    25    197


"""
def fetchQuarantine(infilepath):
    d = {}
    csvReader = csv.reader(open(infilepath, 'rb'))
    
    header = csvReader.next()
    """
    uniqueid,restrictionscale,country,location,border_country,
    [5] restrictiontype,
    [6] restrictionnature,
    adm1,adm1_code,adm2,adm2_code,adm3,adm3_code,
    [13] date_from,
    [14] date_to,
    source,source_link,notes,country_code,
    [-3, -2, -1] sdr_id,sdr_name,sdr_level
    """
    
    out_header = [header[13], header[14], header[5], header[6]]
    
    
    for row in csvReader:
        (id, name, level)   = row[-3:]
        
        if id == '0':
            continue
        
        try:
            from_date   = datetime.strptime(row[13], '%Y-%m-%d')
        except ValueError:
            continue
        
        try:
            to_date     = datetime.strptime(row[14], '%Y-%m-%d')
        except ValueError:
            to_date = None
        
        out_row = [from_date, to_date, row[5], row[6]]
        
        try:
            
            d[id].append(out_row)
        except KeyError:
            d[id] = [out_row]
            
    #pdb.set_trace()
    return out_header, d
    
        
        
"""
    pos,
    [1] status,
    id,country,
    adm1,adm1_pcode,adm2,adm2_pcode,location,centre_name,primary_orgnization,secondary_orgnization,third_orgnization,
    [13] type1,
    [14] type2,
    who_status,
    [16] capacity,notes,
    [18] last_update,source,
    [20] centre_opening_date,
    [21] centre_closing_date,osm,latitude,longitude,coordinats_verified,staff_count,
    [27] sdr_id,sdr_name,sdr_level
"""


def fetchETUInfo(infilepath):
    d = {}
    csvReader = csv.reader(open(infilepath, 'rU'))
    
    header = csvReader.next()
    
    out_header = ["date_opened", "date_closed", "capacity", "isETC", "isHoldingCenter", "isHospital", "isTransitCenter", "isTriage"]    
    
    for row in csvReader:
        
        (id, name, level)   = row[-3:]
        
        if id == '0':
            print "Bad ID"
            continue
        
        if row[1] != "Functional":
            continue
        
        try:
            date_open   = datetime.strptime(row[20], '%d/%m/%Y')
        except ValueError:
            continue
        
        try:
            date_close  = datetime.strptime(row[21], '%d/%m/%Y')
        except ValueError:
            date_close = None
            
        capacity = row[16]
        
        """
        Types:
            ETC
            Holding Centre
            Hospital
            Transit Centre
            Triage
        """
        bIsETC      = True if (row[13] == "ETC" or row[14] == "ETC") else False
        bIsHolding  = True if (row[13] == "Holding Centre" or row[14] == "Holding Centre") else False
        bIsHospital = True if (row[13] == "Hospital" or row[14] == "Hospital") else False
        bIsTransit  = True if (row[13] == "Transit Centre" or row[14] == "Transit Centre") else False
        bIsTriage   = True if (row[13] == "Triage" or row[14] == "Triage") else False
        
        out_row = [date_open, date_close, capacity, bIsETC, bIsHolding, bIsHospital, bIsTransit, bIsTriage]
        
        try:            
            d[id].append(out_row)
        except KeyError:
            d[id] = [out_row]
            
    #pdb.set_trace()
    return out_header, d
    
       
        

def fetchDemographics(infilepath):
    d = {}
    csvReader = csv.reader(open(infilepath, 'rb'))
    
    header = csvReader.next()
    """
    [0 - 6] pos,country_code,iso_code,country,year,gdlcode,region, 
    iwi,edyr,edyr_fem,edyr_male,urban,wrk_agr,wrk_lnagr,wrk_unagr,tv,phone,electr,small_house,large_house,qual_floor,bad_floor,tap_water,bad_water,flush_toilet,bad_toilet,age09,age1019,age2029,age3039,age4049,age5059,age6069,age7079,age8089,age90hi,N,Nhh,
    [-3, -2, -1] sdr_id,sdr_name,sdr_level
    """
    
    keys = header[7:-3]
    
    
    for row in csvReader:
        (id, name, level)   = row[-3:]
        year                = row[4]
        
        if id == '0':
            continue
        
        vals = row[7:-3]
        
        """
        try:
            d[id][year] = vals
            # TURNS OUT THIS NEVER HAPPENS
        except KeyError:
            d[id] = {year: vals}
        """ 
        d[id] = vals
        
    return keys, d
    # pdb.set_trace()
        


"""
d_cas[id] = {rep_date: {category: value}}

"""
def outputCombined(k_demog, d_demog, k_quar, d_quar, k_etu, d_etu, d_cas, d_level, outfilepath, outfilepath2):
    
    csvWriter  = csv.writer(open(outfilepath, 'wb')) 
    csvWriter2 = csv.writer(open(outfilepath2, 'wb')) 
    
    header = ['adm_id', 'level', 'name', 'date', 'cases', 'deaths']
    header.extend(k_demog)
    header.extend(['area_blockade', 'border_closure', 'national_law'])
    header.extend(['bIsETC', 'bIsHolding', 'bIsHospital', 'bIsTransit', 'bIsTriage'])
    
    csvWriter.writerow(header)
    csvWriter2.writerow(header)
    
    for this_id in sorted(d_cas.keys()):
        (this_level, this_name) = d_level[this_id]
        
        max_cases = 0
        max_deaths = 0
        
        sorted_dates = sorted(d_cas[this_id].keys())
        last_date = sorted_dates[-1]
        
        for this_date in sorted_dates:
            
            # Casualty Data
            try:
                cases =  d_cas[this_id][this_date]["Confirmed cases"]
                if cases > max_cases:
                    max_cases = cases
                
            except KeyError:
                cases = None
                
            try:
                deaths =  d_cas[this_id][this_date]["Deaths"]
                if deaths > max_deaths:
                    max_deaths = deaths
                
            except KeyError:
                deaths = None
                
            out_row = [this_id, this_level, this_name, this_date, cases, deaths]
            
            
            # Demographics
            try:
                demog_info = d_demog[this_id]
            except KeyError:
                demog_info = [None] * len(k_demog)
                
            out_row.extend(demog_info)
            
            # Quarantine - was there a quarantine a this time?
            try:
                # From date, To date, Type, Nature
                bAreaBlockade   = False
                bBorderClosure  = False
                bNationalLaw    = False
                quar_info = d_quar[this_id]
                for this_quar_row in quar_info:
                    (from_date, to_date, type, nature) = this_quar_row
                    if from_date <= this_date and (to_date is None or to_date >= this_date):
                        if type == "Area Blockade":
                            bAreaBlockade = True
                        elif type == "Border Closure":
                            bBorderClosure = True
                        elif type == "National Law":
                            bNationalLaw = True
                         
                            
                quar_out = [bAreaBlockade, bBorderClosure, bNationalLaw]
            except KeyError:
                quar_out = [None, None]  
                
            out_row.extend(quar_out)   
            
            # Quarantine - was there a quarantine a this time?
            try:
                # From date, To date, Type, Nature
                fIsETC      = False
                fIsHolding  = False
                fIsHospital = False
                fIsTransit  = False
                fIsTriage   = False
                
                etu_info = d_etu[this_id]
                for this_etu_row in etu_info:
                    (date_open, date_close, capacity, bIsETC, bIsHolding, bIsHospital, bIsTransit, bIsTriage) = this_etu_row
                    if date_open <= this_date and (date_close is None or date_close >= this_date):
                        fIsETC      = fIsETC or bIsETC
                        fIsHolding  = fIsHolding or bIsHolding
                        fIsHospital = fIsHospital or bIsHospital
                        fIsTransit  = fIsTransit or bIsTransit
                        fIsTriage   = fIsTriage or bIsTriage
                        
                etu_out = [fIsETC, fIsHolding, fIsHospital, fIsTransit, fIsTriage]
            except KeyError:
                etu_out = [None, None, None, None, None]  
                
            out_row.extend(etu_out)  
            
            csvWriter.writerow(out_row)
            if this_date == last_date:
                out_row[4] = max_cases
                out_row[5] = max_deaths
                csvWriter2.writerow(out_row)
    




# Demographic Data
infilepath = 'data/csv/6.csv'
k_demog, d_demog = fetchDemographics(infilepath)


# Quarantine Data
infilepath = 'data/csv/4.csv'
k_quar, d_quar = fetchQuarantine(infilepath)

# ETC Data
infilepath = 'data/csv/5.csv'
k_etu, d_etu = fetchETUInfo(infilepath)

# Casualty Data
infilepath = 'data/csv/2_mod.csv'
d_cas, d_level = fetchCasualtyInfo(infilepath)


outfilepath  = 'data/combined.csv'
outfilepath2 = 'data/combined_last.csv'
outputCombined(k_demog, d_demog, k_quar, d_quar, k_etu, d_etu, d_cas, d_level, outfilepath, outfilepath2)



outfilepath3 = 'data/combined_monthly.csv'
outputCombinedMonthly(k_demog, d_demog, k_quar, d_quar, k_etu, d_etu, d_cas, d_level, outfilepath, outfilepath3)








