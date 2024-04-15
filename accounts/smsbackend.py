from sendsms.backends.base import BaseSmsBackend
import ghasedakpack


# class CustomSmsBackend(BaseSmsBackend):
#     def send_messages(self, messages):
#             for message in messages:
#                 for to in message.to:
#                     try:
#                         pass
                        # message = " متن پیامک"
                        # receptor = "09045250913"
                        # linenumber = "10008566"
                        # sms = ghasedakpack.Ghasedak("")
                        # sms.send({
                        #     'message': message,                            
                        #     'receptor': receptor,                            
                        #     'linenumber': linenumber
                        # })
                    # except:
                    #     if not self.fail_silently:
                    #         raise "dd"