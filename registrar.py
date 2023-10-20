import html # html_code.escape() is used to thwart XSS attacks
import flask
import reg_db

app = flask.Flask(__name__, template_folder='.')

def clean_arg(arg):
    if arg:
        arg = arg.strip().replace('%', r'\%').replace('_', r'\_')
        return '%'+arg+'%'

    return '%'

@app.route('/regdetails', methods=['GET'])
def regdetails():
    classid = flask.request.args.get('classid')

    results = reg_db.connect_to_db(classid, 'get_detail')

    html_code = flask.render_template('regdetails.html', results=results, classid = classid)
    response = flask.make_response(html_code)
    return response

@app.route('/', methods=['GET'])
def index():
    dept = flask.request.args.get('dept')
    coursenum = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    results = reg_db.connect_to_db([clean_arg(dept), 
                                    clean_arg(coursenum), 
                                    clean_arg(area), 
                                    clean_arg(title)],
                                    'get_overviews')

    html_code = flask.render_template('index.html', 
                                      results=results, 
                                      dept=dept,
                                      coursenum=coursenum,
                                      area=area,
                                      title=title)
    response = flask.make_response(html_code)
    return response

