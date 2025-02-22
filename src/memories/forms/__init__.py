import importlib
import os
import pkgutil

package_name = __name__
package_path = os.path.dirname(__file__)
# Scansiona tutti i moduli nel package e importali dinamicamente
for _, module_name, _ in pkgutil.iter_modules([package_path]):
    importlib.import_module(f"{package_name}.{module_name}")