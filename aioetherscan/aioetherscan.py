# coding:utf-8
import os
import tempfile

import aiohttp_client_cache

from .errors import EtherscanIoException


class Client:

    def __init__(
            self,
            api_key: str,
            network=None,
            cache_backend='sqlite',
            cache_expire_after=5,
    ):

        # API URL
        self._api_url = 'https://api.etherscan.io/api'

        # API Key
        self._api_key = api_key

        # Network
        if network:
            if network not in ['ropsten', 'kovan', 'rinkeby']:
                raise Exception('network could only be None(mainnet) /ropsten/kovan/rinkeby')

            self._api_url = 'https://api-{network}.etherscan.io/api'.format(
                network=network
            )

        # params
        self._params = {
            'apikey': self._api_key,
        }

        # session & cache
        self._session = None
        self._cache_name = os.path.join(tempfile.gettempdir(), 'etherscan_cache')
        self._cache_backend = cache_backend
        self._cache_expire_after = cache_expire_after

    @property
    def _cache_type_factory(self):
        data = {
            'cache_name': self._cache_name,
            'expire_after': self._cache_expire_after
        }
        if self._cache_backend == 'CacheBackend':
            return aiohttp_client_cache.CacheBackend(**data)
        elif self._cache_backend == 'DynamoDBBackend':
            return aiohttp_client_cache.DynamoDBBackend(**data)
        elif self._cache_backend == 'FileBackend':
            return aiohttp_client_cache.FileBackend(**data)
        elif self._cache_backend == 'MongoDBBackend':
            return aiohttp_client_cache.MongoDBBackend(**data)
        elif self._cache_backend == 'RedisBackend':
            return aiohttp_client_cache.RedisBackend(**data)
        elif self._cache_backend == 'SQLiteBackend':
            return aiohttp_client_cache.SQLiteBackend(**data)
        else:
            return aiohttp_client_cache.CacheBackend(self._cache_name or 'demo_cache')

    @property
    def session(self):
        if not self._session:
            self._session = aiohttp_client_cache.CachedSession(
                cache=self._cache_type_factory
            )
            self._session.headers.update(
                {
                    'User-agent': 'aioetherscan - python wrapper '
                                  'around etherscan.io (github.com/viacheslav-sabadash/aioetherscan)'
                }
            )

        return self._session

    async def __req(self):
        async with self._session as session:
            async with session.post(url=self._api_url, data=self._params) as resp:
                r = await resp.json()

        if '0' == r['status']:
            print('--- Etherscan.io Message ---', r['message'])

        return r['result']

    async def __proxy_req(self):
        self._params['module'] = 'proxy'

        # get, json
        async with self._session as session:
            async with session.get(url=self._api_url, data=self._params) as resp:
                r = await resp.json()

        # todo: handle exceptions

        return r['result']

    @staticmethod
    def __bool(x: str):
        """Convert str to bool"""
        if x.lower() in ['0', 'false', 'none', 'null', 'n/a', '']:
            return False
        return True

    @staticmethod
    def __int(x: str):
        """Convert str to int or None"""
        if x == '':
            return None
        return int(x)

    @staticmethod
    def __str(x: str):
        """Return str or None"""
        if x == '':
            return None
        return x

    async def get_eth_price(self):
        """Get ETH price."""
        self._params['module'] = 'stats'
        self._params['action'] = 'ethprice'

        r = await self.__req()

        return {
            'ethbtc': float(r['ethbtc']),
            'ethbtc_timestamp': int(r['ethbtc_timestamp']),
            'ethusd': float(r['ethusd']),
            'ethusd_timestamp': int(r['ethbtc_timestamp']),
        }

    async def get_eth_supply(self):
        self._params['module'] = 'stats'
        self._params['action'] = 'ethsupply'

        return int(await self.__req())

    async def get_eth_balance(self, address: str):
        """Get ETH balance by address."""
        self._params['module'] = 'account'
        self._params['action'] = 'balance'
        self._params['address'] = address

        return int(await self.__req())

    async def get_eth_balances(self, addresses: list):
        """Get ETH balances by addresses list."""
        self._params['module'] = 'account'
        self._params['action'] = 'balancemulti'
        self._params['address'] = ','.join(addresses)

        balances = {}
        rs = await self.__req()
        for row in rs:
            balances[row['account']] = int(row['balance'])

        return balances

    def __transaction(self, source: dict):
        """Repack the __transaction dict"""
        return {
            'timestamp': self.__int(source['timeStamp']),
            'block_number': self.__int(source['blockNumber']),

            'from': self.__str(source['from']),
            'to': self.__str(source['to']),
            'input': self.__str(source['input']),
            'hash': self.__str(source['hash']),
            'value': self.__int(source['value']),

            'gas': self.__int(source['gas']),
            'gas_price': self.__int(source['gasPrice']),
            'gas_used': self.__int(source['gasUsed']),
            'nonce': self.__int(source['nonce']),
            'confirmations': self.__int(source['confirmations']),

            'is_error': self.__bool(source['isError']),
            'tx_receipt_status': self.__bool(source['txreceipt_status']),

            'transaction_index': self.__int(source['transactionIndex']),
            'cumulative_gas_used': self.__int(source['cumulativeGasUsed']),

            'block_hash': self.__str(source['blockHash']),
        }

    async def get_transactions_by_address(
            self,
            address: str,
            type: str = 'normal',
            start_block: int = 0,
            end_block: int = 999999999,
            page: int = 1,
            limit: int = 1000,
            sort: str = 'asc',
    ):
        """Get transactions by address."""
        self._params['module'] = 'account'

        if type == 'normal':
            self._params['action'] = 'txlist'
        elif type == 'internal':
            self._params['action'] = 'txlistinternal'
        else:
            raise Exception('param `type` must be "normal" or "internal"')

        self._params['address'] = address
        self._params['startblock'] = start_block
        self._params['endblock'] = end_block
        self._params['page'] = page
        self._params['offset'] = limit
        self._params['sort'] = sort

        rs = await self.__req()

        transactions = []
        for t in rs:
            transactions.append(self.__transaction(t))

        return transactions

    def __token_transaction(self, source: dict):
        """Repack the token __transaction dict"""
        return {
            'timestamp': self.__int(source['timeStamp']),
            'block_number': self.__int(source['blockNumber']),

            'from': self.__str(source['from']),
            'to': self.__str(source['to']),
            'input': self.__str(source['input']),
            'hash': self.__str(source['hash']),
            'value': self.__int(source['value']),

            'gas': self.__int(source['gas']),
            'gas_price': self.__int(source['gasPrice']),
            'gas_used': self.__int(source['gasUsed']),
            'nonce': self.__int(source['nonce']),
            'confirmations': self.__int(source['confirmations']),

            'contract_address': self.__str(source['contractAddress']),
            'token_decimal': self.__int(source['tokenDecimal']),
            'token_name': self.__str(source['tokenName']),
            'token_symbol': self.__str(source['tokenSymbol']),

            'transaction_index': self.__int(source['transactionIndex']),
            'cumulative_gas_used': self.__int(source['cumulativeGasUsed']),
            'block_hash': self.__str(source['blockHash']),
        }

    async def get_token_transactions(
            self,
            contract_address: str = None,
            address: str = None,
            start_block: int = 0,
            end_block: int = 999999999,
            page: int = 1,
            limit: int = 1000,
            sort: str = 'asc',
    ):
        """Get ERC20 token transactions by contract address."""
        if contract_address is None and address is None:
            raise EtherscanIoException('Param `contract_address` and `address` cannot be None at the same time.')

        self._params['module'] = 'account'
        self._params['action'] = 'tokentx'

        if contract_address:
            self._params['contractaddress'] = contract_address

        if address:
            self._params['address'] = address

        self._params['startblock'] = start_block
        self._params['endblock'] = end_block
        self._params['page'] = page
        self._params['offset'] = limit
        self._params['sort'] = sort

        rs = await self.__req()

        token_transactions = []
        for t in rs:
            token_transactions.append(self.__token_transaction(t))

        return token_transactions

    async def get_gas_price(self):
        """Get gas price."""
        self._params['action'] = 'eth_gasPrice'

        return int(await self.__proxy_req(), 16)

    async def get_block_number(self):
        """Get latest block number."""
        self._params['action'] = 'eth_blockNumber'

        return int(await self.__proxy_req(), 16)

    async def get_block_by_number(self, block_number):
        """Get block by number."""
        self._params['action'] = 'eth_getBlockByNumber'
        self._params['tag'] = hex(block_number)
        self._params['boolean'] = True

        return await self.__proxy_req()
