
#    (c)2011 Bluebolt Ltd.  All rights reserved.
#    
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#    * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#    * Neither the name of Bluebolt nor the names of
#    its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#    
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#    
#    Author:Ashley Retallack - ashley-r@blue-bolt.com
#    Created:2011-06-07
#    Version:

from .Exceptions import *
from .User import User


class Project(object):
    
    def __init__(self, name='test', users=[], xusers=[]):
        self.name = name
        self._users = []
        self.users = users
        self._xusers = []
        self.xusers = xusers

    def users():
        doc = "The users property."
        doc += "Give this a list of User objects for those users who can submit to this project"

        def fget(self):
            return self._users

        def fset(self, value):
            if isinstance(value, list) and all(isinstance(x, User) for x in value):
                self._users = value
            else:
                raise TypeError("Project.users only accepts lists of type User")
        return locals()
    users = property(**users())

    def xusers():
        doc = "The xusers property."
        doc += "Give this a list of User objects for those users who can not submit to this project"

        def fget(self):
            return self._xusers

        def fset(self, value):
            if isinstance(value, list) and all(isinstance(x, User) for x in value):
                self._xusers = value
            else:
                raise TypeError("Project.xusers only accepts lists of type User")
        return locals()
    users = property(**users())

    def __repr__(self):
        return 'Project( {} )'.format(str(vars(self).values()))

    def __str__(self):
        return str(vars(self))
