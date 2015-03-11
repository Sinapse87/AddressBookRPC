# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import addressbook_pb2
import sys

_TIMEOUT_SECONDS = 10

# This function fills in a Person message based on user input.
def PromptForAddress():
    person = addressbook_pb2.Person()
    person.id = int(raw_input("Enter person ID number: "))
    person.name = raw_input("Enter name: ")

    email = raw_input("Enter email address (blank for none): ")
    if email != "":
        person.email = email

    while True:
        number = raw_input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = person.phone.add()
        phone_number.number = number

        type = raw_input("Is this a mobile, home, or work phone? ")
        if type == "mobile":
            phone_number.type = addressbook_pb2.Person.MOBILE
        elif type == "home":
            phone_number.type = addressbook_pb2.Person.HOME
        elif type == "work":
            phone_number.type = addressbook_pb2.Person.WORK
        else:
            print "Unknown phone type; leaving as default value."
    return person



def run():
  with addressbook_pb2.early_adopter_create_AddressBookService_stub('localhost', 50051) as stub:


    response = stub.addPerson(addressbook_pb2.addPersonRequest(person=PromptForAddress()), _TIMEOUT_SECONDS)
    print "Person added: " + response.message
    response = stub.getAddressBook(addressbook_pb2.getAddressBookRequest(addressBookName="addressBook"), _TIMEOUT_SECONDS)
    response.addressBook
    for person in response.addressBook.person:
        print person.id

if __name__ == '__main__':
    run()




