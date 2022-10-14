from .utils import ReviewerMixin
class VerifyEmailValidator(ReviewerMixin):
    success = {"success":True}
    def __init__(self,user,totp,otp) -> None:
        self.user = user
        self.totp = totp
        self.otp = otp

    def check_active_user(self):
        if self.user.is_active:
            return self.success
        return {"success":False,"message":"This account is inactive, contact admin for further assistance"}
    
    def check_provider(self):
        if self.user.auth_provider == 'email':
            return self.success
        return {"success":False,"message":"Please continue your login using " + self.user.auth_provider}
    
    def check_otp(self):
        if self.totp.verify(self.otp):
            return self.success
        return {"success":False,"message":"Invalid user login details or expired otp"}

class CheckOTP:
    pass