from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=200)
    description = models.TextField()
    point_value = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ngrok_base_url = "https://34cc-199-111-224-9.ngrok-free.app"
        scan_url = f"{ngrok_base_url}/app/v1.0/scan/{self.pk}/" 

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(scan_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        stream = BytesIO()
        qr_img.save(stream, format='PNG')
        file_name = f'event_{self.pk}_qr.png'
        self.qr_code.save(file_name, File(stream), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    scanned_events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.user.username