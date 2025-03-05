from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import (DecimalField, IntegerField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, NumberRange


class ProductForm(FlaskForm):
    name = StringField(Markup('<strong>Name</strong>'),
                       validators=[DataRequired()])

    desc = StringField(Markup('<strong>Description</strong>'),
                       validators=[DataRequired()])

    units = SelectField(Markup('<strong>Units</strong>'),
                        choices=[
                            ('POUNDS', 'lb'),
                            ('KILOGRAMS', 'kg'),
                            ('OUNCES', 'oz'),
                            ('GRAMS', 'g'),
                            ('EACH', 'ea'),
                        ],
                        default='OUNCES')

    avg_weight = IntegerField(Markup('<strong>Average weight</strong>'),
                              validators=[NumberRange(min=1)])

    unit_price = DecimalField(Markup('<strong>Unit price</strong>'),
                              validators=[NumberRange(min=1)])

    notes = TextAreaField(Markup('<strong>Notes</strong>'))

    submit = SubmitField('Save changes!')
