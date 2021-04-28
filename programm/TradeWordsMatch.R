# Author: Li Zhixin
# Last Modified Date: 2021-04-27

library(rJava)
library(Rwordseg)
library(tm)
library(stylo)


# ============================================
# ========== Self-defined Functions ==========
# ============================================
wordInfoGen <- function(text, stopwords, dictionary){
  result <- list()
  text <- tolower(text)
  text = gsub("'s"," is ", text)
  text = gsub("'s"," is ", text)
  text = gsub(";"," ", text)
  text = gsub(","," ", text)
  text = gsub("'"," ", text)
  text = gsub(":"," ", text)
  text = gsub("-"," ", text)
  text = gsub("`"," ", text)
  text = gsub("\n"," ", text)
  text = gsub('\"'," ", text, fixed = TRUE)
  text = gsub("?"," ", text, fixed = TRUE)
  text = gsub("*"," ", text, fixed = TRUE)
  text = gsub("."," ", text, fixed = TRUE)
  
  # Remove stop words
  docs <- Corpus(VectorSource(text))
  docs <- tm_map(docs, removePunctuation)
  docs <- tm_map(docs, removeWords, stopwords('english'))
  docs_res <- strsplit(x=docs$content, split=" ")
  clean_text <- delete.stop.words(docs_res, stop.words=stopwords)
  clean_text <- lapply(clean_text, function(z){z[!is.na(z) & z!= ""]})
  clean_text <- as.vector(unlist(clean_text))
  
  wordsFreq <- data.frame(table(clean_text))
  wordsFreq <- wordsFreq[which(nchar(as.vector(wordsFreq$clean_text)) < 25),]
  names(wordsFreq) <- c("words", "freq")
  
  # Intersect characters
  intersect_char <- intersect(clean_text, dictionary)
  if (length(intersect_char) > 0){
    intersect_char <- data.frame(table(intersect_char))
    names(intersect_char) <- c("words", "match")
    words_info <- merge(wordsFreq, intersect_char, by="words", all=T)
  } else {
    words_info <- cbind(wordsFreq, match=rep(0, times=nrow(wordsFreq)))
  }
  
  words_info[is.na(words_info)] <- 0
  result[[1]] <- nrow(intersect_char)
  result[[2]] <- words_info
  return(result)
}

# ============================================
# ================ Code Start ================
# ============================================
file_list <- list.files("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\email_corpus_person")
setwd("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\email_corpus_person")
# file_list <- list.files("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\email_corpus_by_alphabet\\k")
# file_list <- list.files("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\email_corpus_by_selected_person")
# file_list <- file_list[grepl("^[A-Z]", file_list)]
file_list <- file_list[grepl("^[a-z]", file_list)]
file_list
stopwords <- readLines("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\stopwords\\stopword.txt")
stopwords = strsplit(x=stopwords, split=", ")
stopwords <- as.vector(unlist(stopwords))
typeof(stopwords)
dictionary <- readLines("E:\\RProj\\project\\financialFraudDetection\\programm\\data\\word_list\\dictionary_words.txt")
dictionary <- strsplit(x=dictionary, split=", ")
dictionary <- as.vector(unlist(dictionary))
dictionary <- tolower(dictionary)
dictionary

n <- 1
data_list <- list()
for (i in file_list){
  data <- read.csv(i)
  data_list[[n]] <- data
  n <- n + 1
}

length(data_list)

# # ============================================
# # ========== Simple Version Testing ==========
# # ============================================
# data <- data.frame(data_list[[1]])
# nrow(data)
# text <- data[1, "Text"]
# res <- wordInfoGen(text)
# res

# ============================================
# ========== Person Version Testing ==========
# ============================================
match_amt <- c()

data_row_amt <- c()
for (d in 1:length(data_list)){
  data <- data.frame(data_list[[d]])
  data_row_amt <- c(data_row_amt, nrow(data))
}

for (d in 1:length(data_list)){
  data <- data.frame(data_list[[d]])
  n <- nrow(data)
  text <- c()
  for (i in 1:n){
    text <- c(text, data[i,"Text"])
  }
  text <- paste(text, collapse = " ")
  freq_res <- wordInfoGen(text, stopwords, dictionary)
  freq_res_df <- freq_res[[2]]
  match_word_df <- freq_res_df[which(freq_res_df$match > 0),]
  match_word_amt <- sum(match_word_df$freq)
  match_amt <- c(match_amt, match_word_amt)
}
match_amt
email_match <- as.data.frame(cbind(file_list, match_amt))
email_match$match_amt <- as.integer(email_match$match_amt)
final_res <- email_match[order(-email_match$match_amt),]
email_match
final_res

setwd("E:\\RProj\\project\\financialFraudDetection\\programm\\data")
write.csv(final_res, "final_result2.csv")

# ============================================
# =============== Testing Part ===============
# ============================================
# Single Test
file_list[43]
d <- read.csv(file_list[43])
t <- c()
for (i in 1:nrow(d)){
  t <- c(t, d[i, "Text"])
}
t <- paste(t, collapse = " ")
s_freq_res <- wordInfoGen(t, stopwords, dictionary)[[2]]
s_freq_res[which(s_freq_res$match==1),]
wordInfoGen(t, stopwords, dictionary)[[1]]

# "karen_burke_enron_com.csv", karen_buckley_enron_com.csv

a <- c("a", "b", "c")
b <- c("a", "b", "d")
intersect_char <- intersect(a, b)
length(intersect_char)==0
if (length(intersect_char)==0){
  intersect_char <- data.frame(intersect_char="none", Freq=0)
} else {
  intersect_char <- data.frame(table(intersect_char))
}
intersect_char
intersect_char <- cbind(intersect_char, newlist=rep(0, times=nrow(intersect_char)))
intersect_char
