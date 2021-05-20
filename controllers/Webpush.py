import json

#from controllers.Init import Init
#from controllers.ConnectDb import ConnectDb
from pywebpush import WebPushException, webpush


class Webpush():
    
    def send_push(self, sender, text, url):

        conn, cursor = self.connect()
        
        cursor.execute('SELECT * FROM webpush WHERE login NOT IN (%s)', (sender,))
        subscriptions = cursor.fetchall()
        
        #print(subscriptions)
        
        for subscription in subscriptions:
            payload = {
                'head': 'STALEVAR',
                'body': text,
                'icon': 'https://stalevar.herokuapp.com/static/get?path=images/favicon.png',
                'url': url
            }
            #print(subscription)
            self.send_notification(subscription, payload, 43200)
            
        cursor.close()
        conn.close()


    def send_notification(self, subscription, payload, ttl):
        payload = json.dumps(payload)

        subscription_data = self._process_subscription_info(subscription)

        vapid_data = {}

        vapid_private_key = "xWgNVjUrA6ZJ9KIC8KZsmbxH5rHkqJFhK02VkQgm8jk"
        vapid_admin_email = "stalevar@mail.ru"

        # Vapid keys are optional, and mandatory only for Chrome.
        # If Vapid key is provided, include vapid key and claims
        if vapid_private_key:
            vapid_data = {
                'vapid_private_key': vapid_private_key,
                'vapid_claims': {"sub": "mailto:{}".format(vapid_admin_email)}
            }
            
        #print(vapid_data)

        try:
            if self.environ['wsgi.url_scheme'] == 'https' and self.environ['HTTP_HOST'] != 'localhost:8000':
                req = webpush(subscription_info=subscription_data, data=payload, ttl=ttl, **vapid_data)
                return req
            
        except WebPushException as e:
            # If the subscription is expired, delete it.
            if e.response.status_code == 410:
                conn, cursor = self.connect()
                
                cursor.execute('DELETE FROM webpush WHERE id=%s', (subscription.id,))
                
                conn.commit()
                cursor.close()
                conn.close()

            else:
                # Its other type of exception!
                raise e
            
    def _process_subscription_info(self, subscription):

        return {
            "endpoint": subscription.endpoint,
            "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth}
        }
