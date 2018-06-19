import json
import csv
from web3.utils.formatters import hex_to_integer


def main():
    with open('balance/balance_0.json') as data_file:
        data = json.loads(data_file.read())
        state = data['state']

    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for address in state:
            writer.writerow([address,
                             hex_to_integer(state[address]['balance'])])


main()
