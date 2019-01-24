# -*- coding: utf-8 -*-
import sys

def verJava():
        while True:
                try:
                        varJAVA=int(raw_input('Informe a versão de java \n 1 -> para JDK \n 2 -> para Jrockit \n--> '))
                except Exception:
                        print 'Informe 1 ou 2 para a versão do Java\n\n'
                        continue
                else:
                        if varJAVA == 1 or varJAVA == 2:
                                break
                        else:
                                print 'Informe 1 ou 2 para a versão do java\n\n'
                                continue
        return varJAVA

def verFSDump():
        while True:
                try:
                        varDump=raw_input('Informe se o ambiente possui FS de Dumps montado:\nS -> Sim \nN -> Não \n --> ')
                except Exception:
                        print '\nInforme S ou N\n\n'
                        continue
                else:
                        if varDump == 'S' or varDump == 'N':
                                print '\nParametro '+ varDump + '\n'
                                break
                        else:
                                print '\nInforme S ou N \n\n'
       		                continue
	return varDump

def salvarAlter():
        while True:
                try:
                        varSalvar=raw_input('Deseja salvar/ativar as alterações?:\nS -> Sim \nN -> Não \n --> ')
                except Exception:
                        print '\nInforme S ou N\n\n'
                        continue
                else:
                        if varSalvar == 'S':
                                save()
				activate()
                                break
			elif varSalvar =='N':
				cancelEdit()
				break
                        else:
                                print '\nInforme S ou N \n\n'
                                continue
        return

#######AJUSTE DE JVM#########
def ajustaVM():
    
	varJAVA = verJava()
	varDump = verFSDump()
	raw_input('==> FEZ BACKUP DA PASTA CONFIG?\nSenão saia da execução dando Control+C ou Enter pra continuar\n')

	connect(url=varAdminUrl)

	edit()
	startEdit()

	vasServers = cmo.getServers()
	varAdmin=cmo.getAdminServerName()
	varDomain=cmo.getName()

	varHeapHS=" -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/opt/web/dumps"
	varSelfTun = " -Dweblogic.SelfTuningThreadPoolSizeMin=150"
	varEntr=" -Djava.security.egd=file:/dev/./urandom"

	#ServerName > Logging > General
	cd('/Servers/' + varAdmin + '/Log/' + varAdmin)
	cmo.setFileMinSize(65000)
	cmo.setFileName('/opt/web/logs/' + varDomain + '/' + varAdmin + '/' + varAdmin + '.log')
	cmo.setRotateLogOnStartup(true)
	cmo.setLoggerSeverity('Warning')
	cmo.setDomainLogBroadcastSeverity('Warning')
	cmo.setLogFileSeverity('Warning')
	cmo.setStdoutSeverity('Warning')
	cmo.setMemoryBufferSeverity('Warning')

	#ServerName > Logging > Http
	cd('/Servers/' + varAdmin + '/WebServer/' + varAdmin + '/WebServerLog/' + varAdmin)
	cmo.setRotateLogOnStartup(true)
	cmo.setFileMinSize(1500)
	cmo.setFileName('/opt/web/logs/' + varDomain + '/' + varAdmin + '/access.log')
	cmo.setLogFileFormat('extended')
	cmo.setELFFields('c-ip date time cs-method cs-uri sc-status bytes time-taken')

	for server in vasServers:
	    	#Nao altera configuracao do serverAdmin"
		vasServerName = server.getName()
		if vasServerName == varAdmin:
       			continue
		#Domain > Logging
		cd('/Log/' + varDomain)
		cmo.setFileMinSize(65000)
		cmo.setRotateLogOnStartup(true)

		#ServerName > Logging > Genera
		cd('/Servers/' + vasServerName + '/Log/' + vasServerName)
		cmo.setFileMinSize(65000)
		cmo.setFileName('/opt/web/logs/' + varDomain + '/' + vasServerName + '/' + vasServerName + '.log')
		cmo.setRotateLogOnStartup(true)
		cmo.setLoggerSeverity('Warning')
		cmo.setNumberOfFilesLimited(true)
		cmo.setFileCount(7)
		cmo.setDomainLogBroadcastSeverity('Warning')
		cmo.setLogFileSeverity('Warning')
		cmo.setStdoutSeverity('Warning')
		cmo.setMemoryBufferSeverity('Warning')

		#ServerName > Logging > Http
		cd('/Servers/' + vasServerName + '/WebServer/' + vasServerName + '/WebServerLog/' + vasServerName)
		cmo.setFileName('/opt/web/logs/' + varDomain + '/' + vasServerName + '/access.log')
		cmo.setRotateLogOnStartup(true)
		cmo.setFileMinSize(1500)
		cmo.setNumberOfFilesLimited(true)
		cmo.setFileCount(7)
		cmo.setLogFileFormat('extended')
		cmo.setELFFields('c-ip date time cs-method cs-uri sc-status bytes time-taken')

		#Ajuste de SharedCapacityForWorkManagers
		cd('/Servers/' + vasServerName + '/OverloadProtection/' + vasServerName)
		cmo.setSharedCapacityForWorkManagers(500)

		#ServerName > Configuration > Server Start
		cd('/Servers/' + vasServerName + '/ServerStart/' + vasServerName)
		cmo.setBeaHome('/opt/web/wl/wls1036')
		#cmo.setJavaHome('/opt/web/jdk/jrockit')
		#cmo.setJavaVendor('Oracle')
		#cmo.setRootDirectory('/opt/web/domains')
		cmo.setRootDirectory('/opt/web/domains/' + varDomain)
		varArg=cmo.getArguments()
		if varArg.find('Djava.security.egd') > 0:
			print vasServerName + 'já possui Entropia '
		else:
			cmo.setArguments(varArg + varEntr)
			varArg=cmo.getArguments()
		if varArg.find('SelfTuningThreadPoolSizeMin') > 0:
			print vasServerName + ' já possui SelfTuningThreadPoolSizeMin '
		else:
			cmo.setArguments(varArg + varSelfTun)
			varArg=cmo.getArguments()
		if varArg.find('HeapDump') > 0:
       			print vasServerName + ' já possui Parâmetro de HeapDump '
		elif varDump == 'S':
			cmo.setArguments(varArg + varHeapHS)
       			varArg=cmo.getArguments()
	    	#else:
			#continue
		if varArg.find('Xloggc') > 0 and varArg.find('-verbose') > 0 or varArg.find('-Xverboselog') > 0 and varArg.find('-Xverbose') > 0:
       			print vasServerName + ' já possui parâmetro de GC '
		elif varJAVA == 1:
			#raw_input=('Chegou até aqui ') + str(varJAVA)
       			varGCColeta=" -verbose:opt,memory,gc,gcpause,gcreport,compaction -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=99 -XX:GCLogFileSize=10m -Xloggc:/opt/web/logs/coleta/" + vasServerName + ".log"
	       		cmo.setArguments(varArg + varGCColeta)
			varArg=cmo.getArguments()
		elif varJAVA == 2:
			varGCColeta=" -Xverbose:opt,memory,gc,gcpause,gcreport,compaction -Xverboselog:/opt/web/logs/coleta/" + vasServerName + ".log -Xverify:none -Xverbosetimestamp"
			cmo.setArguments(varArg + varGCColeta)
			varArg=cmo.getArguments()
	salvarAlter()
	disconnect()
	return

###########AJUSTE DE DATASOURCE########
def ajustaDS():
	connect(url=varAdminUrl)
	domainConfig()
	domainName = cmo.getName()
	edit()
	startEdit()
	cd("/")
	cd("JDBCSystemResources")
	allJDBCResources = cmo.getJDBCSystemResources()
	cd("/")
	for jdbcResource in allJDBCResources:
        	try:
         	   	cd('/JDBCSystemResources/' + jdbcResource.getName() + '/JDBCResource/' + jdbcResource.getName() + '/JDBCConnectionPoolParams/' + jdbcResource.getName())
        	except Exception:
            		print 'erro ao acessar ds ' + jdbcResource.getName()
	       	cmo.setTestConnectionsOnReserve(true)
        	cmo.setShrinkFrequencySeconds(120)
        	cmo.setTestFrequencySeconds(120)
        	cmo.setTestTableName('SQL BEGIN NULL; END;')
        	varCRS=cmo.getConnectionCreationRetryFrequencySeconds()
        	if varCRS > 0 and varCRS <=300:
               		print "----> Connection Retry do " + jdbcResource.getName() + " está ok"
        	else:
               		print "----> Ajustando Connection Retry para 300 do " + jdbcResource.getName()
               		cmo.setConnectionCreationRetryFrequencySeconds(300)
	       	varHNW=cmo.getHighestNumWaiters()
	       	if varHNW < 30:
                	print "----> HighestNumWaiters do " + jdbcResource.getName() + " está ok"
        	else:
               		print "----> AjustandoHighestNumWaiters do " + jdbcResource.getName()
               		cmo.setHighestNumWaiters(30)
	       	varICTS=cmo.getInactiveConnectionTimeoutSeconds()
        	if varICTS > 0 and varICTS <= 120:
               		print "----> InactiveConnectionTimeout do " + jdbcResource.getName() + " está ok"
        	else:
               		print "----> Ajustando InactiveConnectionTimeout do " + jdbcResource.getName()
               		cmo.setInactiveConnectionTimeoutSeconds(120)
  	      	varSTOut=cmo.getStatementTimeout()
        	if varSTOut != -1:
               		print "----> Statement Timeout configurado"
        	else:
               		print "----> Ajustando Statement Timeout do " + jdbcResource.getName()
        		cmo.setStatementTimeout(120)
       		cd('/JDBCSystemResources/' + jdbcResource.getName() + '/JDBCResource/' + jdbcResource.getName() + '/JDBCDriverParams/' + jdbcResource.getName() + '/Properties/' + jdbcResource.getName() + '/Properties')
        	try:
       	        	cmo.createProperty('oracle.net.CONNECT_TIMEOUT')
               		cd('oracle.net.CONNECT_TIMEOUT')
               		cmo.setValue('5000')
        	except Exception:
       	        	cd ('/JDBCSystemResources/' + jdbcResource.getName() + '/JDBCResource/' + jdbcResource.getName() + '/JDBCDriverParams/' + jdbcResource.getName() + '/Properties/' + jdbcResource.getName() + '/Properties/oracle.net.CONNECT_TIMEOUT')
               		#cmo.unSet('SysPropValue')
               		#cmo.unSet('EncryptedValue')
                	print "----> Setando ConnectTimeout para o DS " + jdbcResource.getName()
                	cmo.setValue('5000')
	salvarAlter()
	return

def defOption():
	#######OPÇÃO DE AJUSTE########
	while True:
		print '\n\n\n\n'
		print '\t\t\t\t\tDefina o tipo do ajuste\n\n'
                print '\t\t\t\t\t(1) - Ajuste de JVM:\n'
                print '\t\t\t\t\t(2) - Ajuste de Datasource\n\n'
                print '\t\t\t\t\t(3) - Sair'
		print '\n\n\n\n'
                try:
                        varOption=int(raw_input('\t\t\t\t\tOpção: '))
                except Exception:
                        print '\nInforme 1, 2 ou 3 para sair\n\n'
                        continue
                else:
                        if varOption == 1:
                                ajustaVM()
                                continue
                        elif varOption == 2:
                                ajustaDS()
                                continue
                        elif varOption == 3:
                                exit(exitcode=12)
                        else:
                                print '\nInforme 1, 2 ou 3 para sair\n\n'
                                continue
        return

###INICIO DO SCRIPT########
argslength = len(sys.argv)
if argslength <> 3 :
    print '==>Necessario passar os parametros: Host do Admin, porta do Admin.'
    print ''
    print ' Ex.: '
    print ''
    print '       java weblogic.WLST padroniza_checklist.py prd-osbproduct1-admin 7000'
    print ''

    exit(exitcode=12)

varAdminHost       = sys.argv[1]
varAdminPort       = sys.argv[2]

varAdminUrl        = 't3://' + varAdminHost + ':' + varAdminPort
defOption()
