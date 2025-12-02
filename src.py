
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

'''
df = pd.read_csv("kepler_data_whole.csv")
print(len(df))

#print(df.pl_name.duplicated().value_counts())

# original dataset contains multiple rows for single planet, so for each planet I'm selecting only rows with the newest information, rest is dropped from dataset
# dataset now has one row for each planet

# by dropping all rows except the newest one for every planet, we lost quite a lot of data, so before dropping these rows I used fill, to at least fill some 
# of the empty cells in newest rows, this drastically decreased number of empty cells in new dataset 

df_filled = df.groupby("pl_name").apply(lambda g: g.ffill().bfill())
df_filled = df_filled.reset_index(drop=True)

df_sorted = df_filled.sort_values("rowupdate", ascending=False)
planets = df_sorted.drop_duplicates(subset="pl_name", keep="first")

print(planets.info())
planets.to_csv("planets_clean.csv", index=False)

# Now I will use this new file.
'''

planets = pd.read_csv("planets_clean.csv")
planets.info()

#Which planets receive Earth-like insolation? How many?
# ADD STARTYPE HERE TO SEE ANY CORRELATION!!!
# earthlike flux > 0.53 - 1.1 earth flux
flux = planets[["pl_insol", "st_spectype"]].copy()
print(flux)
flux.dropna(subset="pl_insol", inplace=True)
earth_like = flux[(flux.pl_insol > 0) & (flux.pl_insol < 2)]["pl_insol"] #range for plottng purposes
earth_like_num = len(flux[(flux.pl_insol > 0.53) & (flux.pl_insol < 1.1)])
print(earth_like_num) #exact number

# limited info about star type, cant really come to a conclusion
# i can check other star of this type to find out more info and relation between startype and insolation
star_to_earthlike = flux[(flux.pl_insol > 0.53) & (flux.pl_insol < 1.1)]["st_spectype"].value_counts()
# print(flux[(flux.pl_insol > 0.53) & (flux.pl_insol < 1.1)]["st_spectype"])
print(star_to_earthlike)

plt.hist(earth_like, bins=50, color='skyblue')
plt.axvspan(0.53, 1.1, color='green', alpha=0.3, label='Earth-like HZ')
plt.xlabel('Insolation Flux [Earth flux]')
plt.ylabel('Number of planets')
plt.title('Distribution of Planet Insolation Flux')
plt.legend()
plt.show()

"""
#Star types distribution
spec_type = planets.st_spectype.value_counts()
top10 = spec_type.head(20)
labels = top10.index
counts = top10.values
plt.bar(labels, counts, color='skyblue')
plt.show()
"""

"""
#Do planets really lie in habitable zone? How many?
lumino = planets[["st_lum", "pl_orbsmax", 'pl_orbeccen']]  # from log(solar) to solar luminosities
lumino = lumino.rename(columns={"pl_orbsmax": "semi-major"})
lumino.dropna(inplace=True)
lumino["st_lum"] = 10 ** lumino["st_lum"]
lumino['semi_minor'] = lumino['semi-major'] * (1 - lumino['pl_orbeccen']**2)**0.5
lumino['hb_inner'] = np.sqrt(lumino["st_lum"]) * 0.95
lumino['hb_outer'] = np.sqrt(lumino["st_lum"]) * 1.67

lumino['peri'] = lumino['semi-major'] * (1 - lumino['pl_orbeccen'])
lumino['ap'] = lumino['semi-major'] * (1 + lumino['pl_orbeccen'])

inside_hz = lumino[(lumino['ap']> lumino['hb_inner']) & (lumino['peri'] < lumino['hb_outer'])]
print(len(inside_hz))
"""


'''
# Does density correlate with mass? It doesn´t look like density really correlates with mass. This suggests that there are mupliple 
# types of planets present in Keplers dataset.

densitymass = planets[["pl_masse", "pl_dens"]].dropna()
print(len(densitymass))

plt.scatter(densitymass.pl_masse, densitymass.pl_dens)
plt.xlim(-90, 9000)
plt.ylim(-5, 500)
plt.xlabel("mass")
plt.ylabel("density")
plt.title("Mass vs. Density")
plt.show()
plt.clf()
'''

"""
# Are massive planets more likely to have longer orbital periods?

temp3 = planets[["pl_rade", "pl_orbper"]].dropna()
print(len(temp3))
print(temp3.sort_values("pl_orbper"))

rade_percentile = np.percentile(temp3.pl_rade, 99)
print(rade_percentile)

orbper_percentile = np.percentile(temp3.pl_orbper, 99)
print(orbper_percentile)

sns.boxplot(temp3.pl_orbper)
plt.show()
plt.clf()

fig, axes = plt.subplots(3, 1, figsize=(12, 8))
#couple of extreme outliers
axes[0].scatter(planets.pl_rade, planets.pl_orbper)
axes[1].scatter(planets.pl_rade, planets.pl_orbper)
axes[1].set_xlim(-1,50)
axes[1].set_ylim(-10, 22000)
axes[2].scatter(planets.pl_rade, planets.pl_orbper)
axes[2].set_xlim(-1,50)
axes[2].set_ylim(-10, 1000)
plt.show()
plt.clf()
"""


'''
# Do bigger planets tend to orbit farther out? mass/radius/density vs Semi-Major Axis
# doesnt seem to be the case, planets with variable length of semi-major axis are often do have similar density, but there are some outliars
# in graphs with mass and radius we can see that there is higher number of planetes with higher mass and radius at relatively small lenghts
# of semi-major axis, this would suggest that planets with higher mass or diameter tend to orbit closer to a star,
# however this sample of around 1400 planets is very small to come to a certain conclusions.

# Filtered columns needed and droping rows with NA values, to have graph for the same set of planets
temp = planets[["pl_masse", "pl_rade", "pl_dens", "pl_orbsmax"]].dropna()
sorted_temp = temp.sort_values("pl_orbsmax")
sorted_temp = sorted_temp[:-6]
print(sorted_temp)

fig, axes = plt.subplots(3, 1, figsize=(12, 8))
axes[0].scatter(sorted_temp.pl_orbsmax, sorted_temp.pl_masse)
axes[0].set_title("Semi-major axis vs. mass of planet")
axes[1].scatter(sorted_temp.pl_orbsmax, sorted_temp.pl_masse )
axes[1].set_title("Semi-major axis vs. radius of planet")
axes[2].scatter(sorted_temp.pl_orbsmax, sorted_temp.pl_dens)
axes[2].set_title("Semi-major axis vs. density of planet")
plt.tight_layout()
plt.show()
'''


'''
# CAN WE DETECT FULTONS GAP?
print(planets.pl_rade.describe())

print(np.percentile(planets.pl_rade.dropna(), 99)) # 99% of planets´ radius <= 19.60, will plot histogram by that to have nice graph

sns.boxplot(planets.pl_rade) # 3 crazy outliars
plt.show()
plt.clf()

plt.hist(x=planets.pl_rade, range=(0,20), bins=200) # all planets histogram
plt.show()
plt.clf()


plt.hist(x=planets.pl_rade, range=(0,4), bins=200) # planets with similar size to earth, visible bimodality
plt.show()
plt.clf()
'''






'''
# HEATMAP of all numerical values
numeric_df = planets.select_dtypes(include=['number'])
# print(numeric_df.columns)
corr = numeric_df.corr()
# print(numeric_df.shape)
# print(corr.shape)

sns.heatmap(corr)
plt.xticks(ticks=range(len(corr.columns)), labels=corr.columns, rotation=45, ha='right', fontsize=8)
plt.yticks(ticks=range(len(corr.columns)), labels=corr.columns, rotation=0, fontsize=8)
plt.tick_params(length=0)
plt.tight_layout()
# plt.show()
'''