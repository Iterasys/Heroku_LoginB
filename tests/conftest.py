import os
import pytest
from selenium import webdriver
from . import config, credentials


# Em um novo projeto, o que mudaria seria apenas os valores default e help (explicação) abaixo
def pytest_addoption(parser):
    parser.addoption('--baseurl',
                     action='store',
                     default='https://the-internet.herokuapp.com',
                     help='endereço dos site alvo do teste'
                     )
    parser.addoption('--host',
                     action='store',
                     default='saucelabs',
                     help='ambiente em que vou executar os testes'
                     )
    parser.addoption('--browser',
                     action='store',
                     default='chrome',
                     help='navegador padrão'
                     )
    parser.addoption('--browserversion',
                     action='store',
                     default='97.0',
                     help='versão do navegador padrão'
                     )
    parser.addoption('--platform',
                     action='store',
                     default='Windows 10',
                     help='Versão do Sistema Operacional'
                     )


@pytest.fixture
def driver(request):
    config.baseurl = request.config.getoption('--baseurl')
    config.host = request.config.getoption('--host')
    config.browser = request.config.getoption('--browser')
    config.browserversion = request.config.getoption('--browserversion')
    config.platform = request.config.getoption('--platform')

    # Configuração para executar no SauceLabs (Nuvem)
    if config.host == 'saucelabs':
        test_name = request.node.name  # adicionar o nome do teste baseado no script
        capabilities = {
            'browserName': config.browser,
            'browserVersion': config.browserversion,
            'platformName': config.platform,
            'sauce:options': {
                'name': test_name  # nome do teste conforme acima
            }
        }
        # credenciais
        _credentials = credentials.SAUCE_USERNAME + ':' + credentials.SAUCE_ACCESS_KEY
        _url = 'https://' + _credentials + '@ondemand.us-west-1.saucelabs.com:443/wd/hub'

        # chamada para o SauceLabs
        driver_ = webdriver.Remote(_url, capabilities)

    else:  # configuração para execução local / localhost

        # no Chrome
        if config.browser == 'chrome':
            _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')
            if os.path.isfile(_chromedriver):
                driver_ = webdriver.Chrome(_chromedriver)  # vai usar o driver dentro da pasta vendor
            else:
                driver_ = webdriver.Chrome()  # vai usar o chromedriver apontado nas variaveis de ambiente
        # no Firefox
        elif config.browser == 'firefox':
            _geckodriver = os.path.join(os.getcwd(), 'vendor', 'geckodriver.exe')
            if os.path.isfile(_geckodriver):
                driver_ = webdriver.Firefox(_geckodriver)  # vai usar o driver dentro da pasta vendor
            else:
                driver_ = webdriver.Firefox()  # vai usar o geckodriver apontado nas variaveis de ambiente

    def quit():  # sub-função para finalizar o objeto do Selenium
        # atualização do status de passou ou falhou
        # regra para marcar se passou ou falho baseado no retorno da requisição
        sauce_result = 'failed' if request.node.rep_call.failed else 'passed'
        # executar um script no SauceLabs que sinaliza para o nosso terminal o resultado baseado na regra
        driver_.execute_script('sauce:job-result={}'.format(sauce_result))
        # desliga o Selenium
        driver_.quit()

    # configura a requisição para que ela execute a subfunção de quit ao finalizar a requisição/job
    request.addfinalizer(quit)

    # retorna o Selenium turbinado (com essas novas configurações e regras) - Sobreposição
    return driver_


# configurar o gatilho para a geração do relatório
@pytest.hookimpl(hookwrapper=True, tryfirst=True)  # ativa o gatilho e no momento da inicialização da requisição
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()  # variavel de relatório que irá guardar o resultado

    # atributos do relatório
    setattr(item, 'rep_' + rep.when, rep)
