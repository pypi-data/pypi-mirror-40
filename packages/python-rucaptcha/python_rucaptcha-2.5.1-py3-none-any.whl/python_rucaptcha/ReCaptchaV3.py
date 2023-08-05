import requests
import time
import asyncio
import aiohttp
from requests.adapters import HTTPAdapter

from .config import url_request_2captcha, url_response_2captcha, url_request_rucaptcha, url_response_rucaptcha, app_key, \
    JSON_RESPONSE
from .errors import RuCaptchaError
from .result_handler import get_sync_result, get_async_result


class ReCaptchaV3:
    """
	Класс служит для работы с новой ReCaptcha v3 от Гугла.
	Для работы потребуется передать ключ от RuCaptcha, затем ключ сайта, тип действия на сайте, ссылка на капчу на сайте.
    
    Подробней: https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
	"""

    def __init__(self, rucaptcha_key, service_type: str = '2captcha', sleep_time: int = 10, action: str = 'verify', min_score: float = 0.4 ,
                 proxy: str = '', proxytype: str = '', pingback: str = ''):
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
		:param sleep_time: Вермя ожидания решения капчи
		:param action: Значение параметра action, которые вы нашли в коде сайта
		:param min_score: Требуемое значение рейтинга (score)
		:param proxy: Для решения рекапчи через прокси - передаётся прокси и данные для аутентификации.
		                ` логин:пароль@IP_адрес:ПОРТ` / `login:password@IP:port`.
		:param proxytype: Тип используемого прокси. Доступные: `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`.
        :param pingback: Параметр для ссылки с на которой будет ожидание callback ответа от RuCaptcha с решением ReCaptchaV3
		"""
        # проверка введённого времени и изменение если минимальный порог нарушен
        if sleep_time < 10:
            raise ValueError(f'\nПараметр `sleep_time` должен быть не менее 10(рекомендуемое - 20 секунд). '
                             f'\n\tВы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # проверка допустимости переданного параметра для рейтинга
        if not 0.1 < min_score < 0.9:
            raise ValueError(f'\nПараметр `min_score` должен быть от `0.1` до `0.9`. \n\tВы передали - {min_score}')
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'userrecaptcha',
                             'version': 'v3',
                             "json": 1,
                             'action': action,
                             'min_score': min_score,
                             "soft_id": app_key}

        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({'pingback': pingback})

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({'proxy': proxy,
                                      'proxytype': proxytype})

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            'taskinfo': 1
                            }

        # создаём сессию
        self.session = requests.Session()
        # выставляем кол-во попыток подключения к серверу при ошибке
        self.session.mount('http://', HTTPAdapter(max_retries = 5))
        self.session.mount('https://', HTTPAdapter(max_retries = 5))

    # Работа с капчей
    # тестовый ключ сайта
    def captcha_handler(self, site_key: str, page_url: str):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча

		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    user_check - ID работника, который решил капчу
                    user_score -  score решившего капчу работника
                    taskId - находится ID задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }		
		'''
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()

        self.post_payload.update({'googlekey': site_key,
                                  'pageurl': page_url})
        # получаем ID капчи
        captcha_id = self.session.post(self.url_request, data = self.post_payload).json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи 
            # и параметр `taskinfo=1` для получения подробной информации об исполнителе
            self.get_payload.update({'id': captcha_id})

            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get('pingback'):
                return self.get_payload
            
            else:
                # Ожидаем решения капчи 10 секунд
                time.sleep(self.sleep_time)
                return get_sync_result(get_payload = self.get_payload,
                                       sleep_time = self.sleep_time,
                                       url_response = self.url_response,
                                       result = self.result)


class aioReCaptchaV3:
    """
	Класс служит для работы с новой ReCaptcha v3 от Гугла.
	Для работы потребуется передать ключ от RuCaptcha, затем ключ сайта, тип действия на сайте, ссылка на капчу на сайте.
    
    Подробней: https://rucaptcha.com/api-rucaptcha#solving_recaptchav3
	"""

    def __init__(self, rucaptcha_key, service_type: str = '2captcha', sleep_time: int = 10, action: str = 'verify', min_score: float = 0.4 ,
                 proxy: str = '', proxytype: str = '', pingback: str = ''):
        """
		Инициализация нужных переменных.
		:param rucaptcha_key:  АПИ ключ капчи из кабинета пользователя
		:param service_type: URL с которым будет работать программа, возможен вариант "2captcha"(стандартный)
                             и "rucaptcha"
		:param sleep_time: Вермя ожидания решения капчи
		:param action: Значение параметра action, которые вы нашли в коде сайта
		:param min_score: Требуемое значение рейтинга (score)
		:param proxy: Для решения рекапчи через прокси - передаётся прокси и данные для аутентификации.
		                ` логин:пароль@IP_адрес:ПОРТ` / `login:password@IP:port`.
		:param proxytype: Тип используемого прокси. Доступные: `HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`.
        :param pingback: Параметр для ссылки с на которой будет ожидание callback ответа от RuCaptcha с решением ReCaptchaV3
		"""
        # проверка введённого времени и изменение если минимальный порог нарушен
        if sleep_time < 10:
            raise ValueError(f'\nПараметр `sleep_time` должен быть не менее 10(рекомендуемое - 20 секунд). '
                             f'\n\tВы передали - {sleep_time}')
        self.sleep_time = sleep_time
        # проверка допустимости переданного параметра для рейтинга
        if not 0.1 < min_score < 0.9:
            raise ValueError(f'\nПараметр `min_score` должен быть от `0.1` до `0.9`. \n\tВы передали - {min_score}')
        # пайлоад POST запроса на отправку капчи на сервер
        self.post_payload = {"key": rucaptcha_key,
                             'method': 'userrecaptcha',
                             'version': 'v3',
                             "json": 1,
                             'action': action,
                             'min_score': min_score,
                             "soft_id": app_key}

        # если был передан параметр для callback`a - добавляем его
        if pingback:
            self.post_payload.update({'pingback': pingback})

        # добавление прокси для решения капчи с того же IP
        if proxy and proxytype:
            self.post_payload.update({'proxy': proxy,
                                      'proxytype': proxytype})

        # выбираем URL на который будут отпраляться запросы и с которого будут приходить ответы
        if service_type == '2captcha':
            self.url_request = url_request_2captcha
            self.url_response = url_response_2captcha
        elif service_type == 'rucaptcha':
            self.url_request = url_request_rucaptcha
            self.url_response = url_response_rucaptcha
        else:
            raise ValueError('Передан неверный параметр URL-сервиса капчи! Возможные варинты: `rucaptcha` и `2captcha`.'
                             'Wrong `service_type` parameter. Valid formats: `rucaptcha` or `2captcha`.')

        # пайлоад GET запроса на получение результата решения капчи
        self.get_payload = {'key': rucaptcha_key,
                            'action': 'get',
                            'json': 1,
                            'taskinfo': 1
                            }

    # Работа с капчей
    async def captcha_handler(self, site_key: str, page_url: str):
        '''
		Метод отвечает за передачу данных на сервер для решения капчи
		:param site_key: Гугл-ключ сайта
		:param page_url: Ссылка на страницу на которой находится капча

		:return: Ответ на капчу в виде JSON строки с полями:
                    captchaSolve - решение капчи,
                    user_check - ID работника, который решил капчу
                    user_score -  score решившего капчу работника
                    taskId - находится ID задачи на решение капчи, можно использовать при жалобах и прочем,
                    error - False - если всё хорошо, True - если есть ошибка,
                    errorBody - полная информация об ошибке:
                        {
                            text - Развернётое пояснение ошибки
                            id - уникальный номер ошибка в ЭТОЙ бибилотеке
                        }		
		'''
        # результат возвращаемый методом *captcha_handler*
        self.result = JSON_RESPONSE.copy()

        self.post_payload.update({'googlekey': site_key, 'pageurl': page_url})
        # получаем ID капчи
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_request, data = self.post_payload) as resp:
                captcha_id = await resp.json()

        # если вернулся ответ с ошибкой то записываем её и возвращаем результат
        if captcha_id['status'] is 0:
            self.result.update({'error': True,
                                'errorBody': RuCaptchaError().errors(captcha_id['request'])
                                }
                               )
            return self.result
        # иначе берём ключ отправленной на решение капчи и ждём решения
        else:
            captcha_id = captcha_id['request']
            # вписываем в taskId ключ отправленной на решение капчи
            self.result.update({"taskId": captcha_id})
            # обновляем пайлоад, вносим в него ключ отправленной на решение капчи
            self.get_payload.update({'id': captcha_id})
                
            # если передан параметр `pingback` - не ждём решения капчи а возвращаем незаполненный ответ
            if self.post_payload.get('pingback'):
                return self.get_payload
                
            else:
                # Ожидаем решения капчи
                await asyncio.sleep(self.sleep_time)
                return await get_async_result(get_payload = self.get_payload,
                                              sleep_time = self.sleep_time,
                                              url_response = self.url_response,
                                              result = self.result)
