import os
import multiprocessing as mp
import numpy as np
import hashlib


def generate_partition(random_seed, output_file):
    print("bahasakita > Generating {} ...".format(output_file))

    hex_digest = hashlib.sha1(random_seed.encode("utf-8")).hexdigest()
    random_seed_int = int(hex_digest, 16) % (2 ** 32)
    np.random.seed(random_seed_int)

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    m_val, max_data = 1000, 7878375

    num_list = (np.random.weibull(1.3, max_data) * m_val).astype(float)

    max_id_int = 2 ** 40 - 1
    random_ids = np.random.randint(low=0, high=max_id_int, size=max_data, dtype=np.int64)
    id_list = np.unique(random_ids)

    max_data = min(len(id_list), max_data)
    rows = ["%x,%.3f" % (id_list[i], num_list[i]) for i in range(0, max_data)]

    header = "planet_id,distance_to_earth"
    output = open(output_file, "w")
    output.write(header + "\n")
    output.write("\n".join(rows))
    output.close()
    print("bahasakita > Generating {} ... DONE".format(output_file))


def generate_data(candidate_email, output_dir, num_files, num_workers):
    random_seed_template = "{id}_{{num:02d}}".format(id=candidate_email)
    output_template = "{dir}/{id}_{{num:02d}}.csv".format(dir=output_dir, id=candidate_email)

    with mp.Pool(processes=num_workers) as pool:
        for i in range(0, num_files):
            random_seed = random_seed_template.format(num=i)
            output_file = output_template.format(num=i)
            pool.apply_async(generate_partition, (random_seed, output_file))
        pool.close()
        pool.join()
