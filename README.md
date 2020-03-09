# Gmail_extractor
This repo was a bad week for me and taught me about the opportunity cost
## INTRODUCTION
This is a script using gmail api to interact with mail in your gmail with the instruction hhttps://developers.google.com/gmail/api/quickstart/python
The purpose of this action is to help someone in HNFWT to extract the tourist information without copying one by one
## Dependencies
1. google-api-python-client 
2. google-auth-httplib2 
3. google-auth-oauthlib
4. bs4
## HOW IT WORKS
Before running this script, the user should get the authentication by following 
the [Gmail API link](https://developers.google.com/gmail/api/quickstart/python)
Also, client_secret.json should be saved in the same directory as this file


The script outputs a dictionary in the following format:

```
{	'customer_name': '', 
	'country': '', 
	'Date': '', 
	'tour': ''
	'number': ''
  'phone number':''
  }
  ```



The dictionary can be exported as a .csv or into a databse

  python gmail_read.py
