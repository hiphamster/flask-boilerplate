# import logging 
from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from app.controllers import paginate
# from app.forms import ForgotPasswordForm
from app.forms import LoginForm
from app.lib import contact
from app.lib.order import OrderSvc
from app.lib.product import ProductSvc
# from app.lib.dashboard import Dashboard
from app.lib.dashboard.dashboard import Dashboard
# from app.models import Contact
from app.models.User import User

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.propagate = True



class AuthController():

    @staticmethod
    def login():
        """
        Login page
        """

        current_app.logger.error('Foo')

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
                    return render_template('pages/auth/login.html', title='Login', form=form, message="User not found!")

                if user.check_password(password):
                    flash('Logged in successfully!')
                    login_user(user)
                    return redirect('/home')


            return render_template('pages/auth/login.html', title='Login', form=form, message="Invalid credentials!")

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
            # 'page': 1
            #XXX need to rename to 'navs' or
            #update paginate()XXX
            'page_nav_size': 3
        }

        current_app.logger.debug(f'request args: {request.args}')

        data.update(
            contact.Contact.get_paginated(
                page=int(request.args.get('page', 1)), page_size=5)
        )
        
        # window => number of 'page' links in the template  
        # data['pagination'] = paginate(pages=data['pages'], window=3)
        current_app.logger.debug(f'table: \n{data}')

        # logger.info('This should work!')
        # logger.debug('And this should work!')
        return render_template('pages/auth/contacts.html', **data)


    @login_required
    def orders():

        if not request.args.get('page'):
            return redirect(url_for('auth.orders', page=1))

        data = {
            'title': 'Orders',
            # default to 1st page 
            'page': request.args.get('page', 1),
            'paginate': paginate,
            # 'page': 1
            #XXX need to rename to 'navs' or
            #update paginate()XXX
            'page_nav_size': 3
        }

        current_app.logger.debug(f'model: {OrderSvc.Model}')

        data.update(
            OrderSvc.get_paginated(page_size=4,
                page=int(request.args.get('page', 1)), 
                                   order_by=OrderSvc.Model.order_date.desc()))
        
        # window => number of 'page' links in the template  
        # data['pagination'] = paginate(pages=data['pages'], window=3)
        current_app.logger.debug(f'data: \n{data}')

        return render_template('pages/auth/orders.html', **data)


    @login_required
    def products():

        if not request.args.get('page'):
            return redirect(url_for('auth.products', page=1))

        data = {
            'title': 'Products',
            # default to 1st page 
            'page': request.args.get('page', 1),
            'paginate': paginate,
            # 'page': 1
            #XXX need to rename to 'navs' or
            #update paginate()XXX
            'page_nav_size': 3
        }

        current_app.logger.debug(f'model: {ProductSvc.Model}')

        data.update(
            ProductSvc.get_paginated(page_size=5,
                page=int(request.args.get('page', 1)), 
                                   order_by=ProductSvc.Model.name))
        
        # window => number of 'page' links in the template  
        # data['pagination'] = paginate(pages=data['pages'], window=3)
        current_app.logger.debug(f'data: \n{data}')

        return render_template('pages/auth/products.html', **data)





















    @login_required
    def settings():
        data = {
            'title': 'Settings',
        }
        return render_template('pages/auth/settings.html', **data)
