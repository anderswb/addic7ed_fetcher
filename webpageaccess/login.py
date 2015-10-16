from webpageaccess.downloadsession import session as session

def login(user, password):
    result = session.post('/dologin.php', data={
        'username': user,
        'password': password,
        'remember': 'true'
    })

    if get_current_user(result):
        return session.cookies['PHPSESSID']

    raise TypeError(result('center p[align="center"]').text())


def get_current_user(page=None):
    if not page:
        page = session.get('/')

    titles = page('.footer_dropup h4')
    if titles and titles[0].text.startswith('Welcome back'):
        return titles[0].text[13:].strip()


def set_session(sess):
    session.cookies['PHPSESSID'] = sess__author__ = 'Anders'
