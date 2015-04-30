import numpy as np
import pandas as pd
from context import campaignadvisor

"""
Contribution classification by quartile population size buckets
"""

def get_state_county(fips_code):
    return campaignadvisor.data_cleanup.get_state_county_from_fips(fips_code)

def get_population_series(county_statistics):
	#return county_statistics['CivPop18ONum']
	return county_statistics['TotalPopEst2013']

def get_bins(serie, num_buckets):
	bucket_size = (serie.max()-serie.min())/num_buckets
	bucket_list = []
	for n in range(0, num_buckets+1):
		bucket_list.append(n*bucket_size)
	return bucket_list

def run_county_statistics_examples(num_buckets=4):
	county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
	county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)

	#counts, bins = np.histogram(get_population_series(county_statistics))	
	serie = get_population_series(county_statistics)
	#bins = get_bins(serie, num_buckets)
	#counts, division = np.histogram(serie, bins = bins)
	#print pd.Series(counts, index=division[:-1])

	print serie.groupby(pd.cut(serie,num_buckets)).count()

	# percentages
	serie_pct = serie.value_counts(normalize=True, bins=num_buckets)
	print serie_pct
	
def main():
	run_county_statistics_examples()

if __name__ == "__main__":
    main()
