# api: http://www.datamuse.com/api/
	# 'ml', means like
	# 'sl', sounds like
	# 'sp', spelled like
	# 'rel_jja', popular nouns modified by the given adjective, per Google Books Ngrams
	# 'rel_jjb', Popular adjectives used to modify the given noun, per Google Books Ngrams
	# 'rel_syn', Synonyms (words contained within the same WordNet synset)
	# 'rel_ant', Antonyms (per WordNet)
	# 'rel_spc',"Kind of" (direct hypernyms, per WordNet)
	# 'rel_gen',"More general than" (direct hyponyms, per WordNet)
	# 'rel_com',"Comprises" (direct holonyms, per WordNet)
	# 'rel_par',"Part of" (direct meronyms, per WordNet)
	# 'rel_bga',Frequent followers (w′ such that P(w′|w) ≥ 0.001, per Google Books Ngrams)
	# 'rel_bgb',Frequent predecessors (w′ such that P(w|w′) ≥ 0.001, per Google Books Ngrams)
	# 'rel_rhy',Rhymes ("perfect" rhymes, per RhymeZone)
	# 'rel_nry',Approximate rhymes (per RhymeZone)
	# 'rel_hom',Homophones (sound-alike words)
	# 'rel_cns',Consonant match
	# 'v',Identifier for the vocabulary to use. If none is provided, a 550,000-term vocabulary of English words and multiword expressions is used. (The value es specifies a 500,000-term vocabulary of words from Spanish-language books. The value enwiki specifies an approximately 6 million-term vocabulary of article titles from the English-language Wikipedia, updated monthly.) Please contact us to set up a custom vocabulary for your application.
	# 'topics',	Topic words: An optional hint to the system about the theme of the document being written. Results will be skewed toward these topics. At most 5 words can be specified. Space or comma delimited. Nouns work best.
	# 'lc', Left context: An optional hint to the system about the word that appears immediately to the left of the target word in a sentence. (At this time, only a single word may be specified.)
	# 'rc', Right context: An optional hint to the system about the word that appears immediately to the right of the target word in a sentence. (At this time, only a single word may be specified.)
	# 'max', Maximum number of results to return, not to exceed 1000. (default: 100)
	# 'md' - "metadata" to include additional info possible kwargs:
		# d - definitions
		# p - parts of speech
		# s - syllable count
		# r - pronunciation
		# f - word frequency

from datamuse.datamuse import Datamuse
from datamuse.scripts import dm_to_df
from str_utils import is_one_away,too_similar
import pandas

pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', 200)


def create_tag_columns(df):
	tags = {tag for tags in df['tags'] if hasattr(tags,'__iter__') for tag in tags}
	for tag in tags:
		tagmask=df.tags.apply(lambda x: tag in x if hasattr(x,'__iter__') else False)
		df["is_"+tag]=tagmask
		# print("\n\nis_"+tag)
		# print(response[tagmask])

def pprint(pdict):
	for key,val in pdict.items():
		print(f"{key} : {val}")


class DatamuseClient():

	def __init__(self,taboo=[]):
		self.dm=Datamuse(max_results=999)
		self.taboo=taboo

	def get_safely(self,tag,qdict,safedict,avoid={}):
		print("in get safely")
		try:
			return self.get_a(tag,qdict={**qdict,**safedict})
		except:
			for key in safedict:
				avoid[key]=avoid.get(key,[])
				safedict[key]=self.get_similar(safedict[key],avoid=avoid[key])
				avoid[key].append(safedict[key])
			return self.get_safely(tag,qdict,safedict,avoid)


	def get_a(self,tag,qdict):
		print(f"qdict:")
		pprint(qdict)
		df = self.dm.words(**qdict)
		print(f"Getting '{tag}' with taboo list {self.taboo}")
		try:
			# print(df)
			df=df[~df['word'].isin(self.taboo)]
			create_tag_columns(df)
			correct_rows =df.ix[df['is_'+tag]]
			sorted_df = correct_rows.sort_values(by=['numSyllables','score'],ascending=False)
			i=0
			new_word= sorted_df.ix[sorted_df.index[i],'word']
			try:
				while too_similar(new_word,self.taboo):
					self.taboo.append(new_word)
					print("{} added to self.taboo".format(new_word))
					i +=1
					new_word=sorted_df.ix[sorted_df.index[i],'word']
			except:
				new_word = sorted_df.ix[sorted_df.index[i-1],'word']

			for piece in new_word.split(' '):
				if piece != ' ' and piece != '':
					self.taboo.append(piece)


			return new_word
		except:
			df = self.dm.words(**qdict)
			# print(df)
			raise

	def clean(self,word):
		return word.split(' ')[-1]

	def generalize(self,word):
		word=self.clean(word)
		try:
			df= self.dm.words(rel_spc=word)
			return df.ix[df.index[0],'word']
		except:
			return word

	def get_similar(self,word,avoid=[]):
		word = self.clean(word)
		try:
			# try ml (means like) instead of sl (sounds like)

			df= self.dm.words(sl=word)
			i = 0
			while df.ix[df.index[i],'word'] in avoid:
				i=i+1
			return df.ix[df.index[i],'word']
		except:
			return word


	def stanza(self,name):
		generalize = self.generalize

		print("\n\nWORD1")
		q=dict(lc='jewish',topics='politics student nonprofit activism',md='sp')
		safedict=dict(rel_rhy=name)
		trait = dmc.get_safely('n',qdict=q,safedict=safedict)

		print("WORD2")
		q=dict(rc=generalize(trait),md='sp')
		descriptor = dmc.get_safely('adj',qdict=q,safedict=safedict)

		print("WORD3")
		q=dict(topics='politics',md='sp')
		safedict=dict(rel_rhy=generalize(trait))
		verb1 = dmc.get_safely('v',qdict=q,safedict=safedict)


		print("WORD4")
		q=dict(topics='politics student nonprofit activism',md='sp')
		safedict=dict(sl=generalize(descriptor),rc=generalize(verb1))
		adverb1 = dmc.get_safely('adv',qdict=q,safedict=safedict)

		print("WORD5")
		q=dict(md='sp')
		safedict=dict(sl=generalize(trait),lc=generalize(verb1))
		verb2 = dmc.get_safely('v',qdict=q,safedict=safedict)

		print("WORD6")
		q=dict(md='sp')
		safedict=dict(sl=generalize(descriptor),rc=generalize(verb2))
		adverb2 = dmc.get_safely('adv',qdict=q,safedict=safedict)


		stanz=f"{name}, {name},\nand the {descriptor} {trait}.\nThey {adverb1} {verb1};\nthey {adverb2} {verb2}."
		return stanz

if __name__=='__main__':
	names = ['Jonathan','Adam']
	dmc =DatamuseClient(taboo=names)
	stanza1=dmc.stanza(names[0])
	stanza2=dmc.stanza(names[1])
	print(f"{names[0]} and {names[1]}\n\n{stanza1}\n\n{stanza2}")




