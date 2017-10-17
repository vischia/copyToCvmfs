import os,sys,datetime
from subprocess import Popen, PIPE

exit_anyway_after_check = False
# exit_anyway_after_check = True

#eos_mount_dir = '/afs/cern.ch/user/p/perrozzi/eos/'

#inputs_dir = '/afs/cern.ch/user/m/mmyllyma/public/gridpacks/'
inputs_dir = '/tmp/chayanit/'
#inputs_dir = '/afs/cern.ch/work/a/aioannou/public/MC_Production/AToZh_13TeV/Round2/'
#inputs_dir ='/afs/cern.ch/work/c/ccaillol/public/For_Chayanit/vbfh01_M125_Toa01a01_Tomumutautau'
# inputs_dir ='/afs/cern.ch/work/m/mharrend/public/gridpacksmartina/'
# inputs_dir ='/afs/cern.ch/work/k/kreis/public/forHIGMC/'
# inputs_dir ='/afs/cern.ch/work/a/ajafari/public/GridPacks'
# inputs_dir ='/afs/cern.ch/user/l/lviliani/public/POWHEG_HJ_MiNLO_NNLOPS/'
# inputs_dir ='/afs/cern.ch/work/z/zghiche/public/GridPacks/ForXanda/'
# inputs_dir ='/afs/cern.ch/user/z/zghiche/public/ForXanda/'
# inputs_dir ='/afs/cern.ch/work/h/hroskes/public/test_centralproduction/highmassgridpacks/2l2nu/CMSSW_7_1_14/src/collect_gridpacks/'
# inputs_dir ='/afs/cern.ch/user/o/obondu/work/public/forMC'
               
version = "v1"
  
#target_main = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/'
target_main = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.3/'
 
print 'target main folder',target_main
#if not os.path.isdir('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/'):
#  print 'mount eos first!'
#  sys.exit(1)
#else:
#  print 'eos mounted'

print 'version',version

print 'input dir',inputs_dir
inputs = filter(None,os.popen('ls '+inputs_dir+' | grep \\\.t').read().split('\n'))

existing_list = []
existing_list2 = []
trow_exception = False

for input in inputs:
  foldername = input.replace('_slc6_amd64_gcc481_CMSSW_7_1_28_tarball','').replace('.tar.gz','').replace('.tar.xz','').replace('.tgz','')
  fullpath = target_main+"/"+foldername
  fullpath_version = fullpath+"/"+version
  print "checking version folder",version,"for",foldername,", check if it is empty"
  if os.path.isdir(fullpath_version) and (len(os.listdir(fullpath_version))!=0):
    print "file already inside",fullpath_version,"please change version"
    existing_list.append(((fullpath_version+"/"+os.listdir(fullpath_version)[0]).replace('/eos/cms','')).replace('//','/'))
    trow_exception = True

if(trow_exception):
  print 'same files already existed, please check'
  print existing_list
  sys.exit(1)

if exit_anyway_after_check: sys.exit(1)
  
for input in inputs:
  foldername = input.replace('_slc6_amd64_gcc481_CMSSW_7_1_28_tarball','').replace('.tar.gz','').replace('.tar.xz','').replace('.tgz','')
  fullpath = target_main+"/"+foldername
  fullpath_version = fullpath+"/"+version+"/"
  print 'foldername',foldername.replace('/eos/cms','')
  print 'os.path.isdir('+fullpath.replace('/eos/cms','')+')',os.path.isdir(fullpath)
  if not os.path.isdir(fullpath):
    os.makedirs(fullpath)
  print 'os.path.isdir('+fullpath_version.replace('/eos/cms','')+')',os.path.isdir(fullpath_version)
  if not os.path.isdir(fullpath_version):
    os.makedirs(fullpath_version)
  
  print("cp "+inputs_dir+"/"+input+" "+fullpath_version.replace('/eos/cms','')+'/')
  os.system("cp "+inputs_dir+"/"+input+" "+fullpath_version+'/')
  existing_list2.append(((fullpath_version+'/'+os.listdir(fullpath_version)[0]).replace('/eos/cms/store/group/phys_generator/cvmfs','/cvmfs/cms.cern.ch/phys_generator')).replace('//','/'))

print 'list of copied files'
print existing_list2
datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
text_file = open("list_of_copied_gridpacks_"+datetime+".txt", "w")
for item in existing_list2:
    text_file.write("%s\n" % item)
text_file.close()
