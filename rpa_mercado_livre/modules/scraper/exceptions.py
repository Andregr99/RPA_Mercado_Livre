class ScrapingError(Exception):
    def __init__(self, source: str, message: str = "Erro durante o scraping"):
        self.source = source
        self.message = f"{message} (fonte: {source})"
        super().__init__(self.message)