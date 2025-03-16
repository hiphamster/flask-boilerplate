from datetime import datetime, timedelta
from flask import url_for
from flask_wtf import FlaskForm
# from wtforms.widgets import SubmitInput
from markupsafe import Markup
from sqlalchemy.sql.visitors import HasTraversalDispatch
from wtforms import (DateTimeField, IntegerField, SelectField, StringField, FormField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, NumberRange

from app.lib.contact import ContactSvc
from app.lib.product import ProductSvc


# from flask import current_app


class OrderLineForm(FlaskForm):

    product = SelectField(choices=ProductSvc.id_name_list)
    quantity = IntegerField(validators=[NumberRange(min=1)])
    remove = SubmitField('-', render_kw={'formaction':'/rm_order_line'})


class OrderForm(FlaskForm):

    order_date = DateTimeField(Markup('<strong>Order date</strong>'), default=datetime.now())

    due_date = DateTimeField(Markup('<strong>Due date</strong>'), default=datetime.now() + timedelta(days=7))

    # with current_app.app_context():
    # _choices = [(str(k),v) for (k,v) in ContactSvc.name_id_list().all()]

    contact = SelectField(Markup('<strong>Contact</strong>'), choices=ContactSvc.id_name_list) # pyright: ignore

    # prod1 = SelectField(choices=[('Trout','Trout'),('Salmon','Salmon')])
    # qty1 = IntegerField(validators=[NumberRange(min=1)])
    # rm1 = SubmitField('-')

    # order_line = FormField(OrderLineForm)

    notes = TextAreaField(Markup('<strong>Notes</strong>'))
    
    # '<i class="ti ti-square-plus"></i>'

    add_product = SubmitField('+')

    save_changes = SubmitField()
    discard_changes = SubmitField(render_kw={'formaction':'/new_order_reset'})


    #TODO handle KeyError

    @classmethod
    def add_order_line(cls, _id=None, name=None):
        if _id:
            setattr(cls, f'order_line_{_id}', FormField(OrderLineForm))
        elif name:
            setattr(cls, f'{name}', FormField(OrderLineForm))

    @classmethod
    def remove_order_line(cls, _id=None, name=None):
        
        _ol = '' 

        if _id:
            _ol = f'order_line_{_id}'
        elif name:
            _ol = name

        if hasattr(cls, _ol):
            delattr(cls, _ol)


    @classmethod
    def remove_all_order_lines(cls):
        for ol in filter(lambda attr: attr.startswith('order_line_'), dir(cls)):
            delattr(cls, ol)



