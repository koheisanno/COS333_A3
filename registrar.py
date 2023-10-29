import sys
import flask
from reg_db import NoSuchClassError, connect_to_db

app = flask.Flask(__name__, template_folder='.')

# clean argument
def clean_arg(arg):
    if arg:
        arg = arg.replace('%', r'\%').replace('_', r'\_')
        return '%'+arg+'%'

    return '%'

def str_or_empty(arg):
    if arg:
        return arg
    return ""

@app.route('/regdetails', methods=['GET'])
def regdetails():
    last_dept = flask.request.cookies.get('dept')
    last_coursenum = flask.request.cookies.get('coursenum')
    last_area = flask.request.cookies.get('area')
    last_title = flask.request.cookies.get('title')

    classid = flask.request.args.get('classid')

    if classid is None or classid == '':
        success = False
        results = 'missing classid'

    else:
        try:
            # check that classid is a valid integer
            classid = int(classid)
            try:
                # if class is int, fetch results
                results = connect_to_db(classid, 'get_detail')
                success = True

            except NoSuchClassError as ex:
                success = False
                results = ex
                print(f'{sys.argv[0]}: {ex}', file=sys.stderr)

            except Exception as ex:
                html_code = flask.render_template('error.html')
                response = flask.make_response(html_code)

                print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
                return response
        except ValueError:
            success = False
            results = 'non-integer classid'

    html_code = flask.render_template('regdetails.html',
                                      success=success, results=results,
                                      dept = last_dept,
                                      coursenum = last_coursenum,
                                      area = last_area,
                                      title = last_title,
                                      classid = classid)
    response = flask.make_response(html_code)
    return response

@app.route('/', methods=['GET'])
def index():
    dept = flask.request.args.get('dept')
    coursenum = flask.request.args.get('coursenum')
    area = flask.request.args.get('area')
    title = flask.request.args.get('title')

    try:
        results = connect_to_db([clean_arg(dept),
                                    clean_arg(coursenum),
                                    clean_arg(area),
                                    clean_arg(title)],
                                    'get_overviews')    
    except Exception as ex:
        html_code = flask.render_template('error.html')
        response = flask.make_response(html_code)

        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)

        return response

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
