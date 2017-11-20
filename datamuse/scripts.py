import pandas as pd

def dm_to_df(datamuse_response):
	"""Converts the json response of the datamuse API into a DataFrame
	:datamuse_response
		[{'word': 'foo', 'score': 100}, {'word': 'bar', 'score': 120}]
	"""
	info_words=set([key for response in datamuse_response for key in response ])


	reformatted = {
		info_word: [response.get(info_word,None) for response in datamuse_response] for info_word in info_words
	}
	# reformatted = {
	# 	'word': [response.get('word',None) for response in datamuse_response],
	# 	'score': [response.get('score',None) for response in datamuse_response]
	# }
	return pd.DataFrame.from_dict(reformatted)
