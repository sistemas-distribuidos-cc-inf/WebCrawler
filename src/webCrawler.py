#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import sys

# Retorna uma string com o conteúdo da página web
def get_page( url ):
    try:
        return urllib.urlopen( url ).read()
    except:
        return ""

# Retorna o primeiro link na página bem como a sua posição final
def get_next_target( page ):
    start_link = page.find( '<a href=' )

    if ( start_link == -1 ):
        return None, 0

    start_quote = page.find( '"', start_link )
    end_quote   = page.find( '"', start_quote + 1 )
    url = page[start_quote+1:end_quote]
    return url, end_quote

# Retorna todos os links da pagina
def get_all_links( page ):
    links = []
    while True:
        url,endpos = get_next_target( page )
        if url:
            links.append( url )
            page = page[endpos:]
        else:
            break
    return links

# Compara se existem elementos iguais. Se não insere o elemento em 'p'
def union( p, q ):
    for e in q:
        if e not in p:
            p.append( e )


#==============================================================================

def lookup( index, keyword ):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

def add_to_index( index, keyword, url ):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append( url )
            return
    # não encontrado, adicione uma nova entrada
    index.append( [ keyword, [url] ] )

def add_page_to_index( index, url, content ):
    words = content.split()
    for word in words:
        add_to_index( index, word, url )

#==============================================================================

# Função principal que inicia o rastreamento
def crawl_web( seed, max_page ): # argumento opcional 'max_page'
    tocrawl = [seed]
    crawled = []
    index   = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled and len( crawled ) < max_page:
            content_page = get_page( page )
            add_page_to_index( index, page, content_page )
            union( tocrawl, get_all_links( content_page ) )
            crawled.append( page )
    return index
#============================ persistência de dados
pagesCrawled =[]

url_seed = ''
max_page = 0
if len( sys.argv ) == 3:
    url_seed = sys.argv[1]
    max_page = sys.argv[2]
    pagesCrawled = crawl_web( url_seed, max_page )
    with open("Conteudo Busca.txt", "w") as links_file: links_file.write( str( pagesCrawled ) )
else:
    print 'Error: Espera-se <programa> <url> <qtd max_page>\n'
