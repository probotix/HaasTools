#! /usr/bin/python3

import os
import re
import argparse

def parse_oword_line( line ):
	match = re.match( r'^(O\d{3,6})(?:\s+\((.*?)\))?$', line.strip(), re.IGNORECASE )
	if match:
		oword = match.group(1).upper()
		comment = match.group(2) if match.group(2) else None
		return oword, comment
	return None

def sanitize_filename( name ):
	name = re.sub( r'[<>:"/\\|?*]', '', name )
	name = re.sub( r'\s+', '_', name.strip() )
	return name

def write_buffer( buffer, filename, output_dir ):
	if not buffer:
		return
	path = os.path.join( output_dir, filename )
	with open( path, 'w' ) as f:
		f.write('%\n')  # opening percent
		f.write( '\n'.join( buffer ) + '\n' )
		f.write('%\n')  # closing percent
	print( f"Wrote: {filename}" )


def clean_output_dir( output_dir ):
	if os.path.exists( output_dir ):
		for filename in os.listdir( output_dir ):
			file_path = os.path.join( output_dir, filename )
			if os.path.isfile( file_path ):
				os.remove( file_path )
	else:
		os.makedirs( output_dir )

def is_comment_line( line ):
	match = re.match( r'^\((.*?)\)$', line.strip() )
	return match.group(1).strip() if match else None

def split_pgm_file( input_file, output_dir ):
	with open( input_file, 'r', encoding='utf-8', errors='ignore' ) as f:
		#lines = [ l.strip() for l in f if l.strip() and l.strip() != '%' ]
		lines = [ l.rstrip('\r\n') for l in f if l.strip() != '%' ]

	clean_output_dir( output_dir )

	buffer = []
	current_filename = "MDI.nc"
	in_mdi = True
	i = 0
	total = len( lines )

	while i < total:
		line = lines[i]
		parsed = parse_oword_line( line )

		if parsed:
			# Write previous buffer
			if buffer:
				write_buffer( buffer, current_filename, output_dir )
				buffer = []

			oword, comment = parsed

			# If no comment on this line, peek at the next line for a comment
			if not comment and (i + 1) < total:
				next_line_comment = is_comment_line( lines[i + 1] )
				if next_line_comment:
					comment = next_line_comment
					buffer.append( lines[i + 1] )  # include it in the block
					i += 1  # skip the comment line from main loop

			if comment:
				current_filename = f"{oword}_{sanitize_filename(comment)}.nc"
			else:
				current_filename = f"{oword}.nc"

			in_mdi = False

		buffer.append( line )
		i += 1

	write_buffer( buffer, current_filename, output_dir )

if __name__ == "__main__":
	parser = argparse.ArgumentParser( description="Split a Haas .PGM file into MDI.nc and O-word programs with comment-based filenames." )
	parser.add_argument( "input_file", help="Path to the .PGM file" )
	parser.add_argument( "-o", "--output_dir", default="split_output", help="Output directory" )
	args = parser.parse_args()

	split_pgm_file( args.input_file, args.output_dir )

