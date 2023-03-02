import requests
from bs4 import BeautifulSoup
import requests_cache
import re
import utils as utils
import sys
sys.path.append('./db')
import db_connection
sys.path.append('./classes')
from pagina import Pagina
import datetime


def request_url(url):
    return db_connection.obter_pagina(url)
    
def search_word(searched_word, url, response = ''):
    if(response == ''):
        response = request_url(url)
        
    soup = BeautifulSoup(response, "html.parser")
    ocurrence_list = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
   
    return ocurrence_list

def search_word_in_title(searched_word, url, response = ''):
    if(response == ''):
        response = request_url(url)
        
    soup = BeautifulSoup(response, "html.parser")
    title = soup.title.string

    # Verifica se o termo está presente no título
    return searched_word in title
    
def find_links_in_url(url, response = ''):
    
    if(response == ''):
        response = request_url(url)
        
    if(response):
        soup = BeautifulSoup(response, "html.parser")
        links = soup.find_all('a')
    
        links = list(map(lambda x: x.get('href'), links))
    
        return links
    return []

def generate_list_with_link_tree(url, max_level,  url_base, level = 0, node_list = []):
    if level <= max_level:
      
        current_list = find_links_in_url(url)
        current_list = list(filter(None, current_list))
        nova_lista = [elemento for elemento in current_list if elemento.startswith('http')]
        nova_lista = [url_base+elemento for elemento in current_list if elemento.startswith('/')]

        if(len(nova_lista) > 0):
            node_list.append(nova_lista)
       
        for link in nova_lista:
            currentUrl = link
            if currentUrl != None:
                if not currentUrl.startswith('h') and not currentUrl.startswith('www'):
                    continue
            else:
                continue
            generate_list_with_link_tree(currentUrl, max_level,url_base, level+1)
            
    return utils.gerar_lista_simples(node_list)
        
def generate_links_ranking(page_list,termo):
    return sorted(page_list, key=lambda pagina: (-pagina.get_ocurrence_amount(termo), -pagina.get_term_is_in_the_title(termo), -int(pagina.get_response_time()))) 
    #primeiro exibir pagina com mais ocorrencia dos termos. Se a pagina não tiver o termo no titulo sera afetada negativamente. A pagina mais acessada terá ranqueamento positivo

def generate_list_of_objects_with_links(url, profundidade):

    list_links = []
    list_links.append(url)
    
    
    if profundidade >= 1:  
        list_links.append(generate_list_with_link_tree(url = url, max_level= (profundidade-1),url_base = 'https://www.bbc.com'))
   
    set_links = set(utils.gerar_lista_simples(list_links))

    list_class_pages = []
    
    print('quantidade de links analisados: ')
    print(len(set_links))
    
    print('carregando....')
    for i, link in enumerate(set_links):
        print(i, link)
        objeto = db_connection.buscar_pagina_no_banco(link)
        if objeto:
            response =  objeto.get_response()
            #ocurrences_list = search_word(termo, link, response=response)
            list_class_pages.append(objeto)
    
    return list_class_pages

def main():
    site = 'https://www.bbc.com/portuguese'
    termo = 'Política'
    profundidade = 1
    
    list_class_pages = generate_list_of_objects_with_links(site, profundidade)
    

    sorted_pages = generate_links_ranking(list_class_pages,termo)
    
    print('\n----- Ranqueamento -----\n')
    for i, page in enumerate(sorted_pages):
        print(i, page.show(termo))
                

    

if __name__ == '__main__':
    main()