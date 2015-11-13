import requests
from kb import KerberosTicket

kbsource = 'HTTP@errata.devel.redhat.com'
url = 'https://errata.devel.redhat.com/docs/draft_release_notes_xml/19347'

krb = KerberosTicket(kbsource)
headers = {"Authorization": krb.auth_header}
r = requests.get(url, headers=headers, verify=False)
print(r.status_code)
print(r.text)
# krb.verify_response(r.headers["www-authenticate"])
