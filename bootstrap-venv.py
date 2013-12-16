import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                     'BlogApplication'])
    subprocess.call([join(home_dir, 'bin', 'paster'),
                     'make-config', 'BlogApplication',
                     join(etc, 'blog.ini')])
    subprocess.call([join(home_dir, 'bin', 'paster'),
                     'setup-app', join(etc, 'blog.ini')])
"""))
f = open('blog-bootstrap.py', 'w').write(output)
