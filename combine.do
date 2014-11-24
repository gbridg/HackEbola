
insheet using "combined.csv", clear
insheet using "combined_last.csv", clear

// No values
drop wrk_agr

encode area_blockade, gen(area_blockade_n)
encode border_closure, gen(border_closure_n)
encode national_law, gen(national_law_n)
encode bisholding, gen(bisholding_n)
encode bishospital, gen(bishospital_n)
encode bistransit, gen(bistransit_n)
encode bistriage, gen(bistriage_n)
encode bisetc, gen(bisetc_n)

gen has_blockade = area_blockade == "True" | border_closure == "True"
gen has_etu 	 = bisholding == "True" | bishospital == "True" | bistransit == "True" | bistriage == "True" | bisetc == "True"
tab has_blockade has_etu

gen death_ratio = deaths / cases

gen bFlag = 0
replace bFlag = 1 if death_ratio <= 1.0

list deaths cases  death_ratio bFlag

reg death_ratio has_blockade has_etu if bFlag == 1, robust

foreach this_var of varlist iwi-age90hi {
	reg death_ratio `this_var' has_blockade has_etu if bFlag == 1, robust
}

reg death_ratio edyr_fem urban small_house bad_water has_blockade has_etu if bFlag == 1, robust

graph box death_ratio, by(has_blockade) noout

graph matrix death_ratio iwi- bad_toilet, half
