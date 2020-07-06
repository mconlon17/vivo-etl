def orcid(val):
    return     dict(orcid=val)

def department(val):
    return     dict(department=val)

def name(val):
    return     dict(name=val)

def pmid (val):
    return dict(pmid=val)

def position(val):
    vals = val.split("|")
    keys = ["start", "end", "title", "unit"]
    return dict(position=dict(zip(keys,vals)))

def education(val):
    vals = val.split("|")
    keys = ["date", "degree", "topic", "awarder"]
    return dict(education=dict(zip(keys,vals)))

def overview(val):
    return dict(overview=val)

def photo(val):
    return dict(photo=val)

def email(val):
    return dict(email=val)

def local_id(val):
    return dict(local_id=val)

def comment(val):
    return dict(comment=val)

def grant(val):
    vals = val.split("|")
    keys = ["date", "id", "awarder", "amount"]
    return dict(grant=dict(zip(keys,vals)))

def teaching(val):
    vals = val.split("|")
    keys = ["date", "course_id"]
    return dict(teaching=dict(zip(keys,vals)))

def address(val):
    vals = val.split("|")
    keys = ["kind", "address1", "address2", "city", "state", "zip", "country"]
    return dict(address=dict(zip(keys,vals)))
    
def topic(val):
    return dict(topic=val)

def title(val):
    return dict(title=val)

def phone(val):
    vals = val.split("|")
    keys = ["kind", "number"]
    return dict(phone=dict(zip(keys,vals)))

def website(val):
    vals = val.split("|")
    keys = ["kind", "url"]
    return dict(website=dict(zip(keys,vals)))

def language(val):
    vals = val.split("|")
    keys = ["capability", "iso639"]
    return dict(language=dict(zip(keys,vals)))
    
    