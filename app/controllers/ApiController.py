# from app.jobs.TestJob import send_test_job
from flask import jsonify
from flask_login import login_required


class ApiController():


    @staticmethod
    @login_required
    def index():
        response_data = {
            'Salmon CS': 10,
            'Salmon HS': 12,
            'Trout HS': 21
        }

        return jsonify(response_data), 200


#    @staticmethod
#    def index_celery():
#        response_data = {
#            "foo": "bar",
#        }
#
#        message_data = {
#            'subject': 'Hello from the flask app!',
#            'body': 'This email was sent asynchronously using Celery.',
#            'recipients': "",
#
#        }
#        send_test_job.apply_async(args=[message_data])
#
#        return jsonify(response_data), 200
