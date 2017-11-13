import cmd
import signal
from engine.engine import Engine

engine = Engine()

class dssCmdLine(cmd.Cmd):
    """Command processor for dss"""
    prompt = '_$ '
    use_rawinput = False
    #FROM ENGINE
    def do_startCollector(self, args):
        params = args.split()
        collector = engine.get_collector(params[0])
        engine.startIndividualCollector(collector)
    #FROM ENGINE
    def do_list(self,args):
        engine.list()
    #FROM ENGINE
    def do_parse_all(self, args):
        engine.parse()

    #FROM ENGINE
    def do_parse(self, args):
        params = args.split()
        collector = engine.get_collector(params[0])
        engine.parser(collector)

    def do_stop_all(self,args):
        engine.stopall_collectors()
    #FROM ENGINE
    def do_export(self,args):
        engine.export()

    def do_delete_all(self, args):
        engine.delete_all()

    def do_close_All(self, args):
        engine.close_all()

    def do_EOF(self,args):
        '"Handles exiting the system with end of file character"'
        print '\n'
        return True

if __name__ == '__main__':
    dssCmdLine().cmdloop()
