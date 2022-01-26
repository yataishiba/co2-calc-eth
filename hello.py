from codecs import getencoder
from pip import main
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("ETHERSCAN_API")

electricity_per_transaction = 8.4
kilowat_to_co2 = 0.85
co2_to_tree = 21


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    my_address = request.form["public_key"]
    response = requests.get(
        f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionCount&address={my_address}&tag=latest&apikey={API_KEY}")
    raw_data = response.json()
    print(raw_data)
    tx = raw_data["result"]
    tx_count = float.fromhex(tx)
    print(tx_count)
    electricity_consumption = tx_count * electricity_per_transaction
    co2 = electricity_consumption * kilowat_to_co2
    formatted_co2 = "{:.2f}".format(co2)
    tree = co2 / co2_to_tree
    formatted_tree = "{:.2f}".format(tree)
    return render_template("result.html", formatted_co2=formatted_co2, formatted_tree=formatted_tree)


if __name__ == "__main__":
    app.run(debug=True)
