import requests

def get_historic_serie(id, type):
    r = requests.get(f"https://gan.iacuft.org.br/api/{type}/seriehistorica/medias/{id}")
    return r.json()


def get_data_list(type):
    r = requests.get(f"https://gan.iacuft.org.br/api/{type}/list")
    return r.json()


class InterventionsDataType():
    VAZAO = "VAZAO"
    CONSUMO = "CONSUMO"
    COBRANCA = "COBRANCA"
    DURACAO = "DURACAO"


class StationsDataType():
    VAZAO = "VAZAO"
    NIVEL = "NIVEL"
    CHUVA = "CHUVA"


class Interventions:
    field_label = "intervencao"
    url = "intervencoes"
    name_label = "rotulo"


class Stations:
    field_label = "estacao"
    url = "estacoes"
    name_label = "nome"


def crawler_csv(type, datatype, outfile):
    intervention_list = get_data_list(type.url)

    interest_years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]
    interest_month = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
    interest_days = range(1, 32)

    with open(outfile, 'w') as f:

        header = f"id, rotulo"
        for y in interest_years:
            for m in interest_month:
                for d in interest_days:
                    header += f",{d}/{m}/{y}"

        f.write(header + "\n")
        print(header)

        for pump in intervention_list:
            id = pump[type.field_label]["id"]
            rotulo = pump[type.field_label][type.name_label]

            historic_serie = get_historic_serie(id, type.url)
            print(f"Processing id {id}")

            if 'Internal Server Error' in str(historic_serie):
                print(f"Erro in {id}")
                continue

            results = []

            data = [y for y in historic_serie if y["type"] == datatype]
            if data:
                data = data[0]
                for year in interest_years:
                    if year not in data["yearsAvailable"]:
                        for _ in interest_month:
                            for _ in interest_days:
                                results += [None]
                        continue

                    data_by_month = next(y for y in data["dataByYear"] if y["year"] == year)

                    for month in interest_month:
                        data_by_day = data_by_month["valuesByMonth"][month]

                        results += data_by_day["valorDiarios"]

            out = f"{id},{rotulo}"
            for r in results:
                out += f",{r}"

            f.write(out + "\n")
            # print(out)


if __name__ == "__main__":
    crawler_csv(Interventions, InterventionsDataType.VAZAO, "vazao1609.csv")
    #crawler_csv(Interventions, InterventionsDataType.CONSUMO, "consumo1609.csv")

    #crawler_csv(Stations, StationsDataType.VAZAO, "estacao_vazao16-09.csv")
    #crawler_csv(Stations, StationsDataType.NIVEL, "nivel16-09.csv")
    #crawler_csv(Stations, StationsDataType.CHUVA, "chuva16-09.csv")

