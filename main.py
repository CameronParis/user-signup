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
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASS_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(username)

def valid_email(email):
    return EMAIL_RE.match(username)

class Signup(webapp2.RequestHandler):
    def get(self):

        signup_form = """
            <form action="/signup" method="post">
                <table>
                    <tr>
                        <td><label for="username">Username</label></td>
                        <td>
                            <input name="username" type="text" value="username" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="Password">Password</label></td>
                        <td>
                            <input name="password" type="password" value="" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" value="" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="" >
                            <span class="error"></span>
                        </td>
                    </tr>

                </table>
                <input type="submit" value="Sign me up, Scotty!"/>
            </form>
            """

        main_content = signup_form
        content = page_header + main_content + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                 email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            #render the html for the errors
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(MainHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            #render the welcome page html
        else:
            self.redirect('/signup')
app = webapp2.WSGIApplication([
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
