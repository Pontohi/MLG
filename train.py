from model import GenAdvNet
import argparse

parser = argparse.ArgumentParser(description='Train the algarfieithm')
parser.add_argument('--tdirs', metavar='N',dest="tdirs",default=['DailyGarf'], type=str, nargs='+',
                    help='Dirs to be used')
parser.add_argument('--shape', metavar=('X','Y','Z'), dest='shape', type=int,
                    default=[64,64,3], nargs=3,
                    help='Set the shape of the model input.')
parser.add_argument('--epochs', metavar='E', dest='epochs', type=int,
                    default=[100000], nargs=1,
                    help='Set how long the model should run')
parser.add_argument('--label', metavar='L', dest='label', type=str,
                    default=['GarfNet'], nargs=1,
                    help='Set the label for saved model info')
parser.add_argument('--imgrate', metavar='N', dest='imgrate', type=int,
                    default=[1000], nargs=1,
                    help='Set the rate at which generated images are produced')
parser.add_argument('--modelrate', metavar='N', dest='mrate', type=int,
                    default=[1000], nargs=1,
                    help='Set the rate at which the current model is saved')
parser.add_argument('--batch', metavar='N', dest='bsize', type=int,
                    default=[64], nargs=1,
                    help='Set the batch size')
parser.add_argument('--load', metavar='K', dest='loadgen', type=int,
                    default=None, nargs=1,
                    help='Generation to load from')
args = parser.parse_args()

tdirs = list(map(lambda x: "Data/"+x,args.tdirs))
network = GenAdvNet(args.shape[0],args.shape[1],args.shape[2],args.label[0])
if args.loadgen != None:
    network.load_weighting(("./saved_models/facegenerator_"+args.label[0]+"{}.hdf5").format(str(args.loadgen[0])), ("./saved_models/facediscriminator_"+args.label[0]+"{}.hdf5").format(str(args.loadgen[0])))
network.train(tdirs,args.epochs[0],args.bsize[0],args.imgrate[0],args.mrate[0])