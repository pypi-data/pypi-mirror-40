#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "@britodfbr"
__copyright__ = "Copyright 2007, incolume.com.br"
__credits__ = ["Ricardo Brito do Nascimento"]
__license__ = "GPL"
__version__ = "1.0a"
__maintainer__ = "@britodfbr"
__email__ = "contato@incolume.com.br"
__status__ = "Production"


import re
import os
import sys
import pdb
import locale
import platform
import json
import numpy as np
import pandas as pd
import requests
from inspect import stack
from bs4 import BeautifulSoup, Doctype, Comment, CData
from bs4.element import NavigableString, Tag
from datetime import datetime as dt
from os.path import abspath, join, isfile, dirname
from unicodedata import normalize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
from functools import lru_cache
sys.path.append(os.path.abspath(os.path.join('..', '..', '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

try:
    from incolumepy.saj_projects import clean, logger
except ModuleNotFoundError:
    from src.incolumepy.saj_projects import clean, logger

if platform.system() == 'Linux':
    logger.info('atualização de locale')
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def iconv(filein, encode_in, encode_out, fileout=None):
    with open(filein, encoding=encode_in) as f:
        content = f.read()
    if fileout:
        return save_html_file(conteudo=content, filename=fileout, encoding=encode_out)
    return save_html_file(conteudo=content, filename=filein, encoding=encode_out)


def includeDelOnLineThrough(conteudo: str) -> str:
    ''' Inclui <del> onde houber style com "line-through" '''
    soup = BeautifulSoup(conteudo, 'html.parser')
    through = soup.find_all(style=re.compile("line-through"))
    for i in through:
        i.wrap(soup.new_tag('del'))
    return clean.one_line(soup.prettify())


def replaceLineThrough2Del(conteudo: str)-> str:
    ''' Substituir line-through '''
    soup = BeautifulSoup(conteudo, 'html.parser')
    through = soup.find_all(style=re.compile("line-through"))
    for i in through:
        logger.debug(f'{stack()[3][0]}:{i!s}')
        change_parent(soup=i, tag_name='span', new_tag_name='del')
    return clean.one_line(soup.prettify())


def locate_parent(**kwargs):
    '''
    :param kwargs: soup and tag_name both strings
    :return: bs4 with element finded
    '''
    try:
        kwargs.get('soup').name
    except (AssertionError, AttributeError):
        raise TypeError("Not instance bs4")

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        return kwargs.get('soup')
    return locate_parent(soup=kwargs.get('soup').parent,
                         tag_name=kwargs.get('tag_name'))


def change_parent(**kwargs):
    ''''''
    # assert isinstance(kwargs.get('soup'), BeautifulSoup) \
    #        or isinstance(kwargs.get('soup'), Tag) \
    #        or isinstance(kwargs.get('soup'), NavigableString), "Not instance bs4"
    try:
        logger.debug(f"{kwargs.get('soup')}")
        logger.debug(f"{kwargs.get('soup').name}")
        if not kwargs.get('tag_name', None):
            raise ValueError('atributo tag_name deverá ser informado')
        if not kwargs.get('new_tag_name', None):
            raise ValueError('atributo new_tag_name deverá ser informado')
    except AttributeError as e:
        # raise AttributeError('Object "{}" not instance bs4, Error: {}'.format(kwargs.get('soup'), e))
        logger.warning(F"Not instance bs4; {kwargs.get('soup')}: {e}")
        raise TypeError('Soup must be instance bs4')
        # return None

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        kwargs.get('soup').name = kwargs.get('new_tag_name')
        return kwargs.get('soup')
    return change_parent(soup=kwargs.get('soup').parent,
                         tag_name=kwargs.get('tag_name'),
                         new_tag_name=kwargs.get('new_tag_name'))


def extract_soup_set_tag_class(soup, nova_tag='p', class_value='ementa', modo_texto=True):
    assert isinstance(soup, BeautifulSoup) \
           or isinstance(soup, Tag) \
           or isinstance(soup, NavigableString), "Not instance bs4"
    nsoup = BeautifulSoup('', 'html.parser')
    # print('>', nsoup)
    tag = nsoup.new_tag(nova_tag, **{'class': class_value})
    # print('>', soup.text.strip())
    if modo_texto:
        tag.string = soup.text.strip()
    else:
        tag.append(soup)
    # print('>', tag)
    return tag


def check_parent(**kwargs):
    '''
    :param kwargs: soup, tag_name, key, value
    :return: soup with setted <tag_name key="value" />
    '''
    assert isinstance(kwargs.get('soup'), BeautifulSoup) \
        or isinstance(kwargs.get('soup'), Tag) \
        or isinstance(kwargs.get('soup'), NavigableString), "Not instance bs4"

    if kwargs.get('soup').name == kwargs.get('tag_name'):
        try:
            kwargs.get('soup')[kwargs.get('key')] = kwargs.get('value')
        except IndexError:
            logger.error(f"{stack()[0][3]}: Não há ancestral para {kwargs.get('soup')}", exc_info=True)
        return kwargs.get('soup')
    return check_parent(soup=kwargs.get('soup').parent,
                        tag_name=kwargs.get('tag_name'),
                        key=kwargs.get('key'), value=kwargs.get('value'))


def presidente_identify(soup, json_file, content=''):
    '''Identifica o presidente no soup recebido'''
    if not soup and content:
        soup = BeautifulSoup(content, 'html5lib')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)

    for item in presidentes['presidentes'].values():
        for i in [x for x in item['nome'].split() if len(x) > 2]:
            result = soup.find_all(string=re.compile(i, re.I), limit=10)
            if result:
                p = result[0].replace('.', '')
                logger.debug(f"{item} {i} {p}")
                if set([x.lower() for x in p.split() if len(x)>2]).issubset(set(item['nome'].lower().split())):
                    logger.debug(result)
                    return result
    return False


def governo_ano(json_file, ano=dt.today().strftime('%Y')):
    '''recebe o ano do governo e retorna str com o nome do presidente'''
    logger.debug(f"{ano}")
    with open(os.path.abspath(json_file)) as jf:
        presidentes = json.load(jf)

    logger.debug(f"{presidentes}")
    for item in presidentes['presidentes'].values():
        logger.debug(f"{item['imandato']}, {item['fmandato']}")
        i, f = dt.strptime(item['imandato'], "%d de %B de %Y"), dt.strptime(item['fmandato'], "%d de %B de %Y")
        if i.year <= dt.strptime(str(int(ano)), "%Y").year <= f.year:
            logger.debug(item['nome'])
            return item['nome'].upper()
    return None


def presidente_em_exercicio(soup, json_file, content=''):
    '''identifica o nome do presidente em exercício'''
    if not soup and content:
        soup = BeautifulSoup(content, 'html5lib')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)

    vices = []

    for item in presidentes['presidentes'].values():
        for i in [x for x in item['nome'].split() if len(x) > 2]:
            result = soup.find_all(string=re.compile(i, re.I), limit=10)
            if result:
                p = result[0].replace('.', '')
                logger.debug(f"{item}{i}{p}")
                if set([x.lower() for x in p.split() if len(x) > 2]).issubset(set(item['nome'].lower().split())):
                    return result
        if isinstance(item['vice'], str):
            vices.append(item['vice'])
        elif isinstance(item['vice'], list):
            vices += item['vice']

    for vice in vices:
        for i in [x for x in vice.split() if len(x) > 2]:
                result = soup.find_all(string=re.compile(i, re.I), limit=10)
                if result:
                    p = result[0].replace('.', '')
                    if set([x.lower() for x in p.split() if len(x) > 2]).issubset(set(vice.lower().split())):
                        return result
    return False


def loc_presidente_exercicio(soup, presidentes_file=join(dirname(__file__), 'data', 'base_presidente_exercicio.csv')):
    '''

    :param soup:
    :param presidentes_file:
    :return:
    '''
    logger.debug('Inicio de {}'.format(stack()[0][3]))
    presidentes_file = abspath(presidentes_file)
    assert isfile(presidentes_file), "Arquivo {} não disponível.".format(presidentes_file)
    assert isinstance(soup, BeautifulSoup), '"soup" deverá ser instancia de bs4.BeautifulSoup'
    df = pd.read_csv(presidentes_file)

    sf0 = pd.concat([df.nome.str.strip().dropna(), df.vice.str.strip().dropna()]).str.upper()
    sf = sf0[~sf0.str.contains('NONE')]
    # for i, j in enumerate(sf):
    #     print(i, j)

    result = pd.Series(np.sort(sf.str.strip().unique()))
    munus3 = lambda s: normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    for i, presidente in enumerate(result):
        logger.info('Presidente em exercício: #{:4} {}'.format(i, presidente))
        for j in [x for x in presidente.split() if len(x)>3]:
            queries = soup.find_all(string=re.compile(j, re.I), limit=1)
            if queries:
                logger.debug(queries)
                logger.info('>> Conteúdo de queries: {}'.format(queries[-1].strip()))
                logger.warning('>> {}'.format(set(queries[-1].strip().upper().split())))
                if set(
                        [munus3(x).upper() for x in queries[-1].strip().replace('.','').split()]
                       ).issubset([munus3(x) for x in presidente.split()]):
                    logger.info('Presidente localizado: {}'.format(queries[-1].strip()))
                    return queries

    logger.info('Presidente não localizado')
    logger.debug('Finalização de {}'.format(stack()[0][3]))
    return []


@lru_cache(maxsize=2000)
def loc_ministro(soup, referenda='data/referendas.csv'):
    '''
    Localiza o ministro pelo nome dentro do soup fornecido.
    :param soup: Objeto SOUP
    :param referenda: lista com o nome de ministros
    :return: Lista com todos os ministros identificados no Ato
    '''
    referenda = abspath(join(dirname(__file__), referenda))
    assert os.path.isfile(referenda), f"Ops: \"{referenda}\" inexistente .."

    assert isinstance(soup, BeautifulSoup) \
        or isinstance(soup, Tag) \
        or isinstance(soup, NavigableString), 'Not is instance bs4'

    logger.debug('Inicio de {}'.format(stack()[0][3]))
    dataframe = pd.read_csv(abspath(referenda), encoding='iso8859-1',
                            names=['sigla', 'orgao', 'titular', 'interino', 'posse', 'afastamento'], header=0)
    sf = pd.concat([dataframe.titular.str.strip().dropna(), dataframe.interino.str.strip().dropna()])

    sf = sf[~sf.str.contains(r'\*|um dos', regex=True, case=False)]
    munus1 = lambda s: re.sub(r'\)', '', string=s).strip()
    munus2 = lambda s: s.split(r'(')[-1]
    munus3 = lambda s: normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    referenda = set()
    df = pd.DataFrame(sf)
    df['1'] = sf.apply(munus1).apply(munus2).apply(munus3)
    df.columns = ["old", "new"]
    result = pd.Series(np.sort(df.new.str.strip().unique()))

    for i, ministro in enumerate(result):
        # logger.info('Ministro #{:4}: {}'.format(i, ministro))
        for j in [x for x in ministro.split() if len(x)>3]:
            result = soup.find_all(string=re.compile(j, re.I), limit=20)
            if result:
                # logger.debug(result)
                for nome in result:
                    logger.info('>> Conteúdo de Result: {}'.format(nome))
                    if set([munus3(x).upper() for x in
                            nome.replace('.', '').split()]).issubset([x for x in ministro.split()]):
                        referenda.add(nome.strip())
    if referenda:
        logger.debug('Ministro Localizado: {}'.format(referenda))
        logger.debug('Finalização de {}'.format(stack()[0][3]))
        return referenda

    logger.warning('Ministro não encontrado.')
    logger.debug('Finalização de {}'.format(stack()[0][3]))
    return False


def vice_identify(json_file, ano=dt.today().strftime('%Y')):
    '''recebe o ano do governo e retorna str com o nome do vice-presidente'''
    ano = str(ano)
    logger.debug(ano)
    if platform.system() == 'Linux':
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    with open(abspath(json_file)) as jf:
        presidentes = json.load(jf)
    try:
        logger.debug(f"{len(presidentes)}")
        for item in presidentes['presidentes'].values():
            logger.debug(f"{item['imandato']}, {item['fmandato']}")
            if (dt.strptime(item['imandato'], "%d de %B de %Y")
                < dt.strptime(ano, "%Y")
                    < dt.strptime(item['fmandato'], "%d de %B de %Y")):
                logger.debug(f"presidente: {item['nome']}\nvice: {item['vice']}")
                return item['vice'].upper().strip()
    except (NameError, AttributeError):
        return []


def save_html_file(conteudo, filename, encoding='iso8859-1'):
    # fatorar este código
    if not isinstance(conteudo, str):
        raise ValueError('"conteudo" deve ser um código HTML de tipo "str"')

    if not isinstance(filename, str):
        raise ValueError('"filename" deve ser um caminho válido no sistemas de arquivo de tipo "str"')

    if '~' in filename:
        filename = os.path.abspath(os.path.join((os.path.expanduser(filename))))
    elif filename.startswith(os.sep):
        filename = os.path.abspath(os.path.join(os.path.abspath(os.sep), *filename.split(os.sep)))
    else:
        filename = os.path.abspath(os.path.join(os.getcwd(), filename))

    soup = BeautifulSoup(conteudo, 'html5lib')
    output_path = os.path.dirname(filename)
    logger.debug(f'Verificado "{os.path.dirname(filename)}"')
    os.makedirs(output_path, 0o777, True)
    with open(filename, 'wb') as file_out:
        file_out.write(soup.prettify(encoding=encoding))
    logger.debug(F'Arquivo "{filename}" gravado.')
    return True, filename


def get_conteudo(filename=None, url=None, encoding='iso8859-1'):
    assert filename or url, "filename or url are required"
    if filename:
        return get_conteudo_file(filename, encoding)
    return get_conteudo_url(url)


def get_conteudo_file(filename: str, encoding: str="iso8859-1") -> str:
    if '~' in filename:
        filename = os.path.abspath(os.path.join(os.path.commonpath(os.get_exec_path()),
                                                *os.path.expanduser(filename).split(os.sep)))
    else:
        filename = os.path.abspath(os.path.join(*filename.split(os.sep)))
    assert os.path.isfile(filename), "Arquivo '{}' indisponível".format(filename)
    with open(filename, encoding=encoding) as f:
        logger.debug('filename: "{}" readed'.format(f.name))
        return f.read()


def get_conteudo_url(url: str) -> str:
    logger.debug('inicio de excução get_conteudo_url')
    try:
        logger.debug('> get_conteudo_requests_url')
        return get_conteudo_requests_url(url)
    except:
        logger.debug('Falha get_conteudo_requests_url')
        logger.debug('> get_conteudo_selenium_url')
        return get_conteudo_selenium_url(url)
    finally:
        logger.debug('fim de excução get_conteudo_url')


def get_conteudo_requests_url(url: str) -> str:
    # pdb.set_trace()
    response = requests.get(url)
    return response.content


def get_conteudo_selenium_url(url: str) -> str:
    # pdb.set_trace()
    navegador = ''
    try:
        firefoxbin = os.path.abspath(os.path.join(os.path.dirname(__file__), 'drivers', 'geckodriver'))
        assert os.path.isfile(firefoxbin), "Driver \"{}\" não disponível.".format(firefoxbin)
        logger.debug(f"firefoxbin: {type(firefoxbin)}")
        navegador = webdriver.Firefox(executable_path=firefoxbin)
        logger.debug(f"navegador: {type(navegador)}")
        while True:
            try:
                element = WebDriverWait(navegador, 2)
                element.until(EC.presence_of_element_located(By.TAG_NAME, 'body'))
            except Exception as e:
                logger.warning(e, exc_info=True)
                break
        navegador.get(url)
    except NameError:
        raise
    else:
        s = randint(5, 9)
        logger.debug('sleep({})'.format(s))
        sleep(s)
        logger.debug(navegador.title)
        conteudo = navegador.page_source
        logger.debug("conteudo baixado..")
        return conteudo
    finally:
        navegador.close()


def definir_titulos(codigo: str, titulos: list=[], tag: str='p', nova_tag: str='h4') -> str:
    ''' Definir titulos '''
    # Titulos nível 4
    fixos = [
        'PREÂMBULO',
        r'TÍTULO\s[xivcm]+',
        r'CAPÍTULO\s[xivcm]+',
        r'Seção\s[xivcm]+',
        r'Subseção\s[xivcm]+',
        r'SECÇÃO\s[xivcm]+',
        r'SUBSECÇÃO\s[xivcm]+',
        r'livro\s*[xivcm]*'
    ]
    if not titulos:
        titulos += fixos
    titulos = set([x.strip().lower() for x in titulos])
    logger.debug(f"Possível titulos fixados: {len(titulos)}")
    soup = BeautifulSoup(codigo, 'html.parser')
    for titulo in titulos:
        # container = soup.find_all(string=re.compile(r'^\s+{}\s+$'.format(titulo), re.I))
        container = soup.find_all(string=re.compile(r'{}'.format(titulo), re.I))
        for item in container:
            logger.debug('{} {} ({} -> {})'.format(type(item), item.strip(), tag, nova_tag))
            change_parent(soup=item, tag_name=tag, new_tag_name=nova_tag)
    return clean.one_line(soup.prettify())


class Legis:
    ''' Classe Legis '''

    def __init__(self, **kwargs):
        self.soup = None
        self.file = None
        self.urls = []
        self.date = None
        for item, value in kwargs.items():
            logger.debug(f"{item}: {value}")
            self.__dict__[item] = value

    @staticmethod
    def definir_titulos(soup: any, titulos: list=[], tag: str='p', nova_tag: str='h4') -> BeautifulSoup:
        ''' Definir titulos '''
        result = definir_titulos(codigo=soup.prettify(), titulos=titulos, tag=tag, nova_tag=nova_tag)
        return BeautifulSoup(result, 'html.parser')
        # Titulos nível 4
        fixos = [
            'PREÂMBULO',
            r'TÍTULO\s[xivcm]+',
            r'CAPÍTULO\s[xivcm]+',
            r'Seção\s[xivcm]+',
            r'Subseção\s[xivcm]+',
            r'SECÇÃO\s[xivcm]+',
            r'SUBSECÇÃO\s[xivcm]+',
            r'Livro\s?[xivcm]*'
        ]
        titulos += fixos
        #assert isinstance(soup, BeautifulSoup), "Não é BeautifulSoup"

        logger.debug(f"Titulos identificados: {len(titulos)}")
        for titulo in titulos:
            logger.debug(titulo)
            container = soup.find_all(string=re.compile(r'^\s+{}\s+$'.format(titulo), re.I))
            for item in container:
                logger.debug(item)
                soup = BeautifulSoup(change_parent(soup=item, tag_name=tag, new_tag_name=nova_tag),
                                     'html.parser')

    @staticmethod
    def replace_tag(soup, tag_name, new_tag_name):
        tags_for_replace = soup.find_all(tag_name)
        logger.debug(f"itens identificados: {len(tags_for_replace)}")
        for item in tags_for_replace:
            logger.debug(f"{item} {tag_name}> {new_tag_name}")
            change_parent(soup=item, tag_name=tag_name, new_tag_name=new_tag_name)

    @staticmethod
    def loc_dou(soup):
        regex = r"Este\s+texto\s+não\s+substitui\s+o\s+publicado\s+n[ao]\s+(D.O.U.|DOU|CLBR)(\.,)?"
        logger.debug(f"regex: {regex}")
        tags = soup.find_all(string=re.compile(regex, re.I))
        logger.debug(f"{tags}")
        try:
            check_parent(soup=tags[0], tag_name='p', key='class', value='dou')
        except IndexError as e:
            logger.error(e)

    @staticmethod
    def loc_data_assinatura(soup):
        '''Data de assinatura (DOU)'''
        # regex = r"(Rio de Janeiro|Brasília|senado*)(.+(República|Independência)){1,2}(\.,)?\w+"
        regex = r"(Rio de Janeiro|Brasília|senado*)(.*)(Independência|República){1,2}(.*)"
        logger.debug(f"Regex: {regex}")
        tags = soup.find_all(string=re.compile(regex, re.I))
        logger.info(f'Data de assinatura (DOU): {tags}')
        try:
            check_parent(soup=tags[0], tag_name='p', key='class', value='data')
        except IndexError as e:
            logger.warning(f'Data de publicação DOU não identificada: {e}')
            # print(e)

    @staticmethod
    def loc_epigrafe(soup):
        '''
        Localiza ementa e define p[class="epigrafe"]
        Aplique clean.oridinais() antes de gerar o soup para este metodo.
        :param soup: BeatifulSoup
        :return: bool
        '''

        assert isinstance(soup, BeautifulSoup) \
               or isinstance(soup, Tag) \
               or isinstance(soup, NavigableString), 'Not is instance bs4'
        regex = r"(DECRETO|DECRETO-LEI|LEI)\s*n\w{1}\s*(\d\.?)+,?\s*\w{,2}\s*(\d{1,2}\w?)\s*\w{,2}\s*\w+\s*\w{,2}\s*\d{4}\.?"
        # regex = r"(LEI|DECRETO-LEI|DECRETO)\s+N\s+\w\s+(\d\.?)+,?  DE  \d{1,2}  DE  \w{4,8}  DE  \d{4}."
        # regex = r"\s*(LEI|DECRETO-LEI|DECRETO)\s+N\s+\w\s+(\d\.?)+,?\s+DE\s+\d{1,2}\s+DE\s+\w{4,9}\s+DE\s+\d{4}.\s*"
        try:
            tags = soup.find_all(string=re.compile(regex, re.IGNORECASE), limit=1)
            logger.debug(f'tags: {tags}')
            check_parent(
                soup=tags[0],
                tag_name='p',
                key='class',
                value='epigrafe'
            )
        except Exception as e:
            logger.error(f"{stack()[0][3]}: epigrafe não localizada", exc_info=True)
        return True

    @staticmethod
    def link_css(**kwargs) -> BeautifulSoup:
        '''

        :param kwargs: url
        :return: soup with tag link of type css
        '''
        urls=["http://www.planalto.gov.br/ccivil_03/css/legis_3.css",
              "https://www.planalto.gov.br/ccivil_03/css/legis_3.css"]
        # urls.append('../../../css/legis_3.css')

        if 'url' in kwargs:
            urls.append(kwargs['url'])

        soup = BeautifulSoup('', 'html.parser')
        for item in urls:
            soup.append(soup.new_tag('link', type="text/css", rel="stylesheet", href=item))
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def charset(**kwargs) -> BeautifulSoup:
        ''''''
        soup = BeautifulSoup('', 'lxml')
        tag = soup.new_tag('meta')
        tag2 = soup.new_tag('meta')
        tag3 = soup.new_tag('meta')
        try:
            tag['content'] = 'text/html; charset={}'.format(kwargs['charset'])
            tag2['charset'] = kwargs['charset']
        except:
            tag['content'] = 'text/html; charset=UTF-8'
            tag2['charset'] = 'UTF-8'
        finally:
            tag['http-equiv'] = "Content-Type"
            tag3['http-equiv'] = "Content-Language"
            tag3['content'] = "pt-br"
            soup.append(tag3)
            soup.append(tag)
            soup.append(tag2)
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def meta(**kwargs):
        itens = {
            'numero': '',
            'tipo': 'decreto',
            'ano': dt.today().strftime('%Y'),
            'situacao': "vigente ou revogado",
            'origem': 'Poder Executivo',
            'chefe_de_governo': '',
            'referenda': '',
            'correlacao': '',
            'veto': '',
            'dataassinatura': '',
            "generator_user": "@britodfbr",
            'publisher': 'Centro de Estudos Jurídicos da Presidência da República',
            "Copyright":
                'PORTARIA Nº 1.492 DE 5/10/2011. http://www.planalto.gov.br/ccivil_03/Portaria/P1492-11-ccivil.htm',
            'fonte': '',
            'presidente_em_exercicio': '',
            'vice_presidente': '',
            'revised': dt.today().strftime('%Y-%m-%d %X %z'),
            'description': 'Atos Normativos Federais do Governo Brasileiro',
            'keywords':
                'SAJ, Subchefia para Assuntos Jurídicos,Presidência da República,PR, Atos Jurídicos do Governo Federal',
            'robots': 'index, nofollow',
            'googlebot': 'index, follow',
            'generator': 'Centro de Estudos Juridicos (CEJ/SAJ/CC/PR)',
            'reviewer': ''
        }
        soup = BeautifulSoup('', 'html.parser')

        for key, value in itens.items():
            tag = soup.new_tag('meta')
            tag['content'] = value
            tag['name'] = key
            soup.append(tag)
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def nav(min_li: int=5):
        '''
        <nav>
        <ul>
        <li class="fixo">
           <a class="show-action" href="#">Texto completo</a>
           <a class="hide-action" href="#view">Texto original</a>
        </li>
        <li class="fixo"><a class="textoimpressao" href="#textoimpressao">Texto para impressão</a></li>
        <li class="fixo"><a href="#">Vide Recurso extraordinário nº 522897</a></li>
        <li  class="fixo"> </li>
        <li  class="fixo"> </li>
        <li  class="fixo"> </li>
        <li class="fixo">
            <label for="something" class="abrir"> Ver mais.. </label>
        </li>
        <li>
            <label for="something"> Ocultar </label>
        </li>
        </ul>
        </nav>
        :return:
        '''

        soup = BeautifulSoup('', 'lxml')
        soup.append(soup.new_tag('nav'))
        soup.nav.append(soup.new_tag('ul'))
        soup.nav.ul.append(soup.new_tag('input', **{'type': "checkbox", 'id':"something"}))

        a = soup.new_tag('a', **{'href': "#view", 'class': "hide-action"})
        a.string = 'Texto compilado'

        a1 = soup.new_tag('a', **{'href': "#", 'class': "show-action"})
        a1.string = 'Texto atualizado'

        li = soup.new_tag('li', **{'class': 'fixo'})
        li.append(a)
        li.append(a1)
        soup.nav.ul.append(li)

        a2 = soup.new_tag('a', **{'href': "#textoimpressao", 'class': "textoimpressao"})
        a2.string = 'Texto para impressão'
        li1 = soup.new_tag('li', **{'class': 'fixo'})
        li1.append(a2)
        soup.nav.ul.append(li1)

        label = soup.new_tag('label', **{'for': "something", 'class': "abrir"})
        label.string = 'Ver mais ↡'

        label1 = soup.new_tag('label', **{'for': "something"})
        label1.string = 'Ocultar ↟'

        li2 = soup.new_tag('li', **{'class': 'fixo last'})
        li2.append(label)

        li3 = soup.new_tag('li', **{'class': 'last'})
        li3.append(label1)

        soup.nav.ul.append(li2)
        soup.nav.ul.append(li3)

        for i in range(min_li - 2):
            soup.nav.ul.append(soup.new_tag('li', **{'class': 'fixo'}))
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def baseurl(**kwargs):
        soup = BeautifulSoup('', 'lxml')
        if 'target' not in kwargs:
            kwargs['target'] = '_self'
        if 'href' not in kwargs:
            raise ValueError('href nao definido')
        soup.append(soup.new_tag('base', target=kwargs['target'], href=kwargs['href']))
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def header(**kwargs):
        '''  <header>
        <h1>
        Presidência da República
        </h1>
        <h2>
        Casa Civil
        </h2>
        <h3>
        Subchefia para Assuntos Jurídicos
        </h3>
        </header>'''
        if not kwargs:
            kwargs['h1'] = 'Presidência da República'
            kwargs['h2'] = 'Casa Civil'
            kwargs['h3'] = 'Subchefia para Assuntos Jurídicos'

        soup = BeautifulSoup('', 'lxml')
        soup.append(soup.new_tag('header'))
        soup.header.append(soup.new_tag('h1'))
        soup.header.append(soup.new_tag('h2'))
        soup.header.append(soup.new_tag('h3'))
        soup.header.h1.string = kwargs['h1']
        soup.header.h2.string = kwargs['h2']
        soup.header.h3.string = kwargs['h3']
        logger.info(f"{soup}")
        return soup

    @staticmethod
    def doctype(text='', default='html5'):
        DTD={'html5':'html',
            'html_401s':'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"',
            'html_401t': 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"',
            'html_401f':'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"',
            'xhtml_11': 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"',
            'xhtml_10f': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"',
            'xhtml_10t': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"',
            'xhtml_10s': 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"'
             }
        if not text:
            text = DTD[default]
        tag = Doctype(text)
        logger.info(tag)
        return tag

    @staticmethod
    def comment(text):
        tag = Comment(text)
        logger.info(tag)
        return tag

    @staticmethod
    def dou(text=None):
        soup = BeautifulSoup('', 'lxml')
        tag = soup.new_tag('p', **{'class': "dou"})
        tag.string = 'Este texto não substitui o publicado no D.O.U.'
        if text:
            tag['string'] = text
        logger.info(tag)
        return tag

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        try:
            if value:
                value = os.path.abspath(os.path.expanduser(value))
                assert os.path.exists(value), f"Arquivo {value} inexistente."
                self._file = value
        except AssertionError as e:
            logger.error(f"{value}: {e}")
            raise

    def get_soup_from_file(self, parser_index=0):
        parser = ["html.parser", 'lxml', 'lxml-xml', 'xml', 'html5lib']
        if not self._file:
            raise ValueError('self.file not defined')
        try:
            f = open(self._file).read()
        except:
            f = open(self._file, encoding='iso8859-1').read()

        self.soup = BeautifulSoup(f, parser[parser_index])
        return self.soup

    def replace_brastra(self, img=None, str_busca='Brastra', index=1):
        img_l=[
            'http://www.planalto.gov.br/ccivil_03/img/Brastra.gif',
            'http://www.planalto.gov.br/ccivil_03/img/Brastra.png',
            'http://www.planalto.gov.br/ccivil_03/img/Brastra01.png',
            'http://www.planalto.gov.br/ccivil_03/img/brasaorep.png'
        ]
        logo = self.soup.select(f'img[src*="{str_busca}"]')
        logger.debug(logo)
        if logo:
            logo[0]['alt'] = 'Brasão da República do Brasil'
            if img:
                logo[0]['src'] = img
            else:
                logo[0]['src'] = img_l[index]
        logger.debug(f"Novo logo: {logo}")
        return True, logo

    @classmethod
    def date_conv(cls, date):
        ''' convert date to timestamp
                :param date: ' de 8 de Janeiro de 1900'
                :return: 1900/1/8
        '''
        if platform.system() == 'Linux':
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        else:
            locale.setlocale(locale.LC_ALL, 'pt_BR')

        date = date.lower().replace('.', '').strip()
        logger.debug(date)
        try:
            result = dt.strptime(date, 'de %d de %B de %Y').strftime('%Y/%m/%d')
        except ValueError:
            result = dt.strptime(date, 'de %dº de %B de %Y').strftime('%Y/%m/%d')
        logger.debug(result)
        return result

    def set_date(self):
        tag = self.soup.select('p[class="epigrafe"]')[0].text.strip()
        logger.debug(tag)
        epigrafe = re.split('[,–.-]', tag)
        logger.debug(epigrafe)
        if epigrafe[-1]:
            self.date = self.date_conv(epigrafe[-1])
        else:
            self.date = self.date_conv(epigrafe[-2])
        logger.debug(self.date)
        return self.date


def run():
    a = Legis()
    print(type(a.link_css()))
    print((a.link_css().prettify()))

    print('*'*20)
    print(type(a.meta(numero=1234)))
    print(a.meta(numero=1234).prettify())
    print('*'*20)
    print(a.header().prettify())
    print('*'*20)
    print(a.nav().prettify())
    print('*'*20)
    print(a.baseurl(href='http://www.planalto.gov.br/ccivil_03/', target='_blank'))
    print('*' * 20)

    print(a.doctype())
    print(type(a.comment('Comentario de teste.')))

    print('*' * 20)
    a.file = '../../../CCIVIL_03/decreto/1980-1989/1985-1987/D95578.htm'
    print(a.file)
    print('*' * 20)
    print(a.get_soup_from_file())
    print('*' * 20)
    print(a.replace_brastra('http://www.planalto.gov.br/ccivil_03/img/Brastra.png'))
    print(a.soup)

    print('*' * 20)
    a.file = '../../../CCIVIL_03/decreto/D3630.htm'
    (a.get_soup_from_file())
    print(a.replace_brastra())
    print(a.soup)

    print(a.date_conv(' DE 8 DE MAIO DE 2018'))
    print(a.dou())
    print(a.meta(charset='UTF-8'))
    print(type(a.doctype()), a.doctype())

    soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    soup.insert(0, a.doctype(default='xhtml_11'))
    soup.body.append(a.comment("It's a comment!"))
    print(soup.prettify())

    soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    soup.insert(0, a.doctype())
    print(soup.prettify())

    soup = BeautifulSoup('', 'lxml')
    soup.append(a.baseurl(href='http://www.planalto.gov.br/ccivil_03'))
    print(soup.prettify())

    print(a.nav().prettify())

    print(a.charset())


if __name__ == '__main__':
    pass
    # run()
