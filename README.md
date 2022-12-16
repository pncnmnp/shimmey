# Shimmey
End-to-end privacy for link shimming using private information retrieval

# Our Research

## What is the Problem?
When a user clicks on a particular URL on a web page, the resulting HTTP header consists of an HTTP referrer header. 
This referrer header contains a complete or partial address of the source from which a particular resource has been requested by the user. 
For instance, if you are at a URL say [https://news.ycombinator.com/item?id=28748203](https://news.ycombinator.com/item?id=28748203) and you click on a URL redirecting you to Facebook, Facebook would know that you were redirected from Hacker News.
They can then use this data for analytics, optimized caching, and even targeted advertising. 
This referrer header usually contains the origin, path, and query string mentioned in the URL. 
However, it does not contain information stored in the URL fragments (a fragment identifier usually starts with a hash mark # and contains information about sections and sub-sections).

To protect against the malicious use of HTTP referrer headers, the _Referrer-Policy HTTP header_ was introduced. 
This helps control the amount of information a user would like to share with the destination URLs. 
For instance, a referrer policy like `Referrer-Policy: origin` would inform the browser to only send the origin information in the referrer header. 
For instance, using the example mentioned above, Facebook would get [https://news.ycombinator.com/](https://news.ycombinator.com/) and not the id.

While modern browsers support Referrer-Policy, the partially legacy browsers such as older versions of Safari, Samsung Internet, and Opera only support `rel=noreferrer`, which is a type of link relation that can be mentioned in HTML’s `a`, `area`, or `link` elements. 
While this tag prevents the browser to send the page address as a referrer to a destination, it is necessary for this link type to be explicitly mentioned in the HTML tags.

Then there exists fully legacy browsers that do not support any HTTP referrer privacy mechanisms. 
For instance, [Frank Li](https://www.usenix.org/system/files/sec20-li-frank.pdf) mentions that 23% of the South Korean clients that used Facebook were using fully legacy browsers due to the high usage of Internet Explorer in the country.
Furthermore, this was also true for many African nations.

In order to mitigate this issue, websites such as Facebook and Gmail use link-shimming to pass the URL to an intermediate endpoint that modifies the HTTP referrer such that only the origin is visible, and also performs a scan of the URL to ensure that the user is clicking on a non-malicious URL. 
However, there is a privacy concern - these websites can track every URL clicked by the user.

**To mitigate this issue, we propose an end-to-end privacy scheme using Private Information Retrieval.**

## How do bloom filters fit in?
To understand how this scheme works, we first need to understand how we can detect malicious URLs using a bloom filter.
[Here's a great answer from Stack Overflow that dives into this topic](https://stackoverflow.com/a/30247022/7543474).

However, there is an issue if we use a similar scheme for link-shimming. 
What if the server creates and stores an inverted index of `k` indices corresponding to their URLs? 
This can be done by first fetching the URLs mentioned in say [the Common Crawl dataset](https://commoncrawl.org/) and then supplementing it with the URLs mentioned in [uBlock Origin’s blocklist](https://github.com/gorhill/uBlock).
Now, a malicious server can again track every single link clicked by the user on their domain.

## What is Private Information Retrieval
To mitigate this issue, we propose using a private information retrieval (PIR) scheme.
Private Information Retrieval is a primitive used to hide the identity of the data items that were queried for, without hiding the existence of the interaction with the user. 
A great analogy for this would be to imagine buying in a store without letting the seller know what you bought. 
PIR schemes usually assume that the server is _semi-honest_. 
This means that the server is trustable in terms of honestly following the protocol.
It knows every bit of data and can record clients’ requests/queries. 
However, it cannot act in a malicious manner - i.e. it cannot collude with other parties, drop messages, or change messages.

## What are we proposing?
A trivial PIR scheme would be when the server sends the entire database to the user. 
Assuming a database of size `n`, such a communication can have a `O(n)` overhead. 
Therefore, such schemes are not optimal. 
To solve the problem of enabling end-to-end privacy during link-shimming, **we propose using a variant of the K-server PIR scheme** - a 2-server PIR architecture that contains an `O(n^0.5)` communication overhead.

## Our approach
![Screen Shot 2022-12-16 at 1 18 55 AM](https://user-images.githubusercontent.com/24948340/208035191-5c5971e3-b69b-423f-8a6a-c82811a41807.png)

As the name suggests, this architecture requires 2 non-malicious servers. 
Each server will store the bloom filter (this is a bit-array with `m` bits) which encodes the list of malicious servers (for simplicity, we call this list a database). 
This information is then queried by a particular client using PIR. 
We first start by making the $m$ bit array on the server side as a `m^0.5 x m^0.5` matrix. 
Each row of this matrix will then contain `m^0.5` bits from the database. 
Then on the client side, when a user clicks on a URL, the URL is hashed `T` times (this number is chosen in a way that minimizes the rate of false positives of the Bloom filter). 
Once the hashing is completed, we get a list of `T` indices. 
Our goal is to then find out the corresponding values at these indices from the server.

For each such index (say `I’`), we start by querying the first server. 
This is done by creating a random string `S’` of length `m^0.5` and sending it to the first server. 
The first server uses `S’` and performs dot product with each row of the database and XORs the results across. 
The end result is a column of bits `C’`. It sends `C’` back to the client. 
The client then queries the second server, only this time it XORs `S’` with a one-hot vector where the `I’` bit is one. 
Let’s call this resulting string `S''`. 
When the second server receives this information, it performs the exact same calculation as the first server and returns a column of bits `C''` back to the client. 
The client then fetches the `I’` index from `C’` and `C''` and XORs it to obtain the value of the index stored at `I’`.
A similar operation can then be performed `T` times for all the indices.

If at any position the bit is zero, we can say that the URL is not malicious. 
However, if it is one, it might be malicious (this would depend on the false positive rate of the Bloom filter). 
If the link is malicious, we can then inform the user about it - using the same strategies as the existing link-shimming schemes. 
However, if it is non-malicious, we can update the HTTP referrer on the client side itself. 
In this way, we show how Private Membership Testing can be done for link-shimming using PIR, and how this ensures end-to-end privacy.
