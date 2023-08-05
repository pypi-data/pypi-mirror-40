from unittest import main, TestCase
from collections import namedtuple
try:
    from incolumepy.saj_projects import clean
except ImportError:
    from src.incolumepy.saj_projects import clean

try:
    from unittest import mock
except ImportError:
    import mock

class TestClean(TestCase):
    def setUp(self):
        self.valores = namedtuple('teste', 'entrada saida')
        self.t = self.valores('', '')

    def test_replace_break(self):
        self.assertEqual(dict, type(clean.replace_break.__annotations__))
        self.assertEqual({'codigo': str, 'return': str}, clean.replace_break.__annotations__)
        lista = [
            self.valores('<p></p>', '<p></p>'),
            self.valores('<p><br></p>', '<p></p><p></p>'),
            self.valores('<p><br/></p>', '<p></p><p></p>'),
            self.valores('<p><br /></p>', '<p></p><p></p>'),
            self.valores('<p><br><br/><br /></p>', '<p></p><p></p><p></p><p></p>'),
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.replace_break(item.entrada))

    def test_limpar_espacos(self):
        self.assertEqual(dict, type(clean.limpar_espacos.__annotations__))
        self.assertEqual({'codigo': str, 'return': str}, clean.limpar_espacos.__annotations__)
        t = self.valores
        t.entrada = '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;oi&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n\n\n\n\n\n\n\n\n</p>'
        t.saida = '<p> oi </p>'
        self.assertEqual(t.saida, clean.limpar_espacos(t.entrada))

    def test_remove_attr(self):
        self.assertEqual(dict, type(clean.remover_attr.__annotations__))
        self.assertEqual({'atributos': list, 'codigo': str, 'return': str}, clean.remover_attr.__annotations__)
        lista = [
            self.valores(
                entrada='<hr class="None"  />',
                saida='<html> <head> </head> <body> <hr/> </body> </html>'),
            self.valores(
                '<p class="RedNose" align="center"> Olá </p>',
                '<html> <head> </head> <body> <p align="center"> Olá </p> </body> </html>'),
            self.valores(
                '<p class="texto2" align="center"> Olá </p>',
                '<html> <head> </head> <body> <p align="center"> Olá </p> </body> </html>')
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.remover_attr(item.entrada, ['class']))
        self.assertEqual(lista[1].saida, clean.remover_attr(lista[1].entrada, ['class=RedNose']))
        self.assertEqual(lista[1].saida, clean.remover_attr(lista[1].entrada, ['class^=Red']))
        self.assertEqual(lista[1].saida, clean.remover_attr(lista[1].entrada, ['class$=Nose']))
        self.assertEqual(lista[1].saida, clean.remover_attr(lista[1].entrada, ['class*=edNo']))

        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class=texto2']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class*=ext']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class^=text']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class$=xto2']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class="texto2"']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class*="xt"']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class^="tex"']))
        self.assertEqual(lista[2].saida, clean.remover_attr(lista[2].entrada, ['class$="xto2"']))


    def test_desatachar_tags(self):
        self.assertEqual(dict, type(clean.desatachar_tags.__annotations__))
        self.assertEqual({'codigo': str, 'return': str, 'tags': list}, clean.desatachar_tags.__annotations__)
        entrada = '<html><head></head><body><font><span>oi</span></font></body></html>'
        saida = '<html>\n <head>\n </head>\n <body>\n  oi\n </body>\n</html>'
        self.assertEqual(saida, clean.desatachar_tags(entrada, ['font', 'span']))

    def test_ordinais(self):
        self.assertEqual(dict, type(clean.ordinais.__annotations__))
        self.assertEqual({'codigo': str, 'return': str}, clean.ordinais.__annotations__)
        lista_testes = [
            self.valores('N<sup>o</sup>', '<html> <head> </head> <body> Nº </body> </html>'),
            self.valores('1<sup><u>o</u></sup>', '<html> <head> </head> <body> 1º </body> </html>'),
            self.valores('2<u><sup>a</sup></u>', '<html> <head> </head> <body> 2ª </body> </html>'),
            self.valores('1<sup>  <u> o </u> </sup> e 2<sup> <u> a</u> </sup>',
                         '<html> <head> </head> <body> 1º e 2ª </body> </html>'),
            self.valores('1<sup>  <u> o </u> \n\n\n\n\n\n</sup> e 2<sup> \n<u> \na</u> </sup>',
                         '<html> <head> </head> <body> 1º e 2ª </body> </html>'),
        ]
        for item in lista_testes:
            self.assertEqual(item.saida, clean.ordinais(item.entrada))

    def test_remover_tags(self):
        self.assertEqual(dict, type(clean.remover_tags.__annotations__))
        self.assertEqual({'codigo': str, 'return': str, 'tags': list}, clean.remover_tags.__annotations__)
        entrada = '<html><head></head><body><font><span>oi</span></font></body></html>'
        saida = '<html> <head> </head> <body> </body> </html>'
        self.assertEqual(saida, clean.remover_tags(entrada, ['font']))

    def test_remover_acentos(self):
        self.assertEqual(dict, type(clean.remover_acentos.__annotations__))
        self.assertEqual({'txt': str, 'return': str}, clean.remover_acentos.__annotations__)
        entrada = 'áàãâäÁÀÃÂÄ! éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.'
        saida = 'aaaaaAAAAA! eeeeEEEEE? iiiiIIIII, oooooOOOOO; uuuuUUUUU.'
        self.assertEqual(saida, clean.remover_acentos(entrada))

    def test_one_line(self):
        self.assertEqual(dict, type(clean.one_line.__annotations__))
        self.assertEqual({'codigo_html': str, 'return': str}, clean.one_line.__annotations__)

        lista = [
            self.valores('<html>\n<head>\n</head>\n<body>\n</body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('1<sup>  <u> o </u> \n\n\n\n\n\n</sup> e 2<sup> \n<u> \na</u> </sup>',
                         '1<sup> <u> o </u> </sup> e 2<sup> <u> a</u> </sup>'),
            self.valores('<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;oi&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n\n\n\n\n\n\n\n\n</p>',
                         '<p> oi </p>'),
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.one_line(item.entrada))

    def test_remove_tag_string(self):
        with self.assertRaises(AssertionError):
            clean.remover_tag_string('', 'a')

        with self.assertRaisesRegex(AssertionError, 'Error lista_indesejados'):
            clean.remover_tag_string('', 'a')
            clean.remover_tag_string('', 1)
            clean.remover_tag_string('', 1.1)

    def test_remove_tag_string0(self):
        lista = [
            self.valores('<html>\n <head>\n </head>\n <body>\n </body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n <p> oi </p>\n </body>\n</html>',
                         '<html> <head> </head> <body> <p> oi </p> </body> </html>'),
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.remover_tag_string(item.entrada))

    def test_remove_tag_string1(self):
        lista = [
            self.valores('<html>\n <head>\n </head>\n <body>\n </body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n <p> oi </p>\n </body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n<p> Texto compilado</p></body>\n</html>',
                         '<html> <head> </head> <body> <p> Texto compilado </p> </body> </html>'),
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.remover_tag_string(item.entrada, lista_indesejados=['oi']))

    def test_remove_tag_string2(self):
        lista = [
            self.valores('<html>\n <head>\n </head>\n <body>\n </body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n <p> oi </p>\n </body>\n</html>',
                         '<html> <head> </head> <body> <p> oi </p> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n<p> Texto compilado</p></body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            ]
        for item in lista:
            self.assertEqual(item.saida, clean.remover_tag_string(item.entrada, lista_indesejados=['Texto compilado']))

    def test_remove_tag_string3(self):
        lista = [
            self.valores('<html>\n <head>\n </head>\n <body>\n<p> Texto compilado</p></body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n'
                         '<p> Texto compilado</p><p>Texto completo</p></body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
            self.valores('<html>\n <head>\n </head>\n <body>\n<p> Texto compilado</p>'
                         '<p>Texto completo</p></body>\n</html>',
                         '<html> <head> </head> <body> </body> </html>'),
        ]
        for item in lista:
            self.assertEqual(item.saida, clean.remover_tag_string(item.entrada, lista_indesejados=[]))

    def test_replace_espacos(self):
        texto = '<html>\n <head>\n </head>\n <body>\n ' \
                '<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>\n </body>\n</html>'

        with self.assertRaisesRegex(AssertionError, "codigo deve ser instancia de str"):
            self.assertEqual(1, clean.replace_espacos(1))

        self.assertEqual('', clean.replace_espacos(''))
        self.assertEqual(r'\)&nbsp;&nbsp;\(', clean.replace_espacos(r')    ('))

    def test_replace_middle_element(self):
        t = namedtuple('teste', 'entrada, saida, elemento')
        lista = [
            t("<p> bla bla bla <br /> bla bla bla</p>",
                "<p> bla bla bla </p> <p> bla bla bla </p>",
                "br"),
            t("<h4> bla bla bla <br /> bla bla <br /> bla bla bla</h4>",
                "<h4> bla bla bla </h4> <h4> bla bla </h4> <h4> bla bla bla </h4>",
                "br"),
            t("<h5> bla bla bla <br /> bla bla </h5>",
                "<h5> bla bla bla </h5> <h5> bla bla </h5>",
                "br"),
            t("<h6> bla bla bla <br /> bla bla </h6>",
                "<h6> bla bla bla </h6> <h6> bla bla </h6>",
                "br")
        ]
        for i in lista:
            self.assertEqual(i.saida, clean.replace_middle_element(i.entrada, i.elemento))

        with self.assertRaisesRegex(AssertionError, 'Elemento "h2" intermediário inválido.'):
            clean.replace_middle_element(lista[0].entrada, elem='h2')

    def test_substituir_tags(self):
        codigo = """<p> bla bla bla <br /> bla bla bla</p>
                        <h4> bla bla bla <br /> bla bla <br /> bla bla bla</h4>
                        <h5> bla bla bla <br /> bla bla </h5>
                        <h6> bla bla bla <br /> bla bla </h6>"""

        texto = '<p>\n bla bla bla\n <br/>\n bla bla bla\n</p>\n' \
                '<h4>\n bla bla bla\n <br/>\n bla bla\n <br/>\n bla bla bla\n</h4>\n' \
                '<h4>\n bla bla bla\n <br/>\n bla bla\n</h4>\n<h4>\n bla bla bla\n <br/>\n bla bla\n</h4>'

        texto1 = '<p>\n bla bla bla\n <hr/>\n bla bla bla\n</p>\n<h4>\n' \
                 ' bla bla bla\n <hr/>\n bla bla\n <hr/>\n bla bla bla\n</h4>\n' \
                 '<h5>\n bla bla bla\n <hr/>\n bla bla\n</h5>\n<h6>\n bla bla bla\n <hr/>\n bla bla\n</h6>'
        result = clean.substituir_tags(codigo, ['h6', 'h5'], 'h4')
        self.assertEqual(texto, result)

        result = clean.substituir_tags(codigo, ['br'], 'hr')
        self.assertEqual(texto1, result)

        with self.assertRaisesRegex(TypeError, '"codigo" deve ser str'):
            clean.substituir_tags(None, None, None)

        with self.assertRaisesRegex(TypeError, '"tag_in" deve ser str'):
            clean.substituir_tags('', [''], None)

        with self.assertRaisesRegex(TypeError, '"tag_out" deve ser uma lista com str'):
            clean.substituir_tags('', '', '')


if __name__ == '__main__':
    main()
