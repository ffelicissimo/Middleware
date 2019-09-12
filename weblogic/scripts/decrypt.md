$DOMAIN_HOME/servers/<AdminServerName>/security

cd $DOMAIN_HOME/servers/AdminServer/security
cat boot.properties
 
#Tue Sep 05 14:05:32 CEST 2017
password={AES}hjP+5eQrx8j6S6b5JRdluvACHjtov3vo3pQ10c+h/Pg\=
username={AES}bHAMPwpk4izstmC7RW3K0jjQK4h4WlNEGu17LqRKYaE\=

Now start the script with your wlst.sh from $ORACLE_HOME/oracle_common/common/bin, provide your DOMAIN_HOME directory and provide the encrypted password.


$ORACLE_HOME/oracle_common/common/bin/wlst.sh decrypt.py
 
Initializing WebLogic Scripting Tool (WLST) ...
 
Welcome to WebLogic Server Administration Scripting Shell
 
Type help() for help on available commands
 
Provide Domain Home location: /u00/app/oracle/user_projects/domains/demo_domain
Provide encrypted password (e.g.: {AES}jNdVLr...): {AES}hjP+5eQrx8j6S6b5JRdluvACHjtov3vo3pQ10c+h/Pg\=
Make sure that nobody is staying behind you :-) Press ENTER to see the password ...
Value in cleartext is: Oracle12c
