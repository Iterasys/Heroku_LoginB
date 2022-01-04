from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # erro: próprio autor que achou
    # defeito: outra pessoa encontrou, sem executar o software
    # falha: outra pessoa encontrou, ao executar o software

    # lista de seletores de elementos da página (locator)
    _username_input = {'by': By.ID, 'value': 'username'}
    _password_input = {'by': By.ID, 'value': 'password'}
    _submit_button = {'by': By.CSS_SELECTOR, 'value': 'button.radius'}
    _failure_message = {'by': By.CSS_SELECTOR, 'value': '.flash.error'}
    _success_message = {'by': By.CSS_SELECTOR, 'value': 'div.flash.success'}
    _login_form = {'by': By.ID, 'value': 'login'}




