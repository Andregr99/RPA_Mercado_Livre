import math
import pandas as pd
import os
import mysql.connector
from dotenv import load_dotenv
from typing import List, Dict
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME")
    )

def insert_produto(produto: Dict) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, preco, avaliacao, vendedor, qtd_avaliacoes, data_coleta) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                produto['nome'],
                produto['preco'],
                produto['avaliacao'],
                produto['vendedor'],
                produto['qtd_avaliacoes'],
                produto['data_coleta']
            )
        )
        conn.commit()
    except mysql.connector.Error as err:
        logger.error(f"Erro ao inserir produto: {err}")
    finally:
        cursor.close()
        conn.close()

def batch_insert_produtos(produtos: List[Dict]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    produtos_limpos = []
    for produto in produtos:
        produto_limpo = {
            key: None if (isinstance(value, float) and math.isnan(value)) or pd.isna(value) else value
            for key, value in produto.items()
        }
        produtos_limpos.append(produto_limpo)
    
    try:
        cursor.executemany(
            "INSERT INTO produtos (nome, preco, avaliacao, vendedor, qtd_avaliacoes, data_coleta) VALUES (%s, %s, %s, %s, %s, %s)",
            [
                (
                    p['nome'],
                    p['preco'],
                    p['avaliacao'],
                    p['vendedor'],
                    p['qtd_avaliacoes'],
                    p['data_coleta']
                ) for p in produtos_limpos  
            ]
        )
        conn.commit()
    except mysql.connector.Error as err:
        logger.error(f"Erro ao inserir produtos em lote: {err}")
    finally:
        cursor.close()
        conn.close()