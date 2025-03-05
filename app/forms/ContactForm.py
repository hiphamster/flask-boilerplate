from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from markupsafe import Markup

STATES = [('AL', 'AL'), ('KY', 'KY'), ('OH', 'OH'), ('AK', 'AK'), ('LA', 'LA'),
          ('OK', 'OK'), ('AZ', 'AZ'), ('ME', 'ME'), ('OR', 'OR'), ('AR', 'AR'),
          ('MD', 'MD'), ('PA', 'PA'), ('AS', 'AS'), ('MA', 'MA'), ('PR', 'PR'),
          ('CA', 'CA'), ('MI', 'MI'), ('RI', 'RI'), ('CO', 'CO'), ('MN', 'MN'),
          ('SC', 'SC'), ('CT', 'CT'), ('MS', 'MS'), ('SD', 'SD'), ('DE', 'DE'),
          ('MO', 'MO'), ('TN', 'TN'), ('DC', 'DC'), ('MT', 'MT'), ('TX', 'TX'),
          ('FL', 'FL'), ('NE', 'NE'), ('TT', 'TT'), ('GA', 'GA'), ('NV', 'NV'),
          ('UT', 'UT'), ('GU', 'GU'), ('NH', 'NH'), ('VT', 'VT'), ('HI', 'HI'),
          ('NJ', 'NJ'), ('VA', 'VA'), ('ID', 'ID'), ('NM', 'NM'), ('VI', 'VI'),
          ('IL', 'IL'), ('NY', 'NY'), ('WA', 'WA'), ('IN', 'IN'), ('NC', 'NC'),
          ('WV', 'WV'), ('IA', 'IA'), ('ND', 'ND'), ('WI', 'WI'), ('KS', 'KS'),
          ('MP', 'MP'), ('WY', 'WY')]


class ContactForm(FlaskForm):

    fname = StringField(Markup('<strong>First name</strong>'),
                        validators=[DataRequired()])

    lname = StringField(Markup('<strong>Last name</strong>'),
                        validators=[DataRequired()])

    email = StringField(Markup('<strong>email</strong>'),
                        validators=[Email()])

    mobile_phone = StringField(Markup('<strong>Mobile phone</strong>'),
                               validators=[])

    street = StringField(Markup('<strong>Street</strong>'), validators=[])

    city = StringField(Markup('<strong>City</strong>'), validators=[])

    state = SelectField(Markup('<strong>State</strong>'),
                        choices=STATES,
                        default='CA')

    zipcode = StringField(Markup('<strong>Zip</strong>'), validators=[])

    fb_url = StringField(Markup('<strong>FB url</strong>'), validators=[])

    notes = TextAreaField(Markup('<strong>Notes</strong>'))

    submit = SubmitField('Save changes!')
