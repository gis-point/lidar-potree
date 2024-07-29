import subprocess
import os


def use_potree_converter(input_file, output_dir):
    try:
        # Check if the output directory exists, and create it if it doesn't
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construct the command
        command = ["PotreeConverter/build/PotreeConverter", input_file, "-o", output_dir]

        # Execute the command
        subprocess.run(command, check=True)
        print("PotreeConverter ran successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running PotreeConverter: {e}")
