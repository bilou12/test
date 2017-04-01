import charts

aapl = charts.data.aapl()
msft = charts.data.msft()
ohlc = charts.data.ohlc()

ohlc['display'] = False

series = [
    aapl,
    msft,
    ohlc
]

options = dict(height=400, title=dict(text='My first chart!'))

charts.plot(series, options, stock=True, show='inline')
