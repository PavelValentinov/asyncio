import asyncio
import aiosqlite
import smtplib

from email.message import EmailMessage

DB_NAME = 'contacts.db'
LOGIN_MAILER = 'email'
PASS_MAILER = 'pass'

async def create_mail(user_info):
    info_user = {}
    message = f'Уважаемый {user_info[1]} {user_info[0]}! Спасибо, что пользуетесь нашим сервисом объявлений.'
    info_user[user_info[2]] = message
    return info_user


async def main():
    db = await aiosqlite.connect(DB_NAME)
    cursor = await db.execute('select first_name, last_name, email from contacts')
    rows = await cursor.fetchall()

    tasks = []
    for row in rows:
        task = asyncio.create_task(create_mail(row))
        tasks.append(task)

    emails = await asyncio.gather(*tasks)
    await cursor.close()
    await db.close()

    print(emails)
    for row in emails:
        for u_email, u_massage in row.items():
            # создает сеанс SMTP
            s = smtplib.SMTP("smtp.gmail.com", 587)
            # запустите TLS для обеспечения безопасности
            s.starttls()
            # Идентификация
            s.login(LOGIN_MAILER, PASS_MAILER)
            # отправка почты
            em = EmailMessage()
            msg = u_massage
            em.set_content(msg)
            em['To'] = u_email
            em['From'] = LOGIN_MAILER
            em['Subject'] = "Тема письма"
            s.send_message(em)
            # завершение сессии
            s.quit()

asyncio.run(main())
