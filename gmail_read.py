'''
Reading GMAIL using Python
	- Abhishek Chhibber
'''

'''
This script does the following:
- Go to Gmal inbox
- Find and read all the unread messages
- Extract details (Date, Sender, Subject, Snippet, Body) and export them to a .csv file / DB
- Mark the messages as Read - so that they are not read again 
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import json
import re

def gmail_api():
    # Creating a storage.JSON file with authentication details
	SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
	store = file.Storage('storage.json') 
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
	return GMAIL

def get_unread_message():
	# Getting all the unread messages from Inbox
	# labelIds can be changed accordingly
	unread_msgs = gmail_api().users().messages().list(userId='me',labelIds=[label_id_one, label_id_two],q=primary).execute()
	return unread_msgs

def extract_email():
	# We get a dictonary. Now reading values for the key 'messages'
	unread_mail=get_unread_message()
	mssg_list = unread_mail['messages']

	# print ("Total unread messages in inbox: ", str(len(mssg_list)))
	# print(mssg_list)
	guest_list = [ ]


	for mssg in mssg_list:
		temp_dict = { }
		field_dict= { }
		m_id = mssg['id'] # get id of individual message
		message = gmail_api().users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
		payld = message['payload'] # get payload of the message 
		headr = payld['headers'] # get header of the payload


		# for one in headr: # getting the Subject
		# 	if one['name'] == 'Subject':
		# 		msg_subject = one['value']
		# 		temp_dict['Subject'] = msg_subject
		# 	else:
		# 		pass


		# for two in headr: # getting the date
		# 	if two['name'] == 'Date':
		# 		msg_date = two['value']
		# 		date_parse = (parser.parse(msg_date))
		# 		m_date = (date_parse.date())
		# 		temp_dict['Date'] = str(m_date)
		# 	else:
		# 		pass

		# for three in headr: # getting the Sender
		# 	if three['name'] == 'From':
		# 		msg_from = three['value']
		# 		temp_dict['Sender'] = msg_from
		# 	else:
		# 		pass

		# temp_dict['Snippet'] = message['snippet'] # fetching message snippet


		try:
			
			# Fetching message body
			mssg_parts = payld['parts'] # fetching the message parts
			part_one  = mssg_parts[0] # fetching first element of the part 
			part_body = part_one['body'] # fetching body of the message
			part_data = part_body['data'] # fetching data from the body
			clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
			clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
			clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
			soup = BeautifulSoup(clean_two , "lxml" )
			mssg_body = soup.body()
			# mssg_body is a readible form of message body
			# depending on the end user's requirements, it can be further cleaned 
			# using regex, beautiful soup, or any other method
			main_content=str(mssg_body).replace('\r\nTour detail:','')
			main_content=re.sub('<.*?>','',main_content)
			elements=main_content.split('\r\n\r\n')[1:-1]
			guest_number=elements[7].split(',')
			for ele in elements:
				ele=ele.split(':')
				if len(ele)==2:
					field_dict[ele[0]]=ele[1]
			field_dict['guest_number']=elements[7]
			print(field_dict)
			# temp_dict['Message_body'] = main_content
		except :
			pass
		guest_list.append(field_dict)
		# final_list.append(temp_dict) # This will create a dictonary item in the final list
		# This will mark the messagea as read
		# gmail_api().users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
		return guest_list

'''

The final_list will have dictionary in the following format:

{	'Sender': '"email.com" <name@email.com>', 
	'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
	'Date': 'yyyy-mm-dd', 
	'Snippet': 'Lorem ipsum dolor sit amet'
	'Message_body': 'Lorem ipsum dolor sit amet'}


The dictionary can be exported as a .csv or into a databse
'''

#exporting the values as .csv
def to_csv():
	with open('CSV_NAME.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
		fieldnames = ["Start date","Name Customer","Phone","Email",'Country','Pickup address','Name tour ',"guest_number",'Starts at ']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
		writer.writeheader()
		for val in extract_email():
			writer.writerow(val)

        
if __name__=='__main__':
    json_file=open('/home/viethoang/web_crawler/Gmail-Api-through-Python/result.json','w+',encoding='utf-8')
    user_id =  'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'
    primary='in:inbox -category:{social promotions forums}'
    get_unread_message()
    guest_list=extract_email()
    json.dump(guest_list,json_file,ensure_ascii=False,indent=4)
    json_file.close()
    to_csv()