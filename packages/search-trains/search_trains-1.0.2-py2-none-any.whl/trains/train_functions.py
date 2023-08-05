from bs4 import BeautifulSoup as bs
import requests

target_url = 'https://indianrailways.info/seat_availability/'


def fetch_train_suggestions(keyword):
    """This function takes station code/name as input and returns a list containing station codes along with station names.

        Ex: fetch_train_suggestions('VSKP')
        returns: [('VSKP', 'Visakhapatnam'),]
    """

    while True:
        try:
            suggestions = requests.get('https://indianrailways.info/incl/auto_complete/', params={'keyword': keyword.upper(), 'type': 'station_list'}, timeout=5).json()

            if not suggestions:
                print '\n[-]Invalid Station Code/Name. Try entering first 3 letters of station Code/Name'

            return [(item.values()) for item in suggestions]
        except requests.exceptions.ConnectionError:
            return 'no connection'


def search_trains(from_station_code, to_station_code, travel_class='SL', date_range='1', Submit='Submit'):
    """This function searches the trains based on inputs and returns the total trains available on a specified route.

        parameters:

            from_station_code   :   source station code (Ex: VSKP)
            to_station_code     :   destination station code (EX: BZA)
            travel_class        :   SL, 3A, 2A, 1A etc.
    """
    page = requests.post(
        target_url,
        data={
            'from_station_code': from_station_code,
            'to_station_code': to_station_code,
            'travel_class': travel_class,
            'date_range': date_range,
            'Submit': Submit
        }
    )

    if page.status_code == 200:
        soup = bs(page.content, 'html.parser')
    else:
        print 'Awe snap something happened at query page check it once..'
        return

    for tr in soup.tbody.find_all('tr'):
        yield [td.text for td in filter(lambda tag: tag != '\n', list(tr.children))[1:5]]


def get_travel_dates():
    """This function used to retrieve travel dates range and its values

        returns:  Ex:  [(1, 2-15), ]
    """

    main_page = requests.get(target_url)
    global home_soup
    home_soup = bs(main_page.content, 'html.parser')
    for tag in home_soup.find(id='date_range').find_all('option'):
        yield(tag['value'], tag.text)


def get_travel_classes():
    """This function used to retrieve train classes

        returns: SL, 3A, 2A, 1A, etc.
    """

    for tag in home_soup.find(id='travel_class').find_all('option'):
        yield(tag['value'], tag.text)


def get_train_information(train_no):
    """This function used to get a train informatino such as train name, running days, train type etc by using train number

        returns: Train Information.
    """

    train_details_page = requests.post(
        'https://indianrailways.info/train_time_table/',
        data={
            'train_no': train_no,
            'Submit': 'Submit'
        }
    )

    soup = bs(train_details_page.content, 'html.parser')
    yield [td.text for td in filter(lambda tag: tag != '\n', soup.tbody.tr)]
