import string
import os
import re

stops = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

d = dict()
punc = string.punctuation
list_ = [os.path.join(root,f) for root, dirs, files in os.walk(".") for f in files if f.endswith(".md")]

for file_ in list_:
	with open(file_, "r") as f:
		contents = f.read()

	contents = re.sub("```[^`]*```", "", contents) # exclude code blocks
	contents = re.sub("`[^`]*`", "", contents)     # exclude inline code
	contents = re.sub(r"\n\S*:", " ", contents)    # exclude (single-word) yaml keys
	contents = re.sub(r"> \[!.*\]", "", contents)  # exclude callout type identifiers
	contents = contents.lower()

	words = [word.strip(punc) for word in contents.split() if word.strip(punc) != '']
	words = [word for word in words if word not in stops]
	words = [word for word in words if re.search(r"\d|\W", word) == None]

	for word in words:
		if word in d:
			d[word] = d[word] + 1
		else:
			d[word] = 1

sorted = {key: value for key, value in sorted(d.items(), key=lambda item: item[1], reverse=True)}

with open("results.csv", "w+") as f:
	f.write("term,freq")

	for key in list(sorted.keys()):
		f.write("\n" + key + "," + str(sorted[key]))
