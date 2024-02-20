#Importing All Req Module
from flask import Flask , request , jsonify , render_template
import requests
from bs4 import BeautifulSoup
from lxml import html
import urllib.parse

###############################################################################################################

#Creating All Function to Perform Operation

#Extract Home /Search Tiles
def extract_Home(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse the HTML content using lxml
        tree = html.fromstring(response.content)

        # Find all <li> elements within the <ul>
        li_elements = tree.xpath("//ul[@class='items']/li")

        # Iterate over each <li> element and extract information
        Big_Data = dict()
        x = 0
        for li in li_elements:
            # Extract img src from class="img"
            img_src = li.xpath(".//div[@class='img']/a/img/@src")[0] if li.xpath(".//div[@class='img']/a/img/@src") else None

            # Extract title from class="name"
            title = li.xpath(".//p[@class='name']/a/@title")[0] if li.xpath(".//p[@class='name']/a/@title") else None

            # Extract episode from class="episode"
            episode = li.xpath(".//p[@class='episode']/text()")[0] if li.xpath(".//p[@class='episode']/text()") else None

            
            Anime_url   =  li.xpath(".//div[@class='img']/a/@href")[0] if li.xpath(".//div[@class='img']/a/@href") else None
            Anime_url = convert_url(Anime_url)
            #Anime_url = convert_Url(Anime_url,"category",None)
            print("Anime Url : ",Anime_url)
            #Releaded date
            released_date = li.xpath(".//p[@class='released']/text()")[0] if li.xpath(".//p[@class='released']/text()") else None
            
            Data = {
                    "Img_Src": img_src,
                    "Title": title,
                    "Episode": str(episode),
                    "Anime_Url":Anime_url,
                    "Released_date":released_date
                   }
            Big_Data["Data" + str(x) ] = Data
            x += 1
             
        return Big_Data
              # Separator between entries



    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")

#Extract Content / plot/ect
def extract_Anime_Content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse the HTML content using lxml
        tree = html.fromstring(response.content)

        # Extract title
        title = tree.xpath("//div[@class='anime_info_body_bg']/h1/text()")[0] if tree.xpath("//div[@class='anime_info_body_bg']/h1/text()") else None

        # Extract Type
        type_info = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Type: ']/following-sibling::a/text()")[0] if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Type: ']/following-sibling::a/text()") else None

        # Extract Plot Summary
        plot_summary = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Plot Summary: ']/following-sibling::text()")[0].strip() if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Plot Summary: ']/following-sibling::text()") else None

        # Extract Genre
        genre = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Genre: ']/following-sibling::a/text()") if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Genre: ']/following-sibling::a/text()") else None

        # Extract Released
        released = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Released: ']/following-sibling::text()")[0].strip() if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Released: ']/following-sibling::text()") else None

        # Extract Status
        status = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Status: ']/following-sibling::a/text()")[0] if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Status: ']/following-sibling::a/text()") else None

        # Extract Other Name
        other_name = tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Other name: ']/following-sibling::text()")[0].strip() if tree.xpath("//div[@class='anime_info_body_bg']/p[@class='type']/span[text()='Other name: ']/following-sibling::text()") else None

        Episode = tree.xpath("//div[@class='anime_video_body']//a[@class='active']/@ep_end")[0] if tree.xpath("//div[@class='anime_video_body']//a[@class='active']/@ep_end") else None
       
        img_src = tree.xpath("//div[@class='anime_info_body_bg']/img/@src")[0] if tree.xpath("//div[@class='anime_info_body_bg']/img/@src") else None
        # Print extracted information
        Data = {
        "Title": title,
        "Type": type_info,
        "Plot Summary": plot_summary,
        "Genre": ', '.join(genre) if genre else None,
        "Released": released,
        "Status": status,
        "Other Name": other_name,
        "Total No. Of Episode": Episode,
        "Img_Src" : img_src
        }
        return(Data)
        

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")

#Extract embedded link 
def extract_embedded_Video(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div containing the download link
        favorites_div = soup.find('div', class_='favorites_book')

        # Extract the download URL
        download_url = None
        if favorites_div:
            download_a = favorites_div.find('li', class_='dowloads').find('a')
            if download_a:
                download_url = download_a.get('href')

        # Find all iframe elements in the HTML
        iframe_elements = soup.find_all('iframe')

        # Extract and print the src attribute of each iframe
        for iframe in iframe_elements:
            src_attribute = iframe.get('src')
            if src_attribute:
                return {
                    "Video Player Link": src_attribute,
                    "Download URL": download_url
                }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")


###############################################################################################################

class Urls():
    Suffix = "https://anitaku.to"
    Home   = Suffix + "/home.html"
    Search = Suffix + "/search.html?keyword=solo%20leveling"
    Category = Suffix + "/category/ore-dake-level-up-na-ken" 
    Episode  = Suffix +"/ore-dake-level-up-na-ken-episode-1" 

###############################################################################################################


def convert_url(url):
    if "-episode-" in url :   
        url = url[0:url.index("-episode-")]
        return url
    else : 
        if "/category/" in url: 
            url = url.replace("/category/","")
            return url

def convert_search_url(url):
    encoded_query = str(urllib.parse.quote(url))
    search_url = f"https://anitaku.to/search.html?keyword={encoded_query}"
    return search_url

def convert_player_url(url, action = 0):
    if action == 0 :
        url = url.replace("-tv","")
        return url
    else: 
        return url
###############################################################################################################


def content_html(data,episode_data):
    content_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TV Show Details</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        header {
            background-color: #3498db;
            padding: 15px;
            text-align: center;
            color: #fff;
        }

        nav {
            background-color: #2c3e50;
            overflow: hidden;
        }

        nav a {
            float: left;
            display: block;
            color: #ecf0f1;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }

        nav a:hover {
            background-color: #bdc3c7;
            color: #333;
        }

        .tv-show {
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fff;
            margin: 20px;
        }

        .tv-show img {
            width: 10%;
            height: auto;
            border-bottom: 1px solid #ddd;
        }

        .tv-show-info {
            padding: 20px;
        }

        h2, p {
            margin: 0 0 10px;
        }

        .episode-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .episode-list-item {
            margin-bottom: 10px;
        }

        .episode-link {
            text-decoration: none;
            color: #2c3e50;
            display: block;
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        .episode-link:hover {
            background-color: #bdc3c7;
        }
    </style>
</head>
<body>

<header>
    <h1>TV Show Details</h1>
</header>

<nav>
    <h1>HTML Links</h1>
    <a href="../Home">Home</a>
    <a href="../Search">Search</a>
    <a href="../Player">Player</a>
    <a href="#" target="_blank"  onclick="redirectToDataUrl()">Data</a>

    <script>
    function redirectToDataUrl() {
      // Get the current URL and append '/Data' to it
      var dataUrl = window.location.href + "/Data";

      // Redirect to the constructed URL
      window.location.href = dataUrl;
    }
  </script>



</nav>
"""

    content_html2 = f"""
    <ul class="episode-list">
        
        {str(episode_data)}
        <!-- Add more episodes as needed -->
    </ul>
</div>

</body>
</html>

"""
    return str(content_html+str(data)+content_html2)

def search_html(data):
    search_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        header {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 10px;
        }

        nav {
            background-color: #ddd;
            padding: 10px;
        }

        nav a {
            margin: 0 10px;
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }

        .items {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            padding: 20px;
        }

        .item {
            width: 200px;
            margin: 10px;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }

        .search-container {
            text-align: center;
            margin: 20px;
        }

        .search-form {
            display: inline-block;
            padding: 10px;
            border-radius: 5px;
            background-color: #ddd;
        }

        .search-form input[type="text"] {
            padding: 5px;
        }

        .search-form button {
            padding: 5px 10px;
            background-color: #333;
            color: #fff;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <header>
        <h1>My Website</h1>
    </header>

    <nav>
    <h1>HTML Links</h1>
    <a href="../get-user/Home">Home</a>
    <a href="../get-user/Search">Search</a>
    <a href="../get-user/Player">Player</a>
    <a href="#" target="_blank"  onclick="redirectToDataUrl()">Data</a>

    <script>
    function redirectToDataUrl() {
      // Get the current URL and append '/Data' to it
      var dataUrl = window.location.href + "/Data";

      // Redirect to the constructed URL
      window.location.href = dataUrl;
    }
  </script>

    </nav>

    <div class="search-container"> 
        <form class="search-form" method="post">
        <label for="data">Enter Data:</label>
        <input type="text" id="data" name="data" required>
        <button type="submit">Submit</button>
    </form>
    </div>

    <div class="items">
        <!-- Items will be populated dynamically based on the search results from Flask -->
        <!-- For demonstration purposes, a static example is shown below -->
         
"""

    search_html2 = f"""
        {data}
    </div>

</body>
</html>


"""
    return str(search_html+search_html2)


def index_html(data):
       
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }

        header {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 10px;
        }

        nav {
            background-color: #ddd;
            padding: 10px;
        }

        nav a {
            margin: 0 10px;
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }

        .items {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            padding: 20px;
        }

        .item {
            width: 200px;
            margin: 10px;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }
    </style>
</head>
<body>

    <header>
        <h1>My Website</h1>
    </header>

    <nav>
    <h1>HTML Links</h1>
    <a href="../get-user/Home">Home</a>
    <a href="../get-user/Search">Search</a>
    <a href="../get-user/Player">Player</a>
    <a href="#" target="_blank"  onclick="redirectToDataUrl()">Data</a>

    <script>
    function redirectToDataUrl() {
      // Get the current URL and append '/Data' to it
      var dataUrl = window.location.href + "/Data";

      // Redirect to the constructed URL
      window.location.href = dataUrl;
    }
  </script>

    </nav>

    <div class="items">
        <!-- Item 1 -->
        """ 

    index2_html = f"""

        {data}
        

    </div>

</body>
</html>
"""
    return str(index_html+index2_html)

def player_html(data):

    player_html = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; frame-src 'self' {data};">
    <title>Video Player</title>
</head>
<body>
    <h1>HTML Links</h1>
    <a href="../get-user/Home">Home</a>
    <a href="../get-user/Search">Search</a>
    <a href="../get-user/Player">Player</a>
    <a href="#" target="_blank"  onclick="redirectToDataUrl()">Data</a>

    <script>
    function redirectToDataUrl() {
      // Get the current URL and append '/Data' to it
      var dataUrl = window.location.href + "/Data";

      // Redirect to the constructed URL
      window.location.href = dataUrl;
    }
  </script>

"""
    player_html2 = f"""

    <p>
    <iframe width="640" height="360" src="{data}" frameborder="0" allowfullscreen></iframe>
    </p>
    <p>
    <iframe width="640" height="360" src="{data}" frameborder="0" allowfullscreen></iframe>
    </p>
</body>
</html>

    """
    return player_html + player_html2

def css_player_html(data):

    player_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Player</title>

    <!-- Add your custom CSS styles here -->
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        h1 {
            background-color: #333;
            color: #fff;
            padding: 10px;
            text-align: center;
            margin: 0;
        }

        nav {
            background-color: #555;
            padding: 10px;
            text-align: center;
        }

        nav a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }

        p {
            text-align: center;
        }

        iframe {
            width: 100%;
            height: 100%;
            margin: 20px auto;
            display: block;
        }

        .download-btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #3498db;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        .download-btn:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>

    <h1>HTML Links</h1>

    <!-- Navigation Bar -->
    <nav>
        <a href="index.html" target="_self">Home</a>
        <a href="Search.html" target="_self">Search</a>
        <a href="Player.html" target="_blank">Player</a>
    </nav>
"""
    player_html2 = f"""
    <p>
        <iframe width="640" height="640" src="{data["Video Player Link"]}" frameborder="0" allowfullscreen></iframe>
    </p>

    <!-- Download Button -->
    <p style="text-align: center;">
        <a href="{data["Download URL"]}" class="download-btn" target="_blank">Download</a>
    </p>

</body>
</html>

    """
    return str(player_html+player_html2)


def Error_html():
    error_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        .container {
            max-width: 600px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #ff5252;
        }

        p {
            color: #333;
            font-size: 18px;
        }

        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://placekitten.com/600/400" alt="Cat Image">
        <h1>404 - Not Found</h1>
        <p>Oops! The page you are looking for might be in another galaxy.</p>
    </div>
</body>
</html>


    """

    return error_html






###############################################################################################################

#Req Function

def home_content(data):
    html = ""
    for x in data:
        z = data[x]
        Big_data = f"""<div class="item"><img src="{z['Img_Src']}" alt="Item 1 Image"><h3>{z['Title']} </h3><p>{z['Episode']}</p><a href="/get-user/Content/{z['Anime_Url']}">Details</a></div>"""
        html += Big_data    
    return html

def search_content(data):
    html = ""
    for x in data:
        z = data[x]
        Big_data = f"""<div class="item"><img src="{z['Img_Src']}" alt="Item 1 Image"><h3>{z['Title']} </h3><p>{z['Released_date']}</p><a href="/get-user/Content/{z['Anime_Url']}">Details</a></div>"""
        html += Big_data    
    return html


def content_content(data,url):
    content_html = f"""
    <div class="tv-show">
    <img src="{data["Img_Src"]}" >
    <div class="tv-show-info">
        <h2>Title: {data["Title"]}</h2>
        <p>Genre: {data["Genre"]}</p>
        <p>Summary: {data["Plot Summary"]}</p>
        <p>Release Date: {data["Released"]}</p>
        <p>Status: {data["Status"]}</p>
        <p>Other Name: {data["Other Name"]}</p>
        <p>Type: {data["Type"]}</p>
        <p>Total Episode: {data["Total No. Of Episode"]}</p>
    </div>"""

    episode_container_html = ""
    for x in range (1 , 1 + int(data["Total No. Of Episode"])):
        episode_html = f"""
            <li class="episode-list-item">
                <a target="_blank" href="{"/get-user/Player/" + url + "-episode-" + str(x)}" class="episode-link">Episode {x} </a>
            </li>


        """
        episode_container_html += episode_html
    return {"data" : content_html, "episode_data":episode_container_html}


###############################################################################################################


app = Flask(__name__)

###############################################################################################################

#Data For Backend



#Home
@app.route("/get-user/Home/Data")
def get_home():
    try:
        data = extract_Home(Urls.Home)
        #data = dict_content(data)
        return data
    except:
        return {"data" : "data not found" , "data_code": 404 }


#search
@app.route('/get-user/Search/Data', methods=['GET', 'POST'])
def search():
    try:
        if request.method == 'POST':
            # Get data from the form
            data = request.form.get('data')
            if data :
                data = extract_Home(convert_search_url(data))
                if data != {}:
                    return data
                else:
                    return f"For {data} nothing Found!"
            
            else:
            
                # Display the entered data on the same page
                return search_html("<a></a>")
        
        # Render the initial form on the page
        return search_html("<a></a>")
    except: 
        return {"data" : "data not found" , "data_code": 404 }

#Search as per user id
@app.route('/get-user/Search/<user_id>/Data', methods=['GET', 'POST'])
def user_id_search(user_id): 
    try:   
        data = extract_Home(convert_search_url(user_id))
        if data != {}:
            return data
        else:
            return f" For {user_id} Nothing Found!"
    except :
        return {"data" : "data not found" , "data_code": 404 }

#content
@app.route("/get-user/Content/<user_id>/Data")
def get_content(user_id):
    try:
        data = extract_Anime_Content(Urls.Suffix + "/category/" + user_id)
        return data
    except:
        return {"data" : "data not found" , "data_code": 404 }
        
#Player
@app.route("/get-user/Player/<user_id>/Data")
def get_player(user_id):
    try:
        data = extract_embedded_Video(Urls.Suffix + "/" + user_id)
        print(data)
        return data
    except:
        return {"data" : "data not found" , "data_code": 404 }



#FrontEnd

#Home
@app.route("/get-user/Home")
def get_user_home():
    try:
        data = extract_Home(Urls.Home)
        data = home_content(data)
        data = index_html(data)
        return data 
    except :
        return Error_html()

    

#search



@app.route('/get-user/Search', methods=['GET', 'POST'])
def get_user_search():
    try:
        if request.method == 'POST':
            # Get data from the form
            data = request.form.get('data')
            if data :
                data = extract_Home(convert_search_url(data))
                data = search_content(data)
                data = search_html(data)
                return data
            
            else:
            
                # Display the entered data on the same page
                return search_html("<a></a>")
        
        # Render the initial form on the page
        return search_html("<a></a>")
    except:
        return Error_html()

#Search as per user id
@app.route('/get-user/Search/<user_id>', methods=['GET', 'POST'])
def get_user_id_search(user_id):    
    try:
        data = extract_Home(convert_search_url(user_id))
        data = search_content(data)
        data = search_html(data)
        return data
    except:
        return Error_html()

#content
@app.route("/get-user/Content/<user_id>")
def get_user_content(user_id):
    try:
        data = extract_Anime_Content(Urls.Suffix + "/category/" + user_id)
        data = content_content(data,user_id)
        data = content_html(data["data"],data["episode_data"])
        return data
    except:
        return Error_html()


    
#Player
@app.route("/get-user/Player/<user_id>")
def get_user_player(user_id):
    try:
        data = extract_embedded_Video(convert_player_url(Urls.Suffix + "/" + user_id,0))
        if data:
            data = data["Video Player Link"]
            return player_html(data)

            #return css_player_html(data)
        else:
            data = extract_embedded_Video(convert_player_url(Urls.Suffix + "/" + user_id,1))
            data = data["Video Player Link"]
            return player_html(data)

            #return css_player_html(data)
    except:
        return Error_html()

###############################################################################################################

#if __name__ == "__main__":
#    app.run(debug = True)

###############################################################################################################

# Type Of Urls In Application

url_home      = "/get-user/Home"
url_home_Data = "/get-user/Home/Data"


url_search      = "/get-user/Search"
url_search_Data = "'/get-user/Search/Data'"
url_search_Data_ui = "/get-user/Search/<user_id>"
url_search_Data_ui_Data = "/get-user/Search/<user_id>/Data"

url_content      = "/get-user/Content/<user_id>"
url_content_Data = "/get-user/Content/<user_id>/Data"

url_player      = "/get-user/Player/<user_id>"
url_player_Data = "/get-user/Player/<user_id>/Data"

###############################################################################################################
