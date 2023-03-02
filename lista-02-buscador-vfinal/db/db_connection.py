import datetime
import sqlite3
import requests
import requests_cache
import requests
import sys
sys.path.append('./classes')
from pagina import Pagina


def connect_db():
    try:
# Conectar ao banco de dados
        conn = sqlite3.connect('novo_buscador.db')

# Criar uma tabela se ela ainda não existir
        conn.execute('''
    CREATE TABLE IF NOT EXISTS paginas (
    url TEXT PRIMARY KEY,
    response TEXT,
    response_time INT,
    updated_at TEXT NOT NULL
);

''')
        conn.close()
    except Exception as e:
        print('erro: ', e)
        return

def inserir_pagina_no_banco(pagina):
    try:
        conn = sqlite3.connect('novo_buscador.db')
        cursor = conn.cursor()
    
    # Insere a página na tabela 'paginas'now = datetime.datetime.now()
    
        cursor.execute("INSERT INTO paginas (url, response, response_time, updated_at) VALUES (?, ?, ?)", 
                   (pagina._url, pagina._response, pagina._response_time, pagina._updated_at))
    
    # Salva as mudanças e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('erro: ', e)
        return
    
# Função que faz a requisição HTTP e retorna o conteúdo da página
def obter_pagina(url):
    connect_db()
    conn = sqlite3.connect('novo_buscador.db')

    # Verificar se a página já foi salva no banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paginas WHERE url=?", (url,))
    resultado = cursor.fetchone()
    conn.close()

    
    if resultado is not None:
        last_updated = datetime.datetime.strptime(resultado[3],'%Y-%m-%d %H:%M:%S') 
        latencia = datetime.datetime.now() - datetime.timedelta(days=1)
        if last_updated >= latencia:
        # A página já foi salva no banco de dados, retornar o conteúdo salvo
            return resultado[1]
        else:
            try:
                requests_cache.install_cache('nome_do_arquivo_cache', expire_after=3600)
                response = requests.get(url, verify=False)
                response_time = response.elapsed.total_seconds()
                
                if(response):
                # Salvar a página no banco de dados
                    conn = sqlite3.connect('novo_buscador.db')
                    conn.execute("UPDATE paginas SET response = ?, response_time = ?, updated_at = datetime('now') WHERE url = ?", (response.text, response_time,  url))
                    conn.commit()
                    conn.close()
                    print('salvou nova bbbc')

                # Retornar o conteúdo da página
                    return response.text
            except Exception as e:
                print('erro: ', e)
                return
    else:
        # A página ainda não foi salva no banco de dados, fazer a requisição HTTP
        try:
            requests_cache.install_cache('nome_do_arquivo_cache', expire_after=3600)
            response = requests.get(url, verify=False)
            response_time = response.elapsed.total_seconds()
            
            if(response):
            # Salvar a página no banco de dados
                conn = sqlite3.connect('novo_buscador.db')
                conn.execute("INSERT INTO paginas (url, response, response_time, updated_at) VALUES (?, ?, ?, datetime('now'))", (url, response.text, response_time))
                conn.commit()
                conn.close()

            # Retornar o conteúdo da página
                return response.text
        except Exception as e:
            print('erro: ', e)
            return



def buscar_pagina_no_banco(url, nivel = 0):
    if nivel < 2:
        conn = sqlite3.connect('novo_buscador.db')

    # Verificar se a página já foi salva no banco de dados
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paginas WHERE url = ?", (url,))
        pagina_bd = cursor.fetchone()
        if pagina_bd:
            pagina = Pagina(pagina_bd[0], pagina_bd[1], pagina_bd[2], pagina_bd[3])
            return pagina
        else:
            obter_pagina(url)
            buscar_pagina_no_banco(url, nivel +1)
    else:
        return None
    

