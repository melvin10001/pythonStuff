from flask import Flask,render_template,request, redirect, escape
from DBcm import UseDatabase
from vsearch import search4letters
app = Flask(__name__)
app.config['database_name'] = 'vsearchlogDB.sqlite'
def log_request(req: 'flask_request', res: str) -> None:

    with UseDatabase(app.config['database_name']) as cursor:
        _SQL = """insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (?,?,?,?,?)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, 
                                str(req.user_agent.browser), str(res)))
@app.route('/')
def hello() -> '302':
    return redirect('/entry')

@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    answer = search4letters(phrase,letters)
    log_request(request,answer)
    #return str(answer)
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
def view_the_log() -> 'html':
    """Display the contents of the log file as HTML table."""
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


if __name__ == '__main__':
    app.run(debug=True)
