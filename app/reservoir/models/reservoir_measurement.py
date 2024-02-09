from django.db import models


class ReservoirMeasurement(models.Model):
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    duration_hr = models.FloatField()
    reference_rate = models.FloatField()
    q = models.BooleanField()
    P_26hr = models.FloatField()
    T_26hr = models.FloatField()
    P_58hr = models.FloatField()
    T_58hr = models.FloatField()
    wpi = models.FloatField()
    rpi = models.FloatField()
    cpi = models.FloatField()
    is_shutin = models.BooleanField()
    is_prev_shutin = models.BooleanField()
    time_from_shutin = models.IntegerField()
    pressure_std = models.FloatField()
    derivative_std = models.FloatField()
    well_id = models.IntegerField()

    def __str__(self):
        return (f"Measurement from {self.start_timestamp} to "
                f"{self.end_timestamp}")
