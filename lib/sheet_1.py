

def readCsvAsString(filePath, sep=","):
    """Leggi un file csv e crea un dataframe associato.
    utile quando il file csv non ha un numero di colonne 
    fisse e questo crea problemi con read_csv di pandas

    Args:
        filePath (_type_): _description_
    """        
    import pandas as pd
    # 1. Leggi il file CSV come file di testo
    with open(filePath, 'r') as file:
        lines = file.readlines()

    # 2. Dividi ogni riga sui `;`
    lines = [line.strip().split(sep) for line in lines]

    # 3. Trova il numero massimo di colonne
    max_columns = max(len(line) for line in lines)

    # 4. Crea un DataFrame vuoto con il numero massimo di colonne
    df = pd.DataFrame(columns=range(max_columns))

    # 5. Riempi il DataFrame con le righe del file CSV
    for index, line in enumerate(lines):
        df.loc[index] = pd.Series(line)

    # 6. Se vuoi togliere i NaN e mettere valori stringa vuoti
    df = df.fillna("")

    print(df)
    return df


