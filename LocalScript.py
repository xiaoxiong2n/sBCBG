#!/usr/bin/python
# -*- coding: utf-8 -*-

#import shlex
# import subprocess
import os
import time

execTime = time.localtime()
timeString = str(execTime[0])+'_'+str(execTime[1])+'_'+str(execTime[2])+'_'+str(execTime[3])+':'+str(execTime[4])

print 'Time:', timeString

# job for one parameterization test:
#----------------------------------------- 
def launchOneParameterizedRun(i):
  print "Ready to launch job",i

  IDstring = timeString+'_%05d' %(i)

  print 'Create subdirectory:',IDstring
  os.system('mkdir '+IDstring)
  os.system('cp LGneurons.py '+IDstring+'/')
  os.system('cp testFullBG.py '+IDstring+'/')
  os.system('cp testChannelBG.py '+IDstring+'/')
  os.system('cp solutions_simple_unique.csv '+IDstring+'/')
  os.system('cp __init__.py '+IDstring+'/')
  os.chdir(IDstring)
  os.system('mkdir log')

  # creation of the modelParams.py file that will correspond to the run at hand
  mltstr = '''#!/apps/free/python/2.7.10/bin/python

# defines the value of the parameters that will be used by testFullbG.py
# generated by sangoScript.py

interactive = True

params = {'nbCh':     %d,
          'LG14modelID': %2d,
          'whichTest': '%s', # which test was used to generate the log
          'nbMSN': 2644.,
          'nbFSI':   53.,
          'nbSTN':    8.,
          'nbGPe':   25.,
          'nbGPi':   14.,
          'nbCSN': %5.f,
          'nbPTN': %4.f,
          'nbCMPf':   9.,
          'GMSN':     %4.2f,
          'GFSI':     %4.2f,
          'GSTN':     %4.2f,
          'GGPe':     %4.2f,
          'GGPi':     %4.2f, 
          'IeGPe':    %3.1f,
          'IeGPi':    %3.1f,
          'inDegCSNMSN': 100.,
          'inDegPTNMSN':   1.,
          'inDegCMPfMSN':  %3.1f, # 1.,
          'inDegFSIMSN':  30., # according to Humphries et al. 2010, 30-150 FSIs->MSN
          'inDegMSNMSN':  70., # according to Koos et al. 2004, cited by Humphries et al., 2010, on avg 3 synpase per MSN-MSN connection
          'inDegSTNMSN':   0.,
          'inDegGPeMSN':   0.,
          'inDegCSNFSI':  50.,
          'inDegPTNFSI':   1.,
          'inDegSTNFSI':   2.,
          'inDegGPeFSI':  25.,
          'inDegCMPfFSI': %3.1f, # 9.,
          'inDegFSIFSI':  15., # according to Humphries et al., 2010, 13-63 FSIs->FSI
          'inDegPTNSTN':  25.,
          'inDegCMPfSTN': %3.1f, # 9.,
          'inDegGPeSTN':  25.,
          'inDegCMPfGPe': %3.1f, # 9.,
          'inDegSTNGPe':   8.,
          'inDegMSNGPe':2644.,
          'inDegGPeGPe':  25.,
          'inDegMSNGPi':2644.,
          'inDegSTNGPi':   8.,
          'inDegGPeGPi':  23.,
          'inDegCMPfGPi': %3.1f, # 9.,
          'cTypeCSNMSN': 'focused', # defining connection types for channel-based models (focused or diffuse)
          'cTypePTNMSN': 'focused',
          'cTypeCMPfMSN':'%s', #'focused',
          'cTypeFSIMSN': 'diffuse', 
          'cTypeMSNMSN': 'focused', 
          'cTypeSTNMSN': 'diffuse',
          'cTypeGPeMSN': 'diffuse',
          'cTypeCSNFSI': 'focused',
          'cTypePTNFSI': 'focused',
          'cTypeSTNFSI': 'diffuse',
          'cTypeGPeFSI': 'focused',
          'cTypeCMPfFSI':'%s', #'focused',
          'cTypeFSIFSI': 'diffuse', 
          'cTypePTNSTN': 'focused',
          'cTypeCMPfSTN':'%s', #'focused',
          'cTypeGPeSTN': 'diffuse',
          'cTypeCMPfGPe':'%s', #'focused',
          'cTypeSTNGPe': 'diffuse',
          'cTypeMSNGPe': 'focused',
          'cTypeGPeGPe': 'diffuse',
          'cTypeMSNGPi': 'focused',
          'cTypeSTNGPi': 'diffuse',
          'cTypeGPeGPi': 'diffuse',
          'cTypeCMPfGPi':'%s', #'focused',
          'parrotCMPf' : False,
          }
''' %(nbch,lg14modelid,whichtest,nbcsn,nbptn,gmsn,gfsi,gstn,ggpe,ggpi,iegpe,iegpi,indegcmpfmsn,indegcmpffsi,indegcmpfstn,indegcmpfgpe,indegcmpfgpi,ctypefromcmpf,ctypefromcmpf,ctypefromcmpf,ctypefromcmpf,ctypefromcmpf)

  print 'Write modelParams.py'
  paramsFile = open('modelParams.py','w')
  paramsFile.writelines(mltstr)
  paramsFile.close()

  # execute the script file
  #command = 'python testFullBG.py'
  command = 'python '+whichtest+'.py'
  os.system(command)

  os.chdir('..')

#===============================

'''
for iegpi in [10.,11.,12.]:
  launchOneParameterizedRun(i)
  i+=1
'''

i = 0                                                                                                                                                                           
# which LG14 parameterization to use?
lg14modelid = 9

# which test will be carried out?
whichtest = 'testChannelBG' # can be testFullBG, testChannelBG
#whichtest = 'testFullBG' # can be testFullBG, testChannelBG
nbch = 8

# with which additional parameters?
nbcsn = 3000.
nbptn = 100.

D2depletion = 1.

gmsn=3.5
gfsi=1.
gstn=1.4 * D2depletion
ggpe=1.  * D2depletion
ggpi=1.
iegpe=11.
iegpi=10.

# Tests concerning CMPf connectivity parameters:
indegcmpfmsn = 1 # 1 ; 1 - 16 ; modifying from 1 to 2 has a strong effect on MSN activity, from 0.7 to 0.06 Hz !
indegcmpffsi = 9 # 9 ; 0 - 170
indegcmpfstn = 10 # 9 ; 1 - 85
indegcmpfgpe = 3 # 9 ; 0 - 27
indegcmpfgpi = 10 # 9 ; 0 - 78
ctypefromcmpf = 'diffuse'

#nbcsn=12000.
#nbptn=400.
launchOneParameterizedRun(i)
i+=1
