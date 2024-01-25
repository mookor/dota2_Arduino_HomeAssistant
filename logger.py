import loguru

class Logger:
    logger = loguru.logger
    logger.add("bot.log")

    @classmethod
    def info(cls, message):
        cls.logger.info(message)
    
    @classmethod
    def error(cls, message):
        cls.logger.error(message)