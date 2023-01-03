import sys
import time
import subprocess
from utils import Mind, watch, list_files, clear_dir
from bb_services.unique_id import unknown as unique_id
from bb_services.worker import unknown as Worker

my_mind = Mind()


def generate(test):
    prompt = f"""
        The following test will run: {test}.

        Here is code that will pass the test:
    """
    return my_mind.get_completion(prompt)


def iterate(code, input, output, expected):
    prompt = f"""
        The following code was run: 
        
        {code}

        (END CODE)

        The input was {input}, and the output was {output}. The expected output was {expected}.

        This updated code runs correctly:
    """
    return my_mind.get_completion(prompt)


# Code gen pool class
class CodeGenPool:
    def __init__(
        self, test_filename, output_filename, pool_size, cache_dir="./my_code/v2_tmp"
    ):
        self.test_filename = test_filename
        self.output_filename = output_filename
        self.cache_dir = cache_dir
        # Initialize 3 code gen instances
        self.pool = [
            CodeGenWorker(
                self.test_filename,
                self.output_filename,
                max_iterations=5,
                cache_dir=self.cache_dir,
            )
            for _ in range(pool_size)
        ]

    def run(self):
        # Clear cache dir
        clear_dir(self.cache_dir)
        # Run all code gen instances in parallel
        all_resolved = False
        while not all_resolved:
            for code_gen in self.pool:
                if not code_gen.resolved:
                    solution = code_gen.generate()
                    if solution:
                        # Write solution to file
                        with open(self.output_filename, "w") as f:
                            f.write(solution)
                        return True
            all_resolved = all([code_gen.resolved for code_gen in self.pool])
        raise NoSolutionError


class NoSolutionError(Exception):
    pass


INPUT = str([0, 1, 2, 3, 4])
OUTPUT = str([1, 1, 2, 6, 24])
# TESTS = [
#     {
#         "input": "0",
#         "output": "1",
#     },
#     {
#         "input": "1",
#         "output": "1",
#     },
#     {
#         "input": "2",
#         "output": "2",
#     },
#     {
#         "input": "3",
#         "output": "6",
#     },
#     {
#         "input": "4",
#         "output": "24",
#     },
# ]

SEED = """
import sys

def process(input):
    pass

input = sys.argv[1]
print(process(input))
"""

print(INPUT)
print(OUTPUT)


class CodeGenWorker(Worker):
    def __init__(self, test_filename, output_filename, max_iterations, cache_dir):
        super().__init__()
        self.test_filename = test_filename
        self.output_filename = output_filename
        self.cache_dir = cache_dir
        self.id = unique_id()
        # Tmp file name
        self.attempts = 0
        self.max_iterations = max_iterations
        self.tmp_filename = f"{self.cache_dir}/tmp_{self.id}.py"
        self.solution = SEED

        with open(self.test_filename, "r") as f:
            self.test_file_contents = f.read()

    def generate(self):
        # try:
        return self.attempt()
        # except Attempter.MaxIterationsExceededError:
        #     raise NoSolutionError

    def attempt(self):
        self.attempts += 1
        if self.attempts >= self.max_iterations:
            raise Exception
        # Generate code
        # if self.solution is None:
        #     self.solution = generate(self.test_file_contents)
        # full_code = (
        #     self.solution + "\n" + "# BEGIN TESTS" + "\n" + self.test_file_contents
        # )
        with open(self.tmp_filename, "w") as f:
            f.write(self.solution)
        # for test in TESTS:
        # input = test["input"]
        try:
            output = subprocess.check_output(
                ["python3", self.tmp_filename, INPUT], stderr=subprocess.STDOUT
            ).decode("utf-8")
            print("output: ", output)
            assert output == OUTPUT, f"Expected '{OUTPUT}', got '{output}'"
            return self.resolve(self.solution)
        except AssertionError as e:
            err_msg = str(e)
        except subprocess.CalledProcessError as e:
            err_msg = e.stdout
        if err_msg:
            self.solution = iterate(self.solution, INPUT, err_msg, OUTPUT)
            with open(self.tmp_filename, "w") as f:
                f.write(self.solution)
            # # Trim the test from the solution if it's there
            # if "# BEGIN TESTS" in self.solution:
            #     self.solution = self.solution[: self.solution.index("# BEGIN TESTS")]
        # self.tries += 1
        # return None


if __name__ == "__main__":
    # Watch "v2_specs" folder for changes
    def callback(file):
        # Ignore files starting with undesrcore
        if file[0] == "_":
            return
        print(f"Running code generator for {file}")
        code_gen_pool = CodeGenPool(
            f"./my_code/v2_specs/{file}",
            f"./my_code/v2_services/{file}",
            pool_size=5,
        )
        try:
            code_gen_pool.run()
            print(f"Code generator finished for {file}")
        except NoSolutionError:
            print(f"Code generator failed for {file}")

    # If spec doesn't have a service, create one
    for file in list_files("./my_code/v2_specs"):
        if file not in list_files("./my_code/v2_services"):
            callback(file)

    watch("./my_code/v2_specs", callback)
