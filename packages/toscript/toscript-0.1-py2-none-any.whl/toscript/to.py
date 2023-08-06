import os
import glob
import sys

class ToGoer(object):
    """docstring for ToGoer"""
    def __init__(self):
        super(ToGoer, self).__init__()
        self.toscriptdir = self.get_toscriptdir()
        self.toscripts = self.get_toscripts()
        self.toscripts_basenames = [ os.path.basename(s).replace('.sh', '') for s in self.toscripts ]
        self.test_mode = False

    def get_toscriptdir(self):
        return os.environ.get(
            'TOSCRIPTDIR',
            os.path.join(os.environ['HOME'], 'toscripts')
            )

    def get_toscripts(self):
        if not self.exists_toscriptdir():
            return []
        return glob.glob(
            os.path.join(self.toscriptdir, '*.sh')
            )

    def exists_toscriptdir(self):
        return os.path.isdir(self.toscriptdir)

    def has_scripts_toscriptdir(self):
        return len(self.toscripts) > 0

    def get_script(self, basename):
        if not self.exists_toscriptdir():
            print 'No directory \'{0}\''.format(self.toscriptdir)
            sys.exit(1)
        elif not basename in self.toscripts_basenames:
            print 'No script corresponds with \'{0}\''.format(basename)
            print 'Registered scripts: {0}'.format(
                ', '.join(self.toscripts_basenames)
                )
            sys.exit(1)
        else:
            script = self.toscripts[self.toscripts_basenames.index(basename)]
            script = os.path.abspath(script)
            return script

    def print_contents(self, script):
        print 'Would now run \'source {0}\''.format(script)
        print 'Contents of {0}:\n'.format(script)
        with open(script, 'r') as fp:
            print fp.read()
        sys.exit(1)

    def run_script(self, basename):
        """Not useful, executes in subshell"""
        script = get_script(basename)
        if script == '': return
        cmd = 'source ' + script
        if self.test_mode:
            print 'Would now run \'{0}\''.format(cmd)
            print 'Contents of {0}:\n'.format(script)
            with open(script, 'r') as fp:
                print fp.read()
        else:
            os.system(cmd)
