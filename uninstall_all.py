import pkg_resources
import os

packages = [dist.project_name for dist in pkg_resources.working_set]

for package in packages:
    os.system(f"pip uninstall -y {package}")

print("✅ सारे पैकेज uninstall हो गए!")
