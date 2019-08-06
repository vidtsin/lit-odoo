{
    "name": "Restrict Concurrent Users",
    "version": "1.0",
    "author" : "Top Gun",
    "website": "",
 	'price': 5.00,
	'currency': 'EUR',
    "category": "Concurrent Users Restrict",
    "description": """
This Module Restricts the number of concurrent users in the system at given time.By default 2 users are allowed to enter system.Admin/Superuser can enter system even if system has reached the concurrent users limit.To configure Number of users to restrict admin can find link in setting->Configure->Concurrent Users Setting.
===========
""",
    "summary": "Concurrent Users Restrict",
    "depends": [
    	'base',
    	'web',
	
    ],
    "data" : ['views/new_setting.xml'],
   'images': ['images/main_screenshot.png'],
    "installable": True,
}
