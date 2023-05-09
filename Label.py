from Pacotes_Lutzer.convert import convert_ms_to_datetime

data = convert_ms_to_datetime("Apostas.csv", "datetime")
print(data[['id', "add", "datetime"]].head())
