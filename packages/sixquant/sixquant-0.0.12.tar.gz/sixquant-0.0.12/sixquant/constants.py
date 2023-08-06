# coding=utf-8

INDEX_SH = 'IDX.000001'  # 上证指数
INDEX_SZ = 'IDX.399001'  # 深证成指
INDEX_CY = 'IDX.399006'  # 创业板指
INDEX_SH50 = 'IDX.000016'  # 上证50
INDEX_HS300 = 'IDX.000300'  # 沪深300

INDEXS = [INDEX_SH, INDEX_SZ, INDEX_CY, INDEX_SH50, INDEX_HS300]
INDEX_NAMES = ['上证指数', '深证成指', '创业板指', '上证50', '沪深300']

# =========================================================

THRESHOLD_SMALL_CAP = 20 * 10000 * 10000  # 小市值阈值，流通市值（20亿）

# =========================================================

DATA_SERVER_URL = 'http://112.125.89.20/v1/api/stock'
#DATA_SERVER_URL = 'http://127.0.0.1:8888'

CONCEPTS_FILE = DATA_SERVER_URL + '/concepts'

TODAY_FILE = DATA_SERVER_URL + '/today'

TODAY_SMALL_FILE = DATA_SERVER_URL + '/today/small'
TODAY_SMALL_NO_ST_NO_SUBNEW_FILE = DATA_SERVER_URL + '/today/small_no_st_no_subnew'

TODAY_QUOTE_FILE = DATA_SERVER_URL + '/today/quote'
TODAY_MONEY_FILE = DATA_SERVER_URL + '/today/money'

# =========================================================
API_SERVER_URL = 'http://112.125.89.20'
#API_SERVER_URL = 'http://127.0.0.1:8888'
# API_SERVER_URL = 'http://127.0.0.1:8888/api/v1/stock'
API_STOCK_URL = API_SERVER_URL + '/api/v1/stock'

HOLYDAYS_FILE = API_SERVER_URL + '/api/v1/holydays'

NAMES_URL = API_STOCK_URL + '/names'
BASICS_URL = API_STOCK_URL + '/basics'

SUMMARY_LIST_URL = API_STOCK_URL + '/s/summary'

MARKET_GUAUGE_URL = API_STOCK_URL + '/d/market/gauge'
MARKET_COUNTDIST_URL = API_STOCK_URL + '/d/market/countdist'
MARKET_CRAZY_COUNT_URL = API_STOCK_URL + '/d/market/crazy'
CATEGORY_CRAZY_COUNT_URL = API_STOCK_URL + '/d/market/ccrazy'

MARKET_COUNT_URL = API_STOCK_URL + '/m/market/count'

MARKET_MONEY_URL = API_STOCK_URL + '/m/market/money'
MARKET_MONEY_HGT_URL = API_STOCK_URL + '/m/market/moneyhgt'
MARKET_MONEY_SGT_URL = API_STOCK_URL + '/m/market/moneysgt'

MARKET_RATE_URL = API_STOCK_URL + '/m/market/rate'
MARKET_ORDER_URL = API_STOCK_URL + '/m/market/order'

MARKET_CHIPS_URL = API_STOCK_URL + '/d/chips'

INDEX_MINUTELY = API_STOCK_URL + '/m/index'
INDEX_MINUTELY_SH = API_STOCK_URL + '/m/index/sh'
INDEX_MINUTELY_SZ = API_STOCK_URL + '/m/index/sz'
INDEX_MINUTELY_CY = API_STOCK_URL + '/m/index/cy'
INDEX_MINUTELY_HS = API_STOCK_URL + '/m/index/hs'
INDEX_MINUTELY_300 = API_STOCK_URL + '/m/index/300'
INDEX_MINUTELY_50 = API_STOCK_URL + '/m/index/50'

CATEGORIES_HEATMAP_URL = API_STOCK_URL + '/d/categories/heatmap'

MONEY_DAILY = API_STOCK_URL + '/d/money'
QUOTE_DAILY = API_STOCK_URL + '/d/quote'
INDEX_DAILY = API_STOCK_URL + '/d/index'

QUOTE_REAL = API_STOCK_URL + '/r/quote'
INDEX_REAL = API_STOCK_URL + '/r/index'

QUOTES_BASIC_DAILY = API_STOCK_URL + '/d/quotes'
QUOTES_QUANT_DAILY = API_STOCK_URL + '/d/quants'

CRAZY_HEATMAP_URL = API_STOCK_URL + '/d/crazy/heatmap'

CRAZY_DAILY_ZT = API_STOCK_URL + '/d/crazy/list/zt'
CRAZY_DAILY_ZB = API_STOCK_URL + '/d/crazy/list/zb'
CRAZY_DAILY_DT = API_STOCK_URL + '/d/crazy/list/dt'

# =========================================================

BUNDLE_SERVER_URL = 'http://oyiztpjzn.bkt.clouddn.com/'
