from threading import Thread
from flask import Flask,render_template,request, redirect, escape, session, copy_current_request_context
from DBcm import UseDatabase, ConnectionError, CredentialError, SQLError
from vsearch import search4letters
from checker import check_logged_in

from time import sleep


app = Flask(__name__)
app.config['database_name'] = 'vsearchlogDB.sqlite'

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'



@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    
    @copy_current_request_context 
    def log_request(req: 'flask_request', res: str) -> None:
    
        sleep(15)
        #raise
        with UseDatabase(app.config['database_name']) as cursor:
            _SQL = """insert into log
                        (phrase, letters, ip, browser_string, results)
                        values
                        (?,?,?,?,?)"""
            cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, 
                                    str(req.user_agent.browser), str(res)))
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    answer = search4letters(phrase,letters)

    try:
        t = Thread(target=log_request,args=(request, answer))
        t.start()
    except Exception as err:
        print('Something went wrong', str(err))

    return render_template('results.html',
                            the_title=title,
                            the_phrase=phrase, 
                            the_letters=letters, 
                            the_results=str(answer))

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                            the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Display the contents of the log file as HTML table."""
    try:
        with UseDatabase(app.config['database_name']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
                        from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)
    
    except ConnectionError as err:
        print('Is your database available? Error:', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your querry correct? Error: ', str(err))
    except Exception as err:
        print('Something went wront:', str(err))

app.secret_key = 'SimpleSecretKey'


if __name__ == '__main__':
    app.run(debug=True)
