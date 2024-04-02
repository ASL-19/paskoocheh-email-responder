# coding=UTF8
"""
Template file for email responder
"""

TEMPLATES = {
    'EMAIL_SUBJECT': {
        'en': """
            I have a file for you!
        """,
        'fa': """
            منم آقای پستچی. فایل دارم براتون.‎
        """,
        'ar': """
            مفتاحكم الخاص
        """
    },
    'TEXT_BODY': {
        'en': """
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        اینم فایل فیلترشکنی { tool name } که خواسته بودید ضمیمه‌ی این ایمیل شد.

        اگر فایل ویندوز درخواست کردین یادتون باشه که پسوند فایل‌های اجرائی ویندوز را از abc. به exe. تغییر دهید.

        """,
        'ar': """
        """
    },
    'HTML_BODY': {
        'en': """
        """,
        'fa': """
            <p dir="rtl">
            <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟ </span></p><p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اینم فایل فیلترشکن { tool name } که خواسته بودید ضمیمه‌ی این ایمیل شد.</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اگر فایل ویندوز درخواست کردین یادتون باشه که پسوند فایل‌های اجرائی ویندوز را از abc. به exe. تغییر دهید.</span></p>   <p dir="rtl">
            <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
        </p>
        """,
        'ar': """
        """
    },
    'SOS_TEXT_BODY': {
        'en': """
        Hi,
        The paskoocheh's digital rescue package provides a list of best practices for times when there is heavy information control.

        Sicerely,
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        «بسته کمک‌رسان دیجیتال» پس‌کوچه حاوی روش‌های برقراری ارتباط هنگام قطع یا اختلال در اینترنت و همچنین معرفی ابزارها و نرم‌افزارهای جدید و کاربردی و راه‌کار استفاده از آن‌ها در مواقع ضروری است.
        این بسته می‌تواند شما را در برابر اتفاقات پیش‌بینی نشده مثل قطع ارتباط با اینترنت جهانی، مجهز کند و آمادگی این را داشته باشید بنا به شرایط مختلف، بدون مشکل به اطلاعات و اخبار روز دسترسی داشته باشید.
        «بسته کمک‌رسان دیجیتال» پس‌کوچه را برای روز مبادا در جایی قابل دسترس نگهداری کنید و با دوستان و عزیزان‌تان به اشتراک بگذارید

        """,
        'ar': """
        """,
    },
    'SOS_HTML_BODY': {
        'en': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Hi, </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">The paskoocheh's digital rescue package provides a list of best practices for times when there is heavy information control. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Sicerely, </span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">«بسته کمک‌رسان دیجیتال» پس‌کوچه حاوی روش‌های برقراری ارتباط هنگام قطع یا اختلال در اینترنت و همچنین معرفی ابزارها و نرم‌افزارهای جدید و کاربردی و راه‌کار استفاده از آن‌ها در مواقع ضروری است. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">این بسته می‌تواند شما را در برابر اتفاقات پیش‌بینی نشده مثل قطع ارتباط با اینترنت جهانی، مجهز کند و آمادگی این را داشته باشید بنا به شرایط مختلف، بدون مشکل به اطلاعات و اخبار روز دسترسی داشته باشید. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">«بسته کمک‌رسان دیجیتال» پس‌کوچه را برای روز مبادا در جایی قابل دسترس نگهداری کنید و با دوستان و عزیزان‌تان به اشتراک بگذارید </span></p>
                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
        """,
    },
    'WIN_TEXT_BODY': {
        'en': """
        """,
        'fa': """
        ممنون از ایمیلتون. لینک دانلود یا فایل نرم‌افزار درخواست شده ضمیمه این ایمیل شده است.

        **پسوند فایل‌های اجرائی ویندوز را از abc. به exe. تغییر دهید.

        تیم پس‌کوچه

        """,
        'ar': """
        """
    },
    'WIN_HTML_BODY': {
        'en': """
        """,
        'fa': """
            <p dir="rtl">
            <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟ </span></p><p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اینم فایل فیلترشکنی { tool name } که خواسته بودید ضمیمه‌ی این ایمیل شد.</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اگر فایل ویندوز درخواست کردین یادتون باشه که پسوند فایل‌های اجرائی ویندوز را از abc. به exe. تغییر دهید.</span></p>   <p dir="rtl">
            <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
        </p>
        """,
        'ar': """
        """,
    },
    'PROXY_TEXT_BODY': {
        'en': """
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        اینم فایل فیلترشکنی {} که خواسته بودید ضمیمه‌ی این ایمیل شد.
        """,
        'ar': """
        """,
    },
    'PROXY_HTML_BODY': {
        'en': """
        """,
        'fa': """
            <p dir="rtl">
            <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟ </span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اینم لینک «پس‌کوچه پراکسی» برای تلگرام: </span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">برای فعال کردن پراکسی:</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">۱- از نسخه‌ی اصلی تلگرام استفاده کنید و آن را به آخرین نسخه به‌روزرسانی کنید.</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">۲- بر روی لینک کلیک کنید و Connect را بزنید.</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">توجه: هر دو این لینک‌ها یکی هستند. اگر قابل کلیک کردن نیستند، آن‌ها را کپی کرده و در مرورگر خود بگذارید و به مرورگر اجازه دهید تا پراکسی را در اپ تلگرام باز کند. اگر لینک اول کار نکرد لینک دوم را امتحان کنید.</span></p>


            <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
        </p>
        """,
        'ar': """
        """
    },
    'ATTACHMENT_HTML': {
        'en': """
        """,
        'fa': """
        <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{{link}}">لینک دانلود</a></span></p>
        """,
        'ar': """
        """
    },
    'ATTACHMENT_HTML_PASKOOCHEH': {
        'en': """
        """,
        'fa': """
        <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{{link}}">لینک دانلود اپلیکیشن پس‌کوچه</a></span></p>
        """,
        'ar': """
        """
    },
    'BIA_TEXT': {
        'en': """
        """,
        'fa': """
        """,
        'ar': """
        """
    },
    'BIA_HTML': {
        'style': """
            <style>
            table, th, td  {border-collapse: collapse;border: 1px solid #ccc;font-family: 'Helvetica', Arial, Helvetica, sans-serif;os-align: center;}button {display: inline-block;os-align: center;vertical-align: middle;padding: 9px 24px;border: 0px solid #1e6fc6;border-radius: 5px;background: #4092c2;background: -webkit-gradient(linear, left top, left bottom, from(#4092c2), to(#5a91cc));background: -moz-linear-gradient(top, #4092c2, #5a91cc);background: linear-gradient(to bottom, #4092c2, #5a91cc);font: normal normal bold 14px Helvetica;color: #ffffff;os-decoration: none;}button:hover,button:focus {border: 0px solid ##268bf7;background: #4dafe9;background: -webkit-gradient(linear, left top, left bottom, from(#4dafe9), to(#6caef5));background: -moz-linear-gradient(top, #4dafe9, #6caef5);background: linear-gradient(to bottom, #4dafe9, #6caef5);color: #ffffff;os-decoration: none;}button:active {background: #265874;background: -webkit-gradient(linear, left top, left bottom, from(#265874), to(#5a91cc));background: -moz-linear-gradient(top, #265874, #5a91cc);background: linear-gradient(to bottom, #265874, #5a91cc);}button:after{content:  '\\0000a0';display: inline-block;height: 4px;width: 24px;line-height: 20px;margin: 0 -4px -6px 4px;position: relative;top: 0px;left: 0px;background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAA30lEQVRIie3TMUoDQRSH8Z9Wi1hoaktZMVjoJYKNRKzEOmcQG/EUqXMKCwuRVGlt0llaaZEjaOFDxmF3E3fb/WBg5+1/vgfzGHp6urKV7b/wjreWvkMcVHh/WeIJkxbySZxdpsXtLPSBMY4xw84G4t3IHuEiHLW8JN9XmGPYkB9G5rLG0dgAyqhdV2Rv8Ozn3psca3+W+MQURaxp1Mp1jnwGOQPc4wwLPMZaRO0hMhuTdi9wi72kduLvTAa4i2yVo7HBKDtYR4HzNg3a8q8ZdCZ/0iu8dnSeYr+jo6cn4Rs7VSTPzFQ8FwAAAABJRU5ErkJggg==') no-repeat left center transparent;background-size: 100% 100%;} #footer a { text-decoration: none !important }
            </style>
            """,
        'body_top': """
            <body>
                <h2><p align='center' style="background-color: #1d3b6c;"><a href='http://www.paskoocheh.com/' target='_blank'><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/header.gif" alt="پسکوچه" width="650" height="250" style="padding: 1px;" /></a></p><p align='center'><span style='font-family:tahoma,geneva,sans-serif'>جدول به‌روز‌ترین ابزارهای امنیت دیجیتال و فیلترشکن‌های قابل استفاده در ایران</span></p></h2><p align='center'><span style='font-family:tahoma,geneva,sans-serif'>عزیز دل برادر! فیلترشکن یا ابزار درخواستی را برای سیستم عامل مورد استفاده‌ خود انتخاب کن<p align='center'><span style='font-family:tahoma,geneva,sans-serif'>برای دریافت فایل بی‌زحمت دکمه‌ی ارسال را بزن و یه ایمیل خالی به آدرس بنده (أقای پستچی پس‌کوچه) بفرست <table align='center' style='border-collapse: collapse;border: 1px solid black;font-family: 'Helvetica', Arial, Helvetica, sans-serif;os-align: center;' Helvetica', arial, helvetica, sans-serif;os-align: center;'>
                <p align='center'><a style='font-size: 18px' href="http://asl19.us3.list-manage2.com/subscribe?u=75482535a3dea0b0928f5d23c&amp;id=eb6ff21285"> برای خبردارشدن از آخرین نسخه‌ی فیلترشکن‌ها و سایر اخبار مربوطه در خبرنامه‌ی اصل۱۹ ثبت‌نام کنید</a></p> <p align='center'><a href="https://paskoocheh.com/"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="پسکوچه" width="40" height="40" /></a><br /> <p align='center'><a style='padding: 5px' href="https://telegram.me/paskoocheh"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-telegram.png" alt="Telegram" width="30" height="25" /></a><a style='padding: 5px' href="https://twitter.com/paskoocheh"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-twitter.png" alt="Twitter" width="31" height="25" /></a><a style='padding: 5px' href="https://www.instagram.com/paskoocheh/"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-instagram.png" alt="Instagram" width="27" height="27" /></a><a style='padding: 5px' href="https://www.facebook.com/Paskoocheh-229124020782514"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-facebook.png" alt="Facebook" width="15" height="25" /></a></p> </span>
        """,
        'body_bottom': """
            </table>
                <span id="footer"><br /> <p align='center'><a style='font-size: 18px' href="http://asl19.us3.list-manage2.com/subscribe?u=75482535a3dea0b0928f5d23c&amp;id=eb6ff21285"> برای خبردارشدن از آخرین نسخه‌ی فیلترشکن‌ها و سایر اخبار مربوطه در خبرنامه‌ی اصل۱۹ ثبت‌نام کنید</a></p> <p align='center'><a href="https://paskoocheh.com/"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="پسکوچه" width="40" height="40" /></a><br /> <p align='center'><a style='padding: 5px' href="https://telegram.me/paskoocheh"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-telegram.png" alt="Telegram" width="30" height="25" /></a><a style='padding: 5px' href="https://twitter.com/paskoocheh"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-twitter.png" alt="Twitter" width="31" height="25" /></a><a style='padding: 5px' href="https://www.instagram.com/paskoocheh/"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-instagram.png" alt="Instagram" width="27" height="27" /></a><a style='padding: 5px' href="https://www.facebook.com/Paskoocheh-229124020782514"><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-facebook.png" alt="Facebook" width="15" height="25" /></a></p>
        """,
        'table_header': """
            <th style='border-collapse: collapse;border: 1px solid #ccc;font-family: 'Helvetica', Arial, Helvetica, sans-serif;os-align: center;' Helvetica', arial, helvetica, sans-serif;os-align: center;'><span style='font-family: Helvetica, Arial, Helvetica, sans-serif'>{platform_name}</span></th>
        """,
        'table_first_column': """
            <td style='border-collapse: collapse;border: 1px solid #ccc;font-family: 'Helvetica', Arial, Helvetica, sans-serif;os-align: center;' Helvetica', arial, helvetica, sans-serif;os-align: center;'><span style='font-family: Helvetica, Arial, Helvetica, sans-serif'>{tool_name}</span></td>
        """,
        'table_cell': """
            <td style='border-collapse: collapse;border: 1px solid #ccc;font-family: 'Helvetica', Arial, Helvetica, sans-serif;os-align: center;' Helvetica', arial, helvetica, sans-serif;os-align: center;'>{tool_link}</td>
        """,
        'table_tool_link': """
            <a href='mailto:{tool_maillink}'><button name='subject' name='submit' value='ارسال ایمیل' style='display: inline-block;os-align: center;vertical-align: middle;padding: 9px 24px;border: 0px solid #1e6fc6;border-radius: 5px;background: linear-gradient(to bottom, #4092c2, #5a91cc);font: normal normal bold 14px Helvetica;color: #ffffff;os-decoration: none;'>ارسال ایمیل</button></a>
        """,
        'en': """
        """,
        'fa': """
        """,
        'ar': """
        """,
    },
    'OUTLINE_KEY_NEW_TEXT_BODY': {
        'en': """
        outline proxy link: {}
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.
        خدمت شما عرض کنم که تیم پس‌کوچه برای پیگیری مشکلات احتمالی و پشتیبانی بهتر احتیاج دارد تا ایمیل شما را ذخیره کند. پیشنهاد می‌کنم قبل از ادامه‌ی استفاده از Outline درباره‌ی سیستم توزیع پس‌کوچه در سند حریم خصوصی پس‌کوچه بخوانید.
        این هم خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇
        {}
        قربان شما
        آقای پستچی
        """,
        'ar': """
        مرحبا،
        حتى نتمكّن من توفير خدمة Outline لكم، ولنتحقّق من أي مشاكل مُحتملة، سنقوم بالاحتفاظ ببريدكم الالكتروني. للمزيد من التفاصيل نقترح عليكم قراءة سياسة الخصوصيّة التّابعة لاستخدام Outline في https://asl19.org/ar/outline/الأسئلة الأكثر تكراراً.
        إليكم رابط مفتاح Outline. عند ضغطكم على الرّابط، واستخدامكم لدليل التحميل والاستخدام، ستتمكّنون من تحميل Outline على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.
        الرّابط: 👇
        mada@asl19.org أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا
        """,
    },
    'OUTLINE_KEY_NEW_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Outline vpn link: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">خدمت شما عرض کنم که تیم پس‌کوچه برای پیگیری مشکلات احتمالی و پشتیبانی بهتر احتیاج دارد تا ایمیل شما را ذخیره کند. پیشنهاد می‌کنم قبل از ادامه‌ی استفاده از Outline درباره‌ی سیستم توزیع پس‌کوچه در <a href="https://paskoocheh.com/privacy-policy.html#outline-distribution-privacy-policy">سند حریم خصوصی پس‌کوچه</a> بخوانید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">این هم خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">مرحبا،</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">حتى نتمكّن من توفير خدمة Outline لكم، ولنتحقّق من أي مشاكل مُحتملة، سنقوم بالاحتفاظ ببريدكم الالكتروني. للمزيد من التفاصيل نقترح عليكم قراءة سياسة الخصوصيّة التّابعة لاستخدام Outline في <a href="https://asl19.org/ar/outline/">الأسئلة الأكثر تكراراً.</a></span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">إليكم رابط مفتاح Outline. عند ضغطكم على الرّابط، واستخدامكم لدليل التحميل والاستخدام، ستتمكّنون من تحميل Outline على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">الرّابط: 👇</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'OUTLINE_KEY_EXIST_TEXT_BODY': {
        'en': """
        remove previous server as it won't work.
        new outline proxy link: {}
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.
        این هم لینک جدید خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇
        {}

        عزیز دل، به خاطر داشته باشید که با دریافت آدرس جدید، Access Key قبلی از کار خواهد افتاد و حتما سرور قبلی را از درون Outline پاک کنید.
        برای پاک کردن سرور قبلی، هم‌چون تصویر راهنما (ضمیمه شده در همین ایمیل)، بر روی سه نقطه بزنید و روی forget کلیک کنید.

        قربان شما
        آقای پستچی

        """,
        'ar': """
            عند ضغطكم على الرّابط أدناه، واستخدامكم لدليل المستخدمين المرفق، ستتمكّنون من تحميل Outline  على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.
            إليكم الرّابط:
            {}
            يرجى الانتباه أنّ مفتاح الوصول الذي كان لديكم سابقاً أصبح باطلاً. لإلغائه يرجى الضّغط على قائمة الاختيارات، من خلال علامة الثلاث نقاط العاموديّة، ومن ثمّ (Forget) حتى ينسى التطبيق عنوان الخادم.
            مرفق دليل إلغاء خادم من عميل Outline.
            mada@asl19.org أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا
        """,
    },
    'OUTLINE_KEY_EXIST_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Remove previous server as it won't work. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">New Outline vpn link: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">این هم لینک جدید خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عزیز دل، به خاطر داشته باشید که با دریافت آدرس جدید، Access Key قبلی از کار خواهد افتاد و حتما سرور قبلی را از درون Outline پاک کنید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">برای پاک کردن سرور قبلی، هم‌چون تصویر راهنما (ضمیمه شده در همین ایمیل)، بر روی سه نقطه بزنید و روی forget کلیک کنید.</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عند ضغطكم على الرّابط أدناه، واستخدامكم لدليل المستخدمين المرفق، ستتمكّنون من تحميل Outline  على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">إليكم الرّابط: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">يرجى الانتباه أنّ مفتاح الوصول الذي كان لديكم سابقاً أصبح باطلاً. لإلغائه يرجى الضّغط على قائمة الاختيارات، من خلال علامة الثلاث نقاط العاموديّة، ومن ثمّ (Forget) حتى ينسى التطبيق عنوان الخادم. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">مرفق دليل إلغاء خادم من عميل Outline. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'OUTLINE_NEW_TEXT_BODY': {
        'en': """
        outline proxy link: {}
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.
        تیم پس‌کوچه برای پیگیری مشکلات احتمالی و ارائه پشتیبانی بهتر، احتیاج دارد تا شناسه‌ تلگرام شما که به‌طور هش شده وغیر قابل بازگشایی و شناسایی خواهد بود را ذخیره کند. در این ارتباط پیشنهاد می‌کنیم حتما سند حریم خصوصی پس‌کوچه بخوانید.
        این هم خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇
        {}

        توجه: در نسل جدید کلیدهای اوت‌لاین، تغییرات به‌طور خودکار اعمال می‌شود و نیاز نیست که کلید جدید درخواست کنید. دریافت یک کلید از سمت شما کافی است و در صورت بروز اختلال، تیم پس‌کوچه تغییرات لازم را روی کلیدها اعمال می‌کند.

        قربان شما
        آقای پستچی
        """,
        'ar': """
        مرحبا،
        حتى نتمكّن من توفير خدمة Outline لكم، ولنتحقّق من أي مشاكل مُحتملة، سنقوم بالاحتفاظ ببريدكم الالكتروني. للمزيد من التفاصيل نقترح عليكم قراءة سياسة الخصوصيّة التّابعة لاستخدام Outline في https://asl19.org/ar/outline/الأسئلة الأكثر تكراراً.
        إليكم رابط مفتاح Outline. عند ضغطكم على الرّابط، واستخدامكم لدليل التحميل والاستخدام، ستتمكّنون من تحميل Outline على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.
        الرّابط: 👇
        mada@asl19.org أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا
        """,
    },
    'OUTLINE_NEW_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Outline vpn link: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عزیز دل، به سیستمِ توزیع فیلترشکن Outline در پس‌کوچه خوش آمدید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">تیم پس‌کوچه برای پیگیری مشکلات احتمالی و ارائه پشتیبانی بهتر، احتیاج دارد تا شناسه‌ تلگرام شما که به‌طور هش شده و غیر قابل بازگشایی و شناسایی خواهد بود را ذخیره کند. در این ارتباط پیشنهاد می‌کنیم حتما <a href="https://paskoocheh.com/privacy-policy.html#outline-distribution-privacy-policy">سند حریم خصوصی پس‌کوچه</a> را بخوانید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">این هم خدمت شما: با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">توجه: در نسل جدید کلیدهای اوت‌لاین، تغییرات به‌طور خودکار اعمال می‌شود و نیاز نیست که کلید جدید درخواست کنید. دریافت یک کلید از سمت شما کافی است و در صورت بروز اختلال، تیم پس‌کوچه تغییرات لازم را روی کلیدها اعمال می‌کند.</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">مرحبا،</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">حتى نتمكّن من توفير خدمة Outline لكم، ولنتحقّق من أي مشاكل مُحتملة، سنقوم بالاحتفاظ ببريدكم الالكتروني. للمزيد من التفاصيل نقترح عليكم قراءة سياسة الخصوصيّة التّابعة لاستخدام Outline في <a href="https://asl19.org/ar/outline/">الأسئلة الأكثر تكراراً.</a></span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">إليكم رابط مفتاح Outline. عند ضغطكم على الرّابط، واستخدامكم لدليل التحميل والاستخدام، ستتمكّنون من تحميل Outline على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">الرّابط: 👇</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'OUTLINE_EXIST_TEXT_BODY': {
        'en': """

        """,
        'fa': """
        شما کلید سرور اوت‌لاین خود را پیش از این دریافت کرده‌اید. نیازی به درخواست کلید جدید نیست. ما به‌طور خودکار کلید شما را به‌روزرسانی می‌کنیم.

        قربان شما
        آقای پستچی

        """,
        'ar': """
            عند ضغطكم على الرّابط أدناه، واستخدامكم لدليل المستخدمين المرفق، ستتمكّنون من تحميل Outline  على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز.
            إليكم الرّابط:
            {}
            يرجى الانتباه أنّ مفتاح الوصول الذي كان لديكم سابقاً أصبح باطلاً. لإلغائه يرجى الضّغط على قائمة الاختيارات، من خلال علامة الثلاث نقاط العاموديّة، ومن ثمّ (Forget) حتى ينسى التطبيق عنوان الخادم.
            مرفق دليل إلغاء خادم من عميل Outline.
            mada@asl19.org أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا
        """,
    },
    'OUTLINE_EXIST_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Remove previous server as it won't work. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">New Outline vpn link: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">شما کلید سرور اوت‌لاین خود را پیش از این دریافت کرده‌اید. نیازی به درخواست کلید جدید نیست. ما به‌طور خودکار کلید شما را به‌روزرسانی می‌کنیم.</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عند ضغطكم على الرّابط أدناه، واستخدامكم لدليل المستخدمين المرفق، ستتمكّنون من تحميل Outline  على أنظمة: آندرويد، iOS، ماك، و/أو ويندوز. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">إليكم الرّابط: </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif"><a href="{}">{}</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">يرجى الانتباه أنّ مفتاح الوصول الذي كان لديكم سابقاً أصبح باطلاً. لإلغائه يرجى الضّغط على قائمة الاختيارات، من خلال علامة الثلاث نقاط العاموديّة، ومن ثمّ (Forget) حتى ينسى التطبيق عنوان الخادم. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">مرفق دليل إلغاء خادم من عميل Outline. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'ICD_EMAIL_SUBJECT': {
        'en': """
            Outline for ICD
        """,
        'fa': """
            Outline for ICD
        """,
        'ar': """
            Outline for ICD
        """
    },
    'OUTLINE_ICD_TEXT_BODY': {
        'en': """
            Welcome to Iran Cyber Dialogue 2022!

            We have set up an Outline server for you to connect and use for the duration of the event.

            You can find more information about Outline here in English:

            https://getoutline.org/

            You can install the Outline client on your device(s) and connect to our Outline server by clicking the link below.

            اطلاعات بیشتر در مورد Outline [ outline.paskoocheh.com ] در پس‌کوچه.

            با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇

            {}
        """,
        'fa': """
            {}
        """,
        'ar': """
            {}
        """,
    },
    'OUTLINE_ICD_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <p dir="ltr"><span style="font-family:tahoma,geneva,sans-serif">Welcome to Iran Cyber Dialogue 2022!</span></p>
                <p dir="ltr"><span style="font-family:tahoma,geneva,sans-serif">We have set up an Outline server for you to connect and use for the duration of the event.</span></p>
                <p dir="ltr"><span style="font-family:tahoma,geneva,sans-serif">You can find more information about Outline here in English:</span></p>
                <p dir="ltr"><span style="font-family:tahoma,geneva,sans-serif"><a href="https://getoutline.org/">https://getoutline.org/</a></span></p>
                <p dir="ltr"><span style="font-family:tahoma,geneva,sans-serif">You can install the Outline client on your device(s) and connect to our Outline server by clicking the link below.</span></p>
            </p>

            <p dir="rtl">
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اطلاعات بیشتر در مورد Outline در <a href="https://outline.paskoocheh.com">پس‌کوچه</a></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">با کلیک کردن بر روی لینک زیر و با کمک تصویر راهنما (ضمیمه شده در ایمیل)،‌ اپلیکیشن Outline را نصب کرده و سِرور اختصاصی را به آن اضافه کنید👇</span></p>
            </p>

            <p dir="ltr">
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">{}</span></p>
            </p>
        """,
        'fa': """
            {}
        """,
        'ar': """
            {}
        """,
    },
    'OUTLINE_GUIDELINE_PHOTO': {
        'en': "Pask-Outline-guideline.png",
        'fa': "Pask-Outline-guideline.png",
        'ar': "Pask-Outline-guideline-ar.png"
    },
    'NOSERVER_TEXT_BODY': {
        'en': """
        There is no server right no. please ask again in a few hours.
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        عزیز دل،‌ متاسفانه در حال حاضر هیچ سروری برای فیلترشکنِ Outline نداریم. لطفا چند ساعت دیگر دوباره اقدام کنید.

        قربان شما
        آقای پستچی
        """,
        'ar': """
        عفواً ليس لدينا أي خادوم متاح حاليّاً
        """,
    },
    'NOSERVER_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">There is no server right no. please ask again in a few hours.</span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عزیز دل،‌ متاسفانه در حال حاضر هیچ سروری برای فیلترشکنِ Outline نداریم. لطفا چند ساعت دیگر دوباره اقدام کنید.</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">عفواً ليس لدينا أي خادوم متاح حاليّاً </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'DEPRECATED_TEXT_BODY': {
        'en': """
        Paskoocheh Outline distribution system was merged into BeePass project. You can send an email to get@beepassvpn.com to get a new key.
        """,
        'fa': """
        سلام روزتون بخیر، امیدوارم خوب و سلامت باشید
        سیستم توزیع کلیدهای اوتلاین پس‌کوچه در پروژه بی‌پس ادغام شده است. برای دریافت کلید می‌توانید به این آدرس ایمیل بفرستید:
        get@beepassvpn.com

        اگر هم به مشکلی برخوردید، می‌توانید از طریق آدرس‌های زیر با ما در تماس باشید:
        پشتیبانی از طریق تلگرام: http://t.me/beepassvpn_hd_bot
        پشتیبانی از طریق ایمیل: support@beepassvpn.com

        قربان شما
        آقای پستچی
        """,
        'ar': """
        تم دمج نظام توزيع Paskoocheh Outline في مشروع BeePass. يمكنك إرسال بريد إلكتروني إلى get@beepassvpn.com للحصول على مفتاح جديد.
        """,
    },
    'DEPRECATED_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Paskoocheh Outline distribution system was merged into BeePass project. You can send an email to get@beepassvpn.com to get a new key.</span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون بخیر، امیدوارم خوب و سلامت باشید</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سیستم توزیع کلیدهای اوتلاین پس‌کوچه در پروژه بی‌پس ادغام شده است. برای دریافت کلید می‌توانید به این آدرس ایمیل بفرستید:</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">get@beepassvpn.com</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">اگر هم به مشکلی برخوردید، می‌توانید از طریق آدرس‌های زیر با ما در تماس باشید:</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">پشتیبانی از طریق تلگرام: http://t.me/beepassvpn_hd_bot</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">پشتیبانی از طریق ایمیل: support@beepassvpn.com</span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">تم دمج نظام توزيع Paskoocheh Outline في مشروع BeePass. يمكنك إرسال بريد إلكتروني إلى get@beepassvpn.com للحصول على مفتاح جديد.</span></p>
            </p>
        """,
    },
    'MULLVAD_TEXT_BODY': {
        'en': """
        Please use this promo code: {} to activate {} app.
        This code will expire on {}.
        Activation guide link: {}

        Sicerely,
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        شما می‌توانید از طریق این شماره حساب: {} برای ورود به اپلیکیشن {} استفاده کنید.
        به خاطر بسپارید که این حساب کاربری تا تاریخ {} فعال خواهد بود.
        لینک راهنمای وارد کردن کد فعال‌سازی: {}
        قربان شما
        آقای پستچی
        """,
        'ar': """
        مرحبا،
        يرجى استخدام الرمز الترويجي التالي: {} لتفعيل التطبيق: {}.
        mada@asl19.org أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا
        """,
    },
    'MULLVAD_HTML_BODY': {
        'en': """
            <p dir="ltr">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Please use this promo code: {} to activate {} app. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">This code will expire on {}. </span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Activation guide link:  <a href="{}">{}</a></span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">Sicerely, </span></p>
            </p>
        """,
        'fa': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">شما می‌توانید از طریق این شماره حساب: {} برای ورود به اپلیکیشن {} استفاده کنید.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">به خاطر بسپارید که این حساب کاربری تا تاریخ {} فعال خواهد بود.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">لینک راهنمای وارد کردن کد فعال‌سازی <a href="{}">{}</a></span></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">قربان شما</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی</span></p>

                <span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
            </p>
        """,
        'ar': """
            <p dir="rtl">
                <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/outline-logo.png" alt="" style="width:128px;height:128px;" />
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">مرحبا،</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">يرجى استخدام الرمز الترويجي التالي: {} لتفعيل التطبيق: {}.</span></p>
                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">رابط دليل التفعيل <a href="{}">{}</a></span></span></p>

                <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">أسئلة؟ مشاكل تقنيّة؟ اتصلوا بنا mada@asl19.org</span></p>
            </p>
        """,
    },
    'APK_ISSUE_TEXT_BODY': {
        'en': """
        """,
        'fa': """
        سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟
        برای دانلود این فایل‌ APK بایستی ابتدا اپلیکیشن اندروید پس‌کوچه را دانلود و نصب کنید. به این ترتیب شما علاوه بر دریافت جدیدترین نسخه اپلیکیشن مورد نظرتان،  از ویژگی جدید فناوری همتابه‌همتا یعنی (دست‌به‌دست) اپلیکیشن پس‌کوچه نیز بهره‌مند خواهید شد.

        آقای پستچی پس‌کوچه
        """,
        'ar': """
        """
    },
    'APK_ISSUE_HTML_BODY': {
        'en': """
        """,
        'fa': """
            <p dir="rtl">
            <img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/Paskoocheh-Website-UI.png" alt="" style="width:128px;height:128px;" />
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">سلام روزتون به‌خیر. خوبید؟ خانواده چطورند؟ </span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">برای دانلود این فایل‌ APK بایستی ابتدا اپلیکیشن اندروید پس‌کوچه را دانلود و نصب کنید. به این ترتیب شما علاوه بر دریافت جدیدترین نسخه اپلیکیشن مورد نظرتان،  از ویژگی جدید فناوری همتابه‌همتا یعنی (دست‌به‌دست) اپلیکیشن پس‌کوچه نیز بهره‌مند خواهید شد.</span></p>
            <p dir="rtl"><span style="font-family:tahoma,geneva,sans-serif">آقای پستچی پس‌کوچه</span><img src="https://${FILE_S3_BUCKET}.s3.amazonaws.com/icons-email/email-logo.png" alt="" style="width:30px;height:30px;" /></p>
        </p>
        """,
        'ar': """
        """
    }
}
