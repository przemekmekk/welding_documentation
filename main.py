from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
import csv
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wps_list_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


ROWS_PER_PAGE = 10

# connection = sqlite3.connect('wps_list.db')
# cursor = connection.execute('select * from wpqr_list')
# names = list(map(lambda x: x[0], cursor.description))
# connection.close()
# print(names)
wpqr_titles = ['id','Numer WPQR:','Metoda spawania:', 'Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:', 'Grupa materiałowa 2:', 'Spoina:','Zakres:','Nazwa spoiwa:']
new_wpqr_titles = ['id','Numer WPQR:','Instytucja wydania:','Podstawa normatywna:','Metoda spawania:', 'Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:', 'Grupa materiałowa 2:','Blacha/rura','Rodzaj spoiny:','Grubość próbki','Zakres:','Średnica próbki','Zakres kwalifikacji2:','Pozcyja spawania:','Szczegoly:','Temp udarnosci:','Ceq:','Re:','Rm:','Podgrzewanie miedzysciegowe:','Nazwa spoiwa:','Średnica spoiwa:','Rodzaj gazu:','PWHT:','Data wydania:','Uwagi1:','Uwagi2:']
wps_titles = ['ID','Numer WPS:', 'Numer rysunku:','Grupa materiałowa:','Rodzaj złącza:','Metoda spawania:', 'Numer WPQR:']
production_test_titles = ['Numer:','Typ złącza:','Typ spoiny:','Metoda spawania:','Materiał dodatkowy:','Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:','Grupa materiałowa 2:','Numer wps:','Numer rysunku:','Spawacz:','Data spawania:']

class wpqr_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wpqr_num = db.Column(db.String(80),unique=True,nullable=False)
    trzecia_strona = db.Column(db.String(80), unique=True, nullable=False)
    podstawa_normatywna = db.Column(db.String(80), unique=True, nullable=False)
    metoda_spawania = db.Column(db.String(80), unique=True, nullable=False)
    gatunek_mat1 = db.Column(db.String(80), unique=True, nullable=False)
    gatunek_mat2 = db.Column(db.String(80), unique=True, nullable=False)
    grupa_materialowa1 = db.Column(db.String(80), unique=True, nullable=False)
    grupa_materialowa2 = db.Column(db.String(80), unique=True, nullable=False)
    blacha_rura = db.Column(db.String(80), unique=True, nullable=False)
    spoina = db.Column(db.String(80), unique=True, nullable=False)
    grubosc_probki = db.Column(db.String(80), unique=True, nullable=False)
    zakres_kwalifikacji = db.Column(db.String(80), unique=True, nullable=False)
    srednica_prob = db.Column(db.String(80), unique=True, nullable=False)
    zakres_kwalifikacji2 = db.Column(db.String(80), unique=True, nullable=False)
    pozycja_spawania = db.Column(db.String(80), unique=True, nullable=False)
    szczegoly = db.Column(db.String(80), unique=True, nullable=False)
    temp_udarnosci = db.Column(db.String(80), unique=True, nullable=False)
    ceq = db.Column(db.String(80), unique=True, nullable=False)
    re = db.Column(db.String(80), unique=True, nullable=False)
    rm = db.Column(db.String(80), unique=True, nullable=False)
    podgrzewanie_miedzysciegowe = db.Column(db.String(80), unique=True, nullable=False)
    nazwa_spoiwa = db.Column(db.String(80), unique=True, nullable=False)
    srednica_spoiwa = db.Column(db.String(80), unique=True, nullable=False)
    rodzaj_gazu = db.Column(db.String(80), unique=True, nullable=False)
    pwht = db.Column(db.String(80), unique=True, nullable=False)
    data_wydania = db.Column(db.String(80), unique=True, nullable=False)
    uwagi_1 = db.Column(db.String(80), unique=True, nullable=False)
    uwagi_2 = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.wpqr_num},{self.trzecia_strona},{self.podstawa_normatywna},{self.metoda_spawania},{self.gatunek_mat1},{self.gatunek_mat2},{self.grupa_materialowa1},{self.grupa_materialowa2},{self.blacha_rura},{self.spoina}'

class wps_lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nr_wps = db.Column(db.String(80), unique=True, nullable=False)
    Nr_rys = db.Column(db.String(80), unique=True, nullable=False)
    Nr_movex = db.Column(db.String(80), unique=True, nullable=False)
    opis = db.Column(db.String(80), unique=True, nullable=False)
    Group_of_material = db.Column(db.String(80), unique=True, nullable=False)
    Type_of_joint = db.Column(db.String(80), unique=True, nullable=False)
    welding_method = db.Column(db.String(80), unique=True, nullable=False)
    scope_of_thikness = db.Column(db.String(80), unique=True, nullable=False)
    wpqr = db.Column(db.String(80), unique=True, nullable=False)
    hiperlink = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.Nr_wps},{self.Nr_rys},{self.Nr_movex},{self.opis},{self.Group_of_material},{self.Type_of_joint},{self.welding_method},{self.scope_of_thikness},{self.wpqr},{self.hiperlink}'

@app.route('/')
def home():
    connection = sqlite3.connect('wpqr_list.db')
    cur = connection.cursor()
    rows_wpqr = []
    for row in cur.execute('SELECT id FROM wpqr_list ORDER BY id'):
        rows_wpqr.append(row)
    how_many = len(rows_wpqr)
    connection = sqlite3.connect('wps_list_1.db')
    cur = connection.cursor()
    rows_wps = []
    for row in cur.execute('SELECT id FROM wps_lista ORDER BY id'):
        rows_wps.append(row)
    how_many_wps = len(rows_wps)
    connection = sqlite3.connect('list_of_preproduction_test.db')
    cur = connection.cursor()
    rows_list_of_preproduction_test = []
    for row in cur.execute('SELECT id FROM list_of_production_test ORDER BY id'):
        rows_list_of_preproduction_test.append(row)
    how_many_production_test = len(rows_list_of_preproduction_test)
    # print(how_many_production_test)
    return render_template('index.html', wpqrs=how_many, wps=how_many_wps, preproduction_test=how_many_production_test)

@app.route('/wpqr_table')
def wpqr_table():
    connection = sqlite3.connect('wpqr_list.db')
    cur = connection.cursor()
    rows = []
    for row in cur.execute('SELECT id, wpqr_num, metoda_spawania, gatunek_mat1, gatunek_mat2, grupa_materialowa1, grupa_materialowa2, spoina, zakres_kwalifikacji, nazwa_spoiwa FROM wpqr_list ORDER BY id'):
        rows.append(row)
    return render_template('wpqr_table.html', all=rows, titles=wpqr_titles)

@app.route("/show_wpqr/<int:id>", methods=["GET", "POST"])
def show_wpqr(id):
    connection = sqlite3.connect('wpqr_list.db')
    cur = connection.cursor()
    rows = []
    for row in cur.execute(f'SELECT id, wpqr_num, trzecia_strona, podstawa_normatywna, metoda_spawania, gatunek_mat1, gatunek_mat2, grupa_materialowa1, grupa_materialowa2, blacha_rura, spoina, grubosc_probki, zakres_kwalifikacji, srednica_prob, zakres_kwalifikacji2, pozycja_spawania, szczegoly, temp_udarnosci, ceq, re, rm, podgrzewanie_miedzysciegowe, nazwa_spoiwa, srednica_spoiwa, rodzaj_gazu,pwht, data_wydania,uwagi_1,uwagi_2 FROM wpqr_list WHERE id={id}'):
        rows.append(row)
    return render_template('show_wpqr.html',titles=new_wpqr_titles, all=rows)


@app.route('/add_new_wpqr',methods=['GET','POST'])
def add_new_wpqr():
    if request.method == "POST":
        db.create_all()
        new_wpqr = wpqr_list(wpqr_num=request.form["Numer WPQR:"], trzecia_strona=request.form["Instytucja wydania:"], podstawa_normatywna=request.form["Podstawa normatywna:"],metoda_spawania=request.form["Metoda spawania:"],
                             gatunek_mat1=request.form["Gatunek materiału 1:"],gatunek_mat2=request.form["Gatunek materiału 2:"],grupa_materialowa1=request.form["Grupa materiałowa 1:"],
                             grupa_materialowa2=request.form["Grupa materiałowa 2:"],blacha_rura=request.form["Blacha/rura"],spoina=request.form["Rodzaj spoiny:"],grubosc_probki=request.form["Grubość próbki"],
                             zakres_kwalifikacji=request.form["Zakres:"],srednica_prob=request.form["Średnica próbki"],zakres_kwalifikacji2=request.form["Zakres kwalifikacji2:"],
                             pozycja_spawania=request.form["Pozcyja spawania:"],szczegoly=request.form["Szczegoly:"],temp_udarnosci=request.form["Temp udarnosci:"],ceq=request.form["Ceq:"],re=request.form["Re:"],
                             rm=request.form["Rm:"],podgrzewanie_miedzysciegowe=request.form["Podgrzewanie miedzysciegowe:"],nazwa_spoiwa=request.form["Nazwa spoiwa:"],srednica_spoiwa=request.form["Średnica spoiwa:"],
                             rodzaj_gazu=request.form["Rodzaj gazu:"],pwht=request.form["PWHT:"],data_wydania=request.form["Data wydania:"],uwagi_1=request.form["Uwagi1:"],uwagi_2=request.form["Uwagi2:"])
        db.session.add(new_wpqr)
        db.session.commit()
        return redirect(url_for('wpqr_table'))
    return render_template('new_wpqr.html',titles=new_wpqr_titles)

@app.route('/wps_list',methods=['GET','POST'])
def wps_list():
    # connection = sqlite3.connect('wps_list.db')
    # cur = connection.cursor()
    # rows = []
    # for row in cur.execute('SELECT id, Nr_wps, Nr_rys, Group_of_material, Type_of_joint, welding_method, wpqr FROM wps_list ORDER BY id'):
    #     rows.append(row)
    # all_wps = db.session.query(wps_list).all()
    # print(all_wps)
    if request.method == "POST":
        wps_to_search = request.form["Rodzaj złącza:"]
        wps_to_search_two = request.form["Metoda spawania:"]
        # print(wps_to_search)
        wps_to_search_value = "%{}%".format(wps_to_search)
        wps_to_search_two_value = "%{}%".format(wps_to_search_two)
        page = request.args.get('page', 1, type=int)
        ROWS_PER_PAGEd = 10
        all_wps = wps_lista.query.filter(wps_lista.Type_of_joint.like(wps_to_search_value),wps_lista.welding_method.like(wps_to_search_two_value)).paginate(page=page, per_page=ROWS_PER_PAGEd)
        # all_wps = db.session.query(wps_lista).filter_by(wps_to_search)
        # all_wps = db.session.query(wps_lista).filter(wps_lista.Nr_wps.ilike(wps_to_search)).all()
        print(all_wps)
        return render_template('wps_list.html',all_rows=all_wps, titles=wps_titles)

    else:
        page = request.args.get('page', 1, type=int)
        all_wps = wps_lista.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('wps_list.html', all_rows=all_wps, titles=wps_titles)

wps_welding_method = []
wps_type_of_joint = []
wps_no_of_drawing = []
@app.route('/search',methods=['GET','POST'])
def search_list():
    # all_wps = db.session.query(wps_list).all()
    # page = request.args.get('page', 1, type=int)
    # all_wps = wps_lista.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    # all_wps = ()
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_welding_method = request.form.get("Metoda spawania:", False)
    request_type_of_joint = request.form.get("Rodzaj złącza:", False)
    request_no_of_drawing = request.form.get("Numer rysunku:", False)
    print(request_welding_method)
    print(request_type_of_joint)
    print(wps_welding_method)
    print(wps_type_of_joint)

    if request_welding_method != '' and request_welding_method != False and request_type_of_joint != '' and request_type_of_joint != False:
        wps_welding_method.append(request_welding_method)
        wps_type_of_joint.append(request_type_of_joint)
        print(wps_welding_method[-1])
        print(wps_type_of_joint[-1])
        wps_welding_method_value = "%{}%".format(wps_welding_method[-1])
        wps_type_of_joint_value = "%{}%".format(wps_type_of_joint[-1])

        all_wps = wps_lista.query.filter(wps_lista.welding_method.like(wps_welding_method_value),wps_lista.Type_of_joint.like(wps_type_of_joint_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
    elif (request_welding_method == False or request_welding_method == '') and (request_type_of_joint != '' and request_type_of_joint!= False):
        wps_type_of_joint.append(request_type_of_joint)
        wps_welding_method.append(request_welding_method)
        wps_type_of_joint_value = "%{}%".format(wps_type_of_joint[-1])

        all_wps = wps_lista.query.filter(wps_lista.Type_of_joint.like(wps_type_of_joint_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
    elif (request_type_of_joint == False or request_type_of_joint == '') and (request_welding_method != '' and request_welding_method != False):
        wps_welding_method.append(request_welding_method)
        wps_type_of_joint.append(request_type_of_joint)
        wps_welding_method_value = "%{}%".format(wps_welding_method[-1])

        all_wps = wps_lista.query.filter(wps_lista.welding_method.like(wps_welding_method_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
    elif request_no_of_drawing != '' and request_no_of_drawing != False:
        wps_no_of_drawing.append(request_no_of_drawing)
        wps_no_of_drawing_value = "%{}%".format(wps_no_of_drawing[-1])

        all_wps = wps_lista.query.filter(wps_lista.Nr_rys.like(wps_no_of_drawing_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
    elif request_type_of_joint == False and request_welding_method == False:
        wps_welding_method_value = "%{}%".format(wps_welding_method[-1])
        wps_type_of_joint_value = "%{}%".format(wps_type_of_joint[-1])
        print(wps_welding_method)
        print(wps_type_of_joint)

        if wps_welding_method_value == False:
            all_wps = wps_lista.query.filter(wps_lista.Type_of_joint.like(wps_type_of_joint_value)).paginate(page=page,
                                                                                                             per_page=ROWS_PER_PAGE)
            return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
        elif wps_type_of_joint_value == False:
            all_wps = wps_lista.query.filter(wps_lista.welding_method.like(wps_welding_method_value)).paginate(page=page,
                                                                                                             per_page=ROWS_PER_PAGE)
            return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)
        else:
            all_wps = wps_lista.query.filter(wps_lista.welding_method.like(wps_welding_method_value),wps_lista.Type_of_joint.like(wps_type_of_joint_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
            return render_template('search_wpqr.html', all_rows=all_wps, titles=wps_titles)





@app.route('/preproduction_test/<int:page_num>')
def preproduction_test():
    connection = sqlite3.connect('list_of_preproduction_test.db')
    cur = connection.cursor()
    rows = []
    for row in cur.execute('SELECT test_no, type_of_joint, type_of_weld, welding_method, filler_material, grade_material_1, grade_material_2, group_of_material_1, group_of_material_2, wps, drawing_no, welder, date_of_welding FROM list_of_production_test ORDER BY id'):
        rows.append(row)

    return render_template('preproduction_test.html', all_rows=rows, titles=production_test_titles)


@app.route("/delete/<int:id>")
def delete(id):
    # DELETE A RECORD BY ID
    wpqr_to_delete = wpqr_list.query.get(id)
    db.session.delete(wpqr_to_delete)
    db.session.commit()
    return redirect(url_for('wpqr_table'))

@app.route("/edit_wpqr/<int:id>", methods=["GET", "POST"])
def edit_wpqr(id):
    if request.method == "POST":
        # UPDATE RECORD
        wpqr_to_update = wpqr_list.query.get(id)
        wpqr_to_update.wpqr_num = request.form["Numer WPQR:"]
        wpqr_to_update.trzecia_strona = request.form["Instytucja wydania:"]
        wpqr_to_update.podstawa_normatywna=request.form["Podstawa normatywna:"]
        wpqr_to_update.metoda_spawania=request.form["Metoda spawania:"]
        wpqr_to_update.gatunek_mat1=request.form["Gatunek materiału 1:"]
        wpqr_to_update.gatunek_mat2=request.form["Gatunek materiału 2:"]
        wpqr_to_update.grupa_materialowa1=request.form["Grupa materiałowa 1:"]
        wpqr_to_update.grupa_materialowa2=request.form["Grupa materiałowa 2:"]
        wpqr_to_update.blacha_rura=request.form["Blacha/rura"]
        wpqr_to_update.spoina=request.form["Rodzaj spoiny:"]
        wpqr_to_update.grubosc_probki=request.form["Grubość próbki"]
        wpqr_to_update.zakres_kwalifikacji=request.form["Zakres:"]
        wpqr_to_update.srednica_prob=request.form["Średnica próbki"]
        wpqr_to_update.zakres_kwalifikacji2=request.form["Zakres kwalifikacji2:"]
        wpqr_to_update.pozycja_spawania=request.form["Pozcyja spawania:"]
        wpqr_to_update.szczegoly=request.form["Szczegoly:"]
        wpqr_to_update.temp_udarnosci=request.form["Temp udarnosci:"]
        wpqr_to_update.ceq=request.form["Ceq:"]
        wpqr_to_update.re=request.form["Re:"]
        wpqr_to_update.rm=request.form["Rm:"]
        wpqr_to_update.podgrzewanie_miedzysciegowe=request.form["Podgrzewanie miedzysciegowe:"]
        wpqr_to_update.nazwa_spoiwa=request.form["Nazwa spoiwa:"]
        wpqr_to_update.srednica_spoiwa=request.form["Średnica spoiwa:"]
        wpqr_to_update.rodzaj_gazu=request.form["Rodzaj gazu:"]
        wpqr_to_update.pwht=request.form["PWHT:"]
        wpqr_to_update.data_wydania=request.form["Data wydania:"]
        wpqr_to_update.uwagi_1=request.form["Uwagi1:"]
        wpqr_to_update.uwagi_2=request.form["Uwagi2:"]
        db.session.commit()
        return redirect(url_for('wpqr_table'))
    connection = sqlite3.connect('wpqr_list.db')
    cur = connection.cursor()
    rows = []
    for row in cur.execute(f'SELECT id, wpqr_num, trzecia_strona, podstawa_normatywna, metoda_spawania, gatunek_mat1, gatunek_mat2, grupa_materialowa1, grupa_materialowa2, blacha_rura, spoina, grubosc_probki, zakres_kwalifikacji, srednica_prob, zakres_kwalifikacji2, pozycja_spawania, szczegoly, temp_udarnosci, ceq, re, rm, podgrzewanie_miedzysciegowe, nazwa_spoiwa, srednica_spoiwa, rodzaj_gazu,pwht, data_wydania,uwagi_1,uwagi_2 FROM wpqr_list WHERE id={id}'):
        rows.append(row)
    wpqr_id = id
    return render_template("edit_wpqr.html", titles=new_wpqr_titles, all=rows, wpqr_ida = wpqr_id)


@app.route('/forms-basic')
def forms_basic():
    return render_template('forms-basic.html')

@app.route('/forms-advanced')
def forms_advanced():
    return render_template('forms-advanced.html')

@app.route('/page-login')
def page_login():
    return render_template('page-login.html')

@app.route('/page-register')
def page_register():
    return render_template('page-register.html')

@app.route('/page-forget')
def page_forget():
    return render_template('pages-forget.html')

if __name__ == '__main__':
    app.run(debug=True)
