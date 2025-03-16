# import logging 
from math import e
import pdb

from ast import Sub
from pprint import pformat
from socket import send_fds
from typing import OrderedDict

from flask import (current_app, flash, get_flashed_messages, make_response,
                   redirect, render_template, request, session, url_for)
from flask.sessions import SessionInterface
from flask_login import current_user, login_required, login_user, logout_user
from flask_migrate import current
from itsdangerous import exc

from app.lib.util import paginate

# from app.forms import ForgotPasswordForm
from app.forms import LoginForm, ProductForm, ContactForm, OrderForm, OrderLineForm
# from app.lib.dashboard import Dashboard
from app.lib.exceptions import KoalatyException, RecordExistsException
from app.lib.dashboard.dashboard import Dashboard
from app.lib.contact import ContactSvc
from app.lib.order import OrderSvc
from app.lib.product import ProductSvc
# from app.models import Contact
from app.models.User import User

from werkzeug.datastructures import MultiDict, accept

#XXX
from wtforms import FormField, SelectField, SubmitField, IntegerField

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.propagate = True



class AuthController():

    @staticmethod
    def login():
        """
        Login page
        """

        form = LoginForm()
        if request.method == 'GET':
            return render_template('pages/auth/login.html', title='Login', form=form)
        else:
            if form.validate_on_submit():
                current_app.logger.error(form.data)

                email = form.data['email']
                password = form.data['password']

                user = User.query.filter_by(email=email).first()
                if user is None:
                    return render_template('pages/auth/login.html', 
                                           title='Login', 
                                           form=form, 
                                           message="User not found!")

                if user.check_password(password):
                    flash('Logged in successfully!','success')
                    login_user(user)
                    return redirect('/home')
                else:
                    flash('Invalid password','error')
                    current_app.logger.error(f'Invalid password')


            return render_template('pages/auth/login.html', 
                                   title='Login', 
                                   form=form, 
                                   message="Invalid credentials!")

#    def forgot_password():
#        """
#        Forgot password
#        """
#        form = ForgotPasswordForm()
#        if request.method == 'GET':
#            return render_template('pages/auth/forgot_password.html', title='Forgot Password', form=form)
#        else:
#            if form.validate_on_submit():
#                email = form.data['email']
#                user = User.query.filter_by(email=email).first()
#                if user is None:
#                    return render_template('pages/auth/forgot_password.html', title="Forgot Password", form=form, message="User not found!")
#                user.send_password_reset_email()
#                return render_template('pages/auth/forgot_password.html', title="Forgot Password", form=form, message="User not found!")
#            return render_template('pages/auth/forgot_password.html', title="Forgot Password", form=form, message="Invalid parameters!")

    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))

    @login_required
    def profile():
        data = {
            'title': 'Profile',
            'user': current_user
        }
        return render_template('pages/auth/profile.html', **data)

    @login_required
    def home():
        return redirect(url_for('auth.dashboard'))


    @login_required
    def dashboard():
        data = {
            'title': 'Dashboard',
            'orders': {}
        }

        # open_order_count = foo.open_orders_count()
        # current_app.logger.error(f'open orders: {open_order_count.open}')
        # data['orders']['open'] = open_order_count.open
        data['orders']['open'] = Dashboard.open_order_count().open

        # props: product, count, list of named tuples
        current_app.logger.error(f'open_order_count_by_product: \n{Dashboard.open_order_count_by_product()}')

        data['ooc_by_product'] = Dashboard.open_order_count_by_product()
        data['oo_product_qty'] = Dashboard.open_orders_product_qty()

        data['product_customer_mapping'] = Dashboard.products_to_customers()
        current_app.logger.error(f"product_to_customer: \n{data['product_customer_mapping']['product_to_customer']}")

        return render_template('pages/auth/dashboard.html', **data)

    
    @login_required
    def contacts():

        if not request.args.get('page'):
            return redirect(url_for('auth.contacts', page=1))

        data = {
            'title': 'Contacts',
            # default to 1st page 
            'page': request.args.get('page', 1),
            'paginate': paginate,
            'navs': 3
        }

        current_app.logger.debug(f'request args: {request.args}')

        data.update(
            ContactSvc.get_paginated(
                page=int(request.args.get('page', 1)), 
                order_by=ContactSvc.Model.last_name.desc(), page_size=5)) # pyright: ignore
        
        # window => number of 'page' links in the template  
        current_app.logger.debug(f'contacts data: \n{data}')

        return render_template('pages/auth/contacts.html', **data)



    @login_required
    def new_contact():

        if request.method == 'POST':
            current_app.logger.debug(f'new_contact: {pformat(request.form)}')
            try:
                c = ContactSvc.add_contact(request.form)
                flash(f'Contact {c.full_name} added!','success') # pyright: ignore
                current_app.logger.debug(f'new contact id: {c.id}, name: {c.full_name}') # pyright: ignore
                return redirect('/contacts')

            except RecordExistsException as e:
                current_app.logger.debug(f'RecordExists: {e}')
                fname = request.form.get("fname","missing")
                lname = request.form.get("lname","missing")
                flash(f'Contact "{fname} {lname}" exists','warning')
                session['contact_form'] = request.form
                return redirect('/new_contact')

            except KoalatyException as e:
                current_app.logger.error(f'KoalatyException: {e}')
                flash(f'Contact not added!','error')
                return redirect('/contacts')

        else:
            # formdata has to be a MultiDict, with getlist() method
            formdata = MultiDict(session.pop('contact_form', {}))
            form = ContactForm(formdata=formdata)
            return render_template('pages/auth/contact_form.html', title='New contact', form=form)


    @login_required
    def orders():

        if not request.args.get('page'):
            return redirect(url_for('auth.orders', page=1))

        data = {
            'title': 'Orders',
            'page': request.args.get('page', 1),
            'paginate': paginate,
            'navs': 3
        }

        current_app.logger.debug(f'model: {OrderSvc.Model}')

        data.update(
            OrderSvc.get_paginated(page_size=4,
                page=int(request.args.get('page', 1)), 
                                   order_by=OrderSvc.Model.order_date.desc())) # pyright: ignore
        
        current_app.logger.debug(f'data: \n{data}')

        return render_template('pages/auth/orders.html', **data)



    @login_required
    def new_order():

        # pdb.set_trace()
        current_app.logger.debug(f"OrderForm order_lines: {list(filter(lambda a: a.startswith('order_line_'),dir(OrderForm)))}")
        current_app.logger.debug(f'Session order_lines: {session.get("order_lines", "none")}')

        if request.method == 'POST':
            current_app.logger.debug(f'----------->request method: {request.method}')
            current_app.logger.debug(f'session: \n{pformat(session)}')
            current_app.logger.debug(f'order request.form: {pformat(request.form)}')
            try:
                # current_app.logger.debug(f'new_order post: \n{pformat(request.form)}')
                session['current_order'] = MultiDict(request.form)
                current_app.logger.debug(f'current_order: \n{pformat(dict(session.get("current_order","none")))}')
                
                # debug
                formdata = MultiDict(session.get('current_order', {}))
                current_app.logger.debug(f'form_data: {formdata}')
                form = OrderForm(formdata=formdata)

                return render_template('pages/auth/order_form.html', title='New order', form=form)

                # XXX XXX
                # after order is saved clear session['current_order'], session['order_lines']
                # and session['ol_id']

                # go back
                # return redirect('/orders')

            except RecordExistsException as e:
                #TODO
                current_app.logger.debug(f'RecordExists: {e}')
                fname = request.form.get("fname","missing")
                lname = request.form.get("lname","missing")
                flash(f'Order "{fname} {lname}" exists','warning')
                session['order_form'] = request.form
                return redirect('/new_order')

            except KoalatyException as e:
                current_app.logger.error(f'KoalatyException: {e}')
                flash(f'Order not added!','error')
                return redirect('/orders')

        else:
            current_app.logger.debug(f'----------->request method: {request.method}')
            current_app.logger.debug(f'-->session: {session}')
            current_app.logger.debug(f"session current_order (t/f): {session.get('current_order', False)}")
            current_app.logger.debug(f'current_order: \n{pformat(dict(session.get("current_order","none")))}')

            # pdb.set_trace()

            if session.get('current_order', False) == False:
            # new order
                # pdb.set_trace()
                current_app.logger.debug('New order')
                session['current_order'] = MultiDict()
                session['order_lines'] = list()
                form = OrderForm()
            else:
            # in-progress order
                current_app.logger.debug(f'Existing order')

                if 'order_lines' in session:                                
                    for ol in session['order_lines']: 
                        current_app.logger.debug(f'adding ol: {ol}')
                        OrderForm.add_order_line(name=ol)
                else:
                    session['order_lines'] = list()

                current_app.logger.debug(f'request.form: {request.form.to_dict()}')
                form = OrderForm(formdata=MultiDict(session['current_order']))


            current_app.logger.debug(f"OrderForm order_lines: {list(filter(lambda a: a.startswith('order_line_'),dir(OrderForm)))}")
            current_app.logger.debug(f'Session order_lines: {session.get("order_lines", "none")}')

            return render_template('pages/auth/order_form.html', title='New order', form=form)


    @login_required
    def add_order_line():

        # only POST

        current_app.logger.debug('add order_line')
        current_app.logger.debug(f'session: {session}')

        session['current_order'] = MultiDict(request.form)

        # new ol_id
        ol_id = session.get('ol_id', 0) + 1

        order_lines = session.get('order_lines', list())
        order_lines.append(f'order_line_{ol_id}')

        session['order_lines'] = order_lines
        session['ol_id'] = ol_id

        current_app.logger.debug(f'session: {session}')
        return redirect(url_for('auth.new_order'))


    @login_required
    def remove_order_line():
        # only POST
        try:
            order_lines = session['order_lines']

            # example button name 'order_line_2-remove'
            ol = ''

            # figure out for which order_line 'remove' button was clicked
            for k in request.form:
                if k.endswith('-remove'):
                    current_app.logger.debug(f'removed clicked: {k}')
                    ol = k.removesuffix('-remove')
                    break

            current_app.logger.debug(f'ol to be removed: {ol}')

            if ol in order_lines:
                order_lines.remove(ol)
                # remove field from the form
                OrderForm.remove_order_line(name=ol)
                session['order_lines'] = order_lines 
            else:
                current_app.logger.error(f'Order line {ol} not found in session["order_lines"]')
                current_app.logger.error(f'session: \n{session}')
                flash(f'Error removing order line','error')

        except KeyError:
            current_app.logger.error(f'KeyError when trying to access session["order_lines"]')
            current_app.logger.error(f'session: \n{session}')
            flash(f'Error removing order line','error')

        current_app.logger.debug(f'session: {session}')
        return redirect(url_for('auth.new_order'))

    @login_required
    def new_order_reset():

        OrderForm.remove_all_order_lines()

        session.pop('current_order', None)
        session.pop('order_lines', None)
        session.pop('ol_id', None)

        current_app.logger.debug(f'order reset, session: {session}')

        return redirect(url_for('auth.new_order'))



    @login_required
    def products():

        if not request.args.get('page'):
            return redirect(url_for('auth.products', page=1))

        data = {
            'title': 'Products',
            # default to 1st page 
            'page': request.args.get('page', 1),
            'paginate': paginate,
            'navs': 3
        }

        current_app.logger.debug(f'model: {ProductSvc.Model}')

        data.update(
            ProductSvc.get_paginated(page_size=5,
                page=int(request.args.get('page', 1)), 
                                   order_by=ProductSvc.Model.name)) # pyright: ignore
        
        current_app.logger.debug(f'data: \n{data}')

        return render_template('pages/auth/products.html', **data)



    @login_required
    def new_product():

        if request.method == 'POST':
            current_app.logger.debug(f'new_product: {pformat(request.form)}')
            try:
                # request.form
                p = ProductSvc.add_product(request.form)
                flash(f'Product {p.name} added!','success')
                current_app.logger.debug(f'new product id: {p.id}, name: {p.name}')
                return redirect('/products')
            except RecordExistsException as e:
                current_app.logger.debug(f'RecordExists: {e}')
                product_name = request.form.get("name","missing")
                flash(f'Product {product_name} exists','warning')
                session['prod_form'] = request.form
                return redirect('/new_product')
            except KoalatyException as e:
                current_app.logger.error(f'KoalatyException: {e}')
                flash(f'Product not added!','error')
                return redirect('/products')

        else:
            # formdata has to be a MultiDict, with getlist() method
            formdata = MultiDict(session.pop('prod_form', {}))
            form = ProductForm(formdata=formdata)
            return render_template('pages/auth/product_form.html', title='New product', form=form)


    @login_required
    def settings():
        data = {
            'title': 'Settings',
        }
        return render_template('pages/auth/settings.html', **data)
