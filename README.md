<h1> Сайт по поиску вакансий </h1>

Сайт доступен по [ссылке](https://find-job-pls.herokuapp.com)

Построение полноценного сайта-сервиса, который собирает данные о  вакансиях с сайтов по поиску работы и рассылает их подписчикам. Подписчики сервиса регистрируются выбирая город и язык программирования. Раз в сутки, происходит отбор всех подписчиков, которые хотят получать письма с вакансиями и на основе их предпочтений (какой город и какой ЯП), формируется список урлов, по которым происходит запуск парсеров для сбора вакансий по этим параметрам. После того, как парсеры отработают, запускается отправка писем тем, кто хочет получать рассылку.
