CUSTOM_ALLAUTH_CONFIG_PATH = "server.apps.main.allauth"
ACCOUNT_ADAPTER = CUSTOM_ALLAUTH_CONFIG_PATH + ".adapter.AllAuthAccountAdapter"
ACCOUNT_FORMS = {
    "signup": CUSTOM_ALLAUTH_CONFIG_PATH + ".forms.SignupForm",
    "reset_password": CUSTOM_ALLAUTH_CONFIG_PATH + ".forms.ResetPasswordForm",
}
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# SOCIALACCOUNT_LOGIN_ON_GET = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#         "SCOPE": [
#             "profile",
#             "email",
#         ],
#         "AUTH_PARAMS": {
#             "access_type": "online",
#         },
#     },
#     "facebook": {
#         "METHOD": "oauth2",
#         "SCOPE": ["email", "public_profile"],
#         "AUTH_PARAMS": {"auth_type": "reauthenticate"},
#         "INIT_PARAMS": {"cookie": True},
#         "FIELDS": [
#             "id",
#             "first_name",
#             "last_name",
#             "middle_name",
#             "name",
#             "name_format",
#             "short_name",
#         ],
#         "EXCHANGE_TOKEN": True,
#         "VERIFIED_EMAIL": False,
#         "VERSION": "v13.0",
#         "GRAPH_API_URL": "https://graph.facebook.com/v13.0",
#     },
# }
