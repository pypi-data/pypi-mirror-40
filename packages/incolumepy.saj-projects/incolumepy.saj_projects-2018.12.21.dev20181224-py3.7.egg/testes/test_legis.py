import os
import re
import sys
import shutil
import logging
import chardet
import datetime
from collections import namedtuple
from unittest import TestCase, main

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from incolumepy.saj_projects import legis, logger
    from incolumepy.saj_projects import clean
    from incolumepy.saj_projects.legis import Legis
    from incolumepy.saj_projects.legis import BeautifulSoup, Comment, Doctype, NavigableString, Tag
    __package__ = 'incolumepy.saj_projects'
except (ImportError, ModuleNotFoundError):
    from src.incolumepy.saj_projects import legis, logger
    from src.incolumepy.saj_projects import clean
    from src.incolumepy.saj_projects.legis import Legis
    from src.incolumepy.saj_projects.legis import BeautifulSoup, Comment, Doctype, NavigableString, Tag
    __package__ = 'src.incolumepy.saj_projects'

try:
    from unittest.mock import mock_open, patch, MagicMock, call, DEFAULT, Mock, sentinel
except ImportError:
    # Python < 3.3
    from mock import mock_open, patch, MagicMock, call, DEFAULT, Mock, sentinel


class TestLegis(TestCase):
    def setUp(self):
        self.valores = namedtuple('teste', 'entrada saida')
        # caminho de gravação
        self.arquivos = {
            '/tmp/file.html': '/tmp/file.html',
            '/tmp/teste/file.txt': '/tmp/teste/',
            '~/tmp/file.txt': os.path.expanduser('~/tmp/'),
            '~/file.txt': os.path.expanduser('~/file.txt'),
            'teste/file.txt': 'teste/',
            'file.txt': 'file.txt'
        }
        self.leg = legis.Legis()
        self.soup1 = BeautifulSoup('<div><p><b><i>teste</i></b></p></div>', 'html5lib')
        self.soup2 = BeautifulSoup('''<head>
        <meta name="GENERATOR" content="Microsoft FrontPage 6.0">
        <title>L8666consol</title>
        </head>
        <body bgcolor="#FFFFFF">
        <body bgcolor="#FFFFFF">
        <div align="center"><center>
        <table border="0" cellpadding="0" cellspacing="0" width="70%">
        <tr>
        <td width="14%"><p align="center">
        <img src="../Brastra.gif" alt="Brastra.gif (4376 bytes)" width="74" height="82"></td>
        <td width="86%"><p align="center"><font color="#808000" face="Arial">
        <strong><big><big>Presidência da República</big></big><br>
        <big>Casa Civil<br>
        </big>Subchefia para Assuntos Jurídicos</strong></font></td>
        </tr>
        </table>
        </center></div>
        <p align="center">
        <a 
        href="http://legislacao.planalto.gov.br/legisla/legislacao.nsf/Viw_Identificacao/lei%208.666-1993?OpenDocument">
        <font face="Arial" color="#000080">
        <strong><small>LEI Nº 8.666, DE 21 DE JUNHO DE 1993</small></strong></font></a></p>
        <table border="0" width="100%" cellspacing="0" cellpadding="0"><tr>
        <td width="51%"><font face="Arial"><small><a href="L8666compilado.htm">Texto compilado</a></small><br>
        <a href="Mensagem_Veto/anterior_98/Vep335-L8666-93.pdf">
        <small>Mensagem de veto</small></a></font><p>
        <font face="Arial">
        <font size="2"><a href="../decreto/Antigos/D99658.htm">(Vide Decreto nº 99.658, de 1990)</a></font><br>
        <font size="2"><a href="../decreto/Antigos/D1054.htm">(Vide Decreto nº 1.054, de 1994)</a></font><br>
        <font size="2"><a href="../_Ato2007-2010/2010/Decreto/D7174.htm">(Vide Decreto nº 7.174, de 2010)</a></font>
        <br></font><font face="Arial" style="font-size: smaller">
        <a href="../_Ato2011-2014/2011/Mpv/544.htm#art15">
        (Vide Medida Provisória nº 544, de 2011)</a></font><font FACE="Arial" SIZE="2"><br>
        <span style="color:black">
        <a href="../_Ato2011-2014/2012/Lei/L12598.htm#art15">(Vide Lei nº 12.598, de 2012)</a></span></font></td>
        <td width="49%"><p ALIGN="JUSTIFY"><font face="Arial" color="#800000"><small>Regulamenta o
        art. 37, inciso XXI, da Constituição Federal, institui normas para licitações e
        contratos da Administração Pública e dá outras providências.</small></font></td>
        </tr></table><p ALIGN="JUSTIFY" style="text-indent: 30px"><small><font face="Arial">
        <strong>O&nbsp;PRESIDENTE DA REPÚBLICA </strong>Faço&nbsp;saber&nbsp;que&nbsp;o Congresso 
        Nacional decreta e eu sanciono&nbsp;a&nbsp;seguinte Lei:</font></small></p>
        <p ALIGN="CENTER"><font face="Arial"><small>Capítulo I</small><br>
        <small>DAS DISPOSIÇÕES GERAIS</small></font></p>
        <p ALIGN="CENTER"><b><font face="Arial"><small>Seção I</small><br>
        <small>Dos Princípios</small></font></b></p>

        <p ALIGN="JUSTIFY" style="text-indent: 30px"><small><font face="Arial">
        <a name="art1"></a>Art.&nbsp;1<sup><u>o</u></sup>&nbsp;&nbsp;Esta Lei estabelece normas gerais sobre
        licitações e contratos administrativos pertinentes a obras, serviços, inclusive de
        publicidade, compras, alienações e locações no âmbito dos Poderes da União, dos
        Estados, do Distrito Federal e dos Municípios.</font></small></p>
        <p ALIGN="JUSTIFY" style="text-indent: 30px"><small>
        <font face="Arial">
        Brasília,&nbsp;21&nbsp;de junho&nbsp;de 1993, 172<sup><u>o</u></sup> da Independência e 105
        <sup><u>o</u></sup> da República.</font></small></p>
        <p ALIGN="JUSTIFY"><font face="Arial"><small>ITAMAR FRANCO</small><br>
        <em><small>Rubens Ricupero</small><br>
        <small>Romildo Canhim</small></em></font></p>
        <p ALIGN="JUSTIFY"><font face="Arial" color="#FF0000"><small>Este texto não substitui o
        publicado no DOU de 22.6.1993, 
        <font color="#FF0000">republicado em 6.7.1994 e </font>
        <a href="1989_1994/RET/rlei-8666-93.pdf">
        <font color="#FF0000">retificado em&nbsp; 6.7.1994</font></a></small></font></p>
        <p align="center"><font color="#FF0000">*</font></p>''', 'html5lib')

    def tearDown(self):
        del self.leg
        del self.soup1
        for arquivo in self.arquivos.values():
            try:
                if os.path.exists(arquivo):
                    os.remove(arquivo)
                    logging.debug(f'removido: {arquivo}')
            except IsADirectoryError:
                shutil.rmtree(arquivo)
                logging.debug(f'removido: {arquivo}')
            except Exception as e:
                logging.debug(f'{arquivo}: {e}')

    def test_instance(self):
        self.assertTrue(isinstance(self.leg, legis.Legis))

    def test_link(self):
        e = '<link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>'
        e += '<link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>'
        self.assertEqual(type(self.leg.link_css()), BeautifulSoup)
        self.assertEqual(BeautifulSoup(e, 'html.parser'), self.leg.link_css())

    def test_header(self):
        h = '<header>'
        h += '<h1>Presidência da República</h1>'
        h += '<h2>Casa Civil</h2>'
        h += '<h3>Subchefia para Assuntos Jurídicos</h3>'
        h += '</header>'
        self.assertEqual(type(self.leg.header()), BeautifulSoup)
        self.assertEqual(BeautifulSoup(h, 'html.parser'), self.leg.header())

    def test_baseUrl(self):
        with self.assertRaisesRegex(ValueError, 'href nao definido'):
            self.leg.baseurl()
        href = "http://www.planalto.gov.br/ccivil_03/"
        result = '<base href="{}" target="{}"/>'
        self.assertEqual(type(self.leg.baseurl(href=href)), BeautifulSoup)

        result0 = BeautifulSoup(result.format(href, '_blank'), 'html.parser')
        self.assertEqual(result0, self.leg.baseurl(href=href, target='_blank'))

        result1 = BeautifulSoup(result.format(href, 'novajanela'), 'html.parser')
        self.assertEqual(result1, self.leg.baseurl(href=href, target='novajanela'))

    def test_nav(self):
        soup = legis.Legis.nav(min_li=5)
        soup2 = legis.Legis.nav(min_li=3)

        self.assertEqual(type(soup), BeautifulSoup)
        self.assertEqual(str(soup),
                         '<nav><ul><input id="something" type="checkbox"/>'
                         '<li class="fixo"><a class="hide-action" href="#view">Texto compilado</a>'
                         '<a class="show-action" href="#">Texto atualizado</a></li>'
                         '<li class="fixo"><a class="textoimpressao" href="#textoimpressao">Texto para impressão</a>'
                         '</li><li class="fixo last"><label class="abrir" for="something">Ver mais ↡</label></li>'
                         '<li class="last"><label for="something">Ocultar ↟</label></li><li class="fixo"></li>'
                         '<li class="fixo"></li><li class="fixo"></li></ul></nav>')

        self.assertEqual(type(soup2), BeautifulSoup)
        self.assertEqual(str(soup2),
                         '<nav><ul><input id="something" type="checkbox"/>'
                         '<li class="fixo"><a class="hide-action" href="#view">Texto compilado</a>'
                         '<a class="show-action" href="#">Texto atualizado</a></li><li class="fixo">'
                         '<a class="textoimpressao" href="#textoimpressao">Texto para impressão</a></li>'
                         '<li class="fixo last"><label class="abrir" for="something">Ver mais ↡</label></li>'
                         '<li class="last"><label for="something">Ocultar ↟</label></li>'
                         '<li class="fixo"></li></ul></nav>')

    def test_comentario(self):
        result1 = 'Comentario de teste.'
        op = self.leg.comment(result1)
        self.assertEqual(Comment, type(op))
        self.assertEqual(result1, op)

    def test_doctype(self):

        self.assertEqual(Doctype, type(self.leg.doctype()))

        self.assertEqual('html', self.leg.doctype())

        self.assertEqual('html', self.leg.doctype(default='html5'))

        r1 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"'
        self.assertEqual(r1, self.leg.doctype(default='html_401s'))
        self.assertEqual(r1, self.leg.doctype(r1))

        r2 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"'
        self.assertEqual(r2, self.leg.doctype(default='html_401t'))
        self.assertEqual(r2, self.leg.doctype(r2))

        r3 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"'
        self.assertEqual(r3, self.leg.doctype(default='html_401f'))
        self.assertEqual(r3, self.leg.doctype(r3))

        r4 = 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'
        self.assertEqual(r4, self.leg.doctype(default='xhtml_11'))
        self.assertEqual(r4, self.leg.doctype(r4))

        r5 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"'
        self.assertEqual(r5, self.leg.doctype(default='xhtml_10f'))
        self.assertEqual(r5, self.leg.doctype(r5))

        r6 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
        r6 += '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"'
        self.assertEqual(r6, self.leg.doctype(default='xhtml_10t'))
        self.assertEqual(r6, self.leg.doctype(r6))

        r7 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"'
        self.assertEqual(r7, self.leg.doctype(default='xhtml_10s'))
        self.assertEqual(r7, self.leg.doctype(r7))

    def test_date_conv(self):
        print(self.leg.date_conv('de 8 de maio de 2018'))

        self.assertEqual('2018/05/08', self.leg.date_conv(' DE 8 DE MAIO DE 2018'))
        self.assertEqual('2018/06/01', self.leg.date_conv(' DE 1º DE JUNHO DE 2018'))
        self.assertEqual('2018/12/01', self.leg.date_conv(' DE 1º DE dezembro DE 2018'))

    def test_date_conv_raises(self):
        self.assertRaises(ValueError, self.leg.date_conv, ' de 29 de fevereiro de 1900')
        with self.assertRaisesRegex(ValueError,
                                    "de 29 de fevereiro de 1891' does not match format 'de %dº de %B de %Y'"):
            self.leg.date_conv(' de 29 de fevereiro de 1891')

    def test_dou(self):
        from bs4.element import Tag
        r1 = '<p class="dou">Este texto não substitui o publicado no D.O.U.</p>'
        expected = BeautifulSoup(r1, 'html.parser').p
        self.assertEqual(type(self.leg.dou()), Tag)
        self.assertTrue(isinstance(self.leg.dou(), Tag))
        self.assertEqual(expected, self.leg.dou())

    def test_locate_parent(self):
        q = self.soup1.find_all(string='teste')
        self.assertEqual(q[0], 'teste')
        self.assertEqual(type(q[0]), NavigableString)
        self.assertEqual(q[0].name, None)
        self.assertEqual(q[0].parent.name, 'i')
        self.assertEqual(Tag, type(legis.locate_parent(soup=q[0], tag_name='div')))
        self.assertEqual('<div><p><b><i>teste</i></b></p></div>',
                         str(legis.locate_parent(soup=q[0], tag_name='div')))

        with self.assertRaisesRegex(TypeError, 'Not instance bs4'):
            legis.locate_parent(soup='<div><p><b><i>teste</i></b></p></div>', tag_name='div')

    def test_change_parent0(self):
        s = BeautifulSoup('<div><span><b><i><u>oi</div>', 'html5lib')

        with self.assertRaisesRegex(TypeError, 'Soup must be instance bs4'):
            legis.change_parent(soup='<div>oi</div>', tag_name='div', new_tag_name='p')
            legis.change_parent(soup='oi', tag_name='div', new_tag_name='p')

        with self.assertRaisesRegex(ValueError, 'atributo tag_name deverá ser informado'):
            legis.change_parent(soup=s, new_tag_name='div')

        with self.assertRaisesRegex(ValueError, "atributo new_tag_name deverá ser informado"):
            legis.change_parent(soup=s, tag_name='div')

        legis.change_parent(soup=s.find(string='oi'), tag_name='div', new_tag_name='p')
        self.assertNotRegex(s.prettify(), 'div')

    def test_change_parent1(self):
        with self.assertRaises(TypeError):
            legis.change_parent(soup='<div>oi</div>', tag_name='div')

        q = self.soup1.find(string='teste')
        result = legis.change_parent(soup=q, tag_name='div', new_tag_name='blockquote')
        self.assertEqual('blockquote', result.name)
        self.assertNotRegex(self.soup1.prettify(), 'div')
        self.assertRegex(self.soup1.prettify(), 'blockquote')

    def test_check_parent(self):
        with self.assertRaisesRegex(AssertionError, 'Not instance bs4'):
            legis.check_parent(soup='<div>oi</div>', tag_name='div')

        q = self.soup1.find_all(string='teste')
        result = legis.check_parent(soup=q[0], tag_name='p', key='id', value='date')
        self.assertEqual('<p id="date"><b><i>teste</i></b></p>', str(result))
        self.assertEqual('date', self.soup1.p['id'])

    def test_save_html_file(self):
        # verificação dos parametros de entrada
        mock_save_html_file = Mock(spec=legis.save_html_file)
        mock_save_html_file(conteudo=self.soup1, filename='/tmp/file.html')
        esperado = call(conteudo=self.soup1, filename='/tmp/file.html')
        self.assertEqual(esperado, mock_save_html_file.call_args)

        texto = '<p>açaí é brasileiro!</p>'
        soup = BeautifulSoup(texto, 'html5lib')
        # test encoding ISO8859-1
        mock_save_html_file.return_value = soup.prettify(encoding='iso8859-1')
        self.assertRegex(r'ISO-8859-1', chardet.detect(mock_save_html_file('file')).get('encoding'))

        # test encoding utf-8
        mock_save_html_file.return_value = soup.prettify(encoding='utf-8')
        self.assertRegex(r'utf-8', chardet.detect(mock_save_html_file('file')).get('encoding'))

        mock_save_html_file.return_value = soup.prettify(encoding='iso8859-1')
        # verificação dos tipos de entrada
        with self.assertRaisesRegex(ValueError, '"conteudo" deve ser um código HTML de tipo "str"'):
            legis.save_html_file(conteudo=self.soup1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=1.1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=object(), filename='/tmp/file.html')
            legis.save_html_file(conteudo=object, filename='/tmp/file.html')

        with self.assertRaisesRegex(ValueError,'"filename" deve ser um caminho válido no sistemas de arquivo de tipo "str"'):
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=object)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=object())
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=1)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=1.1)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=self.soup1)

        ## caminhos inexistentes
        for arquivo in self.arquivos.keys():
            self.assertFalse(os.path.exists(arquivo))
            _, file = legis.save_html_file(self.soup1.prettify(), arquivo)
            logging.debug(f'{os.path.exists(file)}, {file}')
            self.assertTrue(os.path.exists(file))

    def test_presidente_identify(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../incolumepy/saj_projects/data/presidentes.json")
        )
        assert os.path.isfile(file), F"{file} indisponível ou inexistente"
        self.assertEqual(['ITAMAR FRANCO'], legis.presidente_identify(soup=self.soup2, json_file=file))

    def test_loc_epigrafe(self):
        t = [
            '<p><a href="#"><b>LEI Nº10.406,  DE  10  DE  JANEIRO  DE  2002.</b></a></p>',
            '<p><a href="#"><b>DECRETO-LEI Nº10.406,  DE  10  DE  JANEIRO  DE  2002.</b></a></p>',
            '<p><a href="#"><b>DECRETO Nº10.406,  DE  10  DE  JANEIRO  DE  2002.</b></a></p>',
            '<p align="CENTER"><a href="#"><font face="Arial" color="#000080"><small>'
            '<strong>LEI N<sup>o</sup> 8.156, DE 28 DE JANEIRO DE 1990.</strong></small></font></a></p>',
            '<p align="CENTER"><a href="#"><font color="#000080" face="Arial"><small>'
            '<strong>DECRETO-LEI N<sup>o</sup>10.406, DE 10 DE JANEIRO DE 2002.</strong></small></font></a></p>',
            self.soup2.prettify(),
        ]
        for i, item in enumerate(t):
            # print(i, item)
            item = clean.ordinais(item)
            # print(i, item)
            soup = BeautifulSoup(item, 'html.parser')
            self.assertTrue(legis.Legis.loc_epigrafe(soup))
            self.assertIn('class="epigrafe"', str(soup))
            # print(soup)

        with self.assertRaises(AssertionError):
            legis.Legis.loc_epigrafe('fail')

    def test_loc_presidente_exercicio(self):
        file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/presidente_exercicio.csv'))
        assert os.path.exists(file), 'Arquivo {} indisponivel'.format(file)
        self.assertEqual(['ITAMAR FRANCO'], legis.loc_presidente_exercicio(soup=self.soup2, presidentes_file=file))

    def test_vice_identify(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../incolumepy/saj_projects/data/presidentes.json')
        )
        assert os.path.isfile(file), f"Ops: Arquivo \"{file}\" Inexistente"
        t = namedtuple('teste', 'entrada saida')
        testes = [
            t('1993', []),
            t('1905', 'FRANCISCO SILVIANO DE ALMEIDA BRANDÃO'),
            t(2008, 'JOSÉ ALENCAR GOMES DA SILVA'),
            t(2012, 'MICHEL MIGUEL ELIAS TEMER LULIA')
        ]
        for teste in testes:
            self.assertEqual(teste.saida, legis.vice_identify(json_file=file, ano=teste.entrada))

    def test_loc_data_assinatura(self):
        datas_teste = [
            '<p>Brasília, 10 de janeiro de 2002; 181º da Independência e 114º da República.</p>',
            '<p>Brasília, 11 de janeiro de 1973; 152o da Independência e 85o da República.</p>',
            '<p>Brasília, 16 de março de 2015; 194o da Independência e 127o da República.</p>',
            '<p>Rio de Janeiro, 10 de janeiro de 1902; 18º da Independência e 1º da República.</p>',
            '<p> Senado Federal, 1º de dezembro de 1978; 99º da República e 99º da Independência.</p>'
        ]
        for item in datas_teste:
            s = BeautifulSoup(item, 'html.parser')
            Legis.loc_data_assinatura(soup=s)
            self.soup2.select('[class="data"]')
            logging.debug(s.prettify())
            self.assertEqual('p', s.p.name)
            self.assertEqual({'class': 'data'}, s.p.attrs)

    def test_loc_dou(self):
        self.assertEqual(None, Legis.loc_dou(soup=self.soup2))
        s = self.soup2.select('[class="dou"]')
        self.assertEqual('p', s[0].name)
        self.assertEqual({'align': 'JUSTIFY', 'class': 'dou'}, s[0].attrs)

    def test_Legis_charset(self):
        # teste UTF-8
        self.assertEqual(
            '<meta content="pt-br" http-equiv="Content-Language"/>'
            '<meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>'
            '<meta charset="UTF-8"/>', str(legis.Legis.charset(charset='UTF-8')))

        # teste iso8859-1
        self.assertEqual('<meta content="pt-br" http-equiv="Content-Language"/>'
                         '<meta content="text/html; charset=iso8859-1" http-equiv="Content-Type"/>'
                         '<meta charset="iso8859-1"/>', str(legis.Legis.charset(charset='iso8859-1')))

    @patch(f'{__package__}.legis.dt')
    def test_meta(self, mock_date):
        expected = '<meta content="" name="numero"/>' \
                   '<meta content="decreto" name="tipo"/>' \
                   '<meta content="2018" name="ano"/>' \
                   '<meta content="vigente ou revogado" name="situacao"/>' \
                   '<meta content="Poder Executivo" name="origem"/>' \
                   '<meta content="" name="chefe_de_governo"/>' \
                   '<meta content="" name="referenda"/>' \
                   '<meta content="" name="correlacao"/>' \
                   '<meta content="" name="veto"/>' \
                   '<meta content="" name="dataassinatura"/>' \
                   '<meta content="@britodfbr" name="generator_user"/>' \
                   '<meta content="Centro de Estudos Jurídicos da Presidência da República" name="publisher"/>' \
                   '<meta content="PORTARIA Nº 1.492 DE 5/10/2011. ' \
                   'http://www.planalto.gov.br/ccivil_03/Portaria/P1492-11-ccivil.htm" name="Copyright"/>' \
                   '<meta content="" name="fonte"/>' \
                   '<meta content="" name="presidente_em_exercicio"/>' \
                   '<meta content="" name="vice_presidente"/>' \
                   '<meta content="2018-12-14 12:34:56" name="revised"/>' \
                   '<meta content="Atos Normativos Federais do Governo Brasileiro" name="description"/>' \
                   '<meta content="SAJ, Subchefia para Assuntos Jurídicos,Presidência da República,PR, ' \
                   'Atos Jurídicos do Governo Federal" name="keywords"/>' \
                   '<meta content="index, nofollow" name="robots"/>' \
                   '<meta content="index, follow" name="googlebot"/>' \
                   '<meta content="Centro de Estudos Juridicos (CEJ/SAJ/CC/PR)" name="generator"/>' \
                   '<meta content="" name="reviewer"/>'
        mock_date.today.return_value = legis.dt(2018, 12, 14, 12, 34, 56)
        mock_date.today.return_value.strftime.side_effect = ['2018', "2018-12-14 12:34:56"]
        soup = legis.Legis.meta()
        self.assertIsNotNone(str(soup))
        self.assertEqual(expected, str(soup))

    def test_governo_ano(self):
        results = {
            '1889': 'MANUEL DEODORO DA FONSECA',
            1894: 'FLORIANO VIEIRA PEIXOTO',
            1908: 'AFONSO AUGUSTO MOREIRA PENA',
            '1905': 'FRANCISCO DE PAULA RODRIGUES ALVES',
            1955: 'JOÃO FERNANDES CAMPOS CAFÉ FILHO',
            '1956': 'NEREU DE OLIVEIRA RAMOS',
            1961: 'JUSCELINO KUBITSCHEK DE OLIVEIRA',
            '1978': 'ERNESTO BECKMANN GEISEL',
            1985: 'JOÃO BAPTISTA DE OLIVEIRA FIGUEIREDO',
            '2009': 'LUIZ INÁCIO LULA DA SILVA',
            '2011': 'DILMA VANA ROUSSEFF',
            '2018': 'MICHEL MIGUEL ELIAS TEMER LULIA',
            2019: 'JAIR MESSIAS BOLSONARO'
        }
        file = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../incolumepy/saj_projects/data/presidentes.json"))
        assert open(file).read(), f"Arquivo {file} indisponível!"
        for item in results.keys():
            logging.debug(f"{type(item)} {item} {legis.governo_ano(json_file=file, ano=item)}")
            self.assertEqual(results[item], legis.governo_ano(json_file=file, ano=item))


    def test_loc_ministro(self):
        ministros = list(sorted((legis.loc_ministro(self.soup2))))

        #print(ministros)

        self.assertEqual('Romildo Canhim', ministros[0])
        self.assertEqual('Rubens Ricupero', ministros[1])

    def test_presidente_em_exercicio(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../incolumepy/saj_projects/data/presidentes.json")
        )
        assert os.path.isfile(file), f"Ops: Arquivo \"{file}\" inexistente .."

        self.assertEqual(['ITAMAR FRANCO'], legis.presidente_em_exercicio(soup=self.soup2, json_file=file))
        # Teste avançado .. implementar no futuro
        # self.assertEqual(
        #     legis.presidente_em_exercicio(soup=self.soup2, json_file=file),
        #     legis.loc_presidente_exercicio(soup=self.soup2)
        # )

    def test_file(self):
        local = legis.Legis()
        local.file = os.sep #Raiz do SO
        assert os.path.isdir(local.file), "Diretório indisponível."

    def test_replace_brastra(self):
        lista = [
            '''<table width="70%" cellspacing="0" cellpadding="0" border="0">
            <tbody><tr>
            <td width="14%">
            <p align="center"><font size="2">
            <img src="../../../_Ato2007-2010/2008/Decreto/Image4.gif" width="76" height="82"></font></p></td>
            <td width="86%"><p align="center"><font face="Arial" color="#808000"><strong><big><big>
            Presidência da República</big></big><br>
            <big>Casa Civil<br>
            </big>Subchefia para Assuntos Jurídicos</strong></font></p></td>
            </tr>
            </tbody></table>''',
            '''<table width="76%" cellspacing="0" cellpadding="0" border="0">
            <tbody><tr>
            <td width="14%"><p align="center">
            <img src="../decreto/Brastra.gif" alt="Brastra.gif (4376 bytes)" width="74" height="82"></p></td>
            <td width="86%"><p align="center"><font face="Arial" color="#808000"><strong><big><big>Presidência
            da República</big></big><br>
            <big>Casa Civil<br>
            </big>Subchefia para Assuntos Jurídicos</strong></font></p></td>
            </tr>
            </tbody></table>'''
        ]
        for item in lista:
            s = BeautifulSoup(item, 'html5lib')
            a = Legis(soup=s)
            a.replace_brastra(str_busca='Image4')
            a.replace_brastra()

            self.assertIn('Brasão da República do Brasil', s.prettify())
            self.assertEqual('Brasão da República do Brasil', s.img['alt'])
            self.assertRegex(s.img['src'], 'http://www.planalto.gov.br/ccivil_03/img/Brastra.png')

    def test_set_date(self):
        epigrafes = {
            '<p class="epigrafe">LEI Nº 7.565, DE 1º DE Maio DE 1956.</p>': '1956/05/01',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565, DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565 - DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565 – DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565. DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO Nº 7.565, DE 9 DE Junho DE 1978.</p>': '1978/06/09'
        }
        for item in epigrafes.keys():
            logging.debug(item)
            s = BeautifulSoup(item, 'html5lib')
            # print(s.prettify())
            o = Legis(soup=s)
            # print(o.soup.prettify())
            o.set_date()
            self.assertIsInstance(o.date, str)
            self.assertEqual(epigrafes[item], o.date)

    @patch(f'{__package__}.legis.get_conteudo_requests_url')
    def test_get_conteudo_url_0(self, mock_requests):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        tag = '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; açaí, úùûüÚÙŨÛÜ.</p>'
        soup = BeautifulSoup(tag, 'html5lib')
        mock_requests.return_value = soup.prettify(encoding='utf-8')
        result = legis.get_conteudo_url(url)
        self.assertIsNotNone(result)
        self.assertEqual(chardet.detect(result).get('encoding'), 'utf-8')
        self.assertTrue('açaí' in str(result, 'utf-8'))

    @patch(f'{__package__}.legis.get_conteudo_selenium_url')
    @patch(f'{__package__}.legis.get_conteudo_requests_url')
    def test_get_conteudo_url_1(self, mock_requests, mock_selenium):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        tag = '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; açaí, úùûüÚÙŨÛÜ.</p>'
        soup = BeautifulSoup(tag, 'html5lib')
        mock_requests.side_effect = TypeError
        mock_selenium.return_value = soup.prettify(encoding='iso8859-1')
        result = legis.get_conteudo_url(url)
        self.assertIsNotNone(result)
        self.assertTrue(re.match(r'ISO-8859', chardet.detect(result).get('encoding'), flags=re.I))
        self.assertTrue('açaí' in str(result, 'iso8859-1'))

    @patch('requests.get')
    def test_get_conteudo_requests_url(self, get_mock):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        text = '<!DOCTYPE html> <html> <head> </head> ' \
               '<body> <h1> Título </h1> <p> Olá o amanhã é açaí áàâãõoóò </p> </body> </html>'
        soup = BeautifulSoup(text, 'html5lib')

        #Validação ISO8859-1
        get_mock.return_value.content = soup.prettify(encoding='iso8859-1')
        content = legis.get_conteudo_requests_url(url)
        assert content, "Conteudo indisponível"
        self.assertRegex(chardet.detect(content).get('encoding'), r'ISO-8859-\d')
        self.assertEqual(text, clean.one_line(str(content, encoding='iso8859-1')))

        # Validação UTF-8
        get_mock.return_value.content = soup.prettify(encoding='utf-8')
        content = legis.get_conteudo_requests_url(url)
        assert content, "Conteudo indisponível"
        self.assertRegex(chardet.detect(content).get('encoding'), r'utf-8')
        self.assertEqual(text, clean.one_line(str(content, encoding='utf-8')))

    def test_get_conteudo_selenium_url(self):
        os.environ['MOZ_HEADLESS'] = '1' # faz webdriver executar em background

        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        tag = '<head><title>L10973</title></head>' \
              '<body>' \
              '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; açaí, úùûüÚÙŨÛÜ.</p>' \
              '</body>'
        soup = BeautifulSoup(tag, 'html5lib')
        conteudo = legis.get_conteudo_selenium_url(url)
        assert 'L10973' in conteudo, "Conteúdo legis.get_conteudo_selenium_url inválido."
        self.assertEqual('L10973', BeautifulSoup(conteudo, 'html5lib').title.text)
        self.assertEqual(str, type(conteudo))
        self.assertEqual('LEI Nº 10.973' in conteudo, True)
        self.assertTrue('LUIZ INÁCIO LULA DA SILVA' in conteudo)
        # self.assertTrue(re.match(r'LEI Nº 10.973', conteudo, flags=re.I))
        # self.assertEqual(tag, conteudo) # implementar corretamente o mock no futuro

    def test_Legis_definir_titulos(self):
        y = [
            self.valores('<p>PREÂMBULO</p><p>teste</p><p>CAPÍTULO x</p><p>Livro iv</p>',
                         '<html> <head> </head> <body> <h4> PREÂMBULO </h4> <p> teste </p> '
                         '<h4> CAPÍTULO x </h4> <h4> Livro iv </h4> </body> </html>'),
            self.valores(
                '<html> <head> </head> <body> <p> PREÂMBULO </p><p> teste </p> <p> CAPÍTULO x </p> '
                '<p> Livro iv </p> </body> </html>',
                '<html> <head> </head> <body> <p> PREÂMBULO </p> <h2> teste </h2> <p> CAPÍTULO x </p> '
                '<p> Livro iv </p> </body> </html>'),
            self.valores(
                "<html> <head> </head> <body> <h5> PREÂMBULO </h5> "
                "<p> teste </p> <h5> CAPÍTULO x </h5> <h5> Livro iv </h5> </body> </html>",
                '<html> <head> </head> <body> <h2> PREÂMBULO </h2> <p> teste </p> '
                '<h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>'
            ),
            self.valores(
                "<p> PREÂMBULO </h2> <p> teste </p> <p> CAPÍTULO x </p> <p> Livro iv </p>",
                '<html> <head> </head> <body> '
                '<p> PREÂMBULO </p> <p> teste </p> <p> CAPÍTULO x </p> <h4> Livro iv </h4> '
                '</body> </html>'
            )
        ]
        # print("....Jesus....")
        soup = BeautifulSoup(y[0].entrada, 'html5lib')
        # print(clean.one_line(soup.prettify()))
        result = legis.Legis.definir_titulos(soup=soup,tag="p", nova_tag="h4")
        # print(result)
        self.assertEqual(y[0].saida, clean.one_line(result.prettify()))

        soup = BeautifulSoup(y[1].entrada, 'html5lib')
        result = legis.Legis.definir_titulos(soup=soup, titulos=["teste"], tag="p", nova_tag="h2")
        self.assertEqual(y[1].saida, clean.one_line(result.prettify()))

        soup = BeautifulSoup(y[2].entrada, 'html5lib')
        result = legis.Legis.definir_titulos(soup=soup,tag="h5", nova_tag="h2")
        self.assertEqual(y[2].saida, clean.one_line(result.prettify()))

        soup = BeautifulSoup(y[3].entrada, 'html5lib')
        result = legis.Legis.definir_titulos(soup=soup,tag="p", nova_tag="h4", titulos=['livro'])
        self.assertEqual(y[3].saida, clean.one_line(result.prettify()))

    def test_definir_titulos(self):
        y = [
            self.valores('<p>PREÂMBULO</p>',
                         '<h4> PREÂMBULO </h4>'),
            self.valores('<p>PREÂMBULO</p><p>teste</p><p>CAPÍTULO x</p><p>Livro iv</p>',
                         '<h5> PREÂMBULO </h5> <p> teste </p> <h5> CAPÍTULO x </h5> <h5> Livro iv </h5>'),
            self.valores(
                '<html> <head> </head> <body> <h4> PREÂMBULO </h4><p> teste </p> '
                '<h4> CAPÍTULO x </h4> <h4> Livro iv </h4> </body> </html>',
                '<html> <head> </head> <body> <h5> PREÂMBULO </h5> <p> teste </p> '
                '<h5> CAPÍTULO x </h5> <h5> Livro iv </h5> </body> </html>'),
            self.valores(
                "<html> <head> </head> <body> <h5> PREÂMBULO </h5> "
                "<p> teste </p> <h5> CAPÍTULO x </h5> <h5> Livro iv </h5> </body> </html>",
                '<html> <head> </head> <body> <h2> PREÂMBULO </h2> '
                '<p> teste </p> <h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>'
            ),
            self.valores(
                "<html> <head> </head> <body> <h2> PREÂMBULO </h2> <p> teste </p> "
                "<h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>",
                '<html> <head> </head> <body> <h2> PREÂMBULO </h2> <h5> teste </h5> '
                '<h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>'
            ),
            self.valores(
                "<html> <head> </head> <body> <h2> PREÂMBULO </h2> <h2> teste </h2> "
                "<h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>",
                '<html> <head> </head> <body> <h2> PREÂMBULO </h2> <p> teste </p> '
                '<h2> CAPÍTULO x </h2> <h2> Livro iv </h2> </body> </html>'
            )
        ]

        self.assertEqual(y[0].saida, legis.definir_titulos(y[0].entrada, tag="p", nova_tag="h4"))
        self.assertEqual(y[1].saida, legis.definir_titulos(y[1].entrada, tag="p", nova_tag="h5"))
        self.assertEqual(y[2].saida, legis.definir_titulos(y[2].entrada, tag="h4", nova_tag="h5"))
        self.assertEqual(y[3].saida, legis.definir_titulos(y[3].entrada,tag="h5", nova_tag="h2"))
        self.assertEqual(y[4].saida, legis.definir_titulos(y[4].entrada,titulos=["teste"], tag="p", nova_tag="h5"))
        self.assertEqual(y[5].saida, legis.definir_titulos(y[5].entrada,titulos=["teste"], tag="h2", nova_tag="p"))

    def test_replaceLineThrough2Del(self):
        codigo_html = '<p><span style="color:black; text-decoration:line-through">' \
                      '<h4>  Tráfico internacional de pessoa para fim de exploração ' \
                      'sexual</h4></span></p>'

        codigo_html = legis.replaceLineThrough2Del(codigo_html)
        self.assertEqual(codigo_html, '<p> <del style="color:black; text-decoration:line-through"> '
                                      '<h4> Tráfico internacional de pessoa para fim de exploração sexual </h4> '
                                      '</del> </p>')

    def test_get_conteudo_file(self):

        arquivo = open('help.txt', 'w')
        arquivo.write('Teste')
        arquivo.close()


        assert legis.get_conteudo_file(filename="help.txt", encoding="iso8859-1"), "Arquivo help.txt indisponível"

        os.remove('help.txt')

    def test_get_conteudo(self):
        # raise NotImplementedError
        tag = '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.</p>'
        soup = BeautifulSoup(tag, 'html5lib')

        with self.assertRaises(Exception):
            # exceptions filename invalido
            legis.get_conteudo(filename='')
            # exception url invalida
            legis.get_conteudo(url=None)

        with patch.object(legis, 'get_conteudo_file') as mock_get_conteudo_file:
            mock_get_conteudo_file.return_value = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo(filename='file_mock')
            assert content, "Conteúdo iso8859-1 não apresentado"
            # teste encode iso8859-1
            self.assertRegex(chardet.detect(content).get('encoding'), 'ISO-8859-')

            mock_get_conteudo_file.return_value = soup.prettify(encoding='utf-8')
            content = legis.get_conteudo(filename='file_mock')
            assert content, "Conteúdo utf-8 não apresentado"
            self.assertRegex(chardet.detect(content).get('encoding'), 'utf-8')

        with patch.object(legis, 'get_conteudo_url') as mock_get_conteudo_url:
            mock_get_conteudo_url.return_value = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo(url='url')
            assert content, "Conteúdo não apresentado"

            # test encode iso8859-1
            self.assertRegex(chardet.detect(content).get('encoding'), 'ISO-8859-')
            mock_get_conteudo_url.return_value = soup.prettify(encoding='utf-8')
            content = legis.get_conteudo(url='url')
            assert content, "Conteúdo não apresentado"

            # test encode utf-8
            self.assertRegex(chardet.detect(content).get('encoding'), 'utf-8')

    def test_get_soup_from_file(self):
        a = Mock(spec=Legis)
        with patch('builtins.open', mock_open(read_data='<br />')):
            a.file = 'file.html'
            a.soup = BeautifulSoup('<br />', 'html.parser')
            # html.parser
            a.get_soup_from_file()
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<br/>', str(a.soup))

            # lxml
            a.soup = BeautifulSoup('<br />', 'lxml')
            a.get_soup_from_file(parser_index=1)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<html><body><br/></body></html>', str(a.soup))

            # 'lxml-xml'
            a.soup = BeautifulSoup('<br />', 'lxml-xml')
            a.get_soup_from_file(parser_index=2)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<?xml version="1.0" encoding="utf-8"?>\n<br/>', str(a.soup))

            # 'xml'
            a.soup = BeautifulSoup('<br />', 'xml')
            a.get_soup_from_file(parser_index=3)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<?xml version="1.0" encoding="utf-8"?>\n<br/>', str(a.soup))

            # 'html5lib'
            a.soup = BeautifulSoup('<br />', 'html5lib')
            a.get_soup_from_file(parser_index=4)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<html><head></head><body><br/></body></html>', str(a.soup))

    def test_replace_tag(self):
        codigo_html = '''
                        <html lang="pt-br">
                        <head>
                        <link href="//s7.addthis.com/static/r07/widget/css/widget005.old.css" media="all" rel="stylesheet" type="text/css"/>
                        <link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <meta content="pt-br" http-equiv="Content-Language"/>
                        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
                        <meta charset="UTF-8"/>
                        </head>
                        </html>
                    '''
        resultado = '''
                        <html lang="pt-br">
                        <head>
                        <link href="//s7.addthis.com/static/r07/widget/css/widget005.old.css" media="all" rel="stylesheet" type="text/css"/>
                        <link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <p content="pt-br" http-equiv="Content-Language"/>
                        <p content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
                        <p charset="UTF-8"/>
                        </head>
                        </html>
                    '''
        soup = BeautifulSoup(codigo_html, 'html.parser')

        legis.Legis.replace_tag(soup, 'meta', 'p')
        self.assertEqual(soup, BeautifulSoup(resultado, 'html.parser'))

    def test_extract_soup_set_tag_class(self):
        codigo_html = ['<a class="show-action" href="#">Texto completo</a><a class="hide-action" href="#view">Texto original</a>',
                       ' <a href="#art361"> Vigência</a>',
                       '<a href="../LEIS/L6538.htm">(Vide Lei nº 6.538, de 1978)</a>',
                       '<a href="../LEIS/L6538.htm">(Vide Lei nº 6.668, de 2020)</a>']
        cont = 0
        menu = '<nav><ul>'

        for link in codigo_html:
            soup = BeautifulSoup(link, 'html.parser')
            if link == '<a href="Del2848compilado.htm">Texto compilado</a>':
                valor = legis.extract_soup_set_tag_class(soup=soup, nova_tag='li', class_value='fixo', modo_texto=False)
            elif cont <= 2:
                valor = legis.extract_soup_set_tag_class(soup=soup, nova_tag='li', class_value='fixo', modo_texto=False)
            else:
                valor = legis.extract_soup_set_tag_class(soup=soup, nova_tag='li', class_value='', modo_texto=False)

            cont = cont + 1


            menu = '{html_code}{valor}'.format(html_code=menu, valor=valor)



        valor = '<li class="fixo"><label for="something" class="abrir"> Ver mais.. </label></li><li><label for="something"> Ocultar </label></li></ul></nav>'

        menu = '{html_code}{valor}'.format(html_code=menu, valor=valor)

        soup = BeautifulSoup(menu, 'html.parser')

        #Teste do modo texto
        self.assertEqual('<li class="">Texto completo</li>', str(legis.extract_soup_set_tag_class(soup=soup.find('a'), nova_tag='li', class_value='', modo_texto=True)))
        #Teste do modo não texto
        self.assertEqual('<nav><ul><li class="fixo"><a class="show-action" href="#">Texto completo</a><a class="hide-action" href="#view">Texto original</a></li><li class="fixo"> <a href="#art361"> Vigência</a></li><li class="fixo"><a href="../LEIS/L6538.htm">(Vide Lei nº 6.538, de 1978)</a></li><li class=""><a href="../LEIS/L6538.htm">(Vide Lei nº 6.668, de 2020)</a></li><li class="fixo"><label class="abrir" for="something"> Ver mais.. </label></li><li><label for="something"> Ocultar </label></li></ul></nav>', str(soup))

    def test_iconv(self):
        mock_iconv = Mock(spec=legis.iconv)
        content = "<h1> Título</h1> <p>á à é í ó ò ü ú açaí </p>"
        soup = BeautifulSoup(content, 'html5lib')

        mockFile = MagicMock(return_value=soup.prettify(encoding='utf-8'))

        assert os.path.exists(mockFile), "Arquivo Indisponível"
        # assert False, type(mockFile)

        self.assertIn('utf-8', chardet.detect(mockFile.return_value).values())
        self.assertEqual('utf-8', chardet.detect(mockFile.return_value)['encoding'])
        result = mock_iconv(filein=mockFile, encode_in='utf-8', encode_out='iso8859-1',fileout=None)

        self.assertEqual([call(encode_in='utf-8', encode_out='iso8859-1',
                              filein=mockFile, fileout=None)], mock_iconv.mock_calls)

        with patch('builtins.open', mockFile) as file:
            mock_iconv(file, encode_in='utf-8', encode_out='iso8859-1')


        # print(soup)
        #print(f'>>{result}')
        # print(mockFile.return_value)
        # self.assertIn('iso8859-1', chardet.detect(mockFile.return_value).values())
        # self.assertEqual('iso8859-1', chardet.detect(mockFile.return_value)['encoding'])


if __name__ == '__main__':
    main()
