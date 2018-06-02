# DortmundCrawler
This is a web-scraper designed to extract VLE Data tables (TXY and PXY formats) from the Dortmund Data Bank website for any two compounds. 

This utility can be used from the command line as follows. In the commandline, enter:

Python DortmundCrawler.py name_of_compound1 name_of_compound2

Note: If out of the two compounds, one of the compounds has a space in the name (like Acetic Acid), make sure that compound's name is written first. If both compounds have spaces in their names, then the order doesn't matter.

The following compounds are supported:
[Acetonitrile] [Acetone] [1,2-Ethanediol] [Ethanol] [Diethyl ether] [Ethyl acetate] [Benzene] [1-Butanol] [Chloroform] [Cyclohexane] [Acetic acid butyl ester] [Acetic acid] [Hexane] [2-Propanol] [1-Hexene] [Methanol] [Naphthalene] [Tetrahydrofuran] [Water] [m-Xylene] [p-Xylene] [N-Methyl-2-pyrrolidone] [1,3-Butadiene] [Hexadecane] [Sulfolane] [Potassium chloride] [Sodium chloride]

The results are printed in an Excel file in the same folder with the following name format:
name_of_compound1-name_of_compound2_VLEData.xlsx

In the Excel file, the first column is either Temperature (marked in yellow) or Pressure (marked in blue). The second column is the liquid mole fraction (X) and the third column is the vapour mole fraction (Y).
