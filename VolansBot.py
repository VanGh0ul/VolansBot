from aiogram.utils import executor
from create_bot import dp

import requests

async def on_startup(_): 
	print('Online')

from handlers import client, other

client.register_handlers_client(dp)

#admin.register_handlers_priceInfo(dp)

other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
