import time


class AlertEngine:

    def __init__(self):
        self.last_alert_time = {}
        self.cooldown = 5   # seconds


    def process(self, events):

        alerts = []

        for event in events:

            # convert dict to string (fix)
            alert = str(event)

            current_time = time.time()

            if alert not in self.last_alert_time:
                self.last_alert_time[alert] = 0

            if current_time - self.last_alert_time[alert] > self.cooldown:

                alerts.append(alert)
                self.last_alert_time[alert] = current_time

        return alerts