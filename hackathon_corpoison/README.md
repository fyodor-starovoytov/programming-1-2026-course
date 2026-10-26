# Search Poisoning, CORPOISON
Small project made for our concluding Hackathon event on Programming Course 1. Worked in Teams of 3. Mine responsibilities were user interaction and combining every single logic file in Main file. Maintainer of the project.


## What it does?

1. Check search queries: Load a text file containing searches and analyse them for potentially sensitive information.
2. Calculate privacy risk: Use keyword-based scoring to estimate how sensitive each query might be.
3. Add extra searches based on sensitivity to make original search activity less obvious.
4. Monitor memory usage: Measure the program's RAM usage and write the results to a log file.

## How to run it

Must have dependencies listed in requirements.txt installed.

1. Open a terminal in the project folder.
2. Install the required dependencies:

   "pip install -r requirements.txt"

3. Start the program:

    "python src/main.py"

4. Follow the instructions in the terminal. Choose "l" to load a file containing your search queries or "q" to quit.

When loading a file, enter its path once prompted. The program analyses its contents and asks if you want to obfuscate searches. You can then choose whether to inject additional searches or not.

## Security and privacy

Privacy is the main focus of this project.

- The program uses keyword-based scoring, so it can miss sensitive information or flag harmless searches.
- Adding extra searches does not prevent websites, search engines, or internet providers from tracking activity.


## Performance

The program is designed to be light and runs locally using Python. Its workload mainly depends on the number of queries being analysed and the size of the keyword lists.

RAM usage is measured using psutil, allowing us to observe how much memory the program uses while running.

## Sustainability

The project does not require a continuously running server. It can run on an ordinary computer, and its resource usage is mainly tied to the analysis being performed.
