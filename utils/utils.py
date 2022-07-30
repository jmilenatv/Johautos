def get_secure_nro_cta_mode(nro_cta):
	# TODO: This is not too secure absoutly.
	secured_nro_cta_mode = "{first}***********{last}".format(
		first=str(nro_cta)[:2],
		last=str(nro_cta)[len(str(nro_cta))-2:]
	)
	
	return secured_nro_cta_mode