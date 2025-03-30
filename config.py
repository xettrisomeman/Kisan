MAIN_URL = "http://localhost:8000/"

ADD_GOOD_URL = MAIN_URL + "goods/add"
DELETE_GOOD_URL = MAIN_URL + "goods/delete"
LIST_GOOD_URL = MAIN_URL + "goods/show"
EDIT_GOOD_URL = MAIN_URL + "goods/edit"
DETAIL_GOOD_URL = MAIN_URL + "goods/detail/{id}"
SEARCH_GOOD_URL = MAIN_URL + "goods/search"

REGISTER_USER_URL = MAIN_URL + "auth/register"
LOGIN_USER_URL = MAIN_URL + "auth/login"
CURRENT_USER_URL = MAIN_URL + "auth/me"

BUY_GOODS_URL = MAIN_URL + "order/buy"
SHOW_HISTORY_URL = MAIN_URL + "order/show/history"
BUY_PENDING_HISTORY = MAIN_URL + "order/show/buy_requests/pending"
INCOMING_ORDER_PENDING_HISTORY = MAIN_URL + "order/show/incoming_requests/pending"
CANCEL_PENDING_ORDER = MAIN_URL + "order/cancel/buy/{id}"
ACCEPT_PENDING_ORDER = MAIN_URL + "order/accept/{order_item_id}"

ASK_EXPERT_DB = "./database/ask_expert.json"
