### QUICK BUILD OF ASSETS UNIVERSE
fx_universe = {
    "USD": {"Name": "USD", "Ticker": "USDSGD=X"},
    "EUR": {"Name": "EUR", "Ticker": "EURSGD=X"},
    "GBP": {"Name": "GBP", "Ticker": "GBPSGD=X"},
}

asset_universe = {
    "TSLA": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Tesla"},
    "COIN": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Coinbase"},
    "SNOW": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Snowflake"},
    "SPCE": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Virgin Galactic"},
    "HOOD": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Robinhood"},
    "META": {"Ccy": "USDSGD=X", "Type": "Listed_Stock", "Class": "Investment", "Name": "Meta Inc."},
    "USDSGD=X": {"Ccy": "USDSGD=X", "Type": "Currency", "Class": "Cash", "Name": "USD"},
    "SGD": {"Ccy": "SGD",  "Type": "Currency", "Class": "Cash", "Name": "SGD"},
    "EURSGD=X": {"Ccy": "EURSGD=X",  "Type": "Currency", "Class": "Cash", "Name": "EUR"},
    "PDD": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Pinduoduo"},
    "ABNB": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Airbnb"},
    "NVDA": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Nvidia"},
    "TOST": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Toast"},
    "ETH-USD": {"Ccy": "USDSGD=X",  "Type": "Crypto", "Class": "Investment", "Name": "Ethereum"},
    "SOL-USD": {"Ccy": "USDSGD=X",  "Type": "Crypto", "Class": "Investment", "Name": "Solana"},
    "KAPE.L": {"Ccy": "GBPSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Kape Technologies"},
    "PBEE.L": {"Ccy": "GBPSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Pensionbee"},
    "SGRO.L": {"Ccy": "GBPSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Segro"},
    "GBPSGD=X": {"Ccy": "GBPSGD=X",  "Type": "Currency", "Class": "Cash", "Name": "GBP"},
    "MKTX": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "MarketAxess Holdings"},
    "SCHW": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Charles Schwab"},
    "TSM": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Taiwan SMC"},
    "GROW.L": {"Ccy": "GBPSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Molten Ventures Plc"},
    "AT1.L": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Invesco AT1 Capital Bond ETF"},
    "BIRD": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Allbirds"},
    "VET": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Vermilon Energy"},
    "ARCH": {"Ccy": "USDSGD=X",  "Type": "Listed_Stock", "Class": "Investment", "Name": "Arch Resources"},
    "Venture_asset_1": {"Ccy": "USDSGD=X",  "Type": "Unlisted_shares", "Class": "Venture", "Name": "Venture_asset_1"},
    "Venture_asset_2": {"Ccy": "USDSGD=X",  "Type": "Unlisted_shares", "Class": "Venture", "Name": "Venture_asset_2"}
}

### EXTRACTING THE LIST OF INVESTMENTS IN ASSET UNIVERSE
asset_universe_inv = {k:v for (k,v) in asset_universe.items() if "Investment" in v["Class"] or "Venture" in v["Class"]}
investments = asset_universe_inv.keys()

### EXTRACTING THE LIST OF LISTED INVESTMENTS IN ASSET UNIVERSE
asset_universe_listed_inv = {k:v for (k,v) in asset_universe.items() if "Investment" in v["Class"]}
listed_investments = asset_universe_listed_inv.keys()

### EXTRACTING THE LIST OF NON LISTED INVESTMENTS IN ASSET UNIVERSE
asset_universe_non_listed_inv = {k:v for (k,v) in asset_universe.items() if "Collectible" in v["Class"] or "Venture" in v["Class"]}
non_listed_investments = asset_universe_non_listed_inv.keys()

### EXTRACTING THE LIST OF UK STOCKS IN ASSET UNIVERSE
uk_stocks_dict = {k:v for (k,v) in asset_universe.items() if "GBPSGD=X" in v["Ccy"] and "Investment" in v["Class"]}
uk_stocks = list(uk_stocks_dict.keys())
uk_stocks

