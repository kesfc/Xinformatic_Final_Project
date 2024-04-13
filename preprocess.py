import csv


# Compile CO2 emissions per capita data for each country and the world from 2000-2021
def compile_nit(filename1, filename2):
    rows = []
    # Get data from CSV
    with open(filename1, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    # Load data into dictionary: {Country Code: {Country Name: <name>, CO2 Emissions Per Capita: []} }
    nit_data = dict()
    for item in rows:
        code = item[3]
        # Filter out entries that are not countries or that do not contain annual net CO2 emissions data
        if len(code) > 3 or item[4] != "Annual Net Emissions/Removals" or item[11] != "Carbon dioxide":
            continue

        # Sum total CO2 emissions data across all industries
        years = item[43:65]
        if code not in nit_data.keys():
            nit_data[code] = dict()
            nit_data[code]["CO2 Emissions"] = [0.0 for i in range(len(years))]

        for i in range(len(years)):
            if years[i] == "":
                continue
            nit_data[code]["CO2 Emissions"][i] += float(years[i])

    rows = []
    # Get data from 2nd CSV
    with open(filename2, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    # Normalize CO2 emissions by population and convert units from million metric tons to metric tons per capita
    for item in rows:
        name = item[0]
        code = item[1]
        years = item[44:66]
        if code in nit_data.keys():
            loc = nit_data[code]
            loc["Name"] = name
            for i in range(len(years)):
                loc["CO2 Emissions"][i] *= 1000000
                loc["CO2 Emissions"][i] /= int(years[i])

    # Remove any entries that do not have corresponding population data
    to_pop = []
    for code in nit_data.keys():
        if "Name" not in nit_data[code].keys():
            to_pop.append(code)

    for code in to_pop:
        nit_data.pop(code)

    return nit_data


# Compile renewable vs non-renewable energy generation data for each country and the world from 2000-2021
def compile_re(filename):
    rows = []
    # Get data from CSV
    with open(filename, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            rows.append(row)

    # Load data into dictionary: {Country Code: {Renewable: [], Non-Renewable: [], Renewable vs Non-Renewable: []} }
    re_data = dict()
    for item in rows:
        code = item[3]
        # Filter out entries that are not countries or that do not contain energy generation data
        if len(code) > 3 or item[4] == "Electricity Installed Capacity":
            continue

        if code not in re_data.keys():
            re_data[code] = dict()

        years = item[12:34]
        if item[6] == "Total Renewable":
            field_str = "Total Renewable"
        else:
            field_str = "Total Non-Renewable"

        if field_str not in re_data[code].keys():
            re_data[code][field_str] = [0.0 for i in range(len(years))]

        # Sum total renewable and non-renewable energy data across all technologies
        for i in range(len(years)):
            if years[i] == "":
                continue
            re_data[code][field_str][i] += float(years[i])

    # Remove entries that don't contain either renewable or non-renewable energy data
    to_pop = []
    for code in re_data.keys():
        if "Total Renewable" not in re_data[code].keys() or "Total Non-Renewable" not in re_data[code].keys():
            to_pop.append(code)

    for code in to_pop:
        re_data.pop(code)

    # Calculate ratios
    for code in re_data.keys():
        loc_data = re_data[code]
        r_years = loc_data["Total Renewable"]
        nr_years = loc_data["Total Non-Renewable"]
        loc_data["Renewable vs Non-Renewable"] = []
        for i in range(len(r_years)):
            ratio = 0
            if nr_years[i] != 0:
                ratio = r_years[i] / nr_years[i]

            loc_data["Renewable vs Non-Renewable"].append(ratio)

    return re_data


# Combine CO2 emissions per capita and renewable vs non-renewable energy generation datasets into one and write to CSV
def combine(nit_data, re_data, filename_out):
    data = dict()
    # Add CO2 emissions data
    for code in nit_data.keys():
        loc = nit_data[code]
        data[code] = {"Name": loc["Name"], "CO2 Emissions Per Capita": loc["CO2 Emissions"]}

    # Add energy generation data
    for code in re_data.keys():
        loc = re_data[code]
        if code in data.keys():
            data[code]["Renewable vs Non-Renewable Energy Generation"] = loc["Renewable vs Non-Renewable"]

    # Initialize CSV data
    fields = ["Location", "Country Code", "Indicator", "2000", "2001", "2002", "2003", "2004", "2005", "2006",
              "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018",
              "2019", "2020", "2021"]
    # Global data is listed first
    rows = [[data["WLD"]["Name"], "WLD", "CO2 Emissions Per Capita"],
            [data["WLD"]["Name"], "WLD", "Renewable vs Non-Renewable Energy Generation"]]
    rows[0].extend(data["WLD"]["CO2 Emissions Per Capita"])
    rows[1].extend(data["WLD"]["Renewable vs Non-Renewable Energy Generation"])

    # Compile CSV data alphabetically by country codes and remove entries that do not contain
    # renewable vs non-renewable energy generation data
    to_pop = []
    for code in sorted(data.keys()):
        if "Renewable vs Non-Renewable Energy Generation" not in data[code].keys():
            to_pop.append(code)
        elif code == "WLD":
            continue
        else:
            rows.append([data[code]["Name"], code, "CO2 Emissions Per Capita"])
            rows[-1].extend(data[code]["CO2 Emissions Per Capita"])
            rows.append([data[code]["Name"], code, "Renewable vs Non-Renewable Energy Generation"])
            rows[-1].extend(data[code]["Renewable vs Non-Renewable Energy Generation"])

    for code in to_pop:
        data.pop(code)

    # Write data to CSV
    with open(filename_out, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)


# Compile CO2 emissions per capita data from 2 CSVs and renewable vs
# non-renewable energy generation data from another into one CSV of features
def preprocess(filename1, filename2, filename3, filename_out):
    nit_data = compile_nit(filename1, filename2)
    re_data = compile_re(filename3)
    combine(nit_data, re_data, filename_out)
