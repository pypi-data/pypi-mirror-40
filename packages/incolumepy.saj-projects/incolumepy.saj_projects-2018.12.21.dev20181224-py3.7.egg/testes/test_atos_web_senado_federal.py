import unittest
import unittest.mock as mock
import os
import inspect
import numpy as np

try:
    from incolumepy.saj_projects import atos_web_senado_federal, logger
    __package__ = 'incolumepy.saj_projects'
except (ModuleNotFoundError, ImportError) as e:
    from src.incolumepy.saj_projects import atos_web_senado_federal, logger
    __package__ = 'src.incolumepy.saj_projects'


class TestAtosWebSF(unittest.TestCase):
    def setUp(self):
        self.dict = {
                'nome': ['DEC 1820/1978', 'DEC 1821/1978', 'DEC 1822/1978'],
                'data': ['01/01/1978', '01/02/1978', '01/03/1978'],
                'ementa': ['aaaaaaa', 'bbbbbbbb', 'ccccccddd'],
                'total': [None, None, None]
            }

    def tearDown(self):
        pass

    @mock.patch('builtins.open')
    @mock.patch('os.makedirs')
    @mock.patch("pandas.read_excel")
    def test_lista_atos_xlsx_todataframe(self, mock_pd_read_excel, mock_makedirs, mock_open):

        df = atos_web_senado_federal.pd.DataFrame(self.dict)
        mock_pd_read_excel.return_value = df
        mock_pd_read_excel.to_csv.return_value = None
        result = atos_web_senado_federal._lista_atos_xlsx_todataframe(
            xlsx_file='../../../data/DECRETOS_REVOGADOS_COM_LINK_VAZIO.xlsx')
        logger.debug(result.head())
        logger.debug(type(result))
        self.assertIsInstance(result, atos_web_senado_federal.pd.DataFrame)
        self.assertEqual({'data': {0: '01/01/1978', 1: '01/02/1978', 2: '01/03/1978'},
                          'ementa': {0: 'aaaaaaa', 1: 'bbbbbbbb', 2: 'ccccccddd'},
                          'nome': {0: 'DEC 1820/1978', 1: 'DEC 1821/1978', 2: 'DEC 1822/1978'},
                          'total': {0: None, 1: None, 2: None}}, result.to_dict())
        mock_makedirs.assert_called()
        mock_open.assert_called()
        mock_open.assert_has_calls([
            mock.call('/tmp/xlsx_todataframe/lista-xlsx_todataframe.csv', 'w', encoding='utf-8'),
            mock.call().write(',nome,data,ementa,total\n'),
            mock.call().write('0,DEC 1820/1978,01/01/1978,aaaaaaa,\n'),
            mock.call().write('1,DEC 1821/1978,01/02/1978,bbbbbbbb,\n'),
            mock.call().write('2,DEC 1822/1978,01/03/1978,ccccccddd,\n'),
            mock.call().close(),
            mock.call().close()])

    @mock.patch.object(atos_web_senado_federal, '_lista_atos_xlsx_todataframe')
    def test_listar_atos_por_ano(self, mock_xlsx2df):
        df = atos_web_senado_federal.pd.DataFrame(self.dict)
        mock_xlsx2df.return_value = df
        result = atos_web_senado_federal.listar_atos_por_ano(ano='1978')
        logger.debug(result)
        self.assertIsInstance(result, atos_web_senado_federal.pd.DataFrame)
        self.assertEqual({
            'ANO': {0: '1978', 1: '1978', 2: '1978'},
            'NUM': {0: '1820', 1: '1821', 2: '1822'}}, result.to_dict())

    @mock.patch('builtins.open')
    @mock.patch('pandas.read_csv')
    @mock.patch('os.path.exists', side_effect=[True, True])
    def test_relatorio_progresso(self, mock_exists, mock_csv, mock_open):
        mock_csv.side_effect = [
            atos_web_senado_federal.pd.DataFrame(
                {
                    'ANO': {0: '1978', 1: '1978', 2: '1978'},
                    'NUM': {0: '1820', 1: '1821', 2: '1822'},

                }),
            atos_web_senado_federal.pd.DataFrame(
                {
                    'ANO': {0: '1978', 2: '1978'},
                    'NUM': {0: '1820', 2: '1822'},
                    'dou': {0: 'dou1', 2: 'dou3'},
                    'url': {0: 'url1', 2: 'url3'}
                }
            )
        ]
        result = atos_web_senado_federal.relatorio_progresso(
            f'teste/file0.csv',
            f'teste/file1.csv',
            f'teste/file-progresso.csv',
        )
        self.assertIsInstance(result, bool)
        self.assertTrue(result)
        mock_exists.assert_called()
        mock_open.assert_called()
        mock_open.assert_has_calls([
            mock.call('teste/file-progresso.csv', 'w', encoding='utf-8'),
            mock.call().write('ano,num,dou,url\n'),
            mock.call().write('1978,1820,dou1,url1\n'),
            mock.call().write('1978,1821,,\n'),
            mock.call().write('1978,1822,dou3,url3\n'),
            mock.call().close(),
            mock.call().close()])

    @mock.patch('os.access', side_effect=[False, False, False, True])
    def test_merge_csv_files_exceptions(self, mock_access):
        with self.assertRaisesRegex(ValueError, 'O diretório deve ser informado'):
            atos_web_senado_federal.merge_csv_files()

        with self.assertRaisesRegex(IOError, "O diretório informado \"/teste\" não foi encontrado"):
            atos_web_senado_federal.merge_csv_files('/teste')

        with self.assertRaises(IOError):
            atos_web_senado_federal.merge_csv_files('.')
        mock_access.assert_called()

    def test_merge_csv_files0(self):
        F""" Test unitário {inspect.stack()[0][3]} com elementos reais"""
        pathfile = '../../src_production/atos/listas/1967'
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), pathfile))
        assert os.path.exists(filename), f"Ops: \"{filename}\" indisponível .."
        result = atos_web_senado_federal.merge_csv_files(filename)
        self.assertIsInstance(result, atos_web_senado_federal.pd.DataFrame)
        self.assertTrue(atos_web_senado_federal.pd.DataFrame, type(result))

    @mock.patch('builtins.open')
    @mock.patch('pandas.concat')
    @mock.patch('pandas.read_csv')
    @mock.patch('os.walk', site_effect=[(
        'atos/listas/1967', [], ['lista-0.csv', 'lista-1.csv', '61635.csv', '61636.csv', '61543.csv'])])
    @mock.patch('os.access', side_effect=[True, True, True])
    @mock.patch('os.path.exists')
    def test_merge_csv_files1(self, mock_exists, mock_access, mock_walk, mock_pd_read_cvs, mock_pd_concat, mock_open):
        """ Test unitário test_merge_csv_files1 com elementos mock"""
        pathfile = 'atos/listas/1967'
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), pathfile))
        assert os.path.exists(filename), f"Ops: \"{filename}\" indisponível .."
        self.assertIs(atos_web_senado_federal.pd.concat, mock_pd_concat)
        self.assertIs(atos_web_senado_federal.pd.read_csv, mock_pd_read_cvs)
        self.assertIs(atos_web_senado_federal.os.walk, mock_walk)
        self.assertIs(atos_web_senado_federal.os.access, mock_access)
        self.assertIs(atos_web_senado_federal.os.path.exists, mock_exists)

        mock_pd_read_cvs.side_effect = [
            atos_web_senado_federal.pd.DataFrame({'ano': [1967, 1967, 1967], 'num': [61635, 61636, 61543]}),
            atos_web_senado_federal.pd.DataFrame(),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61635], 'dou': ['dou61635'], 'url': ['url61635']}),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61636], 'dou': ['dou61636'], 'url': ['url61636']}),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61543], 'dou': ['dou61543'], 'url': ['url61543']}),
            ]
        concat = atos_web_senado_federal.pd.concat([
            atos_web_senado_federal.pd.DataFrame({'ano': [1967, 1967, 1967], 'num': [61635, 61636, 61543]}),
            atos_web_senado_federal.pd.DataFrame(),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61635], 'dou': ['dou61635'], 'url': ['url61635']}),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61636], 'dou': ['dou61636'], 'url': ['url61636']}),
            atos_web_senado_federal.pd.DataFrame({
                'ano': [1967], 'num': [61543], 'dou': ['dou61543'], 'url': ['url61543']}),
        ], sort=False)
        mock_pd_concat.return_value = concat

        result = atos_web_senado_federal.merge_csv_files(filename)
        # self.assertEqual(mock.call(), mock_open.assert_has_calls([mock.call()]))
        self.assertEqual(result, result)
        mock_exists.assert_called()
        mock_access.assert_called()
        mock_walk.assert_called()
        mock_pd_concat.assert_called()
        with self.assertRaises(Exception):
            mock_open.assert_called()
            mock_pd_read_cvs.assert_called()

    @mock.patch('selenium.webdriver.firefox.webdriver.WebDriver')
    @mock.patch('selenium.webdriver.Firefox')
    def test_query_ato_num_ano(self, mock_firefox, mock_webdriver):
        url = 'http://url.de.test/do/sicon/camara'
        mock_firefox.return_value.current_url = url
        mock_firefox.return_value.title = 'SICON - blablabla blabla'
        mock_firefox.return_value.page_source = 'Informe o argumento, Gestão de Normas Jurídicas'
        mock_firefox.return_value.find_element.return_value.text = 'dou123'
        result = atos_web_senado_federal.query_ato_num_ano(num=90786,
                                                           ano=1985, alias='dec',
                                                           url_consulta='http://legis.senado.leg.br/sicon/#/basica')
        self.assertIsNotNone(result)
        self.assertIn('dou123', result)
        self.assertIn(url, result)


    def test_discover_url_0(self):
        """
        Teste completo com recurso real
        :return: bool
        """
        # raise NotImplementedError
        csv_in = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         f'../../src_production/atos/listas/1980/lista-progresso.csv'))
        path_output = os.path.dirname(csv_in)
        assert os.path.exists(csv_in), f"Ops: {csv_in} inacessível .."
        assert os.path.exists(path_output), f"Ops: {path_output} inacessível .."
        atos_web_senado_federal.discover_url(csv_file=csv_in, dir_output=path_output)

    @mock.patch('pandas.DataFrame.to_csv')
    @mock.patch('os.makedirs')
    @mock.patch.object(atos_web_senado_federal, 'query_ato_num_ano')
    @mock.patch('pandas.read_csv')
    @mock.patch('os.path.exists', return_value = True)
    def test_discover_url_1(self, mock_exists, mock_read_csv, mock_atoswsf, mock_makedirs, mock_to_csv):
        self.assertIs(mock_exists, os.path.exists)
        self.assertIs(mock_makedirs, os.makedirs)

        mock_atoswsf.side_effect = [
            ("dou1821", "url1821"),
            ("dou1822", "url1822")
        ]
        mock_read_csv.return_value = atos_web_senado_federal.pd.DataFrame(
            {
                'num': ['1820', '1821', '1822'],
                'ano': ['1978', '1978', '1978'],
                'dou': ['dou1820', np.nan, np.nan],
                'url': ['url1820', np.nan, np.nan]
            }
        )
        csv_in = f'atos/listas/1978/lista-progresso.csv'
        path_output = os.path.dirname(csv_in)
        result = atos_web_senado_federal.discover_url(csv_file=csv_in, dir_output=path_output)
        self.assertIs(type(result), atos_web_senado_federal.pd.core.frame.DataFrame)
        self.assertEqual(atos_web_senado_federal.pd.core.frame.DataFrame, type(result))
        self.assertEqual(
            {'ano': {0: 1978}, 'dou': {0: 'dou1822'}, 'num': {0: 1822}, 'url': {0: 'url1822'}},
            result.to_dict())

    @mock.patch('os.path.exists', return_value=False)
    def test_discover_url_exception_0(self, mock_exists):
        '''
        Teste completo com recurso mock
        :return: bool
        '''
        csv_in = os.path.abspath(os.path.join(os.path.dirname(__file__), f'atos/listas/1980/lista-progresso.csv'))
        path_output = os.path.dirname(csv_in)
        with self.assertRaisesRegex(AssertionError, F"{csv_in} indisponível!"):
            atos_web_senado_federal.discover_url(csv_file=csv_in, dir_output=path_output)

    @mock.patch('os.access', side_effect=[True])
    @mock.patch('pandas.read_csv', return_value=atos_web_senado_federal.pd.DataFrame({
        'num': ['1820', '1821', '1822'],
        'ano': ['1978', '1978', '1978'],
        'dou': ['dou1820', np.nan, np.nan],
        'url': ['url1820', np.nan, np.nan]
    }))
    @mock.patch('os.path.exists', return_value=True)
    def test_aferir_csv_final(self, mock_exists, mock_read_csv, mock_access):
        csv_in = 'atos/listas/1980/lista-progresso.csv'
        result = atos_web_senado_federal.aferir_csv_final(csv_in=csv_in)
        self.assertTrue(result)

    @mock.patch.object(atos_web_senado_federal, 'realfilename')
    @mock.patch('builtins.open')
    @mock.patch.object(atos_web_senado_federal,'query_ato_num_ano')
    @mock.patch.object(
        atos_web_senado_federal, 'listar_atos_por_ano',
                return_value=atos_web_senado_federal.pd.DataFrame({
                    'num': ['1820', '1821', '1822'],
                    'ano': ['1978', '1978', '1978']
                }))
    def test_elencar_atos_por_ano(self, mock_0, mock_1, mock_open, mock_realfilename):
        mock_1.side_effect = [
            ('dou1820', 'url1820'),
            ('dou1821', 'url1821'),
            ('dou1822', 'url1822'),
        ]
        result = atos_web_senado_federal.elencar_atos_por_ano(ano='1978', dir_output='atos/listas')
        self.assertEqual(True, result)
        mock_0.assert_called()
        mock_1.assert_called()
        mock_realfilename.assert_called()
        mock_open.assert_has_calls([])

    @mock.patch.object(atos_web_senado_federal, 'aferir_csv_final')
    @mock.patch.object(atos_web_senado_federal, 'relatorio_progresso')
    @mock.patch('pandas.DataFrame')
    @mock.patch('os.path.exists', return_value=True)
    @mock.patch.object(atos_web_senado_federal, 'discover_url')
    @mock.patch.object(atos_web_senado_federal, 'merge_csv_files')
    def test_get_lista_atos_tocsv(self, m2, m3, m4, m_pd_dataframe, m8, m9):
        df = atos_web_senado_federal.pd.DataFrame({
            'num': ['1820', '1821', '1822'],
            'ano': ['1978', '1978', '1978'],
            'dou': ['dou1820', 'sou1821', 'dou1822'],
            'url': ['url1920', 'url1821', 'url1822']
        }),
        m_pd_dataframe.return_value = df
        result = atos_web_senado_federal.get_lista_atos_tocsv(ano='1875', path_output='atos/listas')
        self.assertTrue(result)

        m_pd_dataframe.assert_called()
        m2.assert_called()
        m3.assert_called()
        m4.assert_called()
        m8.assert_called()
        m9.assert_called()


if __name__ == '__main__':
    unittest.main()
