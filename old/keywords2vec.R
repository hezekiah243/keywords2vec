text <- "Because ejection fraction (EF) is 99 one of the most -importan't predictors of survival in patients with left ventricular (LV) dysfunction and because Packer showed a large reduction in mortality figures with carvedilol, in contrast to former studies with bisoprolol and metoprolol, we investigated if this difference in survival may be related to a difference in improvement of LV function by different beta-blockers. We searched the MEDLINE database and all reference lists of articles obtained through the search for the relation between beta-blocker treatment and improvement in EF. Forty-one studies met the criteria and we added two of our own studies. Four hundred and fifty-eight patients were treated with metoprolol with a mean follow-up of 9.5 months and a mean increase in EF of 7.4 EF units. One thousand thirty patients were treated with carvedilol with a mean follow up of 7 months and a mean increase in EF of 5.7 EF units. One hundred ninety-nine patients were treated with bucindolol with a mean follow-up of 4 months and a mean increase in EF of 4.6 EF units. Several small studies with nebivolol, atenolol, and propranolol were also studied and, when combined, the mean increase in EF was 8.6 EF units. When patients with idiopathic and ischemic cardiomyopathies were compared, the average increase in EF units was 8.5 vs. 6.0, respectively. The use of beta-blocker treatment in heart failure patients, irrespective of the etiology, improved LV function in almost all studies and it appears that the differences among beta-blockers and among etiologies is small and probably insignificant. However, there is a difference in survival rate when the various beta-blockers are compared, suggesting that mechanisms other than improvement of LV function by beta-blockers are responsible for the difference in survival."
stopwords <- c("__", "several", "on", "while", "than", "own", "you've", "itself", "above", "such", "over", "they're", "mainly", "because", "theirs", "too", "most", "must", "myself", "that", "why's", "it", "can't", "show", "overall", "she", "he'd", "it's", "can", "under", "no", "she'll", "should", "therefore", "his", "you", "various", "mustn't", "are", "doing", "really", "up", "they'd", "having", "these", "made", "we'll", "into", "you'll", "more", "ought", "especially", "hasn't", "seem", "nor", "shows", "here's", "here", "he's", "is", "at", "ml", "always", "nearly", "during", "ours", "this", "aren't", "rather", "being", "very", "shown", "them", "cannot", "just", "or", "where", "didn't", "another", "they'll", "shouldn't", "wasn't", "for", "when's", "in", "could", "off", "down", "further", "won't", "due", "however", "each", "i'd", "a", "that's", "where's", "enough", "neither", "its", "isn't", "any", "himself", "was", "they've", "etc", "there's", "whom", "both", "other", "by", "within", "not", "been", "below", "be", "once", "make", "does", "did", "before", "through", "shan't", "ourselves", "which", "kg", "their", "again", "thus", "about", "few", "either", "they", "do", "our", "you'd", "some", "don't", "although", "almost", "i'll", "often", "i'm", "she'd", "we'd", "yourselves", "using", "between", "if", "upon", "him", "we", "done", "as", "so", "hers", "me", "she's", "there", "and", "i've", "may", "but", "with", "how", "found", "her", "yours", "might", "then", "we've", "the", "yourself", "what's", "km", "without", "same", "those", "my", "perhaps", "all", "haven't", "of", "why", "has", "had", "regarding", "significantly", "when", "i", "until", "used", "would", "among", "what", "let's", "am", "how's", "who's", "weren't", "mm", "hadn't", "have", "mg", "wouldn't", "showed", "were", "an", "we're", "obtained", "themselves", "who", "your", "out", "to", "doesn't", "he", "herself", "pmid", "against", "use", "you're", "couldn't", "after", "he'll", "only", "also", "mostly", "quite", "seen", "since", "__")


regexs = matrix(
		c(
	        c(
	        	paste(stopwords, collapse = "\\b|\\b"),
	        	"’",
	        	"([^a-z0-9\u0020-\uD7FF \n'])",
	        	'[,\\.]',
	        	'(^|[ !])[0-9]+([ !]|$)',
	        	"((^|[ !])[-\\']+)|([-\\']+([ !]|$))",
	        	' *! *',
	        	'!',
	        	'(^|!)[^!\n](!|$)',
		        '!+',
        		'(^!+)|(!+$)'
	        ),
	        c("!!", "'", "!!", "!!", "!!", "!!", "!!", "!!", "!!", "!", "")
	    ),
	    nrow=11,
	    ncol=2   
)


text <- tolower(text)
print(text)
for (r in 1:nrow(regexs)) {
	text <- gsub(regexs[r,1], regexs[r,2], text, ignore.case = TRUE)
	print("\n")
	print(text)
}


# print(	array(regexs,dim = c(2,2,2)))
# print(regexs)
# for(reg in regexs){
# 	print(reg)
# }
# regex_expression <- paste(stopwords, collapse = "\\b|\\b")

#tokenized_text <- 
#print(tokenized_text)
# print(tokenized_text)

# for (token in tokenized_text)
# 	print("token")

# ("\\b" + 
# paste(stopwords, "\\b|\\b")
# 	# , "!!"),

# f <- function() {
#     y <- 10
#     g <- function(x) x + y
#     return(g)
# }
# h <- f()
# h(3)

# regex_expression = ""
# for ( stopword in stopwords )
# 	print(stopword)
#    regex_expression <<- stopword

# print(regex_expression)