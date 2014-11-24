clear
set more off

* Set directory
cap cd "/Users/Grant/Google Drive/Fletcher/HackEbola - Fletcher Team/Data/"

/*
* Insheet csv 2
insheet using "csv/2_mod.csv", names
destring value, replace
save "dta/cases_deaths.dta", replace


* Insheet combined.cvs
clear
insheet using "combined.csv", names

destring death, replace
save "dta/casualty_etu_demog_quar.dta", replace
*/

use "dta/casualty_etu_demog_quar.dta", clear

* Generating numeric date variables
replace date = substr(date,1,11)
gen date_num = date(date,"YMD")
format date_num %d
drop date
ren date_num date
tab date, m

preserve
	collapse (max)confirmed_cases (max)death, by(this_id)
	rename confirmed_cases cases_total
	rename death death_total
	tempfile t
	save `t'
restore
	merge m:1 this_id using `t'
	drop _m
* Drop time variant variables
drop area_blockade-bistriage
drop deaths confirmed_cases 

* Create variable = date of first case
bys this_id: egen first_date = min(date)
format first_date %d

gen t = date - first_date + 1
bys this_id: egen max_t = max(t)

gen case_density = cases_total/max_t
tab case_density, m

* Keep only one observation per region
duplicates drop this_id iwi-nhh, force
duplicates tag this_id, gen(dup_id)
tab dup_id

* Some additional cleaning
lab var urban "percent of pop that is urban"
drop if name == "Freetown"

save "dta/casualty_etu_demog.dta", replace

* Analysis

reg case_density urban iwi bad_water, r
reg case_density iwi edyr_fem, r
reg case_density bad_toilet, r
