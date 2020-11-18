def get_HRDPS_weather(coordinates, tz_info):
    # Query SpotWX
    response = requests.get('https://spotwx.com/products/grib_index.php?model=gem_lam_continental&%s&tz=%s&display=table' % (coordinates, tz_info)).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text = re.compile("var aDataSet =")))
    # Regex parsing
    m = re.search(r'\[.*\](?= )', scripts)
    m = m.group(0)
    data = re.findall(r'\[(.*?)\]', m)
    df = []
    for sets in data:
        sets = sets.split('\',\'')
        for s in sets:
            s = s.replace('\'', '')
        df.append(sets)
    # Create df and drop unwanted colmuns
    df = pd.DataFrame(columns = ["DATETIME", "DATE", "TIME", "TMP", 
                    "DPT", "RH", "WS", "WD", "APCP", "CLOUD", 
                    "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP", 
                    "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX"], data = df)
    # Correct data types from str input
    df["DATETIME"] = ''
    for i in range (0,len(df['TIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'FQP'] = float(df.at[i, 'FQP'])
        df.at[i, 'IQP'] = float(df.at[i, 'IQP'])
        df.at[i, 'DATE'] = datetime.datetime.strptime(df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(df.at[i, 'DATE'], df.at[i, 'TIME'])
    return df

def get_NAM_weather(coordinates, tz_info):
    # Query SpotWX
    response = requests.get('https://spotwx.com/products/grib_index.php?model=nam_awphys&%s&tz=%s&display=table' % (coordinates, tz_info)).text
    soup = BeautifulSoup(response, "lxml")
    scripts = str(soup.find_all('script', text = re.compile("var aDataSet =")))
    # Regex parsing
    m = re.search(r'\[.*\](?= )', scripts)
    m = m.group(0)
    data = re.findall(r'\[(.*?)\]', m)
    df = []
    for sets in data:
        sets = sets.split('\',\'')
        for s in sets:
            s = s.replace('\'', '')
        df.append(sets)
    # Create df and drop unwanted colmuns
    df = pd.DataFrame(columns = ["DATETIME", "DATE", "TIME", "TMP", 
                    "DPT", "RH", "WS", "WD", "WG", "APCP", "CLOUD", 
                    "SLP", "PTYPE", "RQP", "SQP", "FQP", "IQP",
                    "WS925", "WD925", "TMP850", "WS850", "WD850", "4LFTX", "HGT_0C_DB", "HGT_0C_WB"], data = df)
    # Correct data types from str input
    df["DATETIME"] = ''
    for i in range (0,len(df['DATETIME'])):
        df.at[i, 'WD'] = convert_compass(df.at[i, 'WD'])
        df.at[i, 'TMP'] = float(df.at[i, 'TMP'])
        df.at[i, 'WS'] = float(df.at[i, 'WS'])
        df.at[i, 'WG'] = float(df.at[i, 'WG'])
        df.at[i, 'CLOUD'] = float(df.at[i, 'CLOUD'])
        df.at[i, 'RQP'] = float(df.at[i, 'RQP'])
        df.at[i, 'SQP'] = float(df.at[i, 'SQP'])
        df.at[i, 'FQP'] = float(df.at[i, 'FQP'])
        df.at[i, 'IQP'] = float(df.at[i, 'IQP'])
        df.at[i, 'HGT_0C_DB'] = int(df.at[i, 'HGT_0C_DB'])
        df.at[i, 'DATE'] = datetime.datetime.strptime(df.at[i, 'DATE'], '%Y/%m/%d').date()
        df.at[i, 'TIME'] = datetime.datetime.strptime(df.at[i, 'TIME'], '%H:%M').time()
        df.at[i, 'DATETIME'] = datetime.datetime.combine(df.at[i, 'DATE'], df.at[i, 'TIME'])
    return df
  
def get_avy_forecast(avalanche_forecast):
    # Query Avcan API
    response = requests.get('https://www.avalanche.ca/api/forecasts/%s.json' % avalanche_forecast) #prod
    #response = requests.get('https://www.avalanche.ca/api/bulletin-archive/2020-01-07/%s.json' % avalanche_forecast) #testing
    data = response.json()
    return data