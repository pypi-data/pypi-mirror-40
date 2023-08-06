'''Concrete base classes for transactions.'''
# pylint: disable=too-few-public-methods,invalid-name
from multidict import (MultiDict)
import ntier as N

TransactionData = N.TransactionData[MultiDict]

class APITransactionBase(N.APITransactionBase[MultiDict]):
  pass
