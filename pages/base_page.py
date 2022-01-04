from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    # função de inicialização da classe
    def __init__(self, driver):
        self.driver = driver

    # função para abrir uma página
    def _visitar(self, url):
        self.driver.get(url)

    # função genérica de localização de elemento
    def _procurar(self, locator):
        return self.driver.find_element(locator['by'], locator['value'])

    # função para clicar em um elemento
    def _clicar(self, locator):
        self._procurar(locator).click()

    # função para digitar em um elemento
    def _digitar(self, locator, input_text):
        self._procurar(locator).send_keys(input_text)

    # função para ler o texto em um elemento
    def _ler(self, locator):
        self._procurar(locator).text()

    # função para verificar se o elemento está visivel
    def _esta_visivel(self, locator, timeout=0):
        # se precisa ter paciência
        if timeout > 0:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    expected_conditions.visibility_of_element_located(
                        (locator['by'], locator['value'])
                    )
                )
            # Esgotou o tempo de espera
            except TimeoutException:
                return False  # não encontrou o elemento
            return True  # encontrou o elemento
        # se não precisa esperar
        else:
            try:
                return self._procurar(locator).is_displayed()
            # Não encontrou o elementot
            except NoSuchElementException:
                return False  # não encontrou o elemento
            # return True    # encontrou o elemento
