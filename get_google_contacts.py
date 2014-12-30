#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Originally copied from https://gdata-python-client.googlecode.com/hg/samples/contacts/contacts_example.py authored by (Jeffrey Scudder)
# Changed made by (Chirag Gada) on 29th December 2014


import sys
import getopt
import getpass
import atom
import gdata.contacts.data
import gdata.contacts.client

class ContactsApp(object):

  def __init__(self, email, password):
    """Constructor for the ContactsApp object.
    
    Takes an email and password corresponding to a gmail account to
    demonstrate the functionality of the Contacts feed.
    
    Args:
      email: [string] The e-mail address of the account to use for the sample.
      password: [string] The password corresponding to the account specified by
          the email parameter.
    
    Yields:
      A ContactsApp object used to run the sample demonstrating the
      functionality of the Contacts feed.
    """
    self.gd_client = gdata.contacts.client.ContactsClient(source='Contacts-Sync-App-1')
    self.gd_client.ClientLogin(email, password, self.gd_client.source)
    
  def PrintFeed(self, feed, ctr=0):
    """Prints out the contents of a feed to the console.
   
    Args:
      feed: A gdata.contacts.ContactsFeed instance.
      ctr: [int] The number of entries in this feed previously printed. This
          allows continuous entry numbers when paging through a feed.
    
    Returns:
      The number of entries printed, including those previously printed as
      specified in ctr. This is for passing as an argument to ctr on
      successive calls to this method.
    
    """
    if not feed.entry:
      print '\nNo entries in feed.\n'
      return 0
    for i, entry in enumerate(feed.entry):
      print '\n%s %s' % (ctr+i+1, entry.title.text)
      if entry.content:
        print '    %s' % (entry.content.text)
      for email in entry.email:
        if email.primary and email.primary == 'true':
          print '    %s' % (email.address)
      # Show the contact groups that this contact is a member of.
      for group in entry.group_membership_info:
        print '    Member of group: %s' % (group.href)
      # Display extended properties.
      for extended_property in entry.extended_property:
        if extended_property.value:
          value = extended_property.value
        else:
          value = extended_property.GetXmlBlob()
        print '    Extended Property %s: %s' % (extended_property.name, value)
    return len(feed.entry) + ctr

  def PrintPaginatedFeed(self, feed, print_method):
    """ Print all pages of a paginated feed.
    
    This will iterate through a paginated feed, requesting each page and
    printing the entries contained therein.
    
    Args:
      feed: A gdata.contacts.ContactsFeed instance.
      print_method: The method which will be used to print each page of the
          feed. Must accept these two named arguments:
              feed: A gdata.contacts.ContactsFeed instance.
              ctr: [int] The number of entries in this feed previously
                  printed. This allows continuous entry numbers when paging
                  through a feed.
    """
    ctr = 0
    while feed:
      # Print contents of current feed
      ctr = print_method(feed=feed, ctr=ctr)
      # Prepare for next feed iteration
      next = feed.GetNextLink()
      feed = None
      if next:
        if self.PromptOperationShouldContinue():
          # Another feed is available, and the user has given us permission
          # to fetch it
          feed = self.gd_client.GetContacts(uri=next.href)
        else:
          # User has asked us to terminate
          feed = None
          
  def PromptOperationShouldContinue(self):
    """ Display a "Continue" prompt.
    
    This give is used to give users a chance to break out of a loop, just in
    case they have too many contacts/groups.
    
    Returns:
      A boolean value, True if the current operation should continue, False if
      the current operation should terminate.
    """
    while True:
      input = raw_input("Continue [Y/n]? ")
      if input is 'N' or input is 'n':
        return False
      elif input is 'Y' or input is 'y' or input is '':
        return True
  
  def ListAllContacts(self):
    """Retrieves a list of contacts and displays name and primary email."""
    query = gdata.contacts.client.ContactsQuery()
    query.max_results = 2500
    feed = self.gd_client.GetContacts(query=query)
    self.PrintPaginatedFeed(feed, self.PrintContactsFeed)
    
  def PrintContactsFeed(self, feed, ctr):
    if not feed.entry:
      print '\nNo contacts in feed.\n'
      return 0
    for i, entry in enumerate(feed.entry):           
      if not entry.name is None:
        family_name = entry.name.family_name is None and " " or entry.name.family_name.text
        full_name = entry.name.full_name is None and " " or entry.name.full_name.text
        given_name = entry.name.given_name is None and " " or entry.name.given_name.text
        if not entry.phone_number is None and len(entry.phone_number) > 0:
          phone_number = entry.phone_number[0].text         
          continue
          print '\n%s %s: %s - %s (%s)' % (ctr+i+1, full_name, given_name, family_name, phone_number) 
        else:          
          print '\n%s %s: %s - %s' % (ctr+i+1, full_name, given_name, family_name) 
          self.gd_client.Delete(entry)
      else:
        print '\n%s %s (title)' % (ctr+i+1, entry.title.text)    
    return len(feed.entry) + ctr
    
  def UpdateContactMenu(self):
    selected_entry = self._SelectContact()
    new_name = raw_input('Enter a new name for the contact: ')
    if not selected_entry.name:
      selected_entry.name = gdata.data.Name()
    selected_entry.name.full_name = gdata.data.FullName(text=new_name)
    self.gd_client.Update(selected_entry)
    
    
def main():
  """Demonstrates use of the Contacts extension using the ContactsApp object."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
  except getopt.error, msg:
    print 'python contacts_example.py --user [username] --pw [password]'
    sys.exit(2)

  user = ''
  pw = ''
  # Process options
  for option, arg in opts:
    if option == '--user':
      user = arg
    elif option == '--pw':
      pw = arg

  while not user:
    print 'NOTE: Please run this only if you know what you are doing!!!'
    user = raw_input('Please enter your username: ')
  while not pw:
    pw = getpass.getpass()
    if not pw:
      print 'Password cannot be blank.'


  try:
    getContacts = ContactsApp(user, pw)
  except gdata.client.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  getContacts.ListAllContacts()


if __name__ == '__main__':
  main()
