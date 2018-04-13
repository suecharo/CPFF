# coding: utf-8
import numpy
import sys
from scipy import stats


def calc_pvalue(count_1, count_2, count_no_1, count_no_2):
    data = numpy.array([[count_1, count_2], [count_no_1, count_no_2]])
    x2, p, dof, exp = stats.chi2_contingency(data)

    return p


def main():
    with open(sys.argv[1], "r") as f:
        data = f.read()
    l_row = data.split("\n")
    header = l_row[0].split("\t")
    gene_1st_all_count = int(header[1][10:-1])
    gene_2nd_all_count = int(header[2][10:-1])

    print("=== Start calculation P value. ===")
    with open(sys.argv[2], "w") as f:
        f.write("{}\tp_value\n".format("\t".join(header)))
        for row in l_row[1:]:
            if row == "":
                continue
            l_ele = row.split("\t")
            count_1 = int(l_ele[1])
            count_2 = int(l_ele[2])
            count_no_1 = gene_1st_all_count - count_1
            count_no_2 = gene_2nd_all_count - count_2
            p_value = calc_pvalue(count_1, count_2, count_no_1, count_no_2)
            f.write("{}\t{}\n".format(row, p_value))
    print("=== Done. ===")

    sys.exit(0)


if __name__ == "__main__":
    main()
