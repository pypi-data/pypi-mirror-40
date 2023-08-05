import sys
import os
import argparse
# import sendgrid

parser = argparse.ArgumentParser()

parser.add_argument("--from" , help="Sender Address", default="scode@xo.io")
parser.add_argument("--to", help="destination address", default="ilovebugsincode@gmail.com" )
parser.add_argument("-s", "--subject", help="Subject of Email", default="I love mylli")
parser.add_argument("-b", "--body", help="Email Body", default="mylli works well")

args = parser.parse_args()



def main():
    #parse
    print(args.subject)
