# Import the `os` module to manipulate files and directories
import os

# Print a message to the console
print("moet werken")

# Create a new file `test1.txt` in the `/home/vicuser/data-engineering-project-1` directory
with open(os.path.join(os.getcwd(), "test1.txt"), "w") as f:
    f.write("This is a test file.")

