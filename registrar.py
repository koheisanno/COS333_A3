import html # html_code.escape() is used to thwart XSS attacks
import flask
import reg_db

app = flask.Flask(__name__, template_folder='.')

def clean_arg(arg):
    if arg:
        arg = arg.replace('%', r'\%').replace('_', r'\_')
        return '%'+arg+'%'

    return '%'

def str_or_empty(arg):
    if arg: return arg
    else: return ""

@app.route('/regdetails', methods=['GET'])
def regdetails():
    classid = flask.request.args.get('classid')

    results = reg_db.connect_to_db(classid, 'get_detail')

    html_code = flask.render_template('regdetails.html', results=results, classid = classid)
    response = flask.make_response(html_code)
    return response

@app.route('/', methods=['GET'])
def index():
    last_dept = flask.request.cookies.get('dept')
    last_coursenum = flask.request.cookies.get('coursenum')
    last_area = flask.request.cookies.get('area')
    last_title = flask.request.cookies.get('title')
    
    new_dept = flask.request.args.get('dept')
    if new_dept is not None:
        dept = new_dept
    elif last_dept is not None:
        dept = last_dept
    else:
        dept = ''

    new_coursenum = flask.request.args.get('coursenum')
    if new_coursenum is not None:
        coursenum = new_coursenum
    elif last_coursenum is not None:
        coursenum = last_coursenum
    else:
        coursenum = ''
    
    new_area = flask.request.args.get('area')
    if new_area is not None:
        area = new_area
    elif last_area is not None:
        area = last_area
    else:
        area = ''
    
    new_title = flask.request.args.get('title')
    if new_title is not None:
        title = new_title
    elif last_title is not None:
        title = last_title
    else:
        title = ''
    
    
    
    # if coursenum is None: 
    #     coursenum = flask.request.cookies.get('coursenum')
    # if area is None: 
    #     area = flask.request.cookies.get('area')
    # if title is None: 
    #     title = flask.request.cookies.get('title')

    results = reg_db.connect_to_db([clean_arg(dept), 
                                    clean_arg(coursenum), 
                                    clean_arg(area), 
                                    clean_arg(title)],
                                    'get_overviews')

    html_code = flask.render_template('index.html', 
                                      results=str_or_empty(results), 
                                      dept=str_or_empty(dept),
                                      coursenum=str_or_empty(coursenum),
                                      area=str_or_empty(area),
                                      title=str_or_empty(title))
    response = flask.make_response(html_code)
    response.set_cookie('dept', str_or_empty(dept))
    response.set_cookie('coursenum', str_or_empty(coursenum))
    response.set_cookie('area', str_or_empty(area))
    response.set_cookie('title', str_or_empty(title))

    return response

