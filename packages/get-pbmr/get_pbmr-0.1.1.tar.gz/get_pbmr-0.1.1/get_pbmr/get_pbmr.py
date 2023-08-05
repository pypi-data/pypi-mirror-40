import pandas as pd
import matplotlib.pyplot as plt
import argparse

def read_file(input_ob):
    while True:
        line = input_ob.readline()
        if not line:
            break
        yield line

def get_mutation_rate_df(file_path):

    try:
        with open(file_path, "r") as input_ob:
            counts = {}
            key_conv = {
                'I': 'Insertion', 'S': 'Soft Clipping', '=': 'Match',
                'X': 'Mismatch'}

            for line_num, file_line in enumerate(read_file(input_ob)):
                print(line_num, end="\r")
                file_line = file_line.strip()
                if file_line[0] == '@':
                    continue
                file_line_arr = file_line.split()
                # Read the MD value for mismatch positions in 'M' CIGAR ranges
                for c in file_line_arr[11:]:
                    if c.startswith('MD'):
                        MD_string = c.split(':')[2]
                        pos = 0
                        num = 0
                        MD_pos = []
                        for i in list(MD_string):
                            try:
                                tmp = int(i)
                                num = num*10 + tmp
                            except:
                                pos += num
                                pos += 1
                                if i != '^':
                                    MD_pos.append(pos)
                                num = 0
                pos = 1
                pos_md = 1
                num = 0
                # Read CIGAR ranges and increment the catogories' values
                c_string = file_line_arr[5]
                for i in list(c_string):
                    try:
                        tmp = int(i)
                        num = num*10 + tmp
                    except:
                        if i == 'M':
                            for j in range(pos, pos+num):
                                if j not in counts:
                                    counts[j] = {
                                        'Match': 0, 'Mismatch': 0,
                                        'Insertion': 0, 'Soft Clipping': 0}
                                pos_md += 1
                                if pos_md in MD_pos:
                                    counts[j]['Mismatch'] += 1
                                else:
                                    counts[j]['Match'] += 1
                            pos = pos+num
                        elif i in ['X', '=']:
                            for j in range(pos, pos+num):
                                if j not in counts:
                                    counts[j] = {
                                        'Match': 0, 'Mismatch': 0,
                                        'Insertion': 0, 'Soft Clipping': 0}
                                pos_md += 1
                                counts[j][key_conv[i]] += 1
                            pos = pos+num
                        elif i in ['S', 'I']:
                            for j in range(pos, pos+num):
                                if j not in counts:
                                    counts[j] = {
                                        'Match': 0, 'Mismatch': 0,
                                        'Insertion': 0, 'Soft Clipping': 0}
                                counts[j][key_conv[i]] += 1
                            pos = pos+num
                        num = 0
        return pd.DataFrame(counts).T
    except (IOError, OSError):
        print("Error opening / processing file")

def get_mutation_rate_graph(filename=None, prefix=None):

    if not filename and not prefix:
        parser = argparse.ArgumentParser(
            description=('Get Per Base Mutation Rate from sam files. Takes in a'
                         ' SAM file and outputs a PNG file.'),
            add_help=True)

        parser.add_argument(
            '-i', '--input', metavar="<SAM file>", type=str, action='store',
            dest='input', required=True,
            help=('Input file in sam format.'))

        parser.add_argument(
            '-o', '--output', metavar="PREFIX", type=str, action='store',
            dest='prefix', required=True,
            help=('Prefix for PNG output file.'))

        args = parser.parse_args()
        filename = args.input
        prefix = args.prefix

    df = get_mutation_rate_df(filename)
    df['total'] = df.sum(axis=1)
    for i in ['Insertion', 'Match', 'Mismatch', 'Soft Clipping']:
        df['{0} (%)'.format(i)] = df.apply(lambda x: x[i]/x['total'], axis=1)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)

    ax1.plot(df.index, df['Match (%)']*100, 'k.')
    ax1.set_title('Match')
    ax1.set_xlabel('Position (base)')
    ax1.set_ylabel('Match (%)')

    ax2.plot(df.index, df['Mismatch (%)']*100, 'k.')
    ax2.set_title('Mismatch')
    ax2.set_xlabel('Position (base)')
    ax2.set_ylabel('Mismatch (%)')

    ax3.plot(df.index, df['Insertion (%)']*100, 'k.')
    ax3.set_title('Insertion')
    ax3.set_xlabel('Position (base)')
    ax3.set_ylabel('Insertion (%)')

    ax4.plot(df.index, df['Soft Clipping (%)']*100, 'k.')
    ax4.set_title('Soft Clipping')
    ax4.set_xlabel('Position (base)')
    ax4.set_ylabel('Soft Clipping (%)')

    fig.set_figheight(30)
    fig.set_figwidth(len(df)/10)

    plt.savefig("%s.png" % prefix, bbox_inches='tight')

if __name__== "__main__":
    get_mutation_rate_graph()
