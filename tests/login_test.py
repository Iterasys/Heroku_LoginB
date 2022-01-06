import os
import pytest
from selenium import webdriver

from pages.login_page import LoginPage


# um padrão para o PyTest executar no início e no final dos testes
@pytest.fixture
def login(request):
    # anteriormente apontavamos o Chrome Driver diretamente
    # _chromedriver = 'vendor/chromedriver.exe'
    _chromedriver = os.path.join(os.getcwd(), 'vendor', 'chromedriver.exe')

    # caso o Chrome Driver na esteja na pasta indicada do projeto
    # vamos usar a configuração geral do servidor / serviço

    # se encontrar o arquivo localmente
    if os.path.isfile(_chromedriver):
        driver_ = webdriver.Chrome(_chromedriver)
    # se não encontrou localmente
    else:
        # usando o Chrome Driver do servidor / serviço
        driver_ = webdriver.Chrome()
    # instanciar a LoginPage e por consequencia a BasePage e herdar tudo delas
    loginPage = LoginPage(driver_)

    # função de finalização do teste está contida na função de inicialização (login)
    def quit():
        driver_.quit()  # desligou o Selenium

    # chamar o quit (a finalização)
    request.addfinalizer(quit)
    return loginPage


# Terminou a função de Login

# Começam os testes
# Não esqueça de alinhar na margem
# <-------

def testar_login_com_sucesso(login):
    # Faça o login com este usuário e senha
    login.com_('tomsmith', 'SuperSecretPassword!')
    # Validar o resultado = mensagem de sucesso presenta
    assert login.success_message_present()


def testar_login_com_usuario_invalido(login):
    login.com_('juca', 'SuperSecretPassword!')
    assert login.failure_message_present()


def testar_login_com_senha_invalida(login):
    login.com_('tomsmith', 'xpto1234')
    assert login.failure_message_present()
