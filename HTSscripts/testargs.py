import sys, argparse
    
if __name__ != "__main__":
    sys.argv=['testargs.py', 'ID', '-c', '12', '-t', 'treat', '-m', 'med']
parser=argparse.ArgumentParser(description="Build directory of symlinks/shortcuts to images from QFA file archive.")
parser.add_argument("exptID", type=str, help="QFA experiment ID, e.g. QFA00001")
parser.add_argument("-c","--cutoff",type=float, help="Maximum number of days after inoculation, beyond which images are ignored (e.g. 4.0).")
parser.add_argument("-t","--treatment",type=str, help="Only return images of plates from experiment which experienced this treatment (e.g. 30).")
parser.add_argument("-m","--medium",type=str, help="Only return images of plates from experiment which contained this medium (e.g. CSM).")
parser.add_argument("-p","--photos",action='store_true', help="If this flag is specified, return actual photos rather than the default behaviour, which is to return symlinks/shortcuts.")
args = parser.parse_args()

print(sys.argv)
print(args)
