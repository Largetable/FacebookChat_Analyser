from bs4 import BeautifulSoup
import os
import pandas as pd
import dateparser
from datetime import timedelta    #calculate longest inactive period
import matplotlib.pyplot as plt

def get_records():
    records=[]
    directory = '.'
    for root, dirnames, filenames in os.walk(directory):

        for filename in filenames:
            if filename.endswith('.html'):
                soup = BeautifulSoup(open(filename, encoding="utf8").read(), features="lxml")
                results = soup.find_all('div', attrs={'class':'pam _3-95 _2pi0 _2lej uiBoxWhite noborder'})
                for message in results:
                    informations=message.contents
                    name=informations[0].text
                    if (name == 'Mohamed Amara'):
                        name=0
                    else:
                        name=1
                    text_message=informations[1].text
                    date=informations[2].text[:-8]
                    records.append((name, text_message, date))
    return records

def make_df(records):
    df=pd.DataFrame(records, columns=['name', 'message', 'date'])
    return df
def get_msgs_count(df):
    total_msgs=df.shape[0]
    msgs_by_0=df.loc[df['name']==0].shape[0]
    msgs_by_1=total_msgs-msgs_by_0
    return (total_msgs, msgs_by_0, msgs_by_1)

def get_dates_count(df):
    dates_count = df.date.value_counts().reset_index().rename(columns={'index': 'dates', 'date': 'counts'})
    dates_count['dates']=dates_count.apply(lambda x: dateparser.parse(x['dates']), axis=1)
    dates_count=dates_count.sort_values(by='dates', ascending=False)
    dates_count=dates_count.reset_index().rename(columns={'index':'position'})
    return dates_count

def print_avrg_msgs(messages, dates):
    print("""Total messages sent by both user = {}\nMessages sent by user 0 (you): {}\nMessages sent by the other user: {}
     """.format(messages[0], messages[1], messages[2] ))
    print("Average number of msgs sent a day by you: {:.2f}".format(messages[1]/dates.shape[0]))
    print("Average number of msgs sent a day by other user: {:.2f}".format(messages[2]/dates.shape[0]))

def get_counts_sorted(dates_count):
    counts_sorted=dates_count.sort_values(by='position', ascending=True)
    return counts_sorted
def print_longest_inactive_dates(dates_count):
    dates=dates_count['dates']
    aux=(dates.iloc[1], dates.iloc[0], dates.iloc[0]-dates.iloc[1])
    for i in range (dates.shape[0]-1):
        d=dates.iloc[i]-dates.iloc[i+1]
        if (d>aux[2]):
            aux=(dates.iloc[i+1], dates.iloc[i], d)   
    print("Longest number of days without talking = {} days".format(aux[2].days))


def plot_top_dates_msgs(count_sorted):
    top_10dates=count_sorted.iloc[0:10, 0] #preparing X axis
    top_10dates=top_10dates.dt.date

    top_counts=count_sorted.iloc[0:10, 1]  #preparing Y axis
    top_df=pd.DataFrame({'top 10 dates':top_10dates, 'messages per day':top_counts})#plotting X AND Y
    top_df.plot.bar(x='top 10 dates', y='messages per day') 
    plt.show()
def main():
    records=get_records()
    df=make_df(records)
    messages=get_msgs_count(df)
    dates_count=get_dates_count(df)
    print_avrg_msgs(messages, dates_count)
    dates_count.set_index('position', inplace=True)
    counts_sorted=get_counts_sorted(dates_count)
    print_longest_inactive_dates(dates_count)

    plot_top_dates_msgs(counts_sorted)



main()

