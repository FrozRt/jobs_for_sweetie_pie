async def on_startup(dp):
    import filters
    import middlewares

    filters.setup(dp)
    middlewares.setup(dp)

    from core.db_api.init_db import HHDatabaseInit
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)
    await HHDatabaseInit().expand_database()


if __name__ == "__main__":
    from aiogram import executor

    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
