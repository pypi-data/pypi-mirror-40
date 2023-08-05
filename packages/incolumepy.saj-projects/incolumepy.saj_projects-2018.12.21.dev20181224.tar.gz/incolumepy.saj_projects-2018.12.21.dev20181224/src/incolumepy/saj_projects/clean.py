#coding: utf-8
from bs4 import BeautifulSoup
import re
import os
import sys
from incolumepy.utils.files import realfilename
from unicodedata import normalize
from inspect import stack
sys.path.append(os.path.abspath(os.path.join('..', '..', '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

try:
    from incolumepy.saj_projects import legis, logger
except ModuleNotFoundError:
    from src.incolumepy.saj_projects import legis, logger


def substituir_tags(codigo: str, tag_out: list, tag_in: str) -> str:
    '''
    substitui tag_out por tag_in em todo o codigo
    :param codigo: str
    :param tag_out: str
    :param tag_in: str
    :return: str
    '''
    logger.debug(f'inicio {stack()[0][3]}')
    logger.debug('validação de parametros')
    try:
        assert isinstance(codigo, str), '"codigo" deve ser str'
        assert isinstance(tag_in, str), '"tag_in" deve ser str'
        assert isinstance(tag_out, list), '"tag_out" deve ser uma lista com str'
    except AssertionError as e:
        raise TypeError(e)
    tags = []
    soup = BeautifulSoup(codigo, 'html.parser')
    for elemento in tag_out:
        tags += soup.find_all(elemento)
    for tag in tags:
        tag.name = tag_in
    return soup.prettify()


def limpar(conteudo):
    ''''''
    logger.debug('elementos <br> substituídos por <p>')
    html = replace_break(conteudo)

    logger.debug('espaços brancos reduzidos')
    html = limpar_espacos(html)

    # logger.debug('Criado objeto soup')
    # soup = BeautifulSoup(html, 'html5lib')

    # Remove cabeçalho de tabela
    logger.debug('Remove cabeçalho de tabela')
    html = remover_tags(html, tags=['table'])

    # desatachar 'div[id="art"]'
    logger.debug("desatachar 'div[id=\"art\"]'")
    html = desatachar_tags(html, tags=['div[id="art"]'])

    # Desatachar tags
    logger.debug('Desatachar tags nowish')
    nowish = ['link', 'center', 'big', 'u', 'font', 'span', 'strong', 'small']
    html = desatachar_tags(html, nowish)

    # Marca class trash em elementos com Texto específico
    logger.debug('Marca class trash em elementos com Texto específico')
    elem_txt_nowish = [
        'Texto compilado',
        'Texto compilado'
    ]

    soup = BeautifulSoup(html, 'html5lib')
    for k in elem_txt_nowish:
        # logger.debug(k)
        container = soup.find_all(string=re.compile(k, re.I))
        # logger.debug(F'container: {container}')
        try:
            for j, i in enumerate(container):
                # logger.debug('{}, {}'.format(j, i.parent))
                legis.check_parent(soup=i, tag_name='p', key='class', value='trash')
        except AttributeError:
            container[0].wrap(soup.new_tag('p', **{'class': 'trash'}))
    html = soup.prettify()

    # remove tags ou tags com os atributos indicados
    logger.debug('remove tags ou tags com os atributos indicados')
    tags = [
        '[class="trash"]', '[name="generator"]', '[class="tela"]',
        'style', '[class="alert alert-danger"]', '[a=""]', 'script'
    ]
    html = remover_tags(html, tags)

    # attrs remove
    logger.debug('attrs remove')
    tags = ['xmlns', 'bgcolor', 'align', 'style', 'width']
    html = remover_tags(html, tags)

    # remove classes MS
    logger.debug('remove classes MS')
    html = remover_attr(html, ['[class*="Ms"]'])

    logger.info(f"{stack()[0][3]}return OK")
    return html


def ordinais(codigo: str) -> str:
    logger.debug('correção de ordinais')
    codigo = re.sub(r'<sup>\s*<u>\s*o\s*</u>\s*</sup>', 'º ', codigo, flags=re.I)
    codigo = re.sub(r'<sup>\s*<u>\s*a\s*</u>\s*</sup>', 'ª ', codigo, flags=re.I)
    soup = BeautifulSoup(codigo, "html5lib")

    tag0 = soup.find_all('sup', string=re.compile(r'\s*o\s*', re.I))
    if tag0:
        # print(tag0)
        for tag in tag0:
            logger.debug(f"tag0 unwrap: {tag}")
            tag.string = "º "
            tag.unwrap()

    tag1 = soup.find_all('sup', string=re.compile(r'a', re.I))
    if tag1:
        # print(tag1)
        for tag in tag1:
            logger.debug(f"tag1 unwrap: {tag}")
            tag.string = "ª "
            tag.unwrap()

    tag2 = soup.find_all('u', string=re.compile(r'\s*º\s*', re.M))
    tag2 += soup.find_all('u', string=re.compile(r'\s*ª\s*', re.M))
    logger.debug(f"tags <u>: {len(tag2)}")
    if tag2:
        for tag in tag2:
            tag.unwrap()
            logger.debug(f"tag2 unwrap: {tag}")
    logger.info('Correção bem sucedida')
    codigo = soup.prettify()
    codigo = re.sub(r'\s+º', 'º', codigo)
    codigo = re.sub(r'\s+ª', 'ª', codigo)
    return one_line(codigo)


def remover_tag_string(conteudo: str, lista_indesejados: list=None, tag_referencia: str='p')-> str:
    '''Marca class trash em elementos com Texto específico'''
    if not lista_indesejados:
        lista_indesejados = [
            'Texto compilado',
            'Texto completo'
        ]
    logger.debug('verificação de parametros')
    assert isinstance(lista_indesejados, list), "Error lista_indesejados not list"
    soup = BeautifulSoup(conteudo, 'html5lib')

    for s in lista_indesejados:
        logger.debug('localização dos itens a remover')
        container = soup.find_all(string=re.compile(s, re.I))
        try:
            for item in container:
                if item.parent.name == tag_referencia:
                    item.parent.decompose()
                    logger.debug(f"Removido: {item}")
        except AttributeError as e:
            container[0].wrap(soup.new_tag(tag_referencia, **{'class': 'trash'}))
            logger.error(e)
    logger.info('Sucesso na execução')
    return one_line(soup.prettify())


def replace_break(codigo: str)->str:
    logger.debug('replace <br> por </p><p>')
    return re.sub(r'<\s*br[\s/]*>', '</p><p>', codigo, flags=re.I)


def __staff(*args, **kwargs):
    logger.info(f'args: {args}, kwargs: {kwargs}')
    pass


def replace_middle_element(codigo: str, elem: str) -> str:
    ''' Substitui elementos intermediarios pelo imediatamente superior na hierarquia html.'''
    valids = ['hr', 'br']
    assert elem in valids, F"Elemento \"{elem}\" intermediário inválido."

    soup = BeautifulSoup(codigo, 'html.parser')
    elements = soup.select(elem)
    logger.info(f"Quantidade encontrada: {len(elements)} tag(s) '{elem}' encontrada(s).")
    if not elements:
        return codigo

    for i, item in enumerate(elements):
        logger.debug(F"#{i}> {item}")
        tag_parent = legis.locate_parent(soup=item, tag_name='br').parent
        parent_name = tag_parent.name
        # return tag_parent
        # return parent_name
        s = re.sub(r'<\s*br\s*/\s*>', r'</{a}> <{a}>'.format(a=parent_name), tag_parent.prettify(), flags=re.I)
        return one_line(s)


def remove_break(codigo: str) -> str:
    logger.debug('removido <br> ou <br/>')
    return remover_tags(['br'])


def replace_espacos(codigo: str) -> str:
    '''
    Espaçamento duplo entre mensagens de alterações legislativas
    :param codigo: str contendo código HTML
    :return: str HTML
    '''
    logger.debug('validação de parametros')
    assert isinstance(codigo, str), "codigo deve ser instancia de str"
    logger.info('retornado o texto com espaços em formato html')
    return re.sub(r'\)\s+\(', r'\)&nbsp;&nbsp;\(', codigo, flags=re.M)


def limpar_espacos(codigo: str)->str:
    codigo = re.sub(r'&nbsp;', ' ', codigo, flags=re.I)
    codigo = re.sub(r'\s+', ' ', codigo, flags=re.I)
    logger.debug(f'type codigo: {codigo}')
    logger.info('limpo todos os espaços em codigo')
    return codigo


def desatachar_tags(codigo: str, tags: list=None)->str:
    '''Desatachar tags'''
    logger.debug('codigo convertido em soup')
    soup = BeautifulSoup(codigo, 'html5lib')
    if not tags:
        tags = [
            'link',
            'center',
            'big',
            'u',
            'font',
            'span',
            'small',
        ]
    for tag in tags:
        container = soup.select(tag)
        for n, item in enumerate(container):
            item.unwrap()
            logger.debug(f'#{n:2}unwrap: {item}')
    logger.info(f'Sucesso: {stack()[0][3]}')
    return soup.prettify()


def remover_tags(codigo: str, tags: list=None)->str:
    '''remove tags, seus atributos e todo seus conteudos'''
    # import pdb;  pdb.set_trace()
    logger.debug(f"parametro envolvidos: {remover_tags.__annotations__}")
    soup = BeautifulSoup(codigo, 'html5lib')
    logger.info('codigo convertido em soup')
    if not tags:
        logger.debug('tags vázias utilizando default')
        tags = [
            'link[rel*="STYLESHEET"]',
            'meta[name="GENERATOR"]',
            '[class="trash"]',
            '[name="generator"]',
            '[class="tela"]',
            'style',
            '[class="alert alert-danger"]',
            '[a=""]',
            'script'
        ]
    logger.debug(f'validação parametro: codigo: {codigo}')
    assert isinstance(codigo, str)
    logger.debug(f'validação parametro: tags: {tags}')
    assert isinstance(tags, list)
    for tag in tags:
        container = soup.select(tag)
        for item in container:
            try:
                item.decompose()
                logger.debug(f'decompose: {item}')
            except IndexError as e:
                logger.error(F"{stack()[0][3]}: Elemento {tag}", exec_info=True)
    logger.info(f'Sucesso: {stack()[0][3]}')
    return one_line(soup.prettify())


def remover_attr(codigo: str, atributos: list=None)->str:
    logger.debug('codigo convertido em soup')
    soup = BeautifulSoup(codigo, 'html5lib')
    if not atributos:
        atributos = [
            'class*="Ms"',
            'xmlns',
            'bgcolor',
            'align',
            'style',
            'width'
        ]
    for atributo in atributos:
        container = soup.select('[{}]'.format(atributo))
        for item in container:
            del item[re.split(r'\*|\$|\^|=', atributo)[0]]
            logger.debug(f"del: {item}")
    logger.info(f"Sucesso: {stack()[0][3]}")
    return one_line(soup.prettify())


def remover_acentos(txt: str)-> str:
    ''' Remove acentos de caracteres não ascii
    :param txt: string
    :return: string sem caracteres especiais

    >>> remover_acentos('áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.')
    'aaaaaAAAAA! eeeeEEEEE? iiiiIIIII, oooooOOOOO; uuuuUUUUU.'
    '''
    logger.debug('substituir caracteres acentuados')
    result = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    logger.debug(result)
    logger.info(f'Sucesso: {stack()[0][3]}')
    return result


def one_line(codigo_html: str) -> str:
    '''Retorna o codigo html sem quebras'''
    logger.debug('retorna o código sem quebras de linha')
    logger.info(f'Sucesso: {stack()[0][3]}')
    return re.sub('&nbsp;|\n', ' ', limpar_espacos(codigo_html), flags=re.MULTILINE)


def elemento_discartar(soup, elemento: str, pos: int):
    logger.debug(f'Descarta "{elemento}" da posição ({pos}) indicada')
    for item in soup.select(f'{elemento}:nth-of-type({pos})'):
        item.decompose()
        logger.debug(f'Elemento decomposed: {item}')


def elemento_desatachar(soup, elemento: str, pos: int):
    logger.debug(f'desatacha "{elemento}" da posição ({pos})')
    for item in soup.select(f'{elemento}:nth-of-type({pos})'):
        item.unwrap()
        logger.debug(f'Elemento unwraped: {item}')


class Clean_html:
    TXT = '[ACENTUAÇÃO] açaí: áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.'

    def __init__(self):
        self.file = None
        self.data = []
        self.conteudo = None
        self.filename = None
        self.path = None

    @classmethod
    def remover_acentos(self, txt):
        ''' Remove acentos de caracteres não ascii
        :param txt: string
        :return: string sem caracteres especiais

        >>> remover_acentos('áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.')
        'aaaaaAAAAA! eeeeEEEEE? iiiiIIIII, oooooOOOOO; uuuuUUUUU.'
        '''
        logger.info('converter texto para ASCII')
        result = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        logger.debug(result)
        logger.info(f'Sucesso: {stack()[0][3]}')
        return result

    def get_file_content(self):
        logger.debug('Carregando conteúdo')
        try:
            with open(self.file) as file:
                self.data.append(file.read())
                self.path = os.path.dirname(file.name)
                self.filename = os.path.basename(file.name)
                logger.info('Carregado com sucesso')
        except UnicodeEncodeError as e:
            logger.error(f'{file.name}: {e.object}; {e}')
            with open(self.file, encoding='iso8859-1') as file:
                self.data.append(file.read())
                self.path = os.path.dirname(file.name)
                self.filename = os.path.basename(file.name)

    def clean(self):
        logger.debug(stack()[0][3])
        try:
            if not self.conteudo:
                self.get_file_content()

            if not self.data:
                self.data.append(self.conteudo)

            logger.debug('replace espaços')
            self.data.append(re.sub('&nbsp;|\n', ' ', str(BeautifulSoup(self.data[0], 'html5lib')), flags=re.MULTILINE))
            self.data[1] = re.sub(r'\s+', ' ', self.data[1], flags=re.MULTILINE)

            logger.debug('replace ordinais')
            self.data[1] = re.sub(r'<sup>\s?o\s?</sup>', 'º ', self.data[1], flags=re.MULTILINE)
            self.data[1] = re.sub(r'<sup>\s?a\s?</sup>', 'ª ', self.data[1], flags=re.MULTILINE)
            soup = BeautifulSoup(self.data[-1], 'html.parser')

            # remover tags e seu conteudo
            logger.debug('tags indesejadas')
            tag = []
            tag.append('meta[name="GENERATOR"]')
            tag.append('link[rel*="STYLESHEET"]')
            tag.append('style')
            for j in tag:
                container = soup.select(j)
                for a, i in enumerate(container):
                    logger.debug(f'#{a} decompose: {i.parent}')
                    i.decompose()

            ## desatachar tags
            tag = []
            tag.append('big')
            tag.append('u')
            tag.append('font')
            tag.append('span')
            tag.append('strong')
            tag.append('small')
            tag.append('html')
            tag.append('body')
            for j in tag:
                container = soup.select(j)
                for i in container:
                    i.unwrap()
                    logger.debug(f'unwrap: {i}')

            # attrs remove
            tag = []
            tag.append('xmlns')
            tag.append('bgcolor')
            tag.append('align')
            tag.append('style')
            tag.append('width')
            tag.append('class*="Ms"')
            for i in tag:
                container = soup.select('[{}]'.format(i))
                for j in container:
                    del j[i]
                    logger.debug(f'del: {j}')

            # remove classes MS
            container = soup.select('[class*="Ms"]')
            for i in container:
                del i['class']
                logger.debug(f'del: {i}')

            # adding str html e body
            logger.debug('adding str html e body')
            soup = BeautifulSoup('<html><body>{}</body></html>'.format(str(soup)), 'html.parser')

            # wrap body
            logger.debug('wrap body')
            tag = soup.new_tag('body')
            #soup.new_tag('body').wrap(soup)
            #tag.append(soup)

            #for item in soup.find_all():
            #    tag.append(item.extract())
            #soup = tag

            # wrap html
            #soup.wrap(soup.new_tag('html'))
            #container = soup.find_parents('head')
            #print(container)

            # Realocar head
            logger.debug('Realocar head')
            soup.html.insert(0, soup.body.head.extract())

            logger.info(f'Sucesso: {stack()[0][3]}')
            self.conteudo = soup.prettify()
        except IOError as e:
            logger.error(f'{e}')
            raise

    def write(self):
        newer = os.path.join(self.path, self.filename)
        original = realfilename(newer)
        logger.info(f'rename {original}> {newer}')
        os.rename(newer, original)
        logger.info(f'conteudo preservado em: {original}')
        with open(newer, 'w') as file:
            file.write(self.conteudo)
            logger.info(f'{file.name} gravado com sucesso')
        return True

    @staticmethod
    def run(file='../file.html'):
        a = Clean_html()
        try:
            assert os.path.isfile(file)
            a.file = file
        except AssertionError:
            a.file = '../../testes/file.html'

        a.clean()
        print(a.__dict__)
        print(a.filename)
        print(a.write())
        print(a.remover_acentos(a.TXT))
        print(Clean_html.remover_acentos(Clean_html.TXT))


if __name__ == '__main__':
    Clean_html.run()
