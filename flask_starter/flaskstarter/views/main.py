from flask import Blueprint, render_template, request, flash, redirect, url_for
from .. import app, db
from ..models import Probot
from ..forms import SelectProBotForm
from flask.ext.login import login_required
import json

main = Blueprint('main', __name__)



@app.route('/', methods=['GET', 'POST'])
def index():
	"""Index."""
	return render_template('index.html')
    
@app.route('/probots', methods=['GET', 'POST'])
@login_required
def probots():
		
	available_probot = True		#variable to control the HTML content, True: Shows the form 
								#False: Shows a message saying there aren't probots available
	
	form = SelectProBotForm(request.form)

	probots_available_q = Probot.query.filter_by(is_available=1).order_by('botname').all() #queries the database for available probots 
																						   #Returns a list	
	if probots_available_q == []:	#NO probots available
	
		available_probot = False
		
	else:							#At least one probot available

		form.probot.choices = [(probot.id, probot.botname+" "+"["+ str(probot.battery) +"%]") 
			for probot in probots_available_q]	#Fills the form with a radio button for each available probot

		if request.method == 'POST' and form.validate() == False:	#NO radio button checked
	
			form.probot.errors = ['You need to select one ProBot to continue']	#Shows an error in the form
		
		elif request.method == 'POST' and form.validate():			#ALL went good
		
			chosen_probot_id = form.probot.data		#Get chosen probot id from the form
			chosen_probot = Probot.query.filter_by(id = chosen_probot_id).first()			
			chosen_probot.is_available = False
			
			try:
				db.session.add(chosen_probot)
				db.session.commit()               
			except:			
				db.session.rollback()
				error_msg = 'Could not change the ProBot\'s availability'
				flash(error_msg, 'warning')
				raise
			finally:
				db.session.close()
			
			if request.user_agent.platform == ('android' or 'iphone' or 'ipad'):
				return render_template('botcontrolphone.html', chosen_probot_id=chosen_probot_id)				
			else:
				return render_template('botcontrol.html', chosen_probot_id=chosen_probot_id) #render the file with the probot control "console"

	return render_template('probots.html', form=form, available_probot=available_probot)

@app.route('/bridge', methods=['POST'])
def message():
    probot_id = None
    body = json.loads(request.get_data())
    print("args:", body["args"], "kwargs:", body["kwargs"])
    print(body["args"][0])  
    probot_id = int(body["args"][0])
    probot = Probot.query.filter_by(id = probot_id).first()			
    probot.is_available = True
    
    try:
        db.session.add(probot)
        db.session.commit()
        print("ProBot {} availability set to True".format(probot_id))
        probot_id = None               
    except:			
        db.session.rollback()
        print("Could not change ProBot {} availability".format(probot_id))
        probot_id = None
        raise
    finally:
        db.session.close()
        
    return b"OK"
