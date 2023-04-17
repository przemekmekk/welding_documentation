from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy.sql.expression import func
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
app.secret_key = "super secret key"
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///welding_documentation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

ROWS_PER_PAGE = 10

wpqr_titles = ['id','Numer WPQR:','Metoda spawania:', 'Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:', 'Grupa materiałowa 2:', 'Spoina:','Zakres:','Nazwa spoiwa:']
new_wpqr_titles = ['id','Numer WPQR:','Instytucja wydania:','Podstawa normatywna:','Metoda spawania:', 'Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:', 'Grupa materiałowa 2:','Blacha/rura','Rodzaj spoiny:','Grubość próbki','Zakres:','Średnica próbki','Zakres kwalifikacji2:','Pozcyja spawania:','Szczegoly:','Temp udarnosci:','Ceq:','Re:','Rm:','Podgrzewanie miedzysciegowe:','Nazwa spoiwa:','Średnica spoiwa:','Rodzaj gazu:','PWHT:','Data wydania:','Uwagi1:','Uwagi2:']
wps_titles = ['ID','Numer WPS:', 'Numer rysunku:','Grupa materiałowa:','Rodzaj złącza:','Metoda spawania:', 'Numer WPQR:']
wps_titles_for_show = ['id','Numer WPS:', 'Numer rysunku:','Nr movex:','Opis:','Grupy materiałowe:','Rodzaj złącza:','Metoda spawania:','Zakres grubości:','Numer WPQR:','Hiperlink:']
production_test_titles = ['id','Numer:','Typ złącza:','Typ spoiny:','Metoda spawania:','Materiał dodatkowy:','Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:','Grupa materiałowa 2:','Numer wps:','Numer rysunku:','Spawacz:','Data ważności:','Prolongacja:']
production_test_titles_for_show = ['id','Numer:','Typ złącza:','Typ spoiny:','Pozycja spawania:','Metoda spawania:','Materiał dodatkowy:','Gatunek materiału 1:', 'Gatunek materiału 2:', 'Grupa materiałowa 1:','Grupa materiałowa 2:','Grubość materiału:','Numer wps:','Quality level:','Numer rysunku:','Spawacz:','Data spawania:','Data ważności:','Prolongacja:']
list_of_welders_approval_title = ['id','Spawacz:','Nr Spawacza:','Zakres uprawnień:','Metoda spawania:','Grupa materiałowa:','Rodzaj złącza:','Nr certyfikatu:','Data ważności:','Przedłużenie:']
list_of_welders_approval_title_for_show = ['id','Spawacz:','Nr Spawacza:','Zakres uprawnień:','Metoda spawania:','Grupa materiałowa:','Rodzaj złącza:','Grubość próbki:','Średnica/pozycja:','Inne:','Inne_2:','Nr certyfikatu:','Data ważności:','Przedłużenie:']
list_of_welding_consumables_titles = ['id', 'Nazwa:','Średnica:','Nr wytopu:','Waga:','Data certyfikatu:']

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))



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
        return f'{self.wpqr_num},{self.trzecia_strona},{self.podstawa_normatywna},{self.metoda_spawania},{self.gatunek_mat1},{self.gatunek_mat2},{self.grupa_materialowa1},{self.grupa_materialowa2},{self.blacha_rura},{self.spoina},{self.zakres_kwalifikacji},{self.nazwa_spoiwa}'

class wps_list(db.Model):
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
        return f'{self.id},{self.Nr_wps},{self.Nr_rys},{self.Nr_movex},{self.opis},{self.Group_of_material},{self.Type_of_joint},{self.welding_method},{self.scope_of_thikness},{self.wpqr},{self.hiperlink}'

class list_of_preproduction_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    No_of_Test_protocol = db.Column(db.String(80), unique=True, nullable=False)
    Type_of_joint = db.Column(db.String(80), unique=True, nullable=False)
    Marking = db.Column(db.String(80), unique=True, nullable=False)
    welding_position = db.Column(db.String(80), unique=True, nullable=False)
    welding_method = db.Column(db.String(80), unique=True, nullable=False)
    Filler_material = db.Column(db.String(80), unique=True, nullable=False)
    Grade_material_1 = db.Column(db.String(80), unique=True, nullable=False)
    Grade_material_2 = db.Column(db.String(80), unique=True, nullable=False)
    Group_of_material_1 = db.Column(db.String(80), unique=True, nullable=False)
    Group_of_material_2 = db.Column(db.String(80), unique=True, nullable=False)
    Material_thickness = db.Column(db.String(80), unique=True, nullable=False)
    WPS = db.Column(db.String(80), unique=True, nullable=False)
    Quality_level = db.Column(db.String(80), unique=True, nullable=False)
    Drawing_no = db.Column(db.String(80), unique=True, nullable=False)
    welder = db.Column(db.String(80), unique=True, nullable=False)
    Date_of_welding = db.Column(db.String(80), unique=True, nullable=False)
    valid_until = db.Column(db.String(80), unique=True, nullable=False)
    Prolongation_to = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id},{self.No_of_Test_protocol},{self.Type_of_joint},{self.Marking},{self.welding_position},{self.welding_method},{self.Filler_material},{self.Grade_material_1},{self.Grade_material_2},{self.Group_of_material_1},{self.Group_of_material_2},{self.Material_thickness},{self.WPS},{self.Quality_level},{self.Drawing_no},{self.welder},{self.Date_of_welding},{self.valid_until},{self.Prolongation_to}'

class list_of_welders_approval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Spawacz = db.Column(db.String(80), unique=True, nullable=False)
    Nr_spawacza = db.Column(db.String(80), unique=True, nullable=False)
    Zakres_uprawnien = db.Column(db.String(80), unique=True, nullable=False)
    Metoda_spaw = db.Column(db.String(80), unique=True, nullable=False)
    gr_mat = db.Column(db.String(80), unique=True, nullable=False)
    rodzaj_zlacza = db.Column(db.String(80), unique=True, nullable=False)
    grubosc = db.Column(db.String(80), unique=True, nullable=False)
    pozycja_srednica = db.Column(db.String(80), unique=True, nullable=False)
    inne = db.Column(db.String(80), unique=True, nullable=False)
    inne_2 = db.Column(db.String(80), unique=True, nullable=False)
    Nr_certyfikatu = db.Column(db.String(80), unique=True, nullable=False)
    data_waznosci = db.Column(db.String(80), unique=True, nullable=False)
    przedluzenie = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id},{self.Spawacz},{self.Nr_spawacza},{self.Zakres_uprawnien},{self.Metoda_spaw},{self.gr_mat},{self.rodzaj_zlacza},{self.grubosc},{self.pozycja_srednica},{self.inne},{self.inne_2},{self.Nr_certyfikatu},{self.data_waznosci},{self.przedluzenie}'

class welding_consumables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gatunek = db.Column(db.String(80), unique=True, nullable=False)
    srednica = db.Column(db.String(80), unique=True, nullable=False)
    wytop = db.Column(db.String(80), unique=True, nullable=False)
    kg = db.Column(db.String(80), unique=True, nullable=False)
    data_wystawienia = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id},{self.gatunek},{self.srednica},{self.wytop},{self.kg},{self.data_wystawienia}'


@app.route('/')
def home():
    all_rows_of_wpqrs = db.session.query(wpqr_list).all()
    how_many_records_of_wpqrs = len(all_rows_of_wpqrs)

    all_rows_of_wps = db.session.query(wps_list).all()
    how_many_records_of_wps = len(all_rows_of_wps)

    all_rows_of_welders_approval = db.session.query(list_of_welders_approval).all()
    how_many_records_of_weld_approvals = len(all_rows_of_welders_approval)

    all_numbers_of_welders = db.session.query(list_of_welders_approval.Nr_spawacza, db.func.count(list_of_welders_approval.Nr_spawacza)).group_by(list_of_welders_approval.Nr_spawacza).all()
    print(all_numbers_of_welders)
    all_numbers_of_welders_len=(len(all_numbers_of_welders))
    all_list_of_welding_consumables = db.session.query(welding_consumables).all()
    how_many_records = len(all_list_of_welding_consumables)

    # how_many_138_method = wpqr_list.query.filter(
    #             wpqr_list.metoda_spawania.like('138'))
    # print(how_many_138_method)
    how_many_138_method = db.session.query(wpqr_list).filter_by(metoda_spawania='138').count()
    print(how_many_138_method)
    percent_of_138 = int((how_many_138_method / how_many_records_of_wpqrs) * 100)

    how_many_138R_method = db.session.query(wpqr_list).filter_by(metoda_spawania='138 Robot').count()
    print(how_many_138R_method)
    percent_of_138R = int((how_many_138R_method / how_many_records_of_wpqrs) * 100)

    how_many_111_method = db.session.query(wpqr_list).filter_by(metoda_spawania='111').count()
    print(how_many_111_method)
    percent_of_111 = int((how_many_111_method / how_many_records_of_wpqrs) * 100)

    how_many_135_method = db.session.query(wpqr_list).filter_by(metoda_spawania='135').count()
    print(how_many_135_method)
    percent_of_135 = int((how_many_135_method / how_many_records_of_wpqrs) * 100)

    how_many_141_method = db.session.query(wpqr_list).filter_by(metoda_spawania='141').count()
    print(how_many_141_method)

    percent_of_141 = int((how_many_141_method / how_many_records_of_wpqrs)*100)
    print(percent_of_141)


    all_list_of_preproduction_tests = db.session.query(list_of_preproduction_test).all()
    how_many_records_of_preproduction_test = len(all_list_of_preproduction_tests)

    return render_template('index.html', wpqrs=how_many_records_of_wpqrs, wps=how_many_records_of_wps,welders=all_numbers_of_welders_len,production_test = how_many_records_of_preproduction_test,how_many_138_method=how_many_138_method,how_many_138R_method=how_many_138R_method,how_many_111_method=how_many_111_method, how_many_135_method=how_many_135_method,how_many_141_method=how_many_141_method,percent_of_141=percent_of_141,percent_of_135=percent_of_135,percent_of_138=percent_of_138,percent_of_138R=percent_of_138R,percent_of_111=percent_of_111)

@app.route('/list_of_welding_consumables_table',methods=['GET','POST'])
def list_of_welding_consumables_table():
    page = request.args.get('page', 1, type=int)
    all_list_of_welding_consumables = welding_consumables.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    how_many_records = all_list_of_welding_consumables.total
    return render_template('list_of_welding_consumables_table.html', all_rows=all_list_of_welding_consumables, titles=list_of_welding_consumables_titles, how_many_records=how_many_records)

@app.route("/show_welding_consumables/<int:id>", methods=["GET", "POST"])
def show_welding_consumables(id):
    all_show_welding_consumables = welding_consumables.query.filter(welding_consumables.id.like(id))
    return render_template('show_welding_consumables.html',titles=list_of_welding_consumables_titles, all=all_show_welding_consumables)

@app.route('/add_welding_consumables',methods=['GET','POST'])
def add_welding_consumables():
    if request.method == "POST":
        db.create_all()
        new_welding_consumables = welding_consumables(gatunek=request.form["Nazwa:"], srednica=request.form["Średnica:"], wytop=request.form["Nr wytopu:"],kg=request.form["Waga:"],
                             data_wystawienia=request.form["Data certyfikatu:"])
        db.session.add(new_welding_consumables)
        db.session.commit()
        return redirect(url_for('list_of_welding_consumables_table'))
    return render_template('new_welding_consumables.html',titles=list_of_welding_consumables_titles)

@app.route("/edit_welding_consumables/<int:id>", methods=["GET", "POST"])
def edit_welding_consumables(id):
    if request.method == "POST":
        # UPDATE RECORD
        welding_consumables_to_update = welding_consumables.query.get(id)
        welding_consumables_to_update.gatunek = request.form["Nazwa:"]
        welding_consumables_to_update.srednica = request.form["Średnica:"]
        welding_consumables_to_update.wytop = request.form["Nr wytopu:"]
        welding_consumables_to_update.kg = request.form["Waga:"]
        welding_consumables_to_update.data_wystawienia = request.form["Data certyfikatu:"]
        db.session.commit()
        return redirect(url_for('list_of_welding_consumables_table'))
    all_welding_consumables = welding_consumables.query.filter(welding_consumables.id.like(id))
    welding_consumables_id = id
    return render_template("edit_welding_consumables.html", titles=list_of_welding_consumables_titles, all=all_welding_consumables, welding_consumables_id = welding_consumables_id)

@app.route("/delete_welding_consumables/<int:id>")
def delete_welding_consumables(id):
    # DELETE A RECORD BY ID
    welding_consumables_to_delete = welding_consumables.query.get(id)
    db.session.delete(welding_consumables_to_delete)
    db.session.commit()
    return redirect(url_for('list_of_welding_consumables_table'))

welding_consumables_gatunek = []
welding_consumables_srednica = []
welding_consumables_wytop = []
welding_consumables_kg = []
welding_consumables_data_wystawienia = []

@app.route('/search_welding_consumables',methods=['GET','POST'])
def search_welding_consumables():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_gatunek = request.form.get("Nazwa:", False)
    request_srednica = request.form.get("Średnica:", False)
    request_wytop = request.form.get("Nr wytopu:", False)
    request_kg = request.form.get("Waga:", False)
    request_data_wystawienia = request.form.get("Data certyfikatu:", False)

    if request_gatunek != False and request_srednica != False and request_wytop != False and request_kg != False and request_data_wystawienia != False :
        welding_consumables_gatunek.append(request_gatunek)
        welding_consumables_srednica.append(request_srednica)
        welding_consumables_wytop.append(request_wytop)
        welding_consumables_kg.append(request_kg)
        welding_consumables_data_wystawienia.append(request_data_wystawienia)

        welding_consumables_gatunek_value = "%{}%".format(welding_consumables_gatunek[-1])
        welding_consumables_srednica_value = "%{}%".format(welding_consumables_srednica[-1])
        welding_consumables_wytop_value = "%{}%".format(welding_consumables_wytop[-1])
        welding_consumables_kg_value = "%{}%".format(welding_consumables_kg[-1])
        welding_consumables_data_wystawienia_value = "%{}%".format(welding_consumables_data_wystawienia[-1])

        all_welding_consumables = welding_consumables.query.filter(welding_consumables.gatunek.like(welding_consumables_gatunek_value), welding_consumables.srednica.like(welding_consumables_srednica_value), welding_consumables.wytop.like(welding_consumables_wytop_value), welding_consumables.kg.like(welding_consumables_kg_value), welding_consumables.data_wystawienia.like(welding_consumables_data_wystawienia_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        how_many_records = all_welding_consumables.total
        print(how_many_records)
        return render_template('search_welding_consumables.html', all_rows=all_welding_consumables, titles=list_of_welding_consumables_titles, how_many_records=how_many_records)

    elif request_gatunek == False and request_srednica == False and request_wytop == False and request_kg == False and request_data_wystawienia == False:

        welding_consumables_gatunek_value = "%{}%".format(welding_consumables_gatunek[-1])
        welding_consumables_srednica_value = "%{}%".format(welding_consumables_srednica[-1])
        welding_consumables_wytop_value = "%{}%".format(welding_consumables_wytop[-1])
        welding_consumables_kg_value = "%{}%".format(welding_consumables_kg[-1])
        welding_consumables_data_wystawienia_value = "%{}%".format(welding_consumables_data_wystawienia[-1])

        if welding_consumables_gatunek_value != '' and welding_consumables_srednica_value != '' and welding_consumables_wytop_value != '' and welding_consumables_kg_value != '' and welding_consumables_data_wystawienia_value != '' :
            all_welding_consumables = welding_consumables.query.filter(
                welding_consumables.gatunek.like(welding_consumables_gatunek_value),
                welding_consumables.srednica.like(welding_consumables_srednica_value),
                welding_consumables.wytop.like(welding_consumables_wytop_value),
                welding_consumables.kg.like(welding_consumables_kg_value),
                welding_consumables.data_wystawienia.like(welding_consumables_data_wystawienia_value)).paginate(
                page=page, per_page=ROWS_PER_PAGE)
            how_many_records = all_welding_consumables.total
            print(how_many_records)
            return render_template('search_welding_consumables.html', all_rows=all_welding_consumables,
                                   titles=list_of_welding_consumables_titles, how_many_records=how_many_records)


@app.route('/list_of_welders_approval_table',methods=['GET','POST'])
def list_of_welders_approval_table():
    page = request.args.get('page', 1, type=int)
    all_list_of_welders_approval = list_of_welders_approval.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    how_many_records = all_list_of_welders_approval.total
    return render_template('list_of_welders_approval_table.html', all_rows=all_list_of_welders_approval, titles=list_of_welders_approval_title, how_many_records=how_many_records)



@app.route("/show_welder_approval/<int:id>", methods=["GET", "POST"])
def show_welder_approval(id):
    all_show_welder_approval = list_of_welders_approval.query.filter(list_of_welders_approval.id.like(id))
    return render_template('show_welder_approval.html',titles=list_of_welders_approval_title_for_show, all=all_show_welder_approval)

@app.route('/add_welder_approval',methods=['GET','POST'])
def add_welder_approval():
    if request.method == "POST":
        db.create_all()
        new_welder_approval = list_of_welders_approval(Spawacz=request.form["Spawacz:"], Nr_spawacza=request.form["Nr Spawacza:"], Zakres_uprawnien=request.form["Zakres uprawnień:"],Metoda_spaw=request.form["Metoda spawania:"],
                             gr_mat=request.form["Grupa materiałowa:"],rodzaj_zlacza=request.form["Rodzaj złącza:"],grubosc=request.form["Grubość próbki:"],pozycja_srednica=request.form["Średnica/pozycja:"],
                             inne=request.form["Inne:"],inne_2=request.form["Inne_2:"],Nr_certyfikatu=request.form["Nr certyfikatu:"],data_waznosci=request.form["Data ważności:"],
                             przedluzenie=request.form["Przedłużenie:"])
        db.session.add(new_welder_approval)
        db.session.commit()
        return redirect(url_for('list_of_welders_approval_table'))
    return render_template('new_welders_approval.html',titles=list_of_welders_approval_title_for_show)

@app.route("/edit_welder_approval/<int:id>", methods=["GET", "POST"])
def edit_welder_approval(id):
    if request.method == "POST":
        # UPDATE RECORD
        approval_to_update = list_of_welders_approval.query.get(id)
        approval_to_update.Spawacz = request.form["Spawacz:"]
        approval_to_update.Nr_spawacza = request.form["Nr Spawacza:"]
        approval_to_update.Zakres_uprawnien = request.form["Zakres uprawnień:"]
        approval_to_update.Metoda_spaw = request.form["Metoda spawania:"]
        approval_to_update.gr_mat = request.form["Grupa materiałowa:"]
        approval_to_update.rodzaj_zlacza = request.form["Rodzaj złącza:"]
        approval_to_update.grubosc = request.form["Grubość próbki:"]
        approval_to_update.pozycja_srednica = request.form["Średnica/pozycja:"]
        approval_to_update.inne = request.form["Inne:"]
        approval_to_update.inne_2 = request.form["Inne_2:"]
        approval_to_update.Nr_certyfikatu = request.form["Nr certyfikatu:"]
        approval_to_update.data_waznosci = request.form["Data ważności:"]
        approval_to_update.przedluzenie = request.form["Przedłużenie:"]
        db.session.commit()
        return redirect(url_for('list_of_welders_approval_table'))
    all_approval = list_of_welders_approval.query.filter(list_of_welders_approval.id.like(id))
    approval_id = id
    return render_template("edit_welder_approval.html", titles=list_of_welders_approval_title_for_show, all=all_approval, approval_id = approval_id)

@app.route("/delete_welder_approval/<int:id>")
def delete_welder_approval(id):
    # DELETE A RECORD BY ID
    approval_to_delete = list_of_welders_approval.query.get(id)
    db.session.delete(approval_to_delete)
    db.session.commit()
    return redirect(url_for('list_of_welders_approval_table'))

approval_spawacz = []
approval_nr_spawacza = []
approval_zakres_uprawnien = []
approval_metoda_spaw = []
approval_gr_mat = []
approval_rodzaj_zlacza = []
approval_nr_cert = []
approval_data_waznosci = []
approval_przedluzenie = []

@app.route('/search_approval',methods=['GET','POST'])
def search_approval():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_Spawacz = request.form.get("Spawacz:", False)
    request_Nr_spawacza = request.form.get("Nr Spawacza:", False)
    request_Zakres_uprawnien = request.form.get("Zakres uprawnień:", False)
    request_Metoda_spaw = request.form.get("Metoda spawania:", False)
    request_gr_mat = request.form.get("Grupa materiałowa:", False)
    request_rodzaj_zlacza = request.form.get("Rodzaj złącza:", False)
    request_Nr_certyfikatu = request.form.get("Nr certyfikatu:", False)
    request_data_waznosci = request.form.get("Data ważności:", False)
    request_przedluzenie = request.form.get("Przedłużenie:", False)


    if request_Spawacz != False and request_Nr_spawacza != False and request_Zakres_uprawnien != False and request_Metoda_spaw != False and request_gr_mat != False and request_rodzaj_zlacza != False and request_Nr_certyfikatu != False and request_data_waznosci != False and request_przedluzenie != False:
        approval_spawacz.append(request_Spawacz)
        approval_nr_spawacza.append(request_Nr_spawacza)
        approval_zakres_uprawnien.append(request_Zakres_uprawnien)
        approval_metoda_spaw.append(request_Metoda_spaw)
        approval_gr_mat.append(request_gr_mat)
        approval_rodzaj_zlacza.append(request_rodzaj_zlacza)
        approval_nr_cert.append(request_Nr_certyfikatu)
        approval_data_waznosci.append(request_data_waznosci)
        approval_przedluzenie.append(request_przedluzenie)

        approval_spawacz_value = "%{}%".format(approval_spawacz[-1])
        approval_nr_spawacza_value = "%{}%".format(approval_nr_spawacza[-1])
        approval_zakres_uprawnien_value = "%{}%".format(approval_zakres_uprawnien[-1])
        approval_metoda_spaw_value = "%{}%".format(approval_metoda_spaw[-1])
        approval_gr_mat_value = "%{}%".format(approval_gr_mat[-1])
        approval_rodzaj_zlacza_value = "%{}%".format(approval_rodzaj_zlacza[-1])
        approval_nr_cert_value = "%{}%".format(approval_nr_cert[-1])
        approval_data_waznosci_value = "%{}%".format(approval_data_waznosci[-1])
        approval_przedluzenie_value = "%{}%".format(approval_przedluzenie[-1])
        # print(wps_no_value,wps_no_of_drawing_value,material_group_value,wps_type_of_joint_value,wps_welding_method_value,wpqr_no_value)

        all_approvals = list_of_welders_approval.query.filter(list_of_welders_approval.Spawacz.like(approval_spawacz_value), list_of_welders_approval.Nr_spawacza.like(approval_nr_spawacza_value), list_of_welders_approval.Zakres_uprawnien.like(approval_zakres_uprawnien_value), list_of_welders_approval.Metoda_spaw.like(approval_metoda_spaw_value), list_of_welders_approval.gr_mat.like(approval_gr_mat_value), list_of_welders_approval.rodzaj_zlacza.like(approval_rodzaj_zlacza_value), list_of_welders_approval.Nr_certyfikatu.like(approval_nr_cert_value), list_of_welders_approval.data_waznosci.like(approval_data_waznosci_value), list_of_welders_approval.przedluzenie.like(approval_przedluzenie_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        how_many_records = all_approvals.total
        print(how_many_records)
        return render_template('search_welder_approval.html', all_rows=all_approvals, titles=list_of_welders_approval_title, how_many_records=how_many_records)

    elif request_Spawacz == False and request_Nr_spawacza == False and request_Zakres_uprawnien == False and request_Metoda_spaw == False and request_gr_mat == False and request_rodzaj_zlacza == False and request_Nr_certyfikatu == False and request_data_waznosci == False and request_przedluzenie == False:

        approval_spawacz_value = "%{}%".format(approval_spawacz[-1])
        approval_nr_spawacza_value = "%{}%".format(approval_nr_spawacza[-1])
        approval_zakres_uprawnien_value = "%{}%".format(approval_zakres_uprawnien[-1])
        approval_metoda_spaw_value = "%{}%".format(approval_metoda_spaw[-1])
        approval_gr_mat_value = "%{}%".format(approval_gr_mat[-1])
        approval_rodzaj_zlacza_value = "%{}%".format(approval_rodzaj_zlacza[-1])
        approval_nr_cert_value = "%{}%".format(approval_nr_cert[-1])
        approval_data_waznosci_value = "%{}%".format(approval_data_waznosci[-1])
        approval_przedluzenie_value = "%{}%".format(approval_przedluzenie[-1])

        if approval_spawacz_value != '' and approval_nr_spawacza_value != '' and approval_zakres_uprawnien_value != '' and approval_metoda_spaw_value != '' and approval_gr_mat_value != '' and approval_rodzaj_zlacza_value != '' and approval_nr_cert_value != '' and approval_data_waznosci_value != '' and approval_przedluzenie_value != '':
            all_approvals = list_of_welders_approval.query.filter(
                list_of_welders_approval.Spawacz.like(approval_spawacz_value),
                list_of_welders_approval.Nr_spawacza.like(approval_nr_spawacza_value),
                list_of_welders_approval.Zakres_uprawnien.like(approval_zakres_uprawnien_value),
                list_of_welders_approval.Metoda_spaw.like(approval_metoda_spaw_value),
                list_of_welders_approval.gr_mat.like(approval_gr_mat_value),
                list_of_welders_approval.rodzaj_zlacza.like(approval_rodzaj_zlacza_value),
                list_of_welders_approval.Nr_certyfikatu.like(approval_nr_cert_value),
                list_of_welders_approval.data_waznosci.like(approval_data_waznosci_value),
                list_of_welders_approval.przedluzenie.like(approval_przedluzenie_value)).paginate(page=page,
                                                                                                  per_page=ROWS_PER_PAGE)
            how_many_records = all_approvals.total
            print(how_many_records)
            return render_template('search_welder_approval.html', all_rows=all_approvals, titles=list_of_welders_approval_title,
                                   how_many_records=how_many_records)


@app.route('/wpqr_table',methods=['GET','POST'])
def wpqr_table():
    page = request.args.get('page', 1, type=int)
    all_wpqr = wpqr_list.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    how_many_records = all_wpqr.total
    return render_template('wpqr_table.html', all_rows=all_wpqr, titles=wpqr_titles, how_many_records=how_many_records)

@app.route("/show_wpqr/<int:id>", methods=["GET", "POST"])
def show_wpqr(id):
    all_wpqr = wpqr_list.query.filter(wpqr_list.id.like(id))
    return render_template('show_wpqr.html',titles=new_wpqr_titles, all=all_wpqr)


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
    all_wpqr = wpqr_list.query.filter(wpqr_list.id.like(id))
    wpqr_id = id
    return render_template("edit_wpqr.html", titles=new_wpqr_titles, all=all_wpqr, wpqr_id = wpqr_id)

@app.route("/delete_wpqr/<int:id>")
def delete_wpqr(id):
    # DELETE A RECORD BY ID
    wpqr_to_delete = wpqr_list.query.get(id)
    db.session.delete(wpqr_to_delete)
    db.session.commit()
    return redirect(url_for('wpqr_table'))

wpqr_wpqr_no = []
wpqr_welding_method = []
wpqr_grade_material_one = []
wpqr_grade_material_two = []
wpqr_material_group_one = []
wpqr_material_group_two = []
wpqr_type_of_joint = []
wpqr_range_of_qualification = []
wpqr_filler_material = []

@app.route('/search_wpqr',methods=['GET','POST'])
def search_wpqr_list():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_wpqr_no = request.form.get("Numer WPQR:", False)
    request_welding_method = request.form.get("Metoda spawania:", False)
    request_grade_material_one = request.form.get("Gatunek materiału 1:", False)
    request_grade_material_two = request.form.get("Gatunek materiału 2:", False)
    request_material_group_one = request.form.get("Grupa materiałowa 1:", False)
    request_material_group_two = request.form.get("Grupa materiałowa 2:", False)
    request_type_of_joint = request.form.get("Spoina:", False)
    request_range_of_qualification = request.form.get("Zakres:", False)
    request_filler_material = request.form.get("Nazwa spoiwa:", False)


    if request_wpqr_no != False and request_welding_method != False and request_grade_material_one != False and request_grade_material_two != False and request_material_group_one != False and request_material_group_two != False and request_type_of_joint != False and request_range_of_qualification != False and request_filler_material != False:
        wpqr_wpqr_no.append(request_wpqr_no)
        wpqr_welding_method.append(request_welding_method)
        wpqr_grade_material_one.append(request_grade_material_one)
        wpqr_grade_material_two.append(request_grade_material_two)
        wpqr_material_group_one.append(request_material_group_one)
        wpqr_material_group_two.append(request_material_group_two)
        wpqr_type_of_joint.append(request_type_of_joint)
        wpqr_range_of_qualification.append(request_range_of_qualification)
        wpqr_filler_material.append(request_filler_material)

        wpqr_wpqr_no_value = "%{}%".format(wpqr_wpqr_no[-1])
        wpqr_welding_method_value = "%{}%".format(wpqr_welding_method[-1])
        wpqr_grade_material_one_value = "%{}%".format(wpqr_grade_material_one[-1])
        wpqr_grade_material_two_value = "%{}%".format(wpqr_grade_material_two[-1])
        wpqr_material_group_one_value = "%{}%".format(wpqr_material_group_one[-1])
        wpqr_material_group_two_value = "%{}%".format(wpqr_material_group_two[-1])
        wpqr_type_of_joint_value = "%{}%".format(wpqr_type_of_joint[-1])
        wpqr_range_of_qualification_value = "%{}%".format(wpqr_range_of_qualification[-1])
        wpqr_filler_material_value = "%{}%".format(wpqr_filler_material[-1])
        # print(wps_no_value,wps_no_of_drawing_value,material_group_value,wps_type_of_joint_value,wps_welding_method_value,wpqr_no_value)

        all_wpqr = wpqr_list.query.filter(wpqr_list.wpqr_num.like(wpqr_wpqr_no_value), wpqr_list.metoda_spawania.like(wpqr_welding_method_value), wpqr_list.gatunek_mat1.like(wpqr_grade_material_one_value), wpqr_list.gatunek_mat2.like(wpqr_grade_material_two_value), wpqr_list.grupa_materialowa1.like(wpqr_material_group_one_value), wpqr_list.grupa_materialowa2.like(wpqr_material_group_two_value), wpqr_list.spoina.like(wpqr_type_of_joint_value), wpqr_list.zakres_kwalifikacji.like(wpqr_range_of_qualification_value), wpqr_list.nazwa_spoiwa.like(wpqr_filler_material_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        how_many_records = all_wpqr.total
        print(how_many_records)
        return render_template('search_wpqr.html', all_rows=all_wpqr, titles=wpqr_titles, how_many_records=how_many_records)

    elif request_wpqr_no == False and request_welding_method == False and request_grade_material_one == False and request_grade_material_two == False and request_material_group_one == False and request_material_group_two == False and request_type_of_joint == False and request_range_of_qualification == False and request_filler_material == False:

        wpqr_wpqr_no_value = "%{}%".format(wpqr_wpqr_no[-1])
        wpqr_welding_method_value = "%{}%".format(wpqr_welding_method[-1])
        wpqr_grade_material_one_value = "%{}%".format(wpqr_grade_material_one[-1])
        wpqr_grade_material_two_value = "%{}%".format(wpqr_grade_material_two[-1])
        wpqr_material_group_one_value = "%{}%".format(wpqr_material_group_one[-1])
        wpqr_material_group_two_value = "%{}%".format(wpqr_material_group_two[-1])
        wpqr_type_of_joint_value = "%{}%".format(wpqr_type_of_joint[-1])
        wpqr_range_of_qualification_value = "%{}%".format(wpqr_range_of_qualification[-1])
        wpqr_filler_material_value = "%{}%".format(wpqr_filler_material[-1])

        if wpqr_wpqr_no_value != '' and wpqr_welding_method_value != '' and wpqr_grade_material_one_value != '' and wpqr_grade_material_two_value != '' and wpqr_material_group_one_value != '' and wpqr_material_group_two_value != '' and wpqr_type_of_joint_value != '' and wpqr_range_of_qualification_value != '' and wpqr_filler_material_value != '':
            all_wpqr = wpqr_list.query.filter(wpqr_list.wpqr_num.like(wpqr_wpqr_no_value),
                                              wpqr_list.metoda_spawania.like(wpqr_welding_method_value),
                                              wpqr_list.gatunek_mat1.like(wpqr_grade_material_one_value),
                                              wpqr_list.gatunek_mat2.like(wpqr_grade_material_two_value),
                                              wpqr_list.grupa_materialowa1.like(wpqr_material_group_one_value),
                                              wpqr_list.grupa_materialowa2.like(wpqr_material_group_two_value),
                                              wpqr_list.spoina.like(wpqr_type_of_joint_value),
                                              wpqr_list.zakres_kwalifikacji.like(wpqr_range_of_qualification_value),
                                              wpqr_list.nazwa_spoiwa.like(wpqr_filler_material_value)).paginate(
                page=page, per_page=ROWS_PER_PAGE)
            how_many_records = all_wpqr.total
            print(how_many_records)
            return render_template('search_wpqr.html', all_rows=all_wpqr, titles=wpqr_titles,
                                   how_many_records=how_many_records)

@app.route('/wps_table',methods=['GET','POST'])
def wps_table():
    page = request.args.get('page', 1, type=int)
    all_wps = wps_list.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    how_many_records = all_wps.total
    return render_template('wps_table.html', all_rows=all_wps, titles=wps_titles, how_many_records=how_many_records)

@app.route("/show_wps/<int:id>", methods=["GET", "POST"])
def show_wps(id):
    all_wps = wps_list.query.filter(wps_list.id.like(id))
    return render_template('show_wps.html',titles=wps_titles_for_show, all=all_wps)

@app.route('/add_new_wps',methods=['GET','POST'])
def add_new_wps():
    if request.method == "POST":
        db.create_all()
        new_wps = wps_list(Nr_wps=request.form['Numer WPS:'], Nr_rys=request.form["Numer rysunku:"], Nr_movex=request.form["Nr movex:"], opis=request.form["Opis:"],
                           Group_of_material=request.form["Grupy materiałowe:"], Type_of_joint=request.form["Rodzaj złącza:"], welding_method=request.form["Metoda spawania:"],
                           scope_of_thikness=request.form["Zakres grubości:"], wpqr=request.form["Numer WPQR:"], hiperlink=request.form["Hiperlink:"])
        db.session.add(new_wps)
        db.session.commit()
        return redirect(url_for('wps_list'))
    last_id = db.session.query(func.max(wps_list.id)).scalar()
    last_wps_query = wps_list.query.filter(wps_list.id.like(last_id))
    last_wps = []
    for i in last_wps_query:
        last_wps.append((int(i.Nr_wps))+1)
    print(last_wps)
    return render_template('new_wps.html',titles=wps_titles_for_show,all=last_wps)

@app.route('/production_test_table',methods=['GET','POST'])
def production_test_table():
    page = request.args.get('page', 1, type=int)
    all_production_test = list_of_preproduction_test.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    how_many_records = all_production_test.total
    return render_template('production_test_table.html', all_rows=all_production_test, titles=production_test_titles, how_many_records=how_many_records)

@app.route("/show_production_test/<int:id>", methods=["GET", "POST"])
def show_production_test(id):
    all_production_test = list_of_preproduction_test.query.filter(list_of_preproduction_test.id.like(id))
    return render_template('show_production_test.html',titles=production_test_titles_for_show, all=all_production_test)

@app.route('/add_new_production_test',methods=['GET','POST'])
def add_new_production_test():
    if request.method == "POST":
        db.create_all()
        new_production_test = list_of_preproduction_test(No_of_Test_protocol=request.form['Numer:'], Type_of_joint=request.form["Typ złącza:"], Marking=request.form["Typ spoiny:"], welding_position=request.form["Pozycja spawania:"],
                           welding_method=request.form["Metoda spawania:"], Filler_material=request.form["Materiał dodatkowy:"], Grade_material_1=request.form["Gatunek materiału 1:"],
                           Grade_material_2=request.form["Gatunek materiału 2:"], Group_of_material_1=request.form["Grupa materiałowa 1:"], Group_of_material_2=request.form["Grupa materiałowa 2:"],
                            Material_thickness=request.form["Grubość materiału:"], WPS=request.form["Numer wps:"], Quality_level=request.form["Quality level:"],
                            Drawing_no=request.form["Numer rysunku:"], welder=request.form["Spawacz:"], Date_of_welding=request.form["Data spawania:"],
                            valid_until=request.form["Data ważności:"], Prolongation_to=request.form["Prolongacja:"])
        db.session.add(new_production_test)
        db.session.commit()
        return redirect(url_for('production_test_table'))
    return render_template('new_production_test.html', titles=production_test_titles_for_show)

@app.route("/delete_production_test/<int:id>")
def delete_production_test(id):
    # DELETE A RECORD BY ID
    production_test_to_delete = list_of_preproduction_test.query.get(id)
    db.session.delete(production_test_to_delete)
    db.session.commit()
    return redirect(url_for('production_test_table'))

@app.route("/edit_production_test/<int:id>", methods=["GET", "POST"])
def edit_production_test(id):
    if request.method == "POST":
        # UPDATE RECORD
        production_test_to_update = list_of_preproduction_test.query.get(id)
        production_test_to_update.No_of_Test_protocol = request.form['Numer:']
        production_test_to_update.Type_of_joint = request.form["Typ złącza:"]
        production_test_to_update.Marking=request.form["Typ spoiny:"]
        production_test_to_update.welding_position=request.form["Pozycja spawania:"]
        production_test_to_update.welding_method=request.form["Metoda spawania:"]
        production_test_to_update.Filler_material=request.form["Materiał dodatkowy:"]
        production_test_to_update.Grade_material_1=request.form["Gatunek materiału 1:"]
        production_test_to_update.Grade_material_2=request.form["Gatunek materiału 2:"]
        production_test_to_update.Group_of_material_1=request.form["Grupa materiałowa 1:"]
        production_test_to_update.Group_of_material_2=request.form["Grupa materiałowa 2:"]
        production_test_to_update.Material_thickness=request.form["Grubość materiału:"]
        production_test_to_update.WPS=request.form["Numer wps:"]
        production_test_to_update.Quality_level=request.form["Quality level:"]
        production_test_to_update.Drawing_no=request.form["Numer rysunku:"]
        production_test_to_update.welder=request.form["Spawacz:"]
        production_test_to_update.Date_of_welding=request.form["Data spawania:"]
        production_test_to_update.valid_until=request.form["Data ważności:"]
        production_test_to_update.Prolongation_to=request.form["Prolongacja:"]
        db.session.commit()
        return redirect(url_for('production_test_table'))
    all_production_test = list_of_preproduction_test.query.filter(list_of_preproduction_test.id.like(id))
    all_production_test_id = id
    return render_template("edit_production_test.html", titles=production_test_titles_for_show, all=all_production_test, production_test_id = all_production_test_id)

p_test_No_of_Test_protocol = []
p_test_Type_of_joint = []
p_test_Marking = []
p_test_welding_method = []
p_test_Filler_material = []
p_test_Grade_material_1 = []
p_test_Grade_material_2 = []
p_test_Group_of_material_1 = []
p_test_Group_of_material_2 = []
p_test_WPS = []
p_test_Drawing_no = []
p_test_welder = []
p_test_valid_until = []
p_test_Prolongation_to = []

@app.route('/search_production_test',methods=['GET','POST'])
def search_production_test_list():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_No_of_Test_protocol = request.form.get("Numer:", False)
    request_Type_of_joint = request.form.get("Typ złącza:", False)
    request_Marking = request.form.get("Typ spoiny:", False)
    request_welding_method = request.form.get("Metoda spawania:", False)
    request_Filler_material = request.form.get("Materiał dodatkowy:", False)
    request_Grade_material_1 = request.form.get("Gatunek materiału 1:", False)
    request_Grade_material_2 = request.form.get("Gatunek materiału 2:", False)
    request_Group_of_material_1 = request.form.get("Grupa materiałowa 1:", False)
    request_Group_of_material_2 = request.form.get("Grupa materiałowa 2:", False)
    request_WPS = request.form.get("Numer wps:", False)
    request_Drawing_no = request.form.get("Numer rysunku:", False)
    request_welder = request.form.get("Spawacz:", False)
    request_valid_until = request.form.get("Data ważności:", False)
    request_Prolongation_to = request.form.get("Prolongacja:", False)




    if request_No_of_Test_protocol != False and request_Type_of_joint != False and request_Marking != False and request_welding_method != False and request_Filler_material != False and request_Grade_material_1 != False and request_Grade_material_2 != False and request_Group_of_material_1 != False and request_Group_of_material_2 != False and request_WPS != False and request_Drawing_no != False and request_welder != False and request_valid_until != False and request_Prolongation_to != False:
        p_test_No_of_Test_protocol.append(request_No_of_Test_protocol)
        p_test_Type_of_joint.append(request_Type_of_joint)
        p_test_Marking.append(request_Marking)
        p_test_welding_method.append(request_welding_method)
        p_test_Filler_material.append(request_Filler_material)
        p_test_Grade_material_1.append(request_Grade_material_1)
        p_test_Grade_material_2.append(request_Grade_material_2)
        p_test_Group_of_material_1.append(request_Group_of_material_1)
        p_test_Group_of_material_2.append(request_Group_of_material_2)
        p_test_WPS.append(request_WPS)
        p_test_Drawing_no.append(request_Drawing_no)
        p_test_welder.append(request_welder)
        p_test_valid_until.append(request_valid_until)
        p_test_Prolongation_to.append(request_Prolongation_to)


        p_test_No_of_Test_protocol_value = "%{}%".format(p_test_No_of_Test_protocol[-1])
        p_test_Type_of_joint_value = "%{}%".format(p_test_Type_of_joint[-1])
        p_test_Marking_value = "%{}%".format(p_test_Marking[-1])
        p_test_welding_method_value = "%{}%".format(p_test_welding_method[-1])
        p_test_Filler_material_value = "%{}%".format(p_test_Filler_material[-1])
        p_test_Grade_material_1_value = "%{}%".format(p_test_Grade_material_1[-1])
        p_test_Grade_material_2_value = "%{}%".format(p_test_Grade_material_2[-1])
        p_test_Group_of_material_1_value = "%{}%".format(p_test_Group_of_material_1[-1])
        p_test_Group_of_material_2_value = "%{}%".format(p_test_Group_of_material_2[-1])
        p_test_WPS_value = "%{}%".format(p_test_WPS[-1])
        p_test_Drawing_no_value = "%{}%".format(p_test_Drawing_no[-1])
        p_test_welder_value = "%{}%".format(p_test_welder[-1])
        p_test_valid_until_value = "%{}%".format(p_test_valid_until[-1])
        p_test_Prolongation_to_value = "%{}%".format(p_test_Prolongation_to[-1])
        # print(wps_no_value,wps_no_of_drawing_value,material_group_value,wps_type_of_joint_value,wps_welding_method_value,wpqr_no_value)

        all_production_test = list_of_preproduction_test.query.filter(list_of_preproduction_test.No_of_Test_protocol.like(p_test_No_of_Test_protocol_value), list_of_preproduction_test.Type_of_joint.like(p_test_Type_of_joint_value), list_of_preproduction_test.Marking.like(p_test_Marking_value), list_of_preproduction_test.welding_method.like(p_test_welding_method_value), list_of_preproduction_test.Filler_material.like(p_test_Filler_material_value), list_of_preproduction_test.Grade_material_1.like(p_test_Grade_material_1_value), list_of_preproduction_test.Grade_material_2.like(p_test_Grade_material_2_value),list_of_preproduction_test.Group_of_material_1.like(p_test_Group_of_material_1_value), list_of_preproduction_test.Group_of_material_2.like(p_test_Group_of_material_2_value), list_of_preproduction_test.WPS.like(p_test_WPS_value), list_of_preproduction_test.Drawing_no.like(p_test_Drawing_no_value), list_of_preproduction_test.welder.like(p_test_welder_value), list_of_preproduction_test.valid_until.like(p_test_valid_until_value), list_of_preproduction_test.Prolongation_to.like(p_test_Prolongation_to_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        how_many_records = all_production_test.total
        print(how_many_records)
        return render_template('search_production_test.html', all_rows=all_production_test, titles=production_test_titles, how_many_records=how_many_records)

    elif request_No_of_Test_protocol == False and request_Type_of_joint == False and request_Marking == False and request_welding_method == False and request_Filler_material == False and request_Grade_material_1 == False and request_Grade_material_2 == False and request_Group_of_material_1 == False and request_Group_of_material_2 == False and request_WPS == False and request_Drawing_no == False and request_welder == False and request_valid_until == False and request_Prolongation_to == False:

        p_test_No_of_Test_protocol_value = "%{}%".format(p_test_No_of_Test_protocol[-1])
        p_test_Type_of_joint_value = "%{}%".format(p_test_Type_of_joint[-1])
        p_test_Marking_value = "%{}%".format(p_test_Marking[-1])
        p_test_welding_method_value = "%{}%".format(p_test_welding_method[-1])
        p_test_Filler_material_value = "%{}%".format(p_test_Filler_material[-1])
        p_test_Grade_material_1_value = "%{}%".format(p_test_Grade_material_1[-1])
        p_test_Grade_material_2_value = "%{}%".format(p_test_Grade_material_2[-1])
        p_test_Group_of_material_1_value = "%{}%".format(p_test_Group_of_material_1[-1])
        p_test_Group_of_material_2_value = "%{}%".format(p_test_Group_of_material_2[-1])
        p_test_WPS_value = "%{}%".format(p_test_WPS[-1])
        p_test_Drawing_no_value = "%{}%".format(p_test_Drawing_no[-1])
        p_test_welder_value = "%{}%".format(p_test_welder[-1])
        p_test_valid_until_value = "%{}%".format(p_test_valid_until[-1])
        p_test_Prolongation_to_value = "%{}%".format(p_test_Prolongation_to[-1])

        if request_No_of_Test_protocol != '' and request_Type_of_joint != '' and request_Marking != '' and request_welding_method != '' and request_Filler_material != '' and request_Grade_material_1 != '' and request_Grade_material_2 != '' and request_Group_of_material_1 != '' and request_Group_of_material_2 != '' and request_WPS != '' and request_Drawing_no != '' and request_welder != '' and request_valid_until != '' and request_Prolongation_to != '':
            all_production_test = list_of_preproduction_test.query.filter(
                list_of_preproduction_test.No_of_Test_protocol.like(p_test_No_of_Test_protocol_value),
                list_of_preproduction_test.Type_of_joint.like(p_test_Type_of_joint_value),
                list_of_preproduction_test.Marking.like(p_test_Marking_value),
                list_of_preproduction_test.welding_method.like(p_test_welding_method_value),
                list_of_preproduction_test.Filler_material.like(p_test_Filler_material_value),
                list_of_preproduction_test.Grade_material_1.like(p_test_Grade_material_1_value),
                list_of_preproduction_test.Grade_material_2.like(p_test_Grade_material_2_value),
                list_of_preproduction_test.Group_of_material_1.like(p_test_Group_of_material_1_value),
                list_of_preproduction_test.Group_of_material_2.like(p_test_Group_of_material_2_value),
                list_of_preproduction_test.WPS.like(p_test_WPS_value),
                list_of_preproduction_test.Drawing_no.like(p_test_Drawing_no_value),
                list_of_preproduction_test.welder.like(p_test_welder_value),
                list_of_preproduction_test.valid_until.like(p_test_valid_until_value),
                list_of_preproduction_test.Prolongation_to.like(p_test_Prolongation_to_value)).paginate(page=page,
                                                                                                        per_page=ROWS_PER_PAGE)
            how_many_records = all_production_test.total
            print(how_many_records)
            return render_template('search_production_test.html', all_rows=all_production_test,
                                   titles=production_test_titles, how_many_records=how_many_records)


wps_no = []
wps_no_of_drawing = []
wps_material_group = []
wps_type_of_joint = []
wps_welding_method = []
wps_wpqr_no = []

@app.route('/search_wps',methods=['GET','POST'])
def search_wps_list():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 10
    request_wps_no = request.form.get("Numer WPS:", False)
    request_no_of_drawing = request.form.get("Numer rysunku:", False)
    request_welding_method = request.form.get("Metoda spawania:", False)
    request_type_of_joint = request.form.get("Rodzaj złącza:", False)
    request_material_group = request.form.get("Grupa materiałowa:", False)
    request_wpqr_no = request.form.get("Numer WPQR:", False)

    if request_wps_no != False and request_no_of_drawing != False and request_welding_method != False and request_type_of_joint != False and request_material_group != False and request_wpqr_no != False:
        wps_no.append(request_wps_no)
        wps_no_of_drawing.append(request_no_of_drawing)
        wps_material_group.append(request_material_group)
        wps_type_of_joint.append(request_type_of_joint)
        wps_welding_method.append(request_welding_method)
        wps_wpqr_no.append(request_wpqr_no)

        wps_no_value = "%{}%".format(wps_no[-1])
        wps_no_of_drawing_value = "%{}%".format(wps_no_of_drawing[-1])
        material_group_value = "%{}%".format(wps_material_group[-1])
        wps_type_of_joint_value = "%{}%".format(wps_type_of_joint[-1])
        wps_welding_method_value = "%{}%".format(wps_welding_method[-1])
        wpqr_no_value = "%{}%".format(wps_wpqr_no[-1])
        # print(wps_no_value,wps_no_of_drawing_value,material_group_value,wps_type_of_joint_value,wps_welding_method_value,wpqr_no_value)

        all_wps = wps_list.query.filter(wps_list.Nr_wps.like(wps_no_value), wps_list.Nr_rys.like(wps_no_of_drawing_value), wps_list.Group_of_material.like(material_group_value), wps_list.Type_of_joint.like(wps_type_of_joint_value), wps_list.welding_method.like(wps_welding_method_value), wps_list.wpqr.like(wpqr_no_value)).paginate(page=page, per_page=ROWS_PER_PAGE)
        how_many_records = all_wps.total
        print(how_many_records)
        return render_template('search_wps.html', all_rows=all_wps, titles=wps_titles, how_many_records=how_many_records)

    elif request_wps_no == False and request_no_of_drawing == False and request_welding_method == False and request_type_of_joint == False and request_material_group == False and request_wpqr_no == False:

        wps_no_value = "%{}%".format(wps_no[-1])
        wps_no_of_drawing_value = "%{}%".format(wps_no_of_drawing[-1])
        material_group_value = "%{}%".format(wps_material_group[-1])
        wps_type_of_joint_value = "%{}%".format(wps_type_of_joint[-1])
        wps_welding_method_value = "%{}%".format(wps_welding_method[-1])
        wpqr_no_value = "%{}%".format(wps_wpqr_no[-1])
        # print(wps_no_value,wps_no_of_drawing_value,material_group_value,wps_type_of_joint_value,wps_welding_method_value,wpqr_no_value)

        if wps_no_value != '' and wps_no_of_drawing_value != '' and material_group_value != '' and wps_type_of_joint_value != '' and wps_welding_method_value != '' and wpqr_no_value != '':
            all_wps = wps_list.query.filter(wps_list.Nr_wps.like(wps_no_value), wps_list.Nr_rys.like(wps_no_of_drawing_value), wps_list.Group_of_material.like(material_group_value), wps_list.Type_of_joint.like(wps_type_of_joint_value), wps_list.welding_method.like(wps_welding_method_value), wps_list.wpqr.like(wpqr_no_value)).paginate(page=page,
                                                                                                                                                                                                                                                                                                                                                per_page=ROWS_PER_PAGE)
            how_many_records = all_wps.total
            return render_template('search_wps.html', all_rows=all_wps, titles=wps_titles, how_many_records=how_many_records)





@app.route("/delete_wps/<int:id>")
def delete_wps(id):
    # DELETE A RECORD BY ID
    wps_to_delete = wps_list.query.get(id)
    db.session.delete(wps_to_delete)
    db.session.commit()
    return redirect(url_for('wps_list'))



@app.route("/edit_wps/<int:id>", methods=["GET", "POST"])
def edit_wps(id):
    if request.method == "POST":
        # UPDATE RECORD
        wps_to_update = wps_list.query.get(id)
        wps_to_update.Nr_wps = request.form['Numer WPS:']
        wps_to_update.Nr_rys = request.form['Numer rysunku:']
        wps_to_update.Nr_movex = request.form['Nr movex:']
        wps_to_update.opis = request.form['Opis:']
        wps_to_update.Group_of_material = request.form['Grupy materiałowe:']
        wps_to_update.Type_of_joint = request.form['Rodzaj złącza:']
        wps_to_update.welding_method = request.form['Metoda spawania:']
        wps_to_update.scope_of_thikness = request.form['Zakres grubości:']
        wps_to_update.wpqr = request.form['Numer WPQR:']
        wps_to_update.hiperlink = request.form['Hiperlink:']
        db.session.commit()
        return redirect(url_for('wps_list'))
    all_wps = wps_list.query.filter(wps_list.id.like(id))
    wps_id = id
    return render_template("edit_wps.html", titles=wps_titles_for_show, all=all_wps, wps_id = wps_id)

@app.route('/page-register',methods=["GET", "POST"])
def page_register():
    if request.method == "POST":
        hash_and_salted_password = generate_password_hash(
            request.form["password"],
            method='pbkdf2:sha256',
            salt_length=8)
        db.create_all()
        new_user = User(email=request.form['email'], password=hash_and_salted_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('page-register.html')

@app.route('/page-login', methods=['GET', 'POST'])
def page_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template("page-login.html", logged_in=current_user.is_authenticated)
    # return render_template('page-login.html')

@app.route('/forms-basic')
def forms_basic():
    return render_template('forms-basic.html')

@app.route('/forms-advanced')
def forms_advanced():
    return render_template('forms-advanced.html')





@app.route('/page-forget')
def page_forget():
    return render_template('pages-forget.html')

if __name__ == '__main__':
    app.run(debug=True)
