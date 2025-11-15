## A little UK weather MCP server 

Starting with the Antrhropic code at the 
[build an MCP client ](https://home.openweathermap.org/)
page in the MCP documentation, this is a playground to look at 
the MCP protocol etc.

### Adaption to UK Weather

Stripped out US-specific code and replaced it with use of 
[OpenWeatherMap](https://home.openweathermap.org/). OpenWeatherMap supports 
any global location. For people wanting to enter a bank card details there are a
range of services to a generous limit before payment is taken. Or, as with me, you can just get
an API key without bank card details and access just one service; to retrieve the current weather at a location.

An example invocation is 

`https://api.openweathermap.org/data/2.5/weather?lat=51.5234&lon=0.1167&units=metric&appid={API-key}`

which, e.g., returns this JSON 

```
{
  "coord": {
    "lon": 0.1167,
    "lat": 51.5234
  },
  "weather": [
    {
      "id": 801,
      "main": "Clouds",
      "description": "few clouds",
      "icon": "02d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 16.31,
    "feels_like": 16.09,
    "temp_min": 15.45,
    "temp_max": 17.12,
    "pressure": 1007,
    "humidity": 80,
    "sea_level": 1007,
    "grnd_level": 1005
  },
  "visibility": 10000,
  "wind": {
    "speed": 4.12,
    "deg": 240
  },
  "clouds": {
    "all": 20
  },
  "dt": 1763032792,
  "sys": {
    "type": 1,
    "id": 1414,
    "country": "GB",
    "sunrise": 1763018062,
    "sunset": 1763050408
  },
  "timezone": 0,
  "id": 6690871,
  "name": "Dagenham",
  "cod": 200
}
```

### Configuring Claude Desktop to use the server

Details for Mac/Linux and Windows at the URL above. My own cofig for Claude Desktop on
MacOS at `~/Library/Application\ Support/Claude/claude_desktop_config.json`
is

```
{
  "preferences": {
    "quickEntryDictationShortcut": "capslock"
  },
  "mcpServers": {
    "weather": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "--directory",
        "/Users/mark/PycharmProjects/MSc/WeatherMCP/",
        "run",
        "weather.py"
      ]
    }
  }
}
```

Obviously you will need an Anthropic API key, subscription required. As far as I recall, I just logged into
my Anthropic account from Claude Desktop and that action grabbed my
API key.



### Configuring the MCP server for a Chatbot/MCP client example

Using the code at (my example repo)[https://github.com/markvan/MCPclient ] use
Python 3, the chatbot/MCP client script and a path to an MCP server, e.g.

`python client.py ../WeatherMCP/weather.py`

