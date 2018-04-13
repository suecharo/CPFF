# coding: utf-8
import numpy
import sys
from scipy import stats


def calc_pvalue(count_1, count_2, count_no_1, count_no_2, cochran):
    data = numpy.array([[count_1, count_2], [count_no_1, count_no_2]])
    x2, p, dof, exp = stats.chi2_contingency(data)

    if p < 0.05:
        l_exp = list(exp.ravel())
        b_check = False
        for num_exp in l_exp:
            if num_exp <= cochran:
                b_check = True
                break
        if b_check:
            return False
        res = data - exp
        res_var = numpy.zeros(res.shape)
        it = numpy.nditer(data, flags=["multi_index"])
        d_sum = data.sum()
        while not it.finished:
            var = (1 - (data[:, it.multi_index[1]].sum() / d_sum)) * \
                  (1 - (data[it.multi_index[0], :].sum() / d_sum))
            res_var[it.multi_index[0], it.multi_index[1]] = var
            it.iternext()
        stdres = res / numpy.sqrt(exp * res_var)
        if stdres[0][1] >= 1.96:
            return p
    else:
        return False

    return False


def main():
    with open("./sco_sma_sgr_sen_all.tsv", "r") as f:
        data = f.read()
    l_row = data.split("\n")
    header = l_row[0].split("\t")
    gene_1st_all_count = int(header[1][10:-1])
    gene_2nd_all_count = int(header[2][10:-1])

    print("=== Start ensemble ===")
    l_cochran = list(range(11))
    for cochran in l_cochran:
        file_name = "./count_file/count_{}.tsv".format(cochran)

        print("P value : 0.05, Cochran : {}".format(cochran))
        count = 0
        with open(file_name, "w") as f:
            f.write("{}\tp_value\n".format("\t".join(header)))
            for row in l_row[1:]:
                if row == "":
                    continue
                l_ele = row.split("\t")
                count_1 = int(l_ele[1])
                count_2 = int(l_ele[2])
                count_no_1 = gene_1st_all_count - count_1
                count_no_2 = gene_2nd_all_count - count_2
                p_value = calc_pvalue(count_1, count_2, count_no_1,
                                      count_no_2, cochran)
                if p_value is False:
                    continue
                else:
                    f.write("{}\t{}\n".format(row, p_value))
                    count += 1
        print("2nd count : {}".format(count))
        print("=" * 10)
    print("=== Done. ===")

    sys.exit(0)


if __name__ == "__main__":
    main()
