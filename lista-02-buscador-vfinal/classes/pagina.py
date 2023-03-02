from bs4 import BeautifulSoup

class Pagina:
    def __init__(self,url,response = None,  response_time = 0, _updated_at = None,):
        self._url = url
        self._response = response
        self._response_time = response_time
        self._updated_at = _updated_at
        
    def get_ocurrence_amount(self,searched_word):
        return self._response.lower().count(searched_word.lower())
    
    def get_term_is_in_the_title(self,searched_word):
        title = self.get_title()
        if title:
            return  searched_word in title.next
        return False

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def get_response(self):
        return self._response

    def set_response(self, response):
        self._response = response

    def get_response_time(self):
        return self._response_time

    def set_response(self, response_time):
        self._response_time = response_time
        

    def set_updated_at(self, updated_at):
        self._updated_at = updated_at
            
    def get_updated_at(self, updated_at):
        return self.updated_at 
               
    def __str__(self):
        return f"Pagina(url={self._url}, title={self.get_title})"

    def show(self, termo):
        return f"Pagina(url={self._url}, title={self.get_title()}, ocurrence_amount={self.get_ocurrence_amount(termo)}, response_time = {self.get_response_time()})"
        
        
    def get_title(self):
        soup = BeautifulSoup(self._response, "html.parser")

        title_element = soup.find('title')

        # Verifica se o elemento de título foi encontrado
        if title_element is not None:
        # Extrai o texto dentro do elemento de título
            title_text = title_element.text
            # Imprime o título
            return title_element
        