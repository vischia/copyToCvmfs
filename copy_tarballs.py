import os,sys,datetime
from subprocess import Popen, PIPE

import optparse
# Command line options
usage = 'usage: %prog --input]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',          dest='inputDir',       help='input directory',        default='/tmp/doesnotexist/',           type='string')
parser.add_option('-o', '--output',         dest='outputDir',      help='output directory',       default='~/www/susyRA7/',           type='string')
parser.add_option('-v', '--version',        dest='version',   help='gridpack version', default='v1',   type='string')
parser.add_option('-g', '--generator',      dest='generator', help='target phys generator (influences folder)')
parser.add_option('-e', '--energy',         dest='energy',    help='targed cm energy',            default='13', type='string')
parser.add_option('-a', '--exitAfterCheck', dest='exitAfterCheck', help='Exit anyways after check', action='store_true')
parser.add_option('-d', '--dryRun',         dest='dryRun', help='Only print commands, do not actually execute them', action='store_true')

(opt, args) = parser.parse_args()

inputs_dir               = opt.inputDir
outputDir                = opt.outputDir
exit_anyway_after_check = opt.exitAfterCheck
version                  = opt.version
generator                = opt.generator
energy                   = opt.energy
dryRun                   = opt.dryRun

if dryRun:
  print inputs_dir
  print outputDir
  print exit_anyway_after_check
  print version
  print generator
  print energy
  print dryRun
  sys.exit(1)

target_main = ''
if generator.find('powheg') !=-1:
  target_main = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/{e}TeV/powheg/V2/'.format(e=energy)
elif generator.find('madgraph') !=-1:
  target_main = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/{e}TeV/madgraph/V5_2.3.3/'.format(e=energy)
else:
  print("NO GENERATOR SPECIFIED. Exiting.")
  sys.exit(1)

#if dryRun:
#  print "HERE"
#  print target_main
#  sys.exit(1)


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
  if not dryRun:
    os.system("cp "+inputs_dir+"/"+input+" "+fullpath_version+'/')
  existing_list2.append(((fullpath_version+'/'+os.listdir(fullpath_version)[0]).replace('/eos/cms/store/group/phys_generator/cvmfs','/cvmfs/cms.cern.ch/phys_generator')).replace('//','/'))

if dryRun:
  print('Dry run selected: action has not been executed. Listing only.')

print 'list of copied files'
print existing_list2
datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
text_file = open("list_of_copied_gridpacks_"+datetime+".txt", "w")
for item in existing_list2:
    text_file.write("%s\n" % item)
text_file.close()
