import math
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from rpa_mercado_livre.modules.scraper.mercado_livre_scraper import MercadoLivreScraper
from rpa_mercado_livre.modules.database.db_handler import batch_insert_produtos
from rpa_mercado_livre.config.logger import logger

def main():
    try:
        logger.info("Iniciando busca no Mercado Livre")
        scraper = MercadoLivreScraper()
        df = scraper.scrape("teclado mecanico")

        if df.empty:
            logger.warning("Nenhum produto encontrado")
            return

        produtos = df.where(pd.notna(df), None).to_dict('records')
        batch_insert_produtos(produtos)
        
        logger.info(f"{len(df)} produtos processados com sucesso")

    except Exception as e:
        logger.error(f"Erro no processo principal: {str(e)}")

if __name__ == "__main__":
    main()