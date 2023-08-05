
# A 'PCR or optical duplicate' is marked with 0x400 in the FLAG field of SAM
# files.
SAM_FORMAT_FLAG_DUPLICATE = 0x400
line = 'D00597:180:C7NMDANXX:6:1101:1185:57758-GCCGATAT^GAGAAGAG;0^0	83	20	31376864	37	116M	=	31376773	-207	ATCAACTACTTGAAAACAACAGAGGCAAAGGAAATCATTGAAGATCTGAACAACTGCCTAAACCACTGCATTAAATATATTAGATCATTTGACTACAACGCATTTGTGGATGAGGC	FF<FFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFF<FFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF	MD:Z:116	NH:i:1	HI:i:1	NM:i:0	SM:i:37	XQ:i:40	X2:i:0	XO:Z:CU	XG:Z:A'
def update_flag_duplicate_split():
    # recall FLAG is the second field in sam files
    # parts = line.split('\t', 2)
    parts = line.split('\t', 2)
    parts[1] = str(int(parts[1]) | SAM_FORMAT_FLAG_DUPLICATE)
    return '\t'.join(parts)

# import timeit
# print(timeit.timeit(update_flag_duplicate_split))

