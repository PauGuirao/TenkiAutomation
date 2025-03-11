import requests
from bs4 import BeautifulSoup

# 1. Create a session to persist cookies
session = requests.Session()

# 2. Fetch the login page
login_url = "https://www.tenkiapp.com/login.aspx"
login_page_response = session.get(login_url)

# 3. Parse out the hidden ASP.NET fields
soup = BeautifulSoup(login_page_response.text, "html.parser")

# Safely extract hidden fields, providing a default empty string if not found
viewstate = soup.find("input", {"name": "__VIEWSTATE"})
viewstate_generator = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})
event_validation = soup.find("input", {"name": "__EVENTVALIDATION"})

viewstate_value = viewstate["value"] if viewstate else ""
viewstate_generator_value = viewstate_generator["value"] if viewstate_generator else ""
event_validation_value = event_validation["value"] if event_validation else ""

# 4. Build the login payload with the parsed fields plus your credentials
login_payload = {
    "__EVENTTARGET": "btnEntrar",          # From your screenshot
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": viewstate_value,
    "__VIEWSTATEGENERATOR": viewstate_generator_value,
    "__EVENTVALIDATION": event_validation_value,
    "Usuario": "pau.guirao@ebolution.com",       # Replace with actual username
    "Contrasenia": "41603769N"    # Replace with actual password
}

# 5. Optional: Set headers if needed (check your browser dev tools)
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ca-ES,ca;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Content-Length": "599",  # Omit, requests handles automatically
    "Content-Type": "application/x-www-form-urlencoded",
    # "Cookie": "ASP.NET_SessionId=krmdt5c4mprg33f3stpkzjn2; MailketinActivo=Usuario=998",  # Only if needed
    "Host": "www.tenkiapp.com",
    "Origin": "https://www.tenkiapp.com",
    "Referer": "https://www.tenkiapp.com/index.aspx",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}


# 6. Log in by posting to the same login URL
login_response = session.post(login_url, data=login_payload, headers=headers)

# 7. Check if login was successful
#    You might look for specific text in the response or a status code.
if login_response.status_code == 200 and "btnEntrar" not in login_response.text:
    print("Login successful!")
    imputar_url = "https://www.tenkiapp.com/imputar-horas.aspx"
    imputar_response = session.get(imputar_url)
    session.cookies.set("MailketinActivo", "Usuario=998")
    cookies_dict = session.cookies.get_dict()
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
    print(cookie_string)
    # 3. Parse out the hidden ASP.NET fields from the HTML
    soup = BeautifulSoup(imputar_response.text, "html.parser")
    def safe_value(name):
        """Helper to find a hidden input by name, or return an empty string if not found."""
        tag = soup.find("input", {"name": name})
        return tag["value"] if tag and "value" in tag.attrs else ""
    
    viewstate = safe_value("__VIEWSTATE")
    viewstate_gen = safe_value("__VIEWSTATEGENERATOR")
    eventvalidation = safe_value("__EVENTVALIDATION")
    last_focus = safe_value("__LASTFOCUS")      # if present
    event_target = safe_value("__EVENTTARGET")  # if present
    event_argument = safe_value("__EVENTARGUMENT")  # if present

    hours_data = {
        "ctl00$contenidos$FechaTarea": "11/03/2025",
        "ctl00$contenidos$DropClientes": "EBOLUTION | 99999|",
        "ctl00$contenidos$DropProyectos": "P008262 | EBO - Operations Team 2025 | _blank_",
        "ctl00$contenidos$DropTareas": "OPT70001 | Squad - Reuniones planificación general",
        "ctl00$contenidos$DropRecursos": "998",
        "ctl00$contenidos$AreaObserva": "Daily PM",
        "ctl00$contenidos$ObservaMinCar": "0",
        "ctl00$contenidos$TxtMinutos": "0:30",
        "ctl00$contenidos$txtStopWatch": "",
        "ctl00$contenidos$horaInicio": "00:00",
        "ctl00$contenidos$horaFin": "00:30",
        "ctl00$contenidos$tiempoTotal": "",
        "ctl00$contenidos$horaInicioG": "00:00",
        "ctl00$contenidos$horaFinG": "00:30",
        "ctl00$contenidos$TiempoTarea": "00:30",
        "ctl00$contenidos$DropTipoTrabajo": "NORMAL",
        "ctl00$contenidos$gastoKms": "",
        "ctl00$contenidos$gastoDietas": "",
        "ctl00$contenidos$gastoGasolina": "",
        "ctl00$contenidos$gastoPernocta": "",
        "ctl00$contenidos$gastoParking": "",
        "ctl00$contenidos$gastoOtros": "",
        "ctl00$contenidos$CifEmpresa": "B86037256",
        "ctl00$contenidos$btnCostes": "Registrar",
        "ctl00$contenidos$FechaGrafica": "11/03/2025",
        "__EVENTTARGET": event_target,
        "__EVENTARGUMENT": event_argument,
        "__LASTFOCUS": last_focus,
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_gen,
        "__EVENTVALIDATION": eventvalidation,
    }

    print("Hours data:", hours_data)

    hours_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ca-ES,ca;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.tenkiapp.com",
        "Origin": "https://www.tenkiapp.com",
        "Referer": "https://www.tenkiapp.com/imputar-horas.aspx",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    print("Headers:", hours_headers)
    
    submit_response_hours = session.post(imputar_url, data=hours_data, headers=hours_headers,allow_redirects=False)
    print("Hours submission status:", submit_response_hours.status_code)
    print("Response headers:", submit_response_hours.headers)
    print("Responde text status:", submit_response_hours.text)
else:
    print("Login might have failed. Check your credentials or hidden field parsing.")
