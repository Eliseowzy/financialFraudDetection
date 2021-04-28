library(tidytext)
library(textdata)
library(readr)
library(tibble)
library(dplyr)

input_dir = "data/email_corpus_by_selected_person"
file_list <- list.files(input_dir)
i = 1;
for (input in file_list){
  sentiment_score <- get_sentiments_score(input_dir, input)
  if (i == 1) {
    sentiment_score %>% write_csv(., "data/sentiment_score_by_person/sentiment_score_by_person_by_date.csv", 
                                col_names = TRUE , append = TRUE )
  } else {
    sentiment_score %>% write_csv(., "data/sentiment_score_by_person/sentiment_score_by_person_by_date.csv", 
                                  col_names = FALSE , append = TRUE )
  }
  i <- i+1
  
}

intput = ""
get_sentiments_score <- function(input_dir, input){
  data = read_csv(paste(input_dir, "/", input, sep = ""))
  data$date = as.Date(data$Time_stamp)
  tibble_data <- as_tibble(data)
  tidy_text <- tibble_data %>% 
    unnest_tokens(word, Text) 
  tidy_text <- tidy_text %>%
    anti_join(stop_words)
  afinn <- get_sentiments("afinn")
  afinn <- tidy_text %>% 
    inner_join(afinn) %>%
    group_by(FirstName, LastName, date) %>% 
    summarise(sentiment = sum(value)) %>%
    mutate(method = "AFINN")
  return(afinn)
}



