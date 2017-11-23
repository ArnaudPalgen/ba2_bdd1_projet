def doFermeture(dFs, x):
	"""
	
	"""
	reste=dFs#ensemble de tuple ( DF )
	fermeture=x #ensemble d'attributs
	for couple in reste:
		w,z=couple
		if isIn(w,fermeture):
			reste.remove(couple)
			fermeture.append(z)
	return fermeture

def isIn(small, big):
	"""
	Return True if small is in big else return False
	"""
	for sItem in small:
		sItemIsInBig=False
		for bItem in big:
			if sItem==bItem:
				sItemIsInBig=True
				break
		if sItemIsInBig==False:
			return False
	return True