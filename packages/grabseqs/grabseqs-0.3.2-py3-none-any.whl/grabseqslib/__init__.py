__all__ = ["sra","mgrast"]

import os, sys, argparse

from grabseqslib.sra import get_sra_acc_metadata, run_fasterq_dump
from grabseqslib.mgrast import get_mgrast_acc_metadata, download_mgrast_sample

def main():

	# Top-level parser
	parser = argparse.ArgumentParser(prog="grabseqs",
		 description='Download metagenomic sequences from public datasets.')
	parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.3.2')
	subpa = parser.add_subparsers(help='repositories available')

	# Parser for SRA data
	parser_sra = subpa.add_parser('sra', help="download from SRA")
	parser_sra.add_argument('id', type=str, nargs='+', 
				help="One or more BioProject, ERR/SRR or ERP/SRP number(s)")

	parser_sra.add_argument('-o', dest="outdir", type=str, default="",
				help="directory in which to save output. created if it doesn't exist")
	parser_sra.add_argument('-r',dest="retries", type=int, default=2,
				help="number of times to retry download")
	parser_sra.add_argument('-t',dest="threads", type=int, default=1,
				help="threads to use (for fasterq-dump/pigz)")

	parser_sra.add_argument('-f', dest="force", action="store_true",
				help = "force re-download of files")
	parser_sra.add_argument('-l', dest="list", action="store_true",
				help="list (but do not download) samples to be grabbed")
	parser_sra.add_argument('-m', dest="metadata", action="store_true",
				help="save SRA metadata")
	parser_sra.add_argument('--no_parsing', dest="no_SRR_parsing", action="store_true",
				help="do not parse SRR/ERR (pass straight to fasterq-dump)")
	parser_sra.add_argument("--use_fastq_dump", dest="fastqdump", action="store_true",
				help="use legacy fastq-dump instead of fasterq-dump (no multithreaded downloading)")
	
	# Parser for MG-RAST data
	parser_rast = subpa.add_parser('mgrast', help="download from MG-RAST")
	parser_rast.add_argument('rastid', type=str, nargs='+', 
				help="One or more MG-RAST project or sample identifiers (mgp####/mgm######)")

	parser_rast.add_argument('-o', dest="outdir", type=str, default="",
				help="directory in which to save output. created if it doesn't exist")
	parser_rast.add_argument('-r',dest="retries", type=int, default=0,
				help="number of times to retry download")
	parser_rast.add_argument('-t',dest="threads", type=int, default=1,
				help="threads to use (for pigz)")

	parser_rast.add_argument('-f', dest="force", action="store_true",
				help = "force re-download of files")
	parser_rast.add_argument('-l', dest="list", action="store_true",
				help="list (but do not download) samples to be grabbed")
	parser_rast.add_argument('-m', dest="metadata", action="store_true",
				help="save metadata")

	args = parser.parse_args()

	# Make output directories if they don't exist
	try:
		if args.outdir != "":
			if not os.path.exists(args.outdir):
				os.makedirs(args.outdir)
	except AttributeError: # No subcommand provided (all subcomands have `-o`)
		print("Subcommand not specified, run `grabseqs -h` or  `grabseqs sra -h` for help")
		sys.exit(0)
	try:
		if args.rastid:
			for rast_proj in args.rastid:
				target_list = get_mgrast_acc_metadata(rast_proj, args.metadata, args.outdir)
				for target in target_list:
					download_mgrast_sample(target, args.retries, args.threads, args.outdir, args.force, args.list)
	except AttributeError:
		for sra_identifier in args.id:
			acclist = get_sra_acc_metadata(sra_identifier, args.metadata, args.outdir, args.list, args.no_SRR_parsing)

			for acc in acclist:
				run_fasterq_dump(acc, args.retries, args.threads, args.outdir, args.force, args.fastqdump)


