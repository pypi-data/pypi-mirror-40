import os
import sys

from jinjaform import log


args = sys.argv[1:]
cwd = os.getcwd()
env = os.environ.copy()

for name in ('JINJAFORM_PROJECT_ROOT', 'JINJAFORM_TERRAFORM_BIN'):
    if not env.get(name):
        log.bad('{} environment variable missing', name)
        sys.exit(1)

project_root = os.environ['JINJAFORM_PROJECT_ROOT']
jinjaform_root = os.path.join(project_root, '.jinjaform')
terraform_bin = os.environ['JINJAFORM_TERRAFORM_BIN']
workspace_dir = os.path.join(cwd, '.jinjaform')
terraform_dir = os.path.join(workspace_dir, '.terraform')

aws_provider = {}
s3_backend = {}
sessions = {}

env['JINJAFORM_PROJECT_ROOT'] = project_root
env['JINJAFORM_WORKSPACE'] = workspace_dir
