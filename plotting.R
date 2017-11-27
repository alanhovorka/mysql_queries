library(tidyverse)
library(lubridate)
library(zoo)
library(stringr)

setwd('C:/Users/ahovorka/Downloads/parking/segments')

df <- read_csv('time_series_date_no_violations_per_day.csv') %>%
  arrange(ISSUEDATE) %>%
  mutate(count_weekly_avg = rollmean(count, k = 7, na.pad = T))

# weekly averages, drop the filter line to show all years. Change the year to show other years
df %>%
  filter(year(ISSUEDATE) == 2016) %>%
  ggplot(aes(x = ISSUEDATE)) %+%
  geom_line(aes(y = count), alpha = 0.1) %+%
  geom_line(aes(y = count_weekly_avg))

# monthly plots of total tickets per day
df %>%
  filter(year(ISSUEDATE) == 2016) %>%
  mutate(mon = month(ISSUEDATE)) %>%
  ggplot(aes(x = ISSUEDATE, y = count)) %+%
  geom_line() %+%
  facet_wrap(~ mon, scales = 'free_x')

# plots of cumulative total tickets by month
df %>%
  mutate(mon = month(ISSUEDATE),
         yr = year(ISSUEDATE),
         day_of_month = mday(ISSUEDATE)) %>%
  group_by(yr, mon) %>%
  mutate(count_sum = cumsum(count)) %>%
  ggplot(aes(x = day_of_month, y = count_sum, color = factor(yr))) %+%
  geom_line(alpha = 0.5) %+%
  facet_wrap(~ mon, scales = 'free_x')

# plots of cumulative fine amounut by month
df %>%
  mutate(mon = month(ISSUEDATE),
         yr = year(ISSUEDATE),
         day_of_month = mday(ISSUEDATE)) %>%
  group_by(yr, mon) %>%
  mutate(fine_totals_sum = cumsum(fine_totals)) %>%
  ggplot(aes(x = day_of_month, y = fine_totals_sum, color = factor(yr))) %+%
  geom_line(alpha = 0.5) %+%
  facet_wrap(~ mon, scales = 'free_x')

# Number of tickets by day of week all years
df %>%
  filter(year(ISSUEDATE) != 2017) %>%
  mutate(day_of_week = wday(ISSUEDATE)) %>%
  group_by(day_of_week) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = day_of_week, y = count_total)) %+%
  geom_bar(stat = 'identity')

# Total tickets by day of month for all years
df %>%
  mutate(mon = month(ISSUEDATE),
         day_of_month = mday(ISSUEDATE)) %>%
  group_by(mon, day_of_month) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = day_of_month, y = count_total)) %+%
  geom_line() %+%
  facet_wrap(~ mon)

# Day of the year average tickets by month
df %>%
  mutate(mon = month(ISSUEDATE),
         day_of_year = yday(ISSUEDATE)) %>%
  group_by(mon, day_of_year) %>%
  summarize(count_avg = mean(count)) %>%
  ggplot(aes(x = day_of_year, y = count_avg)) %+%
  geom_line() %+%
  facet_wrap(~ mon, scales = 'free_x')

# Total tickets day of week by year
df %>%
  mutate(yr = year(ISSUEDATE),
         day_of_week = wday(ISSUEDATE)) %>%
  group_by(yr, day_of_week) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = day_of_week, y = count_total)) %+%
  geom_bar(stat = 'identity') %+%
  facet_wrap(~ yr)

# Avg. tickets day of week by year
df %>%
  mutate(yr = year(ISSUEDATE),
         day_of_week = wday(ISSUEDATE)) %>%
  group_by(yr, day_of_week) %>%
  summarize(count_avg = mean(count)) %>%
  ggplot(aes(x = day_of_week, y = count_avg)) %+%
  geom_bar(stat = 'identity') %+%
  facet_wrap(~ yr)


# See if there are any days with no tickets
# d0 <- ymd('2009-01-01')
# for (i in 0:(365*9)) {
#   d <- d0 + days(i)
#   n <- df %>% filter(d0 == ISSUEDATE) %>% nrow()
#   if (n < 1) {
#     print(d)
#     print(n)
#   }
# }

df_hours <- read_csv('hour_of_day/hour_of_day_by_day_of_week_by_year.csv') %>%
  mutate(hour_of_day = str_replace(hour_of_day, 'pm', ':00pm'),
         hour_of_day = str_replace(hour_of_day, 'am', ':00am'),
         hour_of_day = ymd_hm(str_c('01-01-01 ', hour_of_day)))

# Hour of day (all years, all days of week) 
df_hours %>%
  group_by(hour_of_day) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = hour_of_day, y = count_total)) %+%
  geom_bar(stat = 'identity')

# Hour of day by year (all days of week) 
df_hours %>%
  group_by(year, hour_of_day) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = hour_of_day, y = count_total)) %+%
  geom_bar(stat = 'identity') %+%
  facet_wrap(~ year)

# Hour of day by days of week (all years)
df_hours %>%
  group_by(dayofweek, hour_of_day) %>%
  summarize(count_total = sum(count)) %>%
  ggplot(aes(x = hour_of_day, y = count_total)) %+%
  geom_bar(stat = 'identity') %+%
  facet_wrap(~ dayofweek)