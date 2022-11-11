# async Etherscan.io API wrapper

An async Etherscan.io API wrapper, for Python.

Based on [https://github.com/neoctobers/etherscan](https://github.com/neoctobers/etherscan) ([@neoctobers](https://github.com/neoctobers))
[https://pypi.org/project/etherscan/](https://pypi.org/project/etherscan/)

## Installation
```
pip3 install aioetherscan
```

## Usage

```python
import asyncio

import aiohttp
import aioetherscan


async def main():
    
    async with aiohttp.ClientSession() as session:
        es = aioetherscan.Client(
            api_key='YOUR_API_KEY',
            session=session
        )
        
        eth_price = await es.get_eth_price()
    
        eth_supply = await es.get_eth_supply()
        
        eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')
        
        eth_balances = es.get_eth_balances([
            '0x39eB410144784010b84B076087B073889411F878',
            '0x39eB410144784010b84B076087B073889411F879',
        ])
        
        gas_price = es.get_gas_price()
        
        block = es.get_block_by_number(block_number=12345)
        
        transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')
        
        token_transations = es.get_token_transactions(
            contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
            address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
        )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

or with [aiohttp_client_cache](https://pypi.org/project/aiohttp-client-cache/)


```python
import asyncio

from aiohttp_client_cache import CachedSession, SQLiteBackend
import aioetherscan


async def main():
    
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        es = aioetherscan.Client(
            api_key='YOUR_API_KEY',
            session=session
        )
        
        eth_price = await es.get_eth_price()
    
        eth_supply = await es.get_eth_supply()
        
        eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')
        
        eth_balances = es.get_eth_balances([
            '0x39eB410144784010b84B076087B073889411F878',
            '0x39eB410144784010b84B076087B073889411F879',
        ])
        
        gas_price = es.get_gas_price()
        
        block = es.get_block_by_number(block_number=12345)
        
        transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')
        
        token_transations = es.get_token_transactions(
            contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
            address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
        )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
