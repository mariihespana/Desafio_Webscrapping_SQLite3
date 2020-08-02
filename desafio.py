import sqlalchemy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as CondicaoEsperada
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from models.db_desafio_models import Produtos, configurar_banco_de_dados, criar_produto, buscar_todos_produtos
from models.base_desafio import Base
import itertools

class webscrapping:
    def __init__(self):
        # Encontrar elementos
        chrome_options = Options()
        chrome_options.add_argument('--lang=pt-BR')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=chrome_options)
        wait = WebDriverWait(
            self.driver,
            10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
    )

    def Iniciar(self):
        self.acessar_site()
        self.scrapping()
        # Busca(query)
        resultado = self.conexao.query(Produtos).all()
        print(resultado)

    def acessar_site(self):
        self.driver.get('https://cursoautomacao.netlify.app/produtos1.html')
        
    def scrapping(self):
        try:
            nome_produto = self.driver.find_elements_by_xpath('//a[contains(text(), "Produto")]')
            descricao_produto = self.driver.find_elements_by_xpath('//p[contains(text(), "Descrição")]')
            precos = self.driver.find_elements_by_xpath('//p[@class = "price-container"]')
            self.dados = zip(nome_produto,descricao_produto,precos)
            self.criar_produtos()

            proxima_pagina = self.driver.find_element_by_xpath(('//button[@id= "proxima_pagina"]'))
            if proxima_pagina is not None:
                proxima_pagina.click()
                self.scrapping()
        except Exception as error:
            print('Não foi possível encontrar outras páginas')

    def criar_produtos(self):
        self.conexao = configurar_banco_de_dados()

        for nome, descricao, preco in self.dados:
            criar_produto(self.conexao, nome.text, descricao.text, float(preco.text[1:]))

desafio = webscrapping()
desafio.Iniciar()

