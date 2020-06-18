# Crawler-Selenium-Screenshot

* The script crawls through urls (max 50) of a page
* Based on the internal links, it crawls further
* The code then filters and finds the immediate URLS (assuming the usual navigation bar nature)
* Create a folder dynamically with a unique filename
* Grab a screenshot (full page) of all the immediate web pages (as PNG), name them dynamically and store them in a folder

Output process
![alt text](https://github.com/kanishk307/Crawler-Selenium-Screenshot/blob/master/Output/OutputInJupyter.png?raw=true)

Folder containing Screenshots
![alt text](https://github.com/kanishk307/Crawler-Selenium-Screenshot/blob/master/Output/ImgsInFolder.png?raw=true)

Inputs that need to be provided : Base URL (eg: https://umd.edu/virusinfo OR https://www.ucf.edu/coronavirus)

You can run the python file as it is (with required imports). I think it is interactive to run the python notebook.

Constraint: chromedriver's location needs to be specified in the PATH

*Folder naming scheme : URL_Screenshots
*File naming scheme: URL-page_slug
