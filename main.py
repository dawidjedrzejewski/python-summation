import timeit
import os
import sys
import platform
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import statistics

# Predefined list of numbers to work on.

numbers = [
    15972490,
    80247910,
    92031257,
    75940266,
    97986012,
    87599664,
    75231321,
    11138524,
    68870499,
    11872796,
    79132533,
    40649382,
    63886074,
    53146293,
    36914087,
    62770938]

median_list = []

# Calling functions and creating .html report file in folder where main.py is.
# Report file contains execution environment info, test results and summary.


def main():
    single_thread_times_list = single_thread_time()
    multiple_threads_time_list = multiple_threads_time()
    multiple_processes_time_list = multiple_processes_time()
    multiple_processes_based_on_cpus_time_list = multiple_processes_based_on_cpus_time()

    html_style = """
    <style>

    body {
      font-size: 10pt;
    }

    h2 {
      padding-top: 10pt;
    }

    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
      table-layout: fixed ;
    }

    td, th {
      border: 2px solid #b9b9b9;
      padding: 10px;
      text-align: center;
      width: 25% ;
    }

    th {
      background-color: #d5d5d5;
    }

    td {
    }

    tr:nth-child(odd) {
      background-color: #eeeeee;
    }
    </style>"""

    with open('report.html', 'w') as report:
        report.write(
            f"""
<html>
<head>
<title>Multithreading/Multiprocessing benchmark results</title>
{html_style}
</head>
<body>

<h1>Multithreading/Multiprocessing benchmark results</h1>
<p>
</p>

<h2>Execution environment</h2>
<p>

Python version: {platform.python_version()}<br/>
Interpreter: {platform.python_implementation()}<br/>
Interpreter version: {sys.version}<br/>
Operating system: {platform.system()}<br/>
Operating system version: {platform.release()}<br/>
Processor: {platform.processor()}<br/>
CPUs: {os.cpu_count()}

</p>


<h2>Test results</h2>
<p>The following table shows detailed test results:</p>
<table>
  <tr>
    <th>Execution:</th>
    <th>1&nbsp;thread (s)</th>
    <th>4&nbsp;threads (s)</th>
    <th>4&nbsp;processes (s)</th>
    <th>processes based on number of CPUs (s)</th>
  </tr>

  <tr>
    <td>1</td>
    <td>{'{:.3f}'.format(single_thread_times_list[0])}</td>
    <td>{'{:.3f}'.format(multiple_threads_time_list[0])}</td>
    <td>{'{:.3f}'.format(multiple_processes_time_list[0])}</td>
    <td>{'{:.3f}'.format(multiple_processes_based_on_cpus_time_list[0])}</td>
  </tr>

  <tr>
    <td>2</td>
    <td>{'{:.3f}'.format(single_thread_times_list[1])}</td>
    <td>{'{:.3f}'.format(multiple_threads_time_list[1])}</td>
    <td>{'{:.3f}'.format(multiple_processes_time_list[1])}</td>
    <td>{'{:.3f}'.format(multiple_processes_based_on_cpus_time_list[1])}</td>
  </tr>

  <tr>
    <td>3</td>
    <td>{'{:.3f}'.format(single_thread_times_list[2])}</td>
    <td>{'{:.3f}'.format(multiple_threads_time_list[2])}</td>
    <td>{'{:.3f}'.format(multiple_processes_time_list[2])}</td>
    <td>{'{:.3f}'.format(multiple_processes_based_on_cpus_time_list[2])}</td>
  </tr>

  <tr>
    <td>4</td>
    <td>{'{:.3f}'.format(single_thread_times_list[3])}</td>
    <td>{'{:.3f}'.format(multiple_threads_time_list[3])}</td>
    <td>{'{:.3f}'.format(multiple_processes_time_list[3])}</td>
    <td>{'{:.3f}'.format(multiple_processes_based_on_cpus_time_list[3])}</td>
  </tr>

  <tr>
    <td>5</td>
    <td>{'{:.3f}'.format(single_thread_times_list[4])}</td>
    <td>{'{:.3f}'.format(multiple_threads_time_list[4])}</td>
    <td>{'{:.3f}'.format(multiple_processes_time_list[4])}</td>
    <td>{'{:.3f}'.format(multiple_processes_based_on_cpus_time_list[4])}</td>
  </tr>

</table>

<h2>Summary</h2>
<p>The following table shows the median of all results:</p>
<table>
  <tr>
    <th>Execution:</th>
    <th>1&nbsp;thread (s)</th>
    <th>4&nbsp;threads (s)</th>
    <th>4&nbsp;processes (s)</th>
    <th>processes based on number of CPUs (s)</th>
  </tr>

  <tr>
    <td>Median:</td>
    <td>{'{:.3f}'.format(median_list[0])}</td>
    <td>{'{:.3f}'.format(median_list[1])}</td>
    <td>{'{:.3f}'.format(median_list[2])}</td>
    <td>{'{:.3f}'.format(median_list[3])}</td>
  </tr>

</table>

<p>App author: Dawid Jędrzejewski</p>

</body>
</html>
""")
        report.close()

# Formula function with sum instead of (n*(n+1)) / 2 for more visible time differences.
# Execution functions and their execution times for single thread, multiple threads,
# multiple processes and processes based on number of CPUs.


def formula(n):
    sum(range(n+1))


def single_thread():
    for n in numbers:
        formula(n)


def multiple_threads():
    with ThreadPoolExecutor(max_workers=4) as executor:
        for n in numbers:
            executor.submit(formula, n)


def multiple_processes():
    with ProcessPoolExecutor(max_workers=4) as executor:
        for n in numbers:
            executor.submit(formula, n)


def multiple_processes_based_on_cpus():
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for n in numbers:
            executor.submit(formula, n)


def single_thread_time():
    single_thread_times_list = []
    for _ in range(5):
        time = timeit.timeit(single_thread, number=1)
        single_thread_times_list.append(time)
    median_list.append(statistics.median(single_thread_times_list))
    return single_thread_times_list


def multiple_threads_time():
    multiple_threads_time_list = []
    for _ in range(5):
        time = timeit.timeit(multiple_threads, number=1)
        multiple_threads_time_list.append(time)
    median_list.append(statistics.median(multiple_threads_time_list))
    return multiple_threads_time_list


def multiple_processes_time():
    multiple_processes_time_list = []
    for _ in range(5):
        time = timeit.timeit(multiple_processes, number=1)
        multiple_processes_time_list.append(time)
    median_list.append(statistics.median(multiple_processes_time_list))
    return multiple_processes_time_list


def multiple_processes_based_on_cpus_time():
    multiple_processes_based_on_cpus_time_list = []
    for _ in range(5):
        time = timeit.timeit(multiple_processes_based_on_cpus, number=1)
        multiple_processes_based_on_cpus_time_list.append(time)
    median_list.append(statistics.median(multiple_processes_based_on_cpus_time_list))
    return multiple_processes_based_on_cpus_time_list


if __name__ == "__main__":
    main()
