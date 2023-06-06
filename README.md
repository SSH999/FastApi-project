# FastApi-project
# Trade Management
The Trade Management System is a simple API that allows us to manage and retrieve trade information. It provides endpoints to fetch a list of trades, fetch a single trade by ID, and perform filtering, sorting, and pagination on the trade data.

Data Models
The trade data is modeled using Pydantic, a library for data validation and serialization. Two main data models are used:

TradeDetails
Represents the details of a trade, including the buySellIndicator (BUY or SELL), price, and quantity.

Trade
Represents a trade, including fields such as asset_class, counterparty, instrument_id, instrument_name, trade_date_time, trade_details, trade_id, and trader. The trade_details field is an instance of the TradeDetails model.

Mocked Database
A mocked database, trades_db, is used to store the trade data. It is a list of Trade objects and is used to simulate the retrieval of trade data from a database or external source. For testing purposes, the mocked database contains a few sample trades.

Fetching Trades
The /trades endpoint is used to fetch a list of trades. It supports various query parameters for filtering, sorting, and pagination. The available query parameters are:

search: Filters trades based on a search query.
assetClass: Filters trades based on the asset class.
start: Filters trades with a minimum trade date.
end: Filters trades with a maximum trade date.
minPrice: Filters trades with a minimum trade price.
maxPrice: Filters trades with a maximum trade price.
tradeType: Filters trades based on the trade type (BUY or SELL).
skip: Number of records to skip for pagination.
limit: Number of records to return for pagination.
sort_by: Field to sort the trades by.
The endpoint applies the specified filters, pagination, and sorting to the trades_db and returns the filtered and sorted trades.

Fetching Single Trade by ID
The /trades/{trade_id} endpoint is used to fetch a single trade by its ID. It takes a path parameter trade_id, which represents the ID of the trade to fetch. The endpoint searches the trades_db for a trade with the specified ID and returns it if found. If no trade is found with the given ID, it returns None.

Testing the API
To test the Trade Management System API, we can run the code and make HTTP requests to the specified endpoints using tools like curl or API testing tools like Postman or Insomnia.

To fetch a list of trades, make a GET request to /trades with optional query parameters to apply filters, sorting, and pagination.
To fetch a single trade by ID, make a GET request to /trades/{trade_id}, where {trade_id} is the ID of the trade we want to fetch.
