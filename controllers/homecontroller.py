# -*- coding: utf-8 -*-

import git
from pyoauth2.client import Client
from odoo import http
import base64
from github import Github
from pprint import pprint
# sourcery skip: avoid-builtin-shadow
import os
import sys
import time
import subprocess
from git import Repo
from git import Git


 
class Example(http.Controller):
    KEY = '6e531a86335d03d813b6'
    SECRET = '063df27d0ea33d09d06a5624ab7377bca763e14b'
    CALLBACK = 'http://localhost:8070/customer/form'

    client = Client(KEY, SECRET, site='https://api.github.com',authorize_url='https://github.com/login/oauth/authorize',
                    token_url='https://github.com/login/oauth/access_token')

    print ('-' * 80)
    authorize_url = client.auth_code.authorize_url(redirect_uri=CALLBACK, scope='user,repo')
    print ('Go to the following link in your browser:')
    print (authorize_url)
    print ('-' * 80)
    code = ''
    # input('Enter the verification code and hit ENTER when you re done:')
    code = code.strip()
    access_token = client.auth_code.get_token(code, redirect_uri=CALLBACK, parse='query')
    print('token', access_token.headers)

    
    @http.route('/home', type='http', auth='public', website=True)
    def render_home_page(self):
        
        return http.request.render('zeyna.idpage', {'authorize_url': self.authorize_url})
    
    @http.route('/customer/form', type='http', auth="public", website=True)
    def partner_form(self, **post):
            code=http.request.params.get('code')
            print('Code',code)
            code = code.strip()
            access_token = self.client.auth_code.get_token(code, redirect_uri=self.CALLBACK, parse='query')
            print('token', access_token.headers)
            print('-' * 80)
            print('get user info')
            ret = access_token.get('/user')
            r=ret.parsed
            print(r)
            username = r.get("login")
            # pygithub object
            g = Github()
            # get that user by username
            if username:
                user = g.get_user(username)
                repos= user.get_repos()
                return http.request.render('zeyna.detailpage', {'my_infos':repos})
   
    @http.route('/customer/form/submit', type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        info = post.get('repository')
        # detail= info.split(',')
        # print("$$$$$$$$$$$$$$$$$$",detail)
        print('########################',info) 
        repo = info.split(',')[0]
        username = repo.split('/')[0]
        username = username.strip("('")
        reponame = repo.split('/')[1]
        reponame = reponame.strip("'")

        remote = info.split(',')[1]
        remote = remote.strip("')")
        remote = remote.replace("'", "") 
        remote =remote.replace(" ", "")  
        print('########################',reponame)
        print('########################',remote)
        print('***********************',username) 
        url="http://localhost:8069/"
        

        worspaces_path='/home/Workspaces'
        user_rep=''
        output_2 = subprocess.Popen(('ls', worspaces_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_2= output_2.stdout.read()
        output_2 = output_2.decode('utf-8')
        output_2 = output_2.split('\n')
        print(output_2)
        if output_2:
            a=1
            n=len(output_2)
            user_folders = ['config','database_files','filestore']
            data_folders = ['config','data','logs']
            user_rep='workspace_'+username
            # addon=worspaces_path+'/'+user_rep+reponame
            if n==1:
                os.mkdir(os.path.join(worspaces_path, user_rep), 0o777)
                sub_path=worspaces_path+'/'+user_rep
                os.chmod(sub_path, 0o777)
                if sub_path:
                    os.mkdir(os.path.join(sub_path, reponame), 0o777)
                    for sub_fol in user_folders:
                        os.mkdir(os.path.join(sub_path, sub_fol), 0o777)
                    data_path=worspaces_path+'/'+user_rep+'/database_files'
                    os.chmod(data_path, 0o777)
                    for data_fol in data_folders:
                        os.mkdir(os.path.join(data_path, data_fol))
                    full_local_path = worspaces_path+'/'+user_rep+'/'+reponame
                    os.chmod(full_local_path, 0o777)
                    # git.Git(full_local_path).clone(remote)
                    repo=git.Repo.init(full_local_path)
                    git.Repo.clone_from(remote, full_local_path)
                    # repo = Repo(full_local_path)
                    # origin = repo.remote(name="master")
                    # origin.pull()
                    print('full_local_path',full_local_path)
                    print('Repo cloned')
            else:
                for i in range(n):
                    urep=output_2[i]
                    if urep.startswith('workspace_') and urep != None:
                        rep = worspaces_path+'/'+urep
                        output_3 = subprocess.Popen(['ls',rep], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output_3= output_3.stdout.read()
                        output_3 = output_3.decode('utf-8')
                        output_3 = output_3.split('\n')
                        print('################',output_3)
                        if reponame in output_3:
                            print('addon exist') 
                            full_local_path = rep
                            os.chmod(full_local_path, 0o777)
                            # repo = Repo(full_local_path,search_parent_directories=True)
                            # origin = repo.remote(name="origin")
                            # origin.pull()
                            break  
                        else:
                            a+=1

                if a == n:
                    n=n-1
                    user_rep='workspace_'+username+str(n) 
                    os.mkdir(os.path.join(worspaces_path, user_rep))
                    sub_path=worspaces_path+'/'+user_rep
                    os.chmod(sub_path, 0o777)
                    os.mkdir(os.path.join(sub_path, reponame), 0o777)
                    for sub_fol in user_folders:
                        os.mkdir(os.path.join(sub_path, sub_fol))
                    data_path=worspaces_path+'/'+user_rep+'/database_files'
                    os.chmod(data_path, 0o777)
                    for data_fol in data_folders:
                        os.mkdir(os.path.join(data_path, data_fol))
                    full_local_path = worspaces_path+'/'+user_rep+'/'+reponame
                    git.Git(full_local_path).clone(remote)
                    # repo = Repo(full_local_path)
                    # origin = repo.remote(name="origin")
                    # origin.pull()
                # partner = http.request.env['res.partner'].sudo().create({
        #     'name': post.get('name'),
           
        # })
        # vals = {
        #     'partner': partner,
        # }
        return http.request.render("zeyna.idsuccess", {'url':url})
       