import sys
import subprocess
import platform

DEPENDENCIES = ["numpy", "pyephem", "requests", "tqdm", "matplotlib", "astropy", "robobrowser", "astroquery", "openpyxl"]

def install_package(package):
    """Installs packages based on os and package specific paths"""
    if platform.system() == "Windows":
        if package == "astroquery":
            subprocess.call(["pip", "install", "--pre", package])
        else:
            subprocess.call(["pip", "install", package])
    else:
        if package == "astroquery":
            subprocess.call(["pip", "install", "--pre", package])
        else:
            subprocess.call(["pip", "install", package])

def check_dependencies():
    """Checks if all the dependencies required are installed"""
    print("\nChecking Dependencies")
    reqs = subprocess.check_output(([sys.executable, '-m', 'pip', 'freeze']))
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    installed = []
    for i in range(0, len(DEPENDENCIES)):
            if DEPENDENCIES[i] not in installed_packages:
                    print("------Installing Dependency: {}------".format(
                            DEPENDENCIES[i].title()))
                    install_package(DEPENDENCIES[i])
                    installed.append(False)
            else:
                    installed.append(True)

    if False in installed:
            print ("Dependencies have been installed")
    else:
            print("All dependencies are already installed")

if __name__=='__main__':
    reqs = subprocess.check_output(([sys.executable, '-m', 'pip', 'freeze']))
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
