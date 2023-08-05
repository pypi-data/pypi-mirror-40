'''Methods to connect N-Tier to aiohttp'''
from http import (HTTPStatus)
from typing import (Any, Mapping, Optional, Sequence, TypeVar, Union)
from aiohttp.web import (Request, Response, json_response)
from multidict import (MultiDict)
from ntier import (TransactionBase, TransactionCode, TransactionResult)
from webdi import (Container)

PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 25
PAGE_KEY = 'page'
PER_PAGE_KEY = 'per_page'
TOTAL_RECORDS_KEY = 'total_records'
TOTAL_PAGES_KEY = 'total_pages'
PAGING_KEY = 'paging'
DATA_KEY = 'data'
ERRORS_KEY = 'errors'
TRANSACTION_CODE_MAP = {
    TransactionCode.success: HTTPStatus.OK,
    TransactionCode.found: HTTPStatus.OK,
    TransactionCode.created: HTTPStatus.CREATED,
    TransactionCode.updated: HTTPStatus.OK,
    TransactionCode.not_changed: HTTPStatus.OK,
    TransactionCode.deleted: HTTPStatus.OK,
    TransactionCode.failed: HTTPStatus.BAD_REQUEST,
    TransactionCode.not_found: HTTPStatus.NOT_FOUND,
    TransactionCode.not_authenticated: HTTPStatus.UNAUTHORIZED,
    TransactionCode.not_authorized: HTTPStatus.FORBIDDEN,
    TransactionCode.not_valid: HTTPStatus.UNPROCESSABLE_ENTITY,
}
Data = Mapping[str, Any]
T = TypeVar('T')

def set_paging(transaction: TransactionBase, data: Data) -> None:
  '''Sets paging on a transaction class based on query string args.'''
  page_str: Optional[str] = data.get(PAGE_KEY)
  per_page_str: Optional[str] = data.get(PER_PAGE_KEY)
  page: Optional[int] = None
  per_page: Optional[int] = None

  try:
    if page_str:
      page = int(page_str)
    if per_page_str:
      per_page = int(per_page_str)
  except ValueError:
    page = PAGE_DEFAULT
    per_page = PER_PAGE_DEFAULT

  if not (page or per_page):
    return

  if not page:
    page = PAGE_DEFAULT
  if not per_page:
    per_page = PER_PAGE_DEFAULT

  transaction.set_paging(page, per_page)

def map_transaction_code(code: TransactionCode) -> HTTPStatus:
  '''Map a TransactionCode to an HTTPStatus code.'''
  status_code = TRANSACTION_CODE_MAP.get(code)
  if status_code is None:
    raise Exception(f'Unrecognized transaction code: {code}')
  return status_code

def head_if_one(items: Sequence[T]) -> Union[T, Sequence[T]]:
  '''Returns the first item in a list if the list has just one item, otherwise the whole list.'''
  if len(items) == 1:
    return items[0]
  return items

def demultidict(data: MultiDict) -> Data:
  '''Turns a multidict into a regular dict, where keys with multiple items have list values.'''
  return {k: head_if_one(data.getall(k)) for k in data}

async def build_transaction_data(request: Request) -> Data:
  '''Build a dict from a Request object.'''
  data = MultiDict(request.query)
  data.extend(request.match_info)
  if request.can_read_body:
    body = await request.json()
    data.extend(body)
  return demultidict(data)

async def execute_transaction(
    transaction_name: str,
    container: Container,
    request: Request,
) -> Response:
  '''Call a transaction with data from a request and build a JSON response.'''
  data = await build_transaction_data(request)
  transaction = container.get(transaction_name)
  set_paging(transaction, data)
  result = await transaction(data)
  http_status = map_transaction_code(result.status_code)

  if http_status < HTTPStatus.BAD_REQUEST:
    result_data = {DATA_KEY: result.payload}
    if result.has_paging:
      result_data[PAGING_KEY] = {
          PAGE_KEY: result.paging.page,
          PER_PAGE_KEY: result.paging.per_page,
          TOTAL_RECORDS_KEY: result.paging.total_records,
          TOTAL_PAGES_KEY: result.paging.total_pages,
      }
    return json_response(result_data, status=http_status)

  result_data = {ERRORS_KEY: result.payload}
  return json_response(result_data, status=http_status)
