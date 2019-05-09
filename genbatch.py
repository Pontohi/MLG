from model import GenAdvNet
import argparse
import os
parser = argparse.ArgumentParser(description='Run the algarfieithm')
parser.add_argument('--load', metavar='N',dest="load",default=['GarfBoy'], type=str, nargs='1',
                    help='Model to use')
parser.add_argument('--shape', metavar=('X','Y','Z'), dest='shape', type=int,
                    default=[128,128,3], nargs=3,
                    help='Set the shape of the model input.')
parser.add_argument('--count', metavar='E', dest='count', type=int,
                    default=[1000], nargs=1,
                    help='Set how many images the model should generate')
args = parser.parse_args()
try:
    os.mkdir(args.load[0])
except:
    print("failed to make batch dir")
network = GenAdvNet(args.shape[0],args.shape[1],args.shape[2],args.load[0])
network.load_weighting("facegenerator"+args.load[0]+".hdf5","facediscriminator"+args.load[0]+".hdf5")
for i in range(args.count[0]):
    network.generate_single_image(args.load[0]+"/"+str(i))
    