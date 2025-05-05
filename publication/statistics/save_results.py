import os

file_path = 'tests_results/'


def save_results(hvs, t, pfs, test_stamp, itr, pop, comination, seed, sample):
    final_dir = file_path + str(itr) + '_' + str(pop) + '/' + test_stamp + '/' + sample + '/' + comination
    os.makedirs(final_dir, exist_ok=True)
    final_path = os.path.join(final_dir, str(seed) + '.txt')

    with open(final_path, 'w') as file:
        file.write(f"{t}\n")

        for hv in hvs:
            file.write(f"{hv}\n")

        for pf in pfs:
            file.write("_front_\n")
            for tup in pf:
                line = ' '.join(map(str, tup)) + '\n'
                file.write(line)
