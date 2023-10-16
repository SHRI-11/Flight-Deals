import smtplib

FROM_EMAIL = "FROM EMAIL"
FROM_PASS = "PASS"


class NotificationManager:
    def send_email(self, price, from_city, from_iata, to_city, to_iata, out_date, return_date, user, stopovers=0, via_city=""):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            message = f"Subject:Low price alert!\n\nOnly ₹{price} to fly from {from_city}-{from_iata} to {to_city}-{to_iata}, from {out_date} to {return_date}."
            if stopovers > 0:
                message += f"\nFlight has {stopovers} stop over, via {via_city}."
            mess = message.encode(encoding="utf-8")
            connection.login(user=FROM_EMAIL, password=FROM_PASS)
            connection.sendmail(from_addr=FROM_EMAIL,
                                to_addrs=user,
                                msg=mess
                                )
            print(f"Email sent to {user}")
