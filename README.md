# covid-vaccine-slot-finder

This script can be used to find slots for Covid vaccination in your state, district or pincode.

## Usage :
- To find vaccination slots in state Delhi for next 3 days starting from 4th May 2021 for 18+ people.
`python covid_vaccine.py --state Delhi  --date 04-05-2021 --minAge 18`
- To find vaccination slots in state Karnataka, district BBPM for next 7 days starting from 4th May 2021 for 45+ people.
`python covid_vaccine.py --state Karnataka --district BBMP --date 04-05-2021 --minAge 45`
- To find vaccination slots in state Delhi, pincode - 110052 for next 7 days starting from 5th May 2021 for 18+ people.
`python covid_vaccine.py --state Delhi --pincode 110052 --date 05-05-2021 --minAge 18`
