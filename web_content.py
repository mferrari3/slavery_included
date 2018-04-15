from bs4 import BeautifulSoup

def get_article_elements( url ):
    soup = BeautifulSoup( urllib.request.urlopen( url ), "html.parser")

    title = soup.find("meta",  property="og:title")

    #site_name = soup.find("meta",  property="og:site_name")
    #if site_name == []:
     #   site_name = soup.find( )

     
def ibm_query_to_html( df,ibm_string):
    # Remove unnecessary index.
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # Combine title and link into href.
    #print(df.columns)
    #print()
    def href_format(row):
        href = '<a href="{0}">{1}</a>'
        return href.format(row['URL'], row['Title'])
    
    df['Article'] = df.apply(href_format, axis=1)
    # Remove title and link.
    df.drop(columns=['Title', 'URL'], inplace=True)
    # Turn df to html to single string.
    return ''.join(df.to_html(escape=False,
                              columns=['Sentiment', 'Article', 'Relevance'],
                              index=False))
