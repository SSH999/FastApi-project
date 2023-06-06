import datetime as dt
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query

app = FastAPI()

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="asset_class", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrument_id", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrument_name", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="trade_date_time", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="trade_details", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="trade_id", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

trades_db = [
    Trade(
        asset_class="Equity",
        counterparty="ABC Corp",
        instrument_id="AAPL",
        instrument_name="Apple Inc",
        trade_date_time=dt.datetime.now(),
        trade_details=TradeDetails(
            buySellIndicator="BUY",
            price=100.0,
            quantity=10
        ),
        trade_id="1",
        trader="Mohan Raj"
    ),
    Trade(
        asset_class="Bond",
        counterparty="XYZ Bank",
        instrument_id="TSLA",
        instrument_name="Tesla Inc",
        trade_date_time=dt.datetime.now(),
        trade_details=TradeDetails(
            buySellIndicator="SELL",
            price=500.0,
            quantity=5
        ),
        trade_id="2",
        trader="Roy Smith"
    ),
    Trade(
        asset_class="Equity",
        counterparty="DEF Corp",
        instrument_id="GOOGL",
        instrument_name="Alphabet Inc",
        trade_date_time=dt.datetime.now(),
        trade_details=TradeDetails(
            buySellIndicator="BUY",
            price=2000.0,
            quantity=2
        ),
        trade_id="3",
        trader="Patt Johnson"
    ),
    Trade(
        asset_class="FX",
        instrument_id="EURUSD",
        instrument_name="Euro/US Dollar",
        trade_date_time=dt.datetime.now(),
        trade_details=TradeDetails(
            buySellIndicator="SELL",
            price=1.2,
            quantity=10000
        ),
        trade_id="4",
        trader="Raj Anand"
    ),
    Trade(
        asset_class="Equity",
        counterparty="GHI Bank",
        instrument_id="AMZN",
        instrument_name="Amazon.com Inc",
        trade_date_time=dt.datetime.now(),
        trade_details=TradeDetails(
            buySellIndicator="BUY",
            price=3000.0,
            quantity=3
        ),
        trade_id="5",
        trader="Sam Wilson"
    ),

]


# Endpoint to fetch a list of trades with pagination and sorting
@app.get("/trades")
def get_trades(
    search: Optional[str] = Query(None, description="Search query"),
    assetClass: Optional[str] = Query(None, description="Asset class of the trade"),
    start: Optional[dt.datetime] = Query(None, description="Minimum date for tradeDateTime"),
    end: Optional[dt.datetime] = Query(None, description="Maximum date for tradeDateTime"),
    minPrice: Optional[float] = Query(None, description="Minimum value for tradeDetails.price"),
    maxPrice: Optional[float] = Query(None, description="Maximum value for tradeDetails.price"),
    tradeType: Optional[str] = Query(None, description="Trade type (BUY or SELL)"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return for pagination"),
    sort_by: Optional[str] = Query(None, description="Field to sort the trades by")
) -> List[Trade]:
    filtered_trades = trades_db

    if search:
        filtered_trades = [trade for trade in filtered_trades if search.lower() in str(trade).lower()]

    if assetClass:
        filtered_trades = [trade for trade in filtered_trades if trade.asset_class == assetClass]

    if start:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_date_time >= start]

    if end:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_date_time <= end]

    if minPrice:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price >= minPrice]

    if maxPrice:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price <= maxPrice]

    if tradeType:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.buySellIndicator == tradeType]

    if sort_by:
        filtered_trades.sort(key=lambda trade: getattr(trade, sort_by), reverse=False)

    return filtered_trades[skip : skip + limit]

# Endpoint to fetch a single trade by ID
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str) -> Optional[Trade]:
    for trade in trades_db:
        if trade.trade_id == trade_id:
            return trade
    return None

