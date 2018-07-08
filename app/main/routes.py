from datetime import datetime
import json
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
#from guess_language import guess_language
from app import db
#from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.main.forms import EditSimpleElementForm, EditInstrumentForm, EditPersonForm, \
    EditLocationForm, EditOrganizationForm, EditEventForm, EditMusicalPieceForm, \
    EditActivityForm
from app.models import User, Profile, History, Event, Country, City, \
    InstrumentType, Instrument, Person, PremiereType, Location, Organization,\
    EventType, MusicalPiece, Activity
#from app.translate import translate
from app.main import bp


def list2csv(some_list):
    return ','.join(map(str, some_list)) 

@bp.route('/favicon.ico')
def hello():
    return redirect(url_for('static', filename='favicon.ico'), code=302)


@bp.before_app_request
def before_request():
    pass
#    if current_user.is_authenticated:
#        current_user.last_seen = datetime.utcnow()
#        db.session.commit()
#        g.search_form = SearchForm()
#    g.locale = str(get_locale())
    
def view_elements(dbmodel,elementsname,title):
    page = request.args.get('page', 1, type=int)
    elements = dbmodel.query.order_by(dbmodel.name.asc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('main.view_'+elementsname, title=title,page=elements.next_num) \
        if elements.has_next else None
    prev_url = url_for('main.view_'+elementsname, title=title, page=elements.prev_num) \
        if elements.has_prev else None
    return render_template('main/'+elementsname+'.html', title=title,
                           elements=elements.items, next_url=next_url,
                           prev_url=prev_url)
    
@bp.route('/view/countries')
@login_required
def view_countries():
    return view_elements(Country,'countries',_('Países'))

@bp.route('/view/eventtypes')
@login_required
def view_eventtypes():
    return view_elements(EventType,'eventtypes',_('Tipos de Eventos'))

@bp.route('/view/cities')
@login_required
def view_cities():
    return view_elements(City,'cities',_('Ciudades'))

@bp.route('/view/instrumenttypes')
@login_required
def view_instrumenttypes():
    return view_elements(InstrumentType,'instrumenttypes',_('Tipos de Instrumento'))

@bp.route('/view/premieretypes')
@login_required
def view_premieretypes():
    return view_elements(PremiereType,'premieretypes',_('Tipos de Premier'))

@bp.route('/view/instruments')
@login_required
def view_instruments():
    return view_elements(Instrument,'instruments',_('Instrumentos'))

@bp.route('/view/activities')
@login_required
def view_activities():
    return view_elements(Activity,'activities',_('Actividades'))

@bp.route('/view/musicalpieces')
@login_required
def view_musicalpieces():
    return view_elements(MusicalPiece,'musicalpieces',_('Obras Musicales'))

@bp.route('/view/locations')
@login_required
def view_locations():
    return view_elements(Location,'locations',_('Lugares'))

@bp.route('/view/organizations')
@login_required
def view_organizations():
    return view_elements(Organization,'organizations',_('Organizaciones'))


@bp.route('/view/people')
@login_required
def view_people():
    elementsname='people'
    title=_('Personas')
    page = request.args.get('page', 1, type=int)
    elements = Person.query.order_by(Person.last_name.asc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('main.view_'+elementsname, title=title,page=elements.next_num) \
        if elements.has_next else None
    prev_url = url_for('main.view_'+elementsname, title=title, page=elements.prev_num) \
        if elements.has_prev else None
    return render_template('main/'+elementsname+'.html', title=title,
                           elements=elements.items, next_url=next_url,
                           prev_url=prev_url)


def getItemList(dbmodel,q,page):    
    itemslist=db.session.query(dbmodel).filter(dbmodel.name.ilike(q+'%')).order_by(dbmodel.name.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    data={ "results": [], "pagination": { "more": itemslist.has_next} }
    for item in itemslist.items:
        data["results"].append( { 'id' : item.id , 'text': item.name} )
    return jsonify(data)

def getItem(dbmodel,id):
    item=dbmodel.query.filter_by(id=id).first_or_404()
    data={ 'id' : item.id , 'text': item.name }
    return jsonify(data)

def getPeople(q,page):    
    itemslist=db.session.query(Person).filter(Person.last_name.ilike(q+'%')).order_by(Person.last_name.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    data={ "results": [], "pagination": { "more": itemslist.has_next} }
    for item in itemslist.items:
        text = '{}, {}'.format(item.last_name,item.first_name) if item.last_name else item.first_name
        data["results"].append( { 'id' : item.id , 'text': text } )
    return jsonify(data)

def getPerson(id):
    item=Person.query.filter_by(id=id).first_or_404()
    text = '{}, {}'.format(item.last_name,item.first_name) if item.last_name else item.first_name
    data={ 'id' : item.id , 'text': text }
    return jsonify(data)



@bp.route('/list/people')
def getPeopleList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getPeople(q,page)

@bp.route('/list/people/<id>')
def getPeopleItem(id):
    return getPerson(id)

@bp.route('/list/countries')
def getCountryList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(Country,q,page)

@bp.route('/list/countries/<id>')
def getCountryItem(id):
    return getItem(Country,id)


@bp.route('/list/eventtypes')
def getEventTypeList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(EventType,q,page)

@bp.route('/list/eventtypes/<id>')
def getEventTypeItem(id):
    return getItem(EventType,id)

@bp.route('/list/cities')
def getCityList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(City,q,page)

@bp.route('/list/cities/<id>')
def getCityItem(id):
    return getItem(City,id)

@bp.route('/list/organizations')
def getOrganizationList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(Organization,q,page)

@bp.route('/list/organizations/<id>')
def getOrganizationItem(id):
    return getItem(Organization,id)

@bp.route('/list/instrumenttypes')
def getInstrumentTypeList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(InstrumentType,q,page)

@bp.route('/list/instrumenttypes/<id>')
def getInstrumentTypeItem(id):
    return getItem(InstrumentType,id)

@bp.route('/list/instruments')
def getInstrumentList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(Instrument,q,page)

@bp.route('/list/instruments/<id>')
def getInstrumentItem(id):
    return getItem(Instrument,id)

@bp.route('/list/musicalpieces')
def getMusicalPieceList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(MusicalPiece,q,page)

@bp.route('/list/mmusicalpieces/<id>')
def getMusicalPieceItem(id):
    return getItem(MusicalPiece,id)

@bp.route('/list/locations')
def getLocationList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(Location,q,page)

@bp.route('/list/locations/<id>')
def getLocationItem(id):
    return getItem(Location,id)

@bp.route('/list/activities')
def getActivityList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(Activity,q,page)

@bp.route('/list/activities/<id>')
def getActivityItem(id):
    return getItem(Activity,id)


@bp.route('/list/premieretypes')
def getPremiereTypeList():
    page = request.args.get('page', 1, type=int)
    q=request.args.get('q', '', type=str)
    return getItemList(PremiereType,q,page)

@bp.route('/list/premieretypes/<id>')
def getPremiereTypeItem(id):
    return getItem(PremiereType,id)


def EditSimpleElement(dbmodel,title,original_name):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    db_element = dbmodel.query.filter_by(name=original_name).first_or_404()
    form = EditSimpleElementForm(dbmodel=dbmodel,original_name=original_name)
    if form.validate_on_submit():
        db_element.name = form.name.data
        db.session.commit()
        flash(_('Tus cambios han sido guardados.'))
        return redirect(url_for('main.edit_elements'))
    elif request.method == 'GET':
        form.name.data = original_name
    return render_template('main/edit_simple_element.html',title=title,form=form)


@bp.route('/edit/country/<country>',methods = ['GET','POST'])
@login_required
def EditCountry(country):
    return EditSimpleElement(Country,_('Editar País'),country)


@bp.route('/edit/eventtype/<event_type>',methods = ['GET','POST'])
@login_required
def EditEventType(event_type):
    return EditSimpleElement(EventType,_('Editar Tipo de Evento'),event_type)

 
@bp.route('/edit/city/<city>',methods = ['GET','POST'])
@login_required
def EditCity(city):
    return EditSimpleElement(City,_('Editar Ciudad'),city)


@bp.route('/edit/instrumenttype/<instrumenttype>',methods = ['GET','POST'])
@login_required
def EditInstrumentType(instrumenttype):
    return EditSimpleElement(InstrumentType,_('Editat Tipo de Instrumento'),instrumenttype) 

@bp.route('/edit/premieretype/<premieretype>',methods = ['GET','POST'])
@login_required
def EditPremiereType(premieretype):
    return EditSimpleElement(PremiereType,_('Editat Tipo de Instrumento'),premieretype) 

def NewSimpleElement(dbmodel,title):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditSimpleElementForm(dbmodel=dbmodel,original_name='')   
    if form.validate_on_submit():
        if  dbmodel.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
        else:
            db.session.add(dbmodel(name=form.name.data))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.')) 
        return redirect('/editelements')
    return render_template('main/edit_simple_element.html',title=title,form=form)
 
@bp.route('/new/country', methods = ['GET','POST'])
@login_required
def NewCountry():
    return NewSimpleElement(Country,_('Agregar País'))

@bp.route('/new/eventtype', methods = ['GET','POST'])
@login_required
def NewEventType():
    return NewSimpleElement(EventType,_('Agregar Tipo de Evento'))

@bp.route('/new/city', methods = ['GET','POST'])
@login_required
def NewCity():
    return NewSimpleElement(City,_('Agregar Ciudad'))

@bp.route('/new/instrumenttype', methods = ['GET','POST'])
@login_required
def NewInstrumentType():
    return NewSimpleElement(InstrumentType,_('Agregar Tipo de Instrumento'))
    
@bp.route('/new/premieretype', methods = ['GET','POST'])
@login_required
def NewPremiereType():
    return NewSimpleElement(PremiereType,_('Agregar Tipo de Premiere'))

@bp.route('/editelements')
@login_required
def edit_elements():
    return render_template('main/edit_elements.html')    

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  return redirect(url_for('users.edit_profile'))


@bp.route('/new/instrument', methods = ['GET','POST'])
@login_required
def NewInstrument():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditInstrumentForm(dbmodel=Instrument,original_name='')   
    if form.validate_on_submit():
        if  Instrument.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editinstrument.html',form=form,title=_('Agregar Instrumento'),selectedElements=None)
        else:
            instrument_type = InstrumentType.query.filter_by(id=int(form.instrument_type.data[0])).first_or_404()
            db.session.add(Instrument(name=form.name.data,instrument_type=instrument_type))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editinstrument.html',form=form,title=_('Agregar Instrumento'),selectedElements=None)

@bp.route('/edit/instrument/<instrument>', methods = ['GET','POST'])
@login_required
def EditInstrument(instrument):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    instrument = Instrument.query.filter_by(name=instrument).first_or_404()
    selectedElements=[]
    selectedElements.append(instrument.instrument_type.id)
    form = EditInstrumentForm(original_name=instrument.name)
    if form.validate_on_submit():
         instrument.name = form.name.data
         instrument_type = InstrumentType.query.filter_by(id=int(form.instrument_type.data[0])).first_or_404()
         instrument.instrument_type = instrument_type
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
        form.name.data = instrument.name            
    return render_template('main/editinstrument.html',form=form,title=_('Editar Instrumento'),selectedElements=list2csv(selectedElements))    

@bp.route('/new/musicalpiece', methods = ['GET','POST'])
@login_required
def NewMusicalPiece():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditMusicalPieceForm(dbmodel=MusicalPiece,original_name='')   
    if form.validate_on_submit():
        if  MusicalPiece.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editmusicalpiece.html',form=form,title=_('Agregar Obra Musical'),selectedElements=None)
        else:
            composer = Person.query.filter_by(id=int(form.composer.data[0])).first_or_404()
            db.session.add(MusicalPiece(name=form.name.data,composer=composer,composition_year=form.composition_year.data))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editmusicalpiece.html',form=form,title=_('Agregar Obra Musical'),selectedElements=None)

@bp.route('/edit/musicalpiece/<id>', methods = ['GET','POST'])
@login_required
def EditMusicalPiece(id):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    musical_piece = MusicalPiece.query.filter_by(id=id).first_or_404()
    selectedElements=[]
    selectedElements.append(musical_piece.composer.id)
    form = EditMusicalPieceForm(original_name=musical_piece.name)
    if form.validate_on_submit():
         musical_piece.name = form.name.data
         composer = Person.query.filter_by(id=int(form.composer.data[0])).first_or_404()
         musical_piece.composer = composer
         musical_piece.composition_year = form.composition_year.data
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
        form.name.data = musical_piece.name  
        form.composition_year.data = musical_piece.composition_year
    return render_template('main/editmusicalpiece.html',form=form,title=_('Editar Obra Musical'),selectedElements=list2csv(selectedElements))    


@bp.route('/new/activity', methods = ['GET','POST'])
@login_required
def NewActivity():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditActivityForm(dbmodel=Instrument,original_name='')   
    if form.validate_on_submit():
        if  Activity.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editactivity.html',form=form,title=_('Agregar Actividad'),selectedElements=None)
        else:
            instrument = Instrument.query.filter_by(id=int(form.instrument.data[0])).first_or_404()
            db.session.add(Activity(name=form.name.data,instrument=instrument))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editactivity.html',form=form,title=_('Agregar Actividad'),selectedElements=None)

@bp.route('/edit/activity/<id>', methods = ['GET','POST'])
@login_required
def EditActivity(id):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    original_activity= Activity.query.filter_by(id=id).first_or_404()
    selectedElements=[]
    selectedElements.append(original_activity.instrument.id)
    form = EditActivityForm(original_name=original_activity.name)
    if form.validate_on_submit():
         original_activity.name = form.name.data
         instrument = Instrument.query.filter_by(id=int(form.instrument.data[0])).first_or_404()
         original_activity.instrument = instrument
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
        form.name.data = original_activity.name
    return render_template('main/editactivity.html',form=form,title=_('Editar Actividad'),selectedElements=list2csv(selectedElements))    



@bp.route('/new/location', methods = ['GET','POST'])
@login_required
def NewLocation():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditLocationForm(dbmodel=Instrument,original_name='')   
    if form.validate_on_submit():
        if  Location.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editlocation.html',form=form,title=_('Agregar Lugar'),selectedElements=None)
        else:
            city = City.query.filter_by(id=int(form.city.data[0])).first_or_404()
            db.session.add(Location(name=form.name.data,city=city,additional_info=form.additional_info.data,address=form.address.data))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editlocation.html',form=form,title=_('Agregar Lugar'),selectedElements=None)

@bp.route('/edit/location/<location>', methods = ['GET','POST'])
@login_required
def EditLocation(location):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    original_location = Location.query.filter_by(name=location).first_or_404()
    selectedElements=[]
    selectedElements.append(original_location.city.id)
    form = EditLocationForm(original_name=location)
    if form.validate_on_submit():
         original_location.name = form.name.data
         original_location.additional_info=form.additional_info.data
         original_location.address=form.address.data
         city = City.query.filter_by(id=int(form.city.data[0])).first_or_404()
         original_location.city = city
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
        form.name.data = original_location.name
        form.additional_info.data = original_location.additional_info
        form.address.data = original_location.address
    return render_template('main/editlocation.html',form=form,title=_('Editar Lugar'),selectedElements=list2csv(selectedElements))    

@bp.route('/new/organization', methods = ['GET','POST'])
@login_required
def NewOrganization():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditOrganizationForm(dbmodel=Organization,original_name='')   
    if form.validate_on_submit():
        if  Organization.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editorganization.html',form=form,title=_('Agregar Organización'))
        else:
            db.session.add(Organization(name=form.name.data,additional_info=form.additional_info.data))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editorganization.html',form=form,title=_('Agregar Organización'))

@bp.route('/edit/organization/<organization>', methods = ['GET','POST'])
@login_required
def EditOrganization(organization):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    original_organization =Organization.query.filter_by(name=organization).first_or_404()
    form = EditOrganizationForm(original_name=organization)
    if form.validate_on_submit():
         original_organization.name = form.name.data
         original_organization.additional_info=form.additional_info.data
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
        form.name.data = original_organization.name
        form.additional_info.data = original_organization.additional_info
    return render_template('main/editorganization.html',form=form,title=_('Editar Organización'))    


@bp.route('/new/person', methods = ['GET','POST'])
@login_required
def NewPerson():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditPersonForm(original_person=None)   
    if form.validate_on_submit():
        person = Person(first_name=form.first_name.data,last_name=form.last_name.data)
        person.birth_date = form.birth_date.data
        person.death_date = form.death_date.data
        person.biography= form.biography.data
        for country_id in form.nationalities.data:
            person.nationalities.append(Country.query.filter_by(id=country_id).first_or_404())
        db.session.add(person)
        db.session.commit()
        flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editperson.html',form=form,title=_('Agregar Persona'),selectedElements=None)

@bp.route('/edit/person/<person_id>', methods = ['GET','POST'])
@login_required
def EditPerson(person_id):
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    person = Person.query.filter_by(id=person_id).first_or_404()
    form = EditPersonForm(person)
    selectedElements=[]
    for nationality in person.nationalities:
        selectedElements.append(nationality.id)
    if form.validate_on_submit():
         person.first_name = form.first_name.data
         person.last_name = form.last_name.data
         person.birth_date = form.birth_date.data
         person.death_date = form.death_date.data
         person.biography= form.biography.data
         person.nationalities.clear()
         for country_id in form.nationalities.data:
             person.nationalities.append(Country.query.filter_by(id=country_id).first_or_404())
         db.session.commit()
         flash(_('Tus cambios han sido guardados.'))
         return redirect('/editelements')
    elif request.method == 'GET':
         form.first_name.data = person.first_name
         form.last_name.data = person.last_name
         form.birth_date.data = person.birth_date
         form.death_date.data = person.death_date
         form.biography.data = person.biography
    return render_template('main/editperson.html',form=form,title=_('Editar Persona'),selectedElements=list2csv(selectedElements))    


@bp.route('/new/event', methods = ['GET','POST'])
@login_required
def NewEvent():
    if (current_user.profile.name != 'Administrador' and  current_user.profile.name != 'Editor'):
        flash(_('Debe ser Administrador/Editor para entrar a esta página'))
        return render_template(url_for('users.login'))
    form = EditEventForm(dbmodel=Event,original_event=None)   
    if form.validate_on_submit():
        if  Event.query.filter_by(name=form.name.data).all().__len__() > 0:
            flash(_('Este nombre ya ha sido registrado'))
            return render_template('main/editevent.html',form=form,title=_('Agregar Evento'),selectedElements=None)
        else:
            location = Location.query.filter_by(id=int(form.location.data[0])).first_or_404()
            organization = Organization.query.filter_by(id=int(form.organization.data[0])).first_or_404()
            event_type = EventType.query.filter_by(id=int(form.event_type.data[0])).first_or_404()
            db.session.add(Event(name=form.name.data,
                                 organization=organization,
                                 location=location,
                                 event_type=event_type,
                                 information=form.information.data,
                                 date=form.event_date.data))
            db.session.commit()
            flash(_('Tus cambios han sido guardados.'))
        return redirect('/editelements')
    return render_template('main/editevent.html',form=form,title=_('Agregar Evento'),selectedElements=None)


#
@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date.desc.desc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=events.next_num) \
        if events.has_next else None
    prev_url = url_for('main.explore', page=events.prev_num) \
        if events.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=events.items, next_url=next_url,
                           prev_url=prev_url)

#
#@bp.route('/user/<username>')
#@login_required
#def user(username):
#    user = User.query.filter_by(username=username).first_or_404()
#    page = request.args.get('page', 1, type=int)
#    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
#        page, current_app.config['POSTS_PER_PAGE'], False)
#    next_url = url_for('main.user', username=user.username,
#                       page=posts.next_num) if posts.has_next else None
#    prev_url = url_for('main.user', username=user.username,
#                       page=posts.prev_num) if posts.has_prev else None
#    return render_template('user.html', user=user, posts=posts.items,
#                           next_url=next_url, prev_url=prev_url)
#
#
#@bp.route('/edit_profile', methods=['GET', 'POST'])
#@login_required
#def edit_profile():
#    form = EditProfileForm(current_user.username)
#    if form.validate_on_submit():
#        current_user.username = form.username.data
#        current_user.about_me = form.about_me.data
#        db.session.commit()
#        flash(_('Your changes have been saved.'))
#        return redirect(url_for('main.edit_profile'))
#    elif request.method == 'GET':
#        form.username.data = current_user.username
#        form.about_me.data = current_user.about_me
#    return render_template('edit_profile.html', title=_('Edit Profile'),
#                           form=form)
#
#
#@bp.route('/follow/<username>')
#@login_required
#def follow(username):
#    user = User.query.filter_by(username=username).first()
#    if user is None:
#        flash(_('User %(username)s not found.', username=username))
#        return redirect(url_for('main.index'))
#    if user == current_user:
#        flash(_('You cannot follow yourself!'))
#        return redirect(url_for('main.user', username=username))
#    current_user.follow(user)
#    db.session.commit()
#    flash(_('You are following %(username)s!', username=username))
#    return redirect(url_for('main.user', username=username))
#
#
#@bp.route('/unfollow/<username>')
#@login_required
#def unfollow(username):
#    user = User.query.filter_by(username=username).first()
#    if user is None:
#        flash(_('User %(username)s not found.', username=username))
#        return redirect(url_for('main.index'))
#    if user == current_user:
#        flash(_('You cannot unfollow yourself!'))
#        return redirect(url_for('main.user', username=username))
#    current_user.unfollow(user)
#    db.session.commit()
#    flash(_('You are not following %(username)s.', username=username))
#    return redirect(url_for('main.user', username=username))
#
#
#@bp.route('/translate', methods=['POST'])
#@login_required
#def translate_text():
#    return jsonify({'text': translate(request.form['text'],
#                                      request.form['source_language'],
#                                      request.form['dest_language'])})
#
#
#@bp.route('/search')
#@login_required
#def search():
#    if not g.search_form.validate():
#        return redirect(url_for('main.explore'))
#    page = request.args.get('page', 1, type=int)
#    posts, total = Post.search(g.search_form.q.data, page,
#                               current_app.config['POSTS_PER_PAGE'])
#    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
#        if total > page * current_app.config['POSTS_PER_PAGE'] else None
#    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
#        if page > 1 else None
#    return render_template('search.html', title=_('Search'), posts=posts,
#                           next_url=next_url, prev_url=prev_url)
