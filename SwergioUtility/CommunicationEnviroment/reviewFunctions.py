'''
Review function to evaluate if message conatains a valid namespace
'''
def HasValidNamespace(reviewer,message):
    ns = message.NameSpace
    if ns in reviewer.env._socketIONamespaces:
        return True
    else:
        return False
