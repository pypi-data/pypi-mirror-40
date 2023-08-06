#!/usr/bin/env python3

import os
import subprocess as sp
import time

from srblib import show_dependency_error_and_exit
from srblib import Colour

try:
    import requests
    from robobrowser import RoboBrowser
except:
    show_dependency_error_and_exit()


class Submit:
    notify_installed = True
    force_stdout = False

    def __init__(self,c_name,p_name,inputfile,username,password,force_stdout=False):
        self.c_name = c_name
        self.p_name = p_name
        self.prob_id = c_name + p_name
        self.inputfile = inputfile
        self.username = username
        self.password = password
        Submit.notify_installed = Submit._is_installed_notify()
        Submit.force_stdout = force_stdout
        if(force_stdout):
            notify_installed = False

    @staticmethod
    def get_latest_verdict(user):
        req = 'http://codeforces.com/api/user.status?'+'handle='+user+'&from=1&count=1'
        r = requests.get(req)
        js = r.json()
        if 'status' not in js or js['status'] != 'OK':
            Colour.print("unable to connect, try it yourself : "+req,Colour.RED)
            raise ConnectionError('Cannot connect to codeforces!')
        try:
            result = js['result'][0]
            id_ = result['id']
            verdict_ = result.get('verdict',None)
            time_ = result['timeConsumedMillis']
            memory_ = result['memoryConsumedBytes'] / 1000
            passedTestCount_ = result['passedTestCount']
        except Exception as e:
            raise ConnectionError('Cannot get latest submission, error')
        return id_, verdict_, time_, memory_, passedTestCount_


    def submit(self):
        last_id, b, c, d, e = Submit.get_latest_verdict(self.username)

        browser = RoboBrowser(parser = 'html.parser')
        browser.open('http://codeforces.com/enter')
        # todo check if it takes time
        enter_form = browser.get_form('enterForm')
        enter_form['handleOrEmail'] = self.username
        enter_form['password'] = self.password
        browser.submit_form(enter_form)

        try:
            checks = list(map(lambda x: x.getText()[1:].strip(),
                browser.select('div.caption.titled')))
            if self.username not in checks:
                Colour.print('Login Failed.. Wrong password.', Colour.RED)
                return
        except Exception as e:
            Colour.print('Login Failed.. Maybe wrong id/password.', Colour.RED)
            return

        # todo check if it takes time
        browser.open('http://codeforces.com/contest/'+self.c_name+'/submit')
        submit_form = browser.get_form(class_ = 'submit-form')
        submit_form['submittedProblemIndex'].value = self.p_name
        submit_form['sourceFile'] = self.inputfile

        browser.submit_form(submit_form)
        print(browser.url)
        # if browser.url[-6:] != 'status': # it was used when submitting from problemset
        if not 'my' in browser.url:
            Colour.print('Failed submission, probably you have submit the same file before', Colour.RED)
            return

        Submit.print_verdict(last_id,self.username,100)
        Colour.print('[{0}] submitted ...'.format(self.inputfile), Colour.GREEN)



    def daemon(func):
        def wrapper(*args, **kwargs):
            if(Submit.force_stdout):
                '''
                in case nofify is not installed it wont run like demon
                '''
                return func(*args,**kwargs)

            if os.fork():
                '''
                main process has value positive while fork has 0
                returning in main process, so no function executed
                '''
                return
            '''
            child process will run this function and return
            as child process is invisible it wont be visible
            but will keep on running after parent finishes
            '''
            func(*args, **kwargs)
            os._exit(os.EX_OK)
        return wrapper

    @daemon
    def print_verdict(last_id,username,max_time = 100,notify_installed = True):
        hasStarted = False
        while True:
            id_, verdict_, time_, memory_, passedTestCount_ = Submit.get_latest_verdict(username)
            if id_ != last_id and verdict_ != 'TESTING' and verdict_ != None:
                if verdict_ == 'OK':
                    message = 'OK - Passed ' + str(passedTestCount_) + ' tests'
                    color = Colour.GREEN
                else:
                    message = verdict_ + ' on ' + str(passedTestCount_+1) + ' test'
                    color = Colour.RED
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): Colour.print(message,color)
                break
            elif verdict_ == 'TESTING' and (not hasStarted):
                message = 'Judgement has begun'
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): Colour.print(message,Colour.GREEN)
                hasStarted = True
            time.sleep(0.5)
            max_time -= 1
            if(max_time < 0):
                message = 'Time out'
                if(Submit.notify_installed): sp.call(['notify-send','Codeforces',message])
                elif(Submit.force_stdout): Colour.print(message,Colour.YELLOW)
                break

    def _is_installed_notify():
        try:
            sp.call(['notify-send','--help'],stdout=sp.PIPE)
            return True
        except:
            Colour.print('notify-send seems not working, please install notify-send',Colour.RED)
            return False
