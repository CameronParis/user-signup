#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {color: red}
    </style>
</head>
<body>
    <a href="/"><h1>Signup</h1></a>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

import re
import cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASS_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

def clear_dict():
    for i in errors.keys():
        errors[i] = ''

errors = {'error_username':'',
          'error_password':'',
          'error_verify':'',
          'error_email':''
}


class Signup(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')



        signup_form = """
            <form action='/welcome' method="post">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="{0}" required>
                            <td class="error">{2}</td>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="Password">Password</label></td>
                        <td>
                            <input name="password" type="password" value="" required>
                            <td class="error">{3}</td>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" value="" required>
                            <td class="error">{4}</td>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="{1}" >
                            <td class="error">{5}</td>
                        </td>
                    </tr>

                </table>
                <input type="submit" value="Sign me up, Scotty!"/>
            </form>
            """.format(username, email , errors['error_username'], errors['error_password'], errors['error_verify'], errors['error_email'])

        clear_dict()
        main_content = signup_form
        content = page_header + main_content + page_footer
        self.response.write(content)


class Welcome(webapp2.RequestHandler):
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        #params = dict(username = username,
        #         email = email)


        if not valid_username(username):
            #params['error_username'] = "That's not a valid username."
            #errors += error_username
            errors['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            #params['error_password'] = "That's not a valid password."
            #errors += error_password
            errors['error_password'] = "That's not a valid password."
            have_error = True
        elif password != verify:
            #params['error_verify'] = "Your passwords didn't match."
            #errors += error_verify
            errors['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            #params['error_email'] = "That's not a valid email."
            #errors += error_email
            errors['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            redirect_message = ''
            for i in errors:
                redirect_message += (errors[i] + '&')
            self.redirect('/?username=' + username + '&email=' + email + '&' + redirect_message)
        else:
            main_content = "<h1>Welcome, " + username + "!<h1>"

            content = page_header + main_content + page_footer

            self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
