# Pega o conteúdo de uma página web
def get_page( page ): # Procedimento ainda não implementado

# Retorna o primeiro link na página bem como a sua posição final
def get_next_target( page ):
    start_link = page.find( '<a href=' )

    if ( start_link == -1 ):
        return None, 0

    start_quote = page.find( '"', start_link )
    end_quote   = page.find( '"', start_quote + 1 )
    url = page[start_quote+1:end_quote]
    return url, end_quote

# Compara se existem elementos iguais. Se não insere o elemento em 'p'
def union( p, q ):
    for e in q:
        if e not in p:
            p.append( e )

# Substitui o procedimento print_all_links (apenas imprimia os links -- teste)
# retorna uma lista de todos os links na página
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

# retorna a lista de todos os links que foram rastreados
def crawl_web( seed ): # argumento opcional 'max_page'
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled: #and len( crawled ) < max_page:
            union( tocrawl, get_all_links( get_page( page ) ) )
            crawled.append( page )
    return crawled
# Opcional que reduz a busca em profundidade. Substituir por crawl_web( seed ):
#def crawl_web(seed,max_depth):
#    tocrawl = [seed]
#    crawled = []
#    next_depth = []
#    depth = 0
#    while tocrawl and depth <= max_depth:
#        page = tocrawl.pop()
#        if page not in crawled:
#            union(next_depth, get_all_links(get_page(page)))
#            crawled.append(page)
#        if not tocrawl:
#            tocrawl, next_depth = next_depth, []
#            depth = depth + 1
#    return crawled
