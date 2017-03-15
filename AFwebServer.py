try:
    import usocket as socket
except:
    import socket

from machine import Pin

relay = Pin(0,Pin.OUT)
relay.high()

html = """<!DOCTYPE html>
<html>
    <head>
        <title>AF IntelliLight - by: http://dobitaobyte.com.br</title>
        <script>
            var ON  = 1;
            var OFF = 0;
            function turnRelay(state){
                if (state == ON){
                    var location_now = window.location.hostname;
                    window.location.replace("/?relay=on");
                }
                else if (state == OFF){
                    var location_now = window.location.hostname;
                    window.location.replace("?relay=off");
                }
            }
        </script>
    </head>
    <body><div align="center">
        <table width="100%" border="2" style="border-radius:10px; 2px solid #0000AF"><tbody><tr><th style="border-radius:10px; border: 2px solid #73AD21">
        <h1 style="color: #DF0000; text-shadow: 2px 2px 5px gray;">Interface de controle</h1>
    <br>
    <h3 style="color:white; text-shadow: 2px 2px 4px #000000; font-family:arial">AF Eletronica e Do bit Ao Byte</h3>
        <table border="0" align="center">
          <tr><center>
              <th>
              <button style="border-radius: 8px; border: 2px solid #0000AF; padding 10px; font-size:60px; font-family: arial; color:#73AD21; text-shadow:-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white; box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);" type="button" onclick="turnRelay(ON)">Ligar</button>
              </th>
              <th>
              <button style="border-radius: 8px; border: 2px solid #0000AF; padding 10px; font-size:60px; font-family: arial; color:#DF0000; text-shadow:-1px 0 white, 0 1px white, 1px 0 white, 0 -1px white; box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);" type="button" onclick="turnRelay(OFF)">Desligar</button>
              </th>
          </center></tr>
        </table><br><br>
        ____
</th></tr></tbody></div>

</html>
"""
request_method  = ""
path            = ""
request_version = ""


def parse_request(text):
        if text != '':
            request_line = text.split("\r\n")[0]
            request_line = request_line.split()
            print(request_line)
            # Break down the request line into components
            (request_method,  # GET
             path,            # /hello
             request_version  # HTTP/1.1
             ) = request_line
            print("Method:", request_method)
            print("Path:", path)
            print("Version:", request_version)
            if request_method == "POST":
                pass
            if request_method == "GET":
                if "?" in path:
                    #este values tem apenas o resultado final
                    filename, values = path.strip('/').split('?')
        
                    if values == 'relay=on':
                        print("Ligando rele")
                        relay.low()
                        
                    elif values == 'relay=off':
                        print("Desligando rele")
                        relay.high()

def startServer():
    s  = socket.socket()
    s.setsockopt(1, 7, 8192)
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>/")
    print("v4.2")
    
    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]

        try:
            header, content = parse_request(client_s.recv(4096).decode('utf-8'))
            print('length of content:' + str(len(content)))
            print (client_addr)
            if header != '':
                client_s.send(header)
                client_s.send(content)
        except:
            print("oh-oh...")
            pass
        try:
            print("pin_value")
            pin_value = relay.value()
            print(pin_value)

            relay_status = "Estado do relay:INDEFINIDO"

            if pin_value == 1:
                relay_status = "Estado do relay:Desligado"   
            
            elif pin_value == 0:
                print("pin_value = 0")
                relay_status = "Estado do relay:Ligado"
            
            print("testando html")
            html2 = html.replace("____",relay_status)
            

            client_s.sendall(html2)
        except:
            pass
        client_s.close()