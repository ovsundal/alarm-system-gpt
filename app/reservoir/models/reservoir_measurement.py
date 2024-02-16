from django.db import models


class ReservoirMeasurement(models.Model):
    start_time = models.FloatField()
    reference_rate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    wpi = models.FloatField()
    rpi = models.FloatField()
    cpi = models.FloatField()

    def __str__(self):
        return (f"Measurement from {self.start_timestamp} to "
                f"{self.end_timestamp}")
