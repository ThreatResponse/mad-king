# MadKing Amazon Web Services Attack Platform

This project was created as a proof of concept.  A marriage of serverless
frameworks and the techniques of researcher Daniel Grzelak for persistance
in an AWS account.  

## Disclaimer

The word “Hack” or “Hacking” that is used on this site shall be regarded as “Ethical Hack” or “Ethical Hacking” respectively.

We do not promote hacking, software cracking and/or piracy.
All the information provided on this site are for educational purposes only.
The site or the authors are not responsible for any misuse of the information.
You shall not misuse the information to gain unauthorized access and/or write malicious programs.
These information shall only be used to expand knowledge and not for causing malicious or damaging attacks.
You may try all of these techniques on your own computer at your own risk.
Performing  any hack attempts/tests without written permission from the owner of the computer system is illegal.
Breaking into computer systems is illegal.

Basically:

1. Don't do bad things.
2. Don't use this for evil.  ( though it could be quite fun in an IR game day )

## How to use this

1. Clone the repository `git clone git@github.com:ThreatResponse/mad-king.git`
2. Set up a virtualenv in the directory.  `virtualenv .`
3. Activate `source bin/activate`
4. Install the requirements `pip install -r requirements.txt`
5. Setup a boto profile in your ~/.aws folder for the account you're "hacking"
6. zappa deploy production

You should get back a URL at the end of your APIGateway based pivot into the AWS account.

Winning!

## What just happened?

The magical framework (Zappa) turned my cobbled together flask app into a ton of APIGateway and lambda functions.
It also attached an innocuous looking role to this called "ComplianceRole1337".  This way if you get kicked out
of the AWS account you're "hacking" you can simply use APIGateway as a pivot back into the environment.  

## Features

1. Disable CloudTrails
2. Encrypt CloudTrails
3. Generate New Developer Access Keys
4. Stop Instances
5. Terminate Instances
6. Burn them all ( Destroy all instances ) -- _It's called MadKing for a reason._
