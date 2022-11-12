
Welcome to etherscan.io API async python wrapper!
==========================================

Usage
-----

.. code-block:: python
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

            eth_balance = await es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')

            eth_balances = await es.get_eth_balances([
                '0x39eB410144784010b84B076087B073889411F878',
                '0x39eB410144784010b84B076087B073889411F879',
            ])

            gas_price = await es.get_gas_price()

            block = await es.get_block_by_number(block_number=12345)

            transactions = await es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')

            token_transactions = await es.get_token_transactions(
                contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
                address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
            )


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



or parallel run with gather:


.. code-block:: python
    import asyncio

    from aiohttp import ClientSession

    import aioetherscan


    async def main():
        session = ClientSession()
        es = aioetherscan.Client(
            api_key='YOUR_API_KEY',
            session=session
        )
        eth_price = es.get_eth_price()
        eth_supply = es.get_eth_supply()
        eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')
        eth_balances = es.get_eth_balances([
            '0x39eB410144784010b84B076087B073889411F878',
            '0x39eB410144784010b84B076087B073889411F879',
        ])
        gas_price = es.get_gas_price()
        block = es.get_block_by_number(block_number=12345)
        transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')
        token_transactions = es.get_token_transactions(
            contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
            address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
        )

        tasks = [
            eth_price,
            eth_supply,
            eth_balance,
            eth_balances,
            gas_price,
            block,
            transactions,
            token_transactions,
        ]

        res = await asyncio.gather(*tasks)

        session.close()

        print(f'res = {res}')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



or same but with aiohttp_client_cache https://pypi.org/project/aiohttp-client-cache/


.. code-block:: python
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

            eth_balance = await es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')

            eth_balances = await es.get_eth_balances([
                '0x39eB410144784010b84B076087B073889411F878',
                '0x39eB410144784010b84B076087B073889411F879',
            ])

            gas_price = await es.get_gas_price()

            block = await es.get_block_by_number(block_number=12345)

            transactions = await es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')

            token_transactions = await es.get_token_transactions(
                contract_address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
                address='0xEF68e7C694F40c8202821eDF525dE3782458639f',
            )


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


