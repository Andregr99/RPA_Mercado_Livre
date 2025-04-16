import logging
from typing import Optional
import pandas as pd
from playwright.sync_api import sync_playwright
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

ML_URL = "https://www.mercadolivre.com.br/"

class ScrapingError(Exception):
    pass

@dataclass
class Produto:
    nome: str
    preco: float
    avaliacao: Optional[float]
    vendedor: Optional[str]
    qtd_avaliacoes: Optional[int]
    data_coleta: str

class MercadoLivreScraper:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    MAX_RESULTS = 10
    POPUP_SELECTORS = [
        "button[data-testid='action:understood-button']",
        "button[data-js='onboarding-cp-close']"
    ]
    
    def __init__(self, headless: bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=[
                "--start-maximized",
                "--window-position=0,0"
            ],
            channel="chrome",
            slow_mo=100
        )
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale='pt-BR',
            user_agent=self.USER_AGENT
        )
        self.page = self.context.new_page()

    def _fechar_popups(self):
        for selector in self.POPUP_SELECTORS:
            try:
                if self.page.locator(selector).count() > 0:
                    self.page.locator(selector).click(timeout=5000)
                    break
            except:
                continue

    def _verificar_bloqueio(self):
        try:
            return "captcha" in self.page.content().lower()
        except:
            return False

    def _extrair_dados_produto(self, item_locator):
        try:                
            return Produto(
                nome=item_locator.locator("h3.poly-component__title-wrapper > a").first.text_content(timeout=10000).strip(),
                preco=float(item_locator.locator("div.poly-price__current .andes-money-amount__fraction").first.text_content(timeout=10000).strip().replace(".", "").replace(",", ".")),
                avaliacao=float(item_locator.locator("span.poly-reviews__rating").first.text_content(timeout=10000)) if item_locator.locator("span.poly-reviews__rating").count() > 0 else None,
                vendedor=item_locator.locator("span.poly-component__seller").first.text_content(timeout=10000) if item_locator.locator("span.poly-component__seller").count() > 0 else None,
                qtd_avaliacoes=int(item_locator.locator("span.poly-reviews__total").first.text_content(timeout=10000).strip("()")) if item_locator.locator("span.poly-reviews__total").count() > 0 else None,
                data_coleta=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except Exception as e:
            logger.debug(f"Erro ao extrair produto: {str(e)}")
            return None

    def scrape(self, termo_busca: str) -> pd.DataFrame:
        try:
            self.page.goto(ML_URL, timeout=15000, wait_until="domcontentloaded")
            
            if self._verificar_bloqueio():
                logger.warning("Bloqueio por CAPTCHA detectado")
                return pd.DataFrame()
                
            self._fechar_popups()
            
            search_input = self.page.locator("input.nav-search-input")
            search_input.fill(termo_busca, timeout=10000)
            self.page.locator("button.nav-search-btn").click(timeout=10000)
            
            self.page.wait_for_selector("div.poly-card__content", timeout=15000)
            
            produtos = []
            items = self.page.locator("div.poly-card__content")
            
            for i in range(min(items.count(), self.MAX_RESULTS)):
                produto = self._extrair_dados_produto(items.nth(i))
                if produto:
                    produtos.append(produto)
            
            return pd.DataFrame([p.__dict__ for p in produtos if p is not None])
            
        except Exception as e:
            self.page.screenshot(path="erro.png")
            logger.error(f"Erro durante scraping: {str(e)}")
            raise ScrapingError("Mercado Livre") from e
        finally:
            self.close()

    def close(self):
        try:
            self.page.close()
            self.context.close()
            self.browser.close()
            self.playwright.stop()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()