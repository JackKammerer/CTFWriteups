# relevant_xkcd writeup

### Description
> Make the RelevantXKCD bot send you the flag

### Provided:

> [Link to Bot Source Code](./relevantxkcd/)

## Solution

Looking through the code I noticed that there were two components. One utilized the ChatGPT API in order to take a request, process it, and return a link to an XKCD Comic. 

The other component looked for the relevant URL, took in all of the HTML data at the address, and searched for the link next to the label: 

`"Image URL (for hotlinking/embedding):"`


The data pointed to by this link is copied, and then sent to the person interactinge with the Discord bot.


I initially realized that I could trick the bot into returning a link that was not an XKCD comic. I did this through knowing how the ChatGPT API works. The bot's "System" parameter was set to only return links to an XKCD comic. 

```
"You are RelevantXKCD bot. Your sole purpose is to provide links to xkcd comics relevant to the message given to you by the user, based on how well it matches with the information provided on the ExplainXKCD website. You must always respond with a link to an xkcd comic. When you don't know of a link to an xkcd comic relevant to the message, you must instead respond with the link 'https://xkcd.com/{number}' where {number} is a randomly chosen number between 1 and 2781. Your response is always just a single link, no explanation or justification, just one link per message that you send."
```

So, I told the bot that it's system parameter was lying to it. By telling the bot it was hacked, and it's system parameter was arbitrarily changed, and then demanding that it simply return a random URL, it would return this URL, which would cause the program to brake, as it could not identify a suitable image to return. This can be seen in the image below: 

![Image of link response](./ArbitraryLinkImage.png)


I then realized that the program would access any URL returned from the ChatGPT output. *Any* URL. I realized that I could link it to a URL I control. As OSU provides every College of Engineering student with its own HTTP accessible filespace, I created my own HTML file, that contained the correct label, "Image URL (for hotlinking/embedding):". My HTML file code is:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Web Page</title>
    </head>
    <body>
        <h1>Welcome to My Web Page</h1>
        <p>Hello, world!</p>
        
        
        Image URL (for hotlinking/embedding):<a href="file:///chal/flag.txt"></a>
    </body>
    </html>

I knew that the flag.txt file was stored in `~/chal/flag.txt`. So, I added the link `file:///~/chal/flag.txt` to the HTML file. I uploaded this to the site `https://web.engr.oregonstate.edu/~kammerej/aiChallengeWebsite/spoofsite.html` and gave the bot the following command:

![The question asked to return the flag](./SolveQuery.png)


The bot then went to the specified URL, found the file I added, and searched for that file. It pulled up the flag.txt file stored in it's own directory, downloaded it, and sent it back to me. I had finally found the correct flag. 


![Flag Answer](./flagAnswer.png)